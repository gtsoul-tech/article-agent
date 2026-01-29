import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def classify_with_llama(title: str, body: str):
    prompt = (
        "Κατηγοριοποίησε το άρθρο σε δύο κατηγορίες:\n"
        "- nationwide_news\n"
        "- larisa_thessaly_news\n\n"
        "Άρθρο:\n"
        f"Τίτλος: {title}\n"
        f"Κείμενο: {body}\n\n"
        "Απάντησε ΜΟΝΟ σε JSON:\n"
        '{"category": "larisa_thessaly_news", "confidence": 0.9}'
    )

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False,
        "temperature": 0
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=240)
    response.raise_for_status()

    text = response.json().get("response", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"category": "nationwide_news", "confidence": 0.5}
