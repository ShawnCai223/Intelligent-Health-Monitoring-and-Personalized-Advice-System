from src.audio import record_audio, transcribe_audio
from src.temperature import read_avg_temperature
from src.llm import ask_llm
import os

def main():
    os.makedirs("session_data", exist_ok=True)
    audio_file = "session_data/input.wav"
    text = transcribe_audio(audio_file if record_audio(audio_file) else None)

    if not text:
        print("No transcription.")
        return

    print(f"User said: {text}")
    temp = read_avg_temperature()
    if temp is None:
        print("Temperature read failed.")
        return

    prompt = (
        f"You are a trustworthy and empathetic AI health advisor. "
        f"Based on the user's speech and head temperature, provide thoughtful, non-diagnostic health suggestions.\n"
        f"The user said: \"{text}\".\n"
        f"The user's head temperature is {temp:.2f} °C.\n"
        f"Guidelines: Offer lifestyle and wellness advice. Be clear and concise."
    )

    ask_llm(prompt)

if __name__ == "__main__":
    main()