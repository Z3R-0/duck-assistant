import requests
import json

with open("duck/config.json") as f:
    config = json.load(f)

OLLAMA_URL = config.get("ollama_url", "http://localhost:11434/api/generate")
MODEL_NAME = config.get("model", "phi3")

def call_model(prompt, system_prompt="You are a helpful assistant."):
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{system_prompt}\n\n{prompt}",
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload)
    data = r.json()
    errors = data.get("error")
    if errors:
        return "[Error] " + errors 
    else:
        return data.get("response", "[No response]")