from stt_module import transcribe_audio
from tts_module import synthesize_tts
from nlp_module import get_response

def run_assistant(audio_folder="./audio_samples"):
    hypotheses = transcribe_audio(audio_folder)

    results = []
    for hypothesis in hypotheses:
        transcription = hypothesis.text
        response_text = get_response(transcription)
        response_wav = synthesize_tts(response_text)
        results.append((transcription, response_wav))

    return results
