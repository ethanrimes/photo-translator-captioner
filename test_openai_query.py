# test_openai_query.py
"""
Test script for OpenAI API querying
"""

import os
import config
from openai_translator import translate_whatsapp_image
from PIL import Image, ImageDraw, ImageFont

def test_openai_query():
    """Test OpenAI API translation functionality."""
    print("Testing OpenAI API query...")
    
    # Check for API key
    if config.OPENAI_API_KEY == "your-api-key-here":
        print("ERROR: Please set your OpenAI API key in config.py or as environment variable")
        return
    
    # Create a sample WhatsApp-style image for testing
    test_image_path = os.path.join(config.PHOTOS_DIR, "test_whatsapp.png")
    
    if not os.path.exists(test_image_path):
        print("Creating sample WhatsApp conversation image...")
        create_sample_whatsapp_image(test_image_path)
    
    # Test the translation
    print(f"\nSending image to OpenAI for translation: {test_image_path}")
    translation = translate_whatsapp_image(test_image_path)
    
    print("\n" + "="*50)
    print("Translation Result:")
    print("="*50)
    print(translation)
    print("="*50)
    
    # Save translation to file
    test_translation_file = os.path.join(config.OUTPUT_DIR, "test_translation.txt")
    with open(test_translation_file, 'w', encoding='utf-8') as f:
        f.write(translation)
    print(f"\nTranslation saved to: {test_translation_file}")

def create_sample_whatsapp_image(output_path):
    """Create a sample WhatsApp-style conversation image."""
    img = Image.new('RGB', (400, 300), (228, 230, 235))
    draw = ImageDraw.Draw(img)
    
    # Add some Spanish text to simulate WhatsApp messages
    messages = [
        "15 enero",
        "Maria: Hola! ¿Cómo estás?",
        "Juan: Muy bien, gracias. ¿Y tú?",
        "Maria: Excelente! ¿Tomamos café mañana?",
        "Juan: Claro, ¿a qué hora?"
    ]
    
    y = 20
    for msg in messages:
        draw.text((20, y), msg, fill=(0, 0, 0))
        y += 40
    
    img.save(output_path)
    print(f"Created sample WhatsApp image: {output_path}")

if __name__ == "__main__":
    test_openai_query()

