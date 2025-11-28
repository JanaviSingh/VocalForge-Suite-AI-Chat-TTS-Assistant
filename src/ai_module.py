import requests
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def get_mistral_response(prompt, api_key, model="mistral-tiny"):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"Connection Error: {str(e)}"