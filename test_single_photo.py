# test_single_photo.py
"""
Test the full pipeline on a single photo specified via command line
Usage: python test_single_photo.py path/to/photo.png


# Basic usage
python test_single_photo.py path/to/photo.png

# Skip saving to translations file
python test_single_photo.py photo.png --no-save

# Custom font size
python test_single_photo.py photo.png --font-size 30

# Show help
python test_single_photo.py --help

"""

import os
import sys
import argparse
import config
from image_processor import save_image_with_caption
from openai_translator import translate_whatsapp_image

def test_single_photo(photo_path, save_to_translations_file=True):
    """Test the complete process on one photo."""
    
    # Check for API key
    if not config.OPENAI_API_KEY:
        print("ERROR: OpenAI API key not found!")
        print("Please create a .env file with: OPENAI_API_KEY=your-api-key")
        return False
    
    # Validate photo exists
    if not os.path.exists(photo_path):
        print(f"ERROR: Photo not found: {photo_path}")
        return False
    
    if not photo_path.lower().endswith('.png'):
        print(f"WARNING: File is not a PNG: {photo_path}")
    
    photo_name = os.path.basename(photo_path)
    print(f"\nProcessing: {photo_name}")
    print("="*50)
    
    # Step 1: Translate the image
    print("\n📝 Step 1: Getting translation from OpenAI...")
    try:
        translation = translate_whatsapp_image(photo_path)
        print(f"✓ Translation received: {len(translation)} characters")
    except Exception as e:
        print(f"✗ Translation failed: {e}")
        return False
    
    # Display translation
    print("\n📋 Translation:")
    print("-"*40)
    print(translation)
    print("-"*40)
    
    # Step 2: Save translation to file (optional)
    if save_to_translations_file:
        print(f"\n💾 Step 2: Saving translation to {config.TRANSLATIONS_FILE}...")
        
        # Load existing translations
        existing_translations = {}
        if os.path.exists(config.TRANSLATIONS_FILE):
            with open(config.TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                entries = content.split('='*50)
                for entry in entries:
                    lines = entry.strip().split('\n')
                    if lines and lines[0].startswith('FILE: '):
                        filename = lines[0].replace('FILE: ', '').strip()
                        trans_text = '\n'.join(lines[1:]).strip()
                        if trans_text:
                            existing_translations[filename] = trans_text
        
        # Add or update this photo's translation
        existing_translations[photo_name] = translation
        
        # Save all translations
        with open(config.TRANSLATIONS_FILE, 'w', encoding='utf-8') as f:
            for filename, trans in existing_translations.items():
                f.write(f"FILE: {filename}\n")
                f.write(f"{trans}\n")
                f.write('='*50 + '\n\n')
        
        print(f"✓ Translation saved to: {config.TRANSLATIONS_FILE}")
    
    # Step 3: Add caption to image
    print(f"\n🖼️  Step 3: Adding caption to image...")
    output_filename = f"captioned_{photo_name}"
    output_path = os.path.join(config.OUTPUT_DIR, output_filename)
    
    try:
        save_image_with_caption(photo_path, output_path, translation, config.DEFAULT_FONT_SIZE)
        print(f"✓ Image with caption saved to: {output_path}")
    except Exception as e:
        print(f"✗ Failed to add caption: {e}")
        return False
    
    # Summary
    print("\n" + "="*50)
    print("✅ Pipeline Complete!")
    print(f"📥 Input: {photo_path}")
    print(f"📤 Output: {output_path}")
    print(f"📝 Translation: {config.TRANSLATIONS_FILE if save_to_translations_file else 'Not saved'}")
    print("="*50)
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='Process a single WhatsApp screenshot through the translation pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_single_photo.py photos/chat1.png
  python test_single_photo.py /path/to/screenshot.png --no-save
  python test_single_photo.py photos/test.png --font-size 30
        """
    )
    
    parser.add_argument('photo_path', 
                       help='Path to the PNG photo to process')
    parser.add_argument('--no-save', 
                       action='store_true',
                       help="Don't save translation to the translations file")
    parser.add_argument('--font-size', 
                       type=int, 
                       default=config.DEFAULT_FONT_SIZE,
                       help=f'Font size for caption (default: {config.DEFAULT_FONT_SIZE})')
    
    args = parser.parse_args()
    
    # Override font size if specified
    if args.font_size != config.DEFAULT_FONT_SIZE:
        print(f"Using custom font size: {args.font_size}px")
        config.DEFAULT_FONT_SIZE = args.font_size
    
    # Run the pipeline
    success = test_single_photo(args.photo_path, save_to_translations_file=not args.no_save)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
