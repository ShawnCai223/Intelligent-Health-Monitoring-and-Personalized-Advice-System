# Intelligent-Health-Monitoring-and-Personalized-Advice-System

## Overview

This project implements a **fully local, privacy-preserving voice assistant** on the NVIDIA Jetson Nano platform. It integrates real-time **speech recognition**, **local LLM-based natural language understanding**, **sensor-based contextual feedback**, and **text-to-speech (TTS)** output, all without requiring an internet connection.

## Features

- Offline Speech Recognition (`whisper.cpp`)
- Lightweight Local Language Model (`TinyLlama` via `Ollama`)
- Real-time Temperature Sensing (`MLX90614`)
- TTS Output using `pico2wave`
- Fully Local Execution (No Internet Required)

## Hardware Requirements

- NVIDIA Jetson Nano 
- USB Microphone
- Speaker 
- MLX90614 Infrared Temperature Sensor
- I2C wiring/circuit setup for MLX90614

## Software Dependencies

| Component         | Description                             |
|------------------|-----------------------------------------|
| `whisper.cpp`     | Real-time offline speech-to-text engine |
| `Ollama`          | LLM serving platform                    |
| `TinyLlama`       | 1.1B parameter local language model     |
| `pico2wave`       | Lightweight text-to-speech tool         |
| `i2c-tools`       | For I2C sensor communication       |
| `Python 3`        | For script and logic coordination       |

## How to Run

1. **Clone the repository**

   ```bash
   git clone https://github.com/repo/local-voice-assistant
   cd local-voice-assistant
   ```

2. **Install Dependencies**

   ```bash
   sudo apt update
   sudo apt install build-essential python3 python3-pip i2c-tools libttspico-utils
   pip3 install smbus2
   ```

3. **Set Up Ollama & TinyLlama**

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama run tinyllama
   ```

4. **Connect MLX90614**

   Enable I2C on Jetson Nano and verify:

   ```bash
   sudo i2cdetect -y 1
   ```

5. **Start the Assistant**

   ```bash
   python3 main.py
   ```

## Example Interaction

- User: "How's my temperature?"
- Sensor reads: 37.5°C
- Assistant response (via TinyLlama): "Your temperature is slightly elevated. Please rest and drink water. ..."

## Acknowledgements

- [whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [Ollama](https://ollama.com/)
- [TinyLlama](https://huggingface.co/TinyLlama)
- [pico2wave](https://github.com/naggety/pico2wave-wrapper)
- NVIDIA Jetson Nano documentation
