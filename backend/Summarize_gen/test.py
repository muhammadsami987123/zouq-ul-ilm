import google.generativeai as genai
import requests
# import ath


def send_message(message,model):
    generation_config = {
        "temperature": 1,
        "top_k": 60,
        "top_p": 0.9,
        "max_output_tokens": 800,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config,
        )
    chat_session = model.start_chat(
            history=[]
        )
    response = chat_session.send_message(f"""Rephrase this text while maintaining all technical details also place the images where it should be place and extract images named as image(n)
                                         {message}""")
    return response.text