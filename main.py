from asr_module import transcribe_audio
from gtts import gTTS
import os
import playsound

qa_dict = {
    "Muraho neza?": "Yego",
    "Witwa nde?": "Nitwa Umufasha Wawe.",
    "Abanyeshuri bazakora ikizamini cya leta ryari?": "Abanyeshuri bazatangira gukora ikizamini cya leta muri gicurasi",
    "Nibamara kwiga bazajya hehe?": "Nibasoza nabo bazajya mubiruhuko barimo no gushaka amashuri ya kaminuza yo gukomerezamo",
    "Andi makuru agezweho ni ayahe?": "Andi makuru nuko iki gihembwe gifite ibyumweru icumi gusa",
}

def get_answer(transcription):
    for question, answer in qa_dict.items():
        if question in transcription.lower():
            return answer
    return "Nyihanganira simbashije kumva ikibazo cyawe!"

def speak_answer(answer_text):
    print("Speaking answer...")
    tts = gTTS(text=answer_text, lang='rw') 
    tts.save("answer.mp3")
    playsound.playsound("answer.mp3")
    os.remove("answer.mp3")  

def main():
    audio_folder = "sample_audio"
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith(".wav")]

    for audio_file in audio_files:
        print("\nProcessing:", audio_file)
        audio_path = os.path.join(audio_folder, audio_file)

        transcription = transcribe_audio(audio_path)
        print("Recognized Text:", transcription)

        answer = get_answer(transcription)
        print("Assistant Answer:", answer)

        speak_answer(answer)

if __name__ == "__main__":
    main()
