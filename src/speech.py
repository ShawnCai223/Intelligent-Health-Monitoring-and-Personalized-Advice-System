import subprocess
import os

def speak(text):
    output_wav = "session_data/tts.wav"
    subprocess.run(["pico2wave", "-l=en-US", "-w", output_wav, text],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["aplay", "-D", "plughw:2,0", output_wav],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(output_wav):
        os.remove(output_wav)