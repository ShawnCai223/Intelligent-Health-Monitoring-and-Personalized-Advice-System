import subprocess
import os
import time

MODEL_PATH = "./whisper.cpp/build/bin/whisper-cli"
MODEL_BIN = "./whisper.cpp/models/ggml-base.en.bin"

def record_audio(filename):
    print("Recording for 10 seconds...")
    result = subprocess.run([
        "arecord", "-D", "plughw:2,0",
        "-f", "S16_LE", "-r", "16000",
        "-c", "1", "-d", "10", filename
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Recording finished.")
    return result.returncode == 0

def transcribe_audio(audio_file):
    if not audio_file:
        return None
    subprocess.run([
        MODEL_PATH,
        "-m", MODEL_BIN,
        "-f", audio_file,
        "-otxt",
        "-l", "en"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    transcript_path = audio_file + ".txt"
    time.sleep(0.5)
    if not os.path.exists(transcript_path):
        return None

    with open(transcript_path, "r") as f:
        return f.read().strip()
