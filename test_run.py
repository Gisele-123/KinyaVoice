
import os
from assistant import run_assistant
from tts_module import setup_kinya_tts

setup_kinya_tts()

audio_folder = os.path.join(os.path.dirname(__file__), "audio_samples")

results = run_assistant(audio_folder)

for idx, (transcription, response_wav) in enumerate(results):
    print(f"\n🎧 Audio #{idx + 1}")
    print("🗣️ Transcription:", transcription)
    print("🔊 Response saved at:", response_wav)

print("\n✅ All audio files processed!")
