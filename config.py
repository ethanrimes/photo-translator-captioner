# config.py
"""
Configuration settings for the WhatsApp translation pipeline
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Directory paths
PHOTOS_DIR = "/Users/ethankallett/Documents/Projects/photo-captioner/WhatsApp_ConversationsCopy"  # Directory containing .png photos
OUTPUT_DIR = "output"  # Directory for processed images
TRANSLATIONS_FILE = "translations.txt"  # File to store translations

# Image settings
DEFAULT_FONT_SIZE = 40
FONT_FAMILY = "Arial"  # Can be changed to any available font
TEXT_COLOR = (0, 0, 0)  # Black text
CAPTION_BG_COLOR = (255, 255, 255)  # White background
PADDING = 20  # Padding around text in caption area
LINE_SPACING = 1.2  # Line spacing multiplier

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY not found in environment variables or .env file")
    print("Please create a .env file with: OPENAI_API_KEY=your-api-key-here")
    
OPENAI_MODEL = "gpt-4o-mini"  # Using vision model for image understanding

# Create directories if they don't exist
os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)