import google.generativeai as genai

def generate_response(text: str) -> str:
    
    with open("google-api-key.txt", "r") as file:
        api_key = file.read().strip()
    
    genai.configure(api_key=api_key)

    response = genai.generate_text(prompt = text)
    return response.result