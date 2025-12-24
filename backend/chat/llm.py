import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

def generate_answer(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"]
# import os
# from pathlib import Path
# import google.generativeai as genai
# from dotenv import load_dotenv

# current_file_path = Path(__file__).resolve()

# env_path = current_file_path.parent.parent / '.env'

# load_dotenv(dotenv_path=env_path)

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     print(f"⚠️ Warning: GEMINI_API_KEY could not be loaded from {env_path}")

# genai.configure(api_key=api_key)

# model = genai.GenerativeModel("gemini-flash-latest")

# def generate_answer(prompt: str) -> str:
#     """
#     Generates a response using Google Gemini.
#     Returns a polite error string if the API fails.
#     """
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         print(f"❌ GenAI Error: {e}")
        
#         return "I'm sorry, I am currently unable to process your request due to a connection issue."