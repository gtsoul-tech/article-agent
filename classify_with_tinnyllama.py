import requests
import json

def classify_with_tinnyllama_api(title: str, body: str):
    prompt = f"""
Κατηγοριοποίησε το άρθρο σε δύο κατηγορίες:
1) nationwide_news
2) larisa_thessaly_news

Άρθρο:
Τίτλος: {title}
Κείμενο: {body}

Απάντησε μόνο σε JSON, όπως αυτό:
{{"category": "larisa_thessaly_news", "confidence": 0.9}}
"""

    url = "http://localhost:11434/v1/chat"  # το Ollama local API
    payload = {
        "model": "llama3.1:8b:latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    response = requests.post(url, json=payload, timeout=1000)
    response.raise_for_status()
    data = response.json()

    # Το output του Ollama API συνήθως είναι μέσα σε data['choices'][0]['message']['content']
    text = data['choices'][0]['message']['content']

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"category": "nationwide_news", "confidence": 0.5}
