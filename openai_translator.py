# openai_translator.py
"""
OpenAI API integration for translating WhatsApp conversations
"""

import base64
from openai import OpenAI
import config

def encode_image(image_path):
    """Encode image to base64 for API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def translate_whatsapp_image(image_path):
    """Send image to OpenAI for translation."""
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    # Encode the image
    base64_image = encode_image(image_path)
    
    prompt = """
    This is a WhatsApp conversation screenshot in Spanish. Please translate it to English.
    
    Format your response EXACTLY as follows:
    - Start with the date (if no year is visible, use 2025)
    - Then list each message with the sender name and translated text
    - Keep the conversation flow clear
    
    Example format:
    Date: January 15, 2025
    
    Ethan: Hello, how are you?
    Sergio: I'm fine, thanks. And you?
    Ethan: Very well, thank you.
    
    Please translate the conversation in the image following this format.

    The green bubbles (from right hand side) belong to Ethan. Ethan is the "You" person in this chat. The grey bubbles on left hand side belong to Sergio. Sergio is the other person in this conversation.
    """
    
    try:
        response = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error translating image: {str(e)}"