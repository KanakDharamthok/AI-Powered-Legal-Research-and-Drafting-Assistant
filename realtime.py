import whisper
import numpy as np
import sounddevice as sd
import queue
import sys

# --- Configuration ---
SAMPLE_RATE = 16000
CHUNK_SECONDS = 3          # Accumulate this many seconds before transcribing (GPU is fast enough for 3s)
SILENCE_THRESHOLD = 0.01   # RMS below this = silence, skip transcription

full_transcript = ""
audio_buffer_queue = queue.Queue()

def audio_stream_callback(indata, frames, time, status):
    """Captures audio chunks into the RAM queue."""
    if status:
        print(status, file=sys.stderr)
    audio_buffer_queue.put(indata.copy())

def is_silent(audio_data, threshold=SILENCE_THRESHOLD):
    """Returns True if the audio chunk is mostly silence."""
    rms = np.sqrt(np.mean(audio_data ** 2))
    return rms < threshold

def run_terminal_only_transcription():
    global full_transcript

    print("--- Initializing Live Whisper Engine [medium | CUDA] ---")
    model = whisper.load_model("medium", device="cuda")

    print("--- Streaming Started ---")
    print(f"Speak now. Transcribing every {CHUNK_SECONDS}s. Press Ctrl+C to stop.\n")

    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_stream_callback)

    accumulated = []  # holds raw float32 arrays until we have enough seconds
    samples_needed = SAMPLE_RATE * CHUNK_SECONDS

    with stream:
        try:
            while True:
                chunk = audio_buffer_queue.get()
                accumulated.append(chunk.flatten().astype(np.float32))

                total_samples = sum(len(c) for c in accumulated)

                if total_samples >= samples_needed:
                    audio_data = np.concatenate(accumulated)
                    accumulated = []  # reset buffer

                    if is_silent(audio_data):
                        sys.stdout.write("\r[Silence — skipping...]    ")
                        sys.stdout.flush()
                        continue

                    result = model.transcribe(
                        audio_data,
                        task="translate",
                        temperature=0.0,
                        fp16=True
                    )
                    text = result.get("text", "").strip()

                    if text:
                        full_transcript += " " + text
                        sys.stdout.write("\r[Live]: " + text[:70] + "   \n")
                        sys.stdout.flush()

        except KeyboardInterrupt:
            # Transcribe any remaining audio in the buffer
            if accumulated:
                print("\n\n[Transcribing remaining audio...]")
                audio_data = np.concatenate(accumulated)
                if not is_silent(audio_data):
                    result = model.transcribe(audio_data, task="translate", temperature=0.0, fp16=True)
                    text = result.get("text", "").strip()
                    if text:
                        full_transcript += " " + text

            print("\n\n✅ Recording stopped.")
            print("\n=============== FULL MASTER SCRIPT ===============")
            print(full_transcript.strip())
            print("====================================================")

if __name__ == "__main__":
    run_terminal_only_transcription()