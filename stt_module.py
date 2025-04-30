import os
from vosk import Model, KaldiRecognizer
import wave
import json
from dotenv import load_dotenv

load_dotenv()

def load_vosk_model(model_path="vosk-model-small-en-us-0.15"):
    """
    Load Vosk model. You can replace with a Kinyarwanda model if available.
    Download models from: https://alphacephei.com/vosk/models
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Vosk model not found at {model_path}. "
            f"Download models from https://alphacephei.com/vosk/models"
        )
    return Model(model_path)

model = load_vosk_model() 

def transcribe_audio(audio_input):
    """Handle both folder paths and direct file lists using Vosk"""
    supported_ext = ('.wav', '.mp3', '.flac')
    
    if isinstance(audio_input, str):
        if not os.path.isdir(audio_input):
            raise ValueError(f"Path {audio_input} is not a valid directory")
            
        audio_files = [
            os.path.join(audio_input, f)
            for f in sorted(os.listdir(audio_input))
            if f.lower().endswith(supported_ext)
        ]
    elif isinstance(audio_input, list):
        audio_files = [
            f for f in audio_input 
            if isinstance(f, str) and f.lower().endswith(supported_ext)
        ]
    else:
        raise ValueError("Input must be either a folder path or list of audio files")

    if not audio_files:
        raise FileNotFoundError("No supported audio files found")

    results = []
    for audio_file in audio_files:
        try:
            if not audio_file.endswith('.wav'):
                audio_file = convert_to_wav(audio_file) 
            
            wf = wave.open(audio_file, "rb")
            recognizer = KaldiRecognizer(model, wf.getframerate())
            recognizer.SetWords(True) 

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    pass 

            final_result = json.loads(recognizer.FinalResult())
            results.append(final_result.get("text", ""))
            
        except Exception as e:
            print(f"Error processing {audio_file}: {e}")
            results.append("")  

    return results

def convert_to_wav(input_file, output_file=None):
    """Helper function to convert audio files to WAV format (Vosk works best with WAV)"""
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".wav"
    
    os.system(f"ffmpeg -i {input_file} -ar 16000 -ac 1 {output_file}")
    return output_file
