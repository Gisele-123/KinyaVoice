import os
import uuid
import re
import torch
import torchaudio
from KinyaTTS.Inference.kinyatts.tts.utils import get_hparams_from_file, load_checkpoint
from KinyaTTS.Inference.kinyatts.tts.models import SynthesizerTrn
from KinyaTTS.Inference.kinyatts.tts.text import text_to_sequence
from KinyaTTS.Inference.kinyatts.tts.text.symbols import symbols
from KinyaTTS.Inference.kinyatts.tts.commons import intersperse

inference_engine = (None, None, None, None)

def setup_kinya_tts():
    global inference_engine

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    config_path = "./KinyaTTS/Inference/kinyatts/ms_ktjw_istft_vits2_base.json"
    model_path = "./TTS_MODEL_ms_ktjw_istft_vits2_base_1M.pt"

    hps = get_hparams_from_file(config_path)

    if not hps:
        raise ValueError("Failed to load hyperparameters from the config file.")
    
    if getattr(hps.model, "use_mel_posterior_encoder", False):
        posterior_channels = 80
        hps.data.use_mel_posterior_encoder = True
    else:
        posterior_channels = hps.data.filter_length // 2 + 1
        hps.data.use_mel_posterior_encoder = False

    model = SynthesizerTrn(
        len(symbols),
        posterior_channels,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=getattr(hps.data, "n_speakers", 0),
        **hps.model
    ).to(device)

    # Load model weights
    _ = model.eval()
    _ = load_checkpoint(model_path, model, None)

    # Make it louder
    vol_boost = torchaudio.transforms.Vol(gain=6.0, gain_type="amplitude")

    # Store in inference engine
    inference_engine = (device, model, hps, vol_boost)
    print("✅ KinyaTTS initialized and ready!")

def text_to_input_tensor(text, hps):
    if hps is None:
        raise ValueError("Hyperparameters (hps) are not loaded correctly. Ensure 'setup_kinya_tts' is called.")

    text_norm = text_to_sequence(text)
    if getattr(hps.data, "add_blank", False):
        text_norm = intersperse(text_norm, 0)
    return torch.LongTensor(text_norm)

def speak(text, out_dir="outputs"):
    global inference_engine
    device, model, hps, vol_boost = inference_engine

    if inference_engine[1] is None:
        raise ValueError("Model has not been initialized. Ensure 'setup_kinya_tts' is called before using this function.")

    os.makedirs(out_dir, exist_ok=True)
    text = re.sub(r"[(){}]", "", text)

    input_tensor = text_to_input_tensor(text, hps)
    speed = 0.97

    with torch.no_grad():
        x = input_tensor.to(device).unsqueeze(0)
        x_len = torch.LongTensor([input_tensor.size(0)]).to(device)

        audio = model.infer(
            x, x_len,
            noise_scale=0.667,
            noise_scale_w=0.8,
            length_scale=1/speed
        )[0][0, 0].cpu().float()

    audio = vol_boost(audio.unsqueeze(0))

    file_name = f"{out_dir}/response_{uuid.uuid4().hex[:8]}.wav"
    torchaudio.save(file_name, audio, hps.data.sampling_rate)

    return file_name

def synthesize_tts(text):
    return speak(text)
