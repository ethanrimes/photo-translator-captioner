# image_processor.py
"""
Image processing functions for adding captions to photos
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import config

def calculate_text_dimensions(text, font_size=config.DEFAULT_FONT_SIZE):
    """Calculate the dimensions needed for text with wrapping."""
    try:
        font = ImageFont.truetype(config.FONT_FAMILY, font_size)
    except:
        font = ImageFont.load_default()
    
    # Create temporary image to measure text
    temp_img = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(temp_img)
    
    # Wrap text to reasonable width (assuming ~800px wide images)
    wrapped_lines = []
    for line in text.split('\n'):
        wrapped_lines.extend(textwrap.wrap(line, width=60))
    
    # Calculate total height needed
    line_height = font_size * config.LINE_SPACING
    total_height = int(len(wrapped_lines) * line_height + 2 * config.PADDING)
    
    return total_height, wrapped_lines, font

def add_caption_space(image_path, caption_text="", font_size=config.DEFAULT_FONT_SIZE):
    """Add white space below image and optionally add caption text."""
    # Open the original image
    img = Image.open(image_path)
    width, height = img.size
    
    # Calculate caption area height
    if caption_text:
        caption_height, wrapped_lines, font = calculate_text_dimensions(caption_text, font_size)
    else:
        caption_height = 200  # Default height if no text
        wrapped_lines = []
        try:
            font = ImageFont.truetype(config.FONT_FAMILY, font_size)
        except:
            font = ImageFont.load_default()
    
    # Create new image with caption space
    new_height = height + caption_height
    new_img = Image.new('RGB', (width, new_height), config.CAPTION_BG_COLOR)
    
    # Paste original image at top
    new_img.paste(img, (0, 0))
    
    # Add caption text if provided
    if caption_text and wrapped_lines:
        draw = ImageDraw.Draw(new_img)
        y_position = height + config.PADDING
        line_height = font_size * config.LINE_SPACING
        
        for line in wrapped_lines:
            draw.text((config.PADDING, y_position), line, 
                     fill=config.TEXT_COLOR, font=font)
            y_position += line_height
    
    return new_img

def save_image_with_caption(image_path, output_path, caption_text, font_size=config.DEFAULT_FONT_SIZE):
    """Process image and save with caption."""
    new_img = add_caption_space(image_path, caption_text, font_size)
    new_img.save(output_path)
    return output_path