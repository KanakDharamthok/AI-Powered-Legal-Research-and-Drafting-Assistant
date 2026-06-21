import os
import whisper
import numpy as np
import sounddevice as sd
import queue
import sys
import torch
from langchain_ollama import OllamaLLM
# --- Configuration ---
SAMPLE_RATE = 16000
CHUNK_SECONDS = 3          # Accumulate this many seconds before transcribing
SILENCE_THRESHOLD = 0.01   # Raw RMS threshold for absolute silence
VAD_CONFIDENCE_THRESHOLD = 0.70  # Drop anything below 70% human speech confidence

full_transcript = ""
audio_buffer_queue = queue.Queue()

# Global variables for the VAD model and helper utilities
vad_model = None
vad_utils = None


def clean_and_translate_transcript(raw_messy_transcript):
    """
    Passes the final raw transcript to Ollama (Gemma2) to structure the legal script,
    filter out ambient chatter, and normalize Hindi/Marathi code-switched text.
    """
    print("\n--- Initializing Transcript Normalization Engine [Ollama | gemma2] ---")
    llm = OllamaLLM(model="gemma2") 
    
    prompt = f"""
    You are an expert AI Legal Assistant specializing in Indian Courtroom Proceedings.
    Your task is to act as a Transcript Normalization Engine. You will ingest a raw, messy speech-to-text transcript that contains a mixture of legal arguments, code-switched phrases (Hindi/Marathi blended with English), and background cross-talk/hallucinations.


    CRITICAL RULES:
    1. FILTER AMBIENT/TECHNICAL CHATTER: Completely remove off-the-record technical side-talk, microphone adjustments, testing equipment phrases, or room management warnings (e.g., "check the microphone", "keep mobile silent", or checking cameras). Do not assign these to legal actors.
    2. TRANSLATE TO LEGAL ENGLISH: Translate regional language variables (Hindi/Marathi) into formal legal English.
    3. ABSOLUTELY NO SUMMARIZATION: Retain every true legal argument, objection, timestamp, and chronological flow.
    4. PRESERVE SPEAKER IDENTITIES: If speaker names are present, retain them; if not, use generic labels like "Judge", "Prosecutor", "Defendant", etc., based on context.
    5. FILTER ADMINISTRATIVE COMPLAINTS: Remove casual complaints regarding court delays, scheduling frustrations, or procedural postponements unless they directly form a legal application for adjournment.
    6. PRESERVE LEGAL ARGUMENTS: Retain all legal arguments, objections, and procedural statements verbatim, translating only the non-English portions.
    7. FORMAT: Output the cleaned, translated text as a formal chronological script.

    Raw Transcript to Clean:
    \"\"\"
    {raw_messy_transcript}
    \"\"\"

    Cleaned Legal English Transcript:
    """
    
    cleaned_output = llm.invoke(prompt)
    return cleaned_output


def init_vad():
    """Initializes the Silero VAD model locally."""
    global vad_model, vad_utils
    print("--- Loading Silero VAD [Noise Exclusion Engine] ---")
    vad_model, vad_utils = torch.hub.load(
        repo_or_dir='snakers4/silero-vad', 
        model='silero_vad', 
        force_reload=False, 
        trust_repo=True
    )
    if torch.cuda.is_available():
        vad_model = vad_model.cuda()


def audio_stream_callback(indata, frames, time, status):
    """Captures audio chunks into the RAM queue."""
    if status:
        print(status, file=sys.stderr)
    audio_buffer_queue.put(indata.copy())


def is_silent(audio_data, threshold=SILENCE_THRESHOLD):
    """Returns True if the audio chunk is mostly silence (RMS check)."""
    rms = np.sqrt(np.mean(audio_data ** 2))
    return rms < threshold


def is_valid_speech(audio_data):
    """Slices the 3-second audio block into 512-sample windows and verifies human speech."""
    global vad_model
    WINDOW_SIZE = 512
    total_samples = len(audio_data)
    
    if total_samples < WINDOW_SIZE:
        return False

    speech_probabilities = []

    for i in range(0, total_samples - WINDOW_SIZE + 1, WINDOW_SIZE):
        chunk_slice = audio_data[i : i + WINDOW_SIZE]
        tensor_audio = torch.from_numpy(chunk_slice)
        
        if tensor_audio.dim() == 1:
            tensor_audio = tensor_audio.unsqueeze(0)
            
        if torch.cuda.is_available():
            tensor_audio = tensor_audio.cuda()
            
        with torch.no_grad():
            prob = vad_model(tensor_audio, SAMPLE_RATE).item()
            speech_probabilities.append(prob)

    if speech_probabilities:
        avg_confidence = np.mean(speech_probabilities)
        return avg_confidence >= VAD_CONFIDENCE_THRESHOLD
        
    return False


def run_terminal_only_transcription():
    global full_transcript

    init_vad()

    print("--- Initializing Live Whisper Engine [medium | CUDA] ---")
    model = whisper.load_model("medium", device="cuda")

    print("--- Streaming Started ---")
    print(f"Speak now. Transcribing every {CHUNK_SECONDS}s. Press Ctrl+C to stop.\n")

    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_stream_callback)

    accumulated = []  
    samples_needed = SAMPLE_RATE * CHUNK_SECONDS

    with stream:
        try:
            while True:
                chunk = audio_buffer_queue.get()
                accumulated.append(chunk.flatten().astype(np.float32))
                total_samples = sum(len(c) for c in accumulated)

                if total_samples >= samples_needed:
                    audio_data = np.concatenate(accumulated)
                    accumulated = []  

                    if is_silent(audio_data):
                        sys.stdout.write("\r[Silence — skipping...]    ")
                        sys.stdout.flush()
                        continue

                    if not is_valid_speech(audio_data):
                        sys.stdout.write("\r[Noise/Side-chatter ignored...]    ")
                        sys.stdout.flush()
                        continue

                    result = model.transcribe(
                        audio_data,
                        task="translate",
                        temperature=0.0,
                        fp16=True,
                        compression_ratio_threshold=2.4, 
                        logprob_threshold=-1.0,          
                        no_speech_threshold=0.6
                    )
                    text = result.get("text", "").strip()

                    if text:
                        full_transcript += " " + text
                        sys.stdout.write("\r[Live]: " + text[:70] + "   \n")
                        sys.stdout.flush()

        except KeyboardInterrupt:
            # Process remaining audio buffer bytes before stopping
            if accumulated:
                print("\n\n[Transcribing remaining audio...]")
                audio_data = np.concatenate(accumulated)
                if not is_silent(audio_data) and is_valid_speech(audio_data):
                    result = model.transcribe(audio_data, task="translate", temperature=0.0, fp16=True)
                    text = result.get("text", "").strip()
                    if text:
                        full_transcript += " " + text

            print("\n\n✅ Recording stopped.")
            print("\n=============== RAW WHISPER TRANSCRIPT ===============")
            print(full_transcript.strip())
            print("======================================================")

            # 🚨 POST-PROCESSING LAYER: Call the LLM Cleaning Pipeline here
            if full_transcript.strip():
                cleaned_script = clean_and_translate_transcript(full_transcript.strip())
                
                print("\n✨=============== CLEANED LEGAL ENGLISH SCRIPT ===============")
                print(cleaned_script.strip())
                print("===============================================================")
            else:
                print("\n[No audio text found to normalize.]")


if __name__ == "__main__":
    run_terminal_only_transcription()