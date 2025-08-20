# test_white_space.py
"""
Test script for white space addition functionality
"""

import os
from PIL import Image
import config
from image_processor import add_caption_space, save_image_with_caption

def test_white_space():
    """Test adding white space to an image."""
    print("Testing white space addition...")
    
    # Create a test image if none exists
    # /Users/ethankallett/Documents/Projects/photo-captioner/WhatsApp_Conversations/IMG_8028.PNG
    test_image_path = os.path.join(config.PHOTOS_DIR, "IMG_8028.PNG.png")
    
    if not os.path.exists(test_image_path):
        # Create a simple test image
        test_img = Image.new('RGB', (800, 600), (100, 150, 200))
        test_img.save(test_image_path)
        print(f"Created test image: {test_image_path}")
    
    # Test 1: Add empty white space
    print("\nTest 1: Adding empty white space...")
    img_with_space = add_caption_space(test_image_path)
    output_path = os.path.join(config.OUTPUT_DIR, "test_white_space.png")
    img_with_space.save(output_path)
    print(f"Saved to: {output_path}")
    
    # Test 2: Add white space with sample text
    print("\nTest 2: Adding white space with sample text...")
    sample_text = """Date: January 15, 2025

Maria: Hello! How are you today?
Juan: I'm doing great, thanks! Just finished work.
Maria: That's wonderful! Want to grab coffee tomorrow?
Juan: Sure, what time works for you?"""
    
    output_path2 = os.path.join(config.OUTPUT_DIR, "test_with_caption.png")
    save_image_with_caption(test_image_path, output_path2, sample_text)
    print(f"Saved to: {output_path2}")
    
    # Test 3: Test different font sizes
    print("\nTest 3: Testing different font sizes...")
    for size in [20, 40, 60]:
        output_path3 = os.path.join(config.OUTPUT_DIR, f"test_font_{size}px.png")
        save_image_with_caption(test_image_path, output_path3, sample_text, font_size=size)
        print(f"Font size {size}px saved to: {output_path3}")
    
    print("\nWhite space tests completed!")

if __name__ == "__main__":
    test_white_space()