import gradio as gr
from asr_module import transcribe_audio
from gtts import gTTS
# import os

responses_dict = {
    "muraho neza": "Muraho neza nawe!",
    "witwa nde": "Nitwa Umufasha Wawe.",
    "abanyeshuri bazakora ikizamini cya leta ryari": "Bazatangira muri Gicurasi.",
    "nimara kwiga bazajya hehe": "Bazajya gushaka amashuri ya kaminuza.",
    "andi makuru agezweho ni ayahe": "Igihembwe gifite ibyumweru icumi gusa.",
    "amakuru yawe": "Ni meza, urakoze kubaza.",
    "ikaze": "Urakaza neza!",
    "izina ry’igihugu cyacu": "Igihugu cyacu ni u RwFanda.",
    "ikinyarwanda kirakomeye": "Yego, ariko gishimishije cyane.",
    "bikorwa bite": "Bimeze neza, ndabashimira!",
    "ufite amafaranga": "Oya, Nge ntayo mfite gusa wayashaka kuri banki",
    "ufite imyaka ingahe": "Ntamyaka izwi mfite",
    "ushobora kumbwira ikibazo mfite hano": "Kinyereke ubundi ngufashe"
}

def get_answer(transcription):
    transcription = transcription.lower()
    for key_text, response in responses_dict.items():
        if key_text in transcription:
            return response
    return "Nyihanganira, sinashoboye kumva neza ibyo wavuze! Subiramo neza."

def process_microphone(audio):
    audio_path = "ibikenewe.wav"
    with open(audio_path, "wb") as f:
        f.write(audio)

    transcription = transcribe_audio(audio_path)
    print("Recognized:", transcription)

    answer = get_answer(transcription)

    tts = gTTS(text=answer, lang='rw')
    tts_output = "response_audio.mp3"
    tts.save(tts_output)

    return transcription, tts_output

app = gr.Interface(
    fn=process_microphone,
    inputs=gr.Audio(source="microphone", type="filepath"),
    outputs=[
        gr.Textbox(label="Recognized Text"),
        gr.Audio(label="Assistant Response")
    ],
    title="Kinyarwanda Voice Assistant",
    description="Speak into the microphone in Kinyarwanda. The assistant will understand and reply!"
)

if __name__ == "__main__":
    app.launch()
