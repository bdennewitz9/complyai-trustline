import os

def load_api_key():
    return os.getenv("OPENAI_API_KEY", "")
