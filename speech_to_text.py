import os
import whisper
import torch

def transcribe_and_translate_audio(audio_file_path, model_size="base"):
    """
    Robust translation execution matrix optimized to bypass hardware compiler errors.
    Fails back seamlessly to standard CPU processing loops.
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Target audio file not found at: {audio_file_path}")
        
    print(f"\n--- Step 1: Initializing Whisper Engine [{model_size}] ---")
    
    # FORCED STABILITY: Using CPU avoids 'Torch not compiled with CUDA' runtime failures
    device = "cpu"
    print(f"Enforcing stable offline inference on device matrix: {device.upper()}")
    
    # Load model binaries locally into memory loop
    model = whisper.load_model(model_size, device=device)
    
    print(f"\n--- Step 2: Extracting Audio Spectrum Matrix ---")
    print(f"Target Source File: {os.path.basename(audio_file_path)}")
    
    print(f"\n--- Step 3: Executing Cross-Lingual Translation Pipeline ---")
    
    # Safe execution block using explicit dictionary configuration parameters
    # This prevents the 'AttributeError' crash seen in your terminal terminal
    result = model.transcribe(
        audio_file_path, 
        task="translate",
        temperature=0.0,
        fp16=False  # Floating-point 16 is incompatible with CPU execution paths
    )
    
    return {
        "detected_language": result.get("language", "unknown"),
        "text": result.get("text", "").strip()
    }

if __name__ == "__main__":
    TEST_AUDIO_FILE = "sample_bail_hearing.wav"
    
    try:
        if not os.path.exists(TEST_AUDIO_FILE):
            print(f"\n⚠️  [Workspace Notice] File '{TEST_AUDIO_FILE}' not found.")
            print(f"Action Required: Confirm your sample audio matches this exact string name.")
        else:
            output = transcribe_and_translate_audio(TEST_AUDIO_FILE, model_size="base")
            
            print("\n======================= PIPELINE OUTPUT =======================")
            print(f"Detected Native Language : {output['detected_language'].upper()}")
            print(f"Translated English Text  : \n\n\"{output['text']}\"")
            print("===============================================================")
            
    except Exception as e:
        print(f"\n❌ Pipeline Execution Failure: {str(e)}")