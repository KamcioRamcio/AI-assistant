from TTS.api import TTS
import os
from playsound import playsound
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
# Initialize TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC").to(device)

# Text-to-Speech and play the audio
def speak_text(text):
    output_file = "output.wav"
    tts.tts_to_file(text=text, file_path=output_file)
    playsound(output_file)
    os.remove(output_file)

