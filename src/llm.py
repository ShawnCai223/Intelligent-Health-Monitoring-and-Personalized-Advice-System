import subprocess
from .speech import speak

def ask_llm(prompt):
    print("\nLLM analyzing...")
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