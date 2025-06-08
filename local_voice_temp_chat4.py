import subprocess
import time
import os
import board
import busio
import adafruit_mlx90614

AUDIO_FILE = "input.wav"
TEXT_FILE = AUDIO_FILE + ".txt"
MODEL_PATH = "./whisper.cpp/build/bin/whisper-cli"
MODEL_BIN = "./whisper.cpp/models/ggml-base.en.bin" 

def record_audio():
    print("Recording for 10 seconds. Please speak...")
    subprocess.run([
        "arecord", "-D", "plughw:2,0",
        "-f", "S16_LE", "-r", "16000",
        "-c", "1", "-d", "5", AUDIO_FILE
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Recording finished. Transcripting...")

def transcribe_audio():
    subprocess.run([
        MODEL_PATH,
        "-m", MODEL_BIN,
        "-f", AUDIO_FILE,
        "-otxt",
        "-l", "en"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Transcription complete. Detecting temperature...")

def read_avg_temperature(duration_sec=5):
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    mlx = adafruit_mlx90614.MLX90614(i2c)
    object_list = []

    start_time = time.time()
    while time.time() - start_time < duration_sec:
        try:
            object_temp = mlx.object_temperature
            object_list.append(object_temp)
        except Exception:
            pass
        print(f"Temperature: {object_temp:.2f} °C", end="\r")
        time.sleep(1)

    if not object_list:
        return None
    return sum(object_list) / len(object_list)

def speak(text):
    subprocess.run(["pico2wave", "-l=en-US", "-w", "tts.wav", text],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["aplay", "-D", "plughw:2,0", "tts.wav"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove("tts.wav")

def ask_llm(prompt):
    print("\nLLM analysising...")
    result = subprocess.run(
        ["ollama", "run", "tinyllama"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode()
    print("\nLLM Response:")
    print(output)
    speak(output)

def main():
    record_audio()
    transcribe_audio()

    print(f"Looking for transcript file: {TEXT_FILE}")
    if not os.path.exists(TEXT_FILE):
        print("No transcription file found.")
        return

    with open(TEXT_FILE, "r") as f:
        speech_text = f.read().strip()
        print(f"User said: {speech_text}")

    if not speech_text:
        print("Transcription is empty.")
        return

    avg_object = read_avg_temperature()
    if avg_object is None:
        print("Failed to read temperature.")
        return

    full_prompt = (
        f"You are a trustworthy and empathetic AI health advisor. "
        f"Based on the user's speech and head temperature, provide thoughtful, non-diagnostic health suggestions.\n"
        f"The user said: \"{speech_text}\".\n"
        f"The user's head temperature is {avg_object:.2f} °C.\n"
        f"Guidelines: Offer lifestyle and wellness advice. And be clear and concise."
    )

    ask_llm(full_prompt)

if __name__ == "__main__":
    main()


