import gradio as gr
from asr_module import transcribe_audio
from gtts import gTTS
import os

responses_dict = {
    "muraho neza": "Muraho neza nawe!",
    "witwa nde": "Nitwa Umufasha Wawe.",
    "abanyeshuri bazakora ikizamini cya leta ryari": "Bazatangira muri Gicurasi.",
    "nimara kwiga bazajya hehe": "Bazajya gushaka amashuri ya kaminuza.",
    "andi makuru agezweho ni ayahe": "Igihembwe gifite ibyumweru icumi gusa.",
    "amakuru yawe": "Ni meza, urakoze kubaza.",
    "ikaze": "Urakaza neza!",
    "izina ry’igihugu cyacu": "Igihugu cyacu ni u Rwanda.",
    "ikinyarwanda kirakomeye": "Yego, ariko gishimishije cyane.",
    "bikorwa bite": "Ni ibiki ushaka gukora",
    "ufite amafaranga": "Oya, Nge ntayo mfite gusa wayashakira kuri banki",
    "ufite imyaka ingahe": "Ntamyaka izwi mfite",
    "umeze neza": "Yego meze neza. Wowe umeze ute?",
    "ushobora kumbwira ikibazo mfite hano": "Kinyereke ubundi ngufashe kumenya ikibazo ufite"
}

def get_answer(transcription):
    transcription = transcription.lower()
    for key_text, response in responses_dict.items():
        if key_text in transcription:
            return response
    return "Nyihanganira, sinashoboye kumva neza ibyo wavuze! Subiramo neza."

def process_microphone(audio):
    try:
        audio_path = "ibikenewe.wav"
        
        with open(audio, "rb") as f:
            audio_data = f.read() 
        
        with open(audio_path, "wb") as f:
            f.write(audio_data) 

        transcription = transcribe_audio(audio_path)
        print("Recognized:", transcription)

        answer = get_answer(transcription)

        tts = gTTS(text=answer, lang='rw')
        tts_output = "response_audio.mp3"
        tts.save(tts_output)

        return transcription, tts_output
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error processing your request. Please try again.", None

app = gr.Interface(
    fn=process_microphone,
    inputs=gr.Audio(type="filepath"),
    outputs=[
        gr.Textbox(label="Recognized Text"),
        gr.Audio(label="Assistant Response")
    ],
    title="Kinyarwanda Voice Assistant",
    description="Speak into the microphone in Kinyarwanda. The assistant will understand and reply!"
)

if __name__ == "__main__":
    app.launch(share=True)
