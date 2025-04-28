from transformers import pipeline

asr_pipeline = pipeline(
    task="automatic-speech-recognition",
    model="benax-rw/KinyaWhisper",
)

def transcribe_audio(file_path):
    """
    Transcribe a Kinyarwanda audio file to text using KinyaWhisper
    """
    result = asr_pipeline(file_path)
    transcription = result['text']
    return transcription
