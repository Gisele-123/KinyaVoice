# app.py

import gradio as gr
import os
import tempfile
import soundfile as sf
from tts_module import setup_kinya_tts, synthesize_tts
from stt_module import transcribe_audio
from nlp_module import get_response

setup_kinya_tts()

def process_audio(audio_input):
    """Handle both microphone input and file uploads"""
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    try:
        if isinstance(audio_input, dict):
            sf.write(temp_path, audio_input["array"], audio_input["sampling_rate"])
        elif isinstance(audio_input, str):
            temp_path = audio_input
        else:
            raise ValueError("Unsupported audio input format")
        
        transcriptions = transcribe_audio([temp_path])
        transcription_text = transcriptions[0].text if hasattr(transcriptions[0], 'text') else str(transcriptions[0])
        
        response_text = get_response(transcription_text)
        response_audio = synthesize_tts(response_text)
        
        return transcription_text, response_audio
        
    except Exception as e:
        print(f"Error: {e}")
        return None, "Habaye ikosa, ongera ugerageze!"
    finally:
        if os.path.exists(temp_path) and temp_path != audio_input:
            os.unlink(temp_path)

with gr.Blocks(title="KinyarwandaVoice") as demo:
    gr.Markdown("# 🎙️ KinyarwandaVoice")
    
    with gr.Tab("🎤 Reba"):
        mic_input = gr.Audio(sources=["microphone"], type="filepath", label="Reba amajwi yawe")
        mic_button = gr.Button("Ohereza")
    
    with gr.Tab("📁 Shyiramo fayilo"):
        file_input = gr.Audio(sources=["upload"], type="filepath", label="Uplode fayilo ya audio")
        file_button = gr.Button("Ohereza")
    
    with gr.Column():
        transcription = gr.Textbox(label="Uvuze ibi ")
        response = gr.Audio(label="Igisubizo", autoplay=True)
    
    mic_button.click(process_audio, inputs=mic_input, outputs=[transcription, response])
    file_button.click(process_audio, inputs=file_input, outputs=[transcription, response])

if __name__ == "__main__":
    demo.launch()