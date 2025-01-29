import requests
import json

url = "http://127.0.0.1:11434/api/generate"


def query_ollama(text):
    data = {
        "model": "codegemma:7b",
        "prompt": text,
    }
    generated_text = ""
    try:
        response = requests.post(url, json=data, stream=True, verify=False)
        if response.status_code == 200:
            print("Response:")
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    result = json.loads(decoded_line)
                    generated_text += result.get("response", "")
        else:
            print("Error: ", response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return generated_text