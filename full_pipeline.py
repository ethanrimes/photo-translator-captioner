# full_pipeline.py
"""
Run the full translation pipeline on all photos
"""

import os
import config
from image_processor import save_image_with_caption
from openai_translator import translate_whatsapp_image

def load_existing_translations():
    """Load existing translations from file."""
    translations = {}
    
    if not os.path.exists(config.TRANSLATIONS_FILE):
        return translations
    
    with open(config.TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse translations
    entries = content.split('='*50)
    for entry in entries:
        lines = entry.strip().split('\n')
        if lines and lines[0].startswith('FILE: '):
            filename = lines[0].replace('FILE: ', '').strip()
            translation = '\n'.join(lines[1:]).strip()
            if translation:
                translations[filename] = translation
    
    return translations

def save_translations(translations):
    """Save all translations to file."""
    with open(config.TRANSLATIONS_FILE, 'w', encoding='utf-8') as f:
        for filename, translation in translations.items():
            f.write(f"FILE: {filename}\n")
            f.write(f"{translation}\n")
            f.write('='*50 + '\n\n')

def run_full_pipeline():
    """Run the complete pipeline on all photos."""
    print("Starting full pipeline...")
    
    # Get all PNG files
    photos = [f for f in os.listdir(config.PHOTOS_DIR) if f.endswith('.png') or f.endswith('.PNG')]
    
    if not photos:
        print(f"No PNG files found in {config.PHOTOS_DIR}")
        return
    
    print(f"Found {len(photos)} photos to process")
    
    # Step 1: Translate all photos
    print("\n" + "="*50)
    print("STEP 1: Translating all photos")
    print("="*50)
    
    translations = load_existing_translations()
    print(f"Loaded {len(translations)} existing translations")
    
    for i, photo in enumerate(photos, 1):
        if photo in translations:
            print(f"[{i}/{len(photos)}] {photo} - Using existing translation")
            continue
        
        print(f"[{i}/{len(photos)}] Translating: {photo}")
        photo_path = os.path.join(config.PHOTOS_DIR, photo)
        
        try:
            translation = translate_whatsapp_image(photo_path)
            translations[photo] = translation
            # Save after each translation in case of interruption
            save_translations(translations)
            print(f"  ✓ Translation saved")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            translations[photo] = f"Error: Could not translate - {str(e)}"
    
    print(f"\nAll translations complete. Saved to: {config.TRANSLATIONS_FILE}")
    print("\n⚠️  You can now manually edit the translations file if needed.")
    input("Press Enter to continue with caption generation...")
    
    # Step 2: Reload translations and apply captions
    print("\n" + "="*50)
    print("STEP 2: Applying captions to images")
    print("="*50)
    
    translations = load_existing_translations()
    successful = 0
    
    for i, photo in enumerate(photos, 1):
        print(f"[{i}/{len(photos)}] Processing: {photo}")
        
        if photo not in translations:
            print(f"  ⚠️  No translation found, skipping")
            continue
        
        photo_path = os.path.join(config.PHOTOS_DIR, photo)
        output_path = os.path.join(config.OUTPUT_DIR, f"captioned_{photo}")
        
        try:
            save_image_with_caption(photo_path, output_path, translations[photo])
            print(f"  ✓ Saved to: {output_path}")
            successful += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "="*50)
    print(f"Pipeline complete! Successfully processed {successful}/{len(photos)} photos")
    print(f"Output directory: {config.OUTPUT_DIR}")
    print(f"Translations file: {config.TRANSLATIONS_FILE}")

if __name__ == "__main__":
    run_full_pipeline()