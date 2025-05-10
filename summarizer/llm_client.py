import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
llm_model = os.getenv("OPENROUTER_MODEL_LLAMA")
def call_llm(sys_prompt: str, user_input: str, model: str = llm_model) -> str:
    print(f"Calling LLM with model: {model}")
    data = {
        "model": model,
        "messages":[
            {"role": "system", "content": str(sys_prompt)},
            {"role": "user", "content": str(user_input)}
        ],
    }
    return call_openrouter(data)


def call_llm_vision(user_input: str, image_url: str, model: str) -> str:
    print(f"Calling LLM with vision model: {model}")
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": str(user_input)
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": str(image_url)
                        }
                    }
                ]
            }
        ]
    }
    return call_openrouter(data)

def call_openrouter(data: dict) -> str:
    try:
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://runmyflow.com", 
            "X-Title": "runmyflow",
        },
        data=json.dumps(data)
        )
        response_json = response.json()
        print(f"response_json: {json.dumps(response_json, indent=2)}")
        if response_json.get("choices"):
            return response_json["choices"][0]["message"]["content"]
        else:
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

if __name__ == "__main__":
   response = call_llm(sys_prompt="You are a helpful assistant", user_input="What is the meaning of life?", model=llm_model)
   print(f"response: {response}")