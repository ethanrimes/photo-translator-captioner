# WhatsApp Screenshot Translator

A Python pipeline that automatically translates WhatsApp conversation screenshots from Spanish to English and adds the translations as captions below the images.

## Features

- 🌐 **Automatic Translation**: Uses OpenAI's GPT-4 Vision to understand and translate WhatsApp conversations
- 📝 **Smart Captions**: Dynamically adjusts caption space based on text length
- ✏️ **Editable Translations**: Saves translations to a text file for manual editing before applying
- 🎨 **Customizable Styling**: Adjustable font size and formatting
- 🚀 **Flexible Processing**: Process single photos or entire directories
- 📅 **Date Handling**: Automatically includes conversation dates (assumes 2025 if year not visible)

## Prerequisites

- Python 3.7+
- OpenAI API key with GPT-4 Vision access

## Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install pillow openai python-dotenv
```

3. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-actual-api-key-here
```

4. Create a `.gitignore` file (if using git):
```
.env
*.pyc
__pycache__/
output/
translations.txt
photos/*.png
```

## Project Structure

```
whatsapp-translator/
├── .env                    # Your OpenAI API key (create this)
├── .gitignore             # Prevents committing sensitive files
├── config.py              # Configuration settings
├── image_processor.py     # Image manipulation functions
├── openai_translator.py   # OpenAI API integration
├── test_white_space.py    # Test caption space addition
├── test_openai_query.py   # Test translation API
├── test_single_photo.py   # Process single photo (CLI tool)
├── full_pipeline.py       # Process all photos
├── photos/                # Input directory for screenshots
├── output/                # Output directory for captioned images
└── translations.txt       # Stored translations (auto-generated)
```

## Usage

### Quick Start - Single Photo

Process a specific WhatsApp screenshot:
```bash
python test_single_photo.py path/to/screenshot.png
```

### Command Line Options

```bash
# Process with custom font size
python test_single_photo.py photo.png --font-size 30

# Process without saving to translations file (quick test)
python test_single_photo.py photo.png --no-save

# Show help
python test_single_photo.py --help
```

### Batch Processing

Process all PNG files in the `photos/` directory:
```bash
python full_pipeline.py
```

This will:
1. Translate all photos via OpenAI
2. Save translations to `translations.txt`
3. Pause for manual editing (optional)
4. Apply captions to all images
5. Save results to `output/` directory

### Testing Components

**Test white space addition:**
```bash
python test_white_space.py
```
Creates sample images with different caption sizes and font sizes.

**Test OpenAI translation:**
```bash
python test_openai_query.py
```
Tests the translation API with a sample image.

## Configuration

Edit `config.py` to customize:

- `DEFAULT_FONT_SIZE`: Caption text size (default: 40px)
- `FONT_FAMILY`: Font for captions (default: Arial)
- `TEXT_COLOR`: Caption text color (default: black)
- `CAPTION_BG_COLOR`: Caption background (default: white)
- `PADDING`: Space around caption text (default: 20px)
- `LINE_SPACING`: Line height multiplier (default: 1.2)
- `OPENAI_MODEL`: GPT model to use (default: gpt-4o)

## Translation File Format

Translations are stored in `translations.txt` with the following format:

```
FILE: screenshot1.png
Date: January 15, 2025

Maria: Hello! How are you today?
Juan: I'm doing great, thanks!
==================================================

FILE: screenshot2.png
Date: January 16, 2025

Carlos: Did you see the game yesterday?
Ana: Yes, it was amazing!
==================================================
```

You can manually edit this file to correct translations before applying captions.

## Workflow Example

1. **Prepare screenshots**: Place WhatsApp conversation PNGs in `photos/` directory

2. **Run initial translation**:
```bash
python full_pipeline.py
```

3. **Review and edit** (optional): Open `translations.txt` and fix any translation errors

4. **Apply captions**: Press Enter in the terminal to continue with caption generation

5. **Find results**: Captioned images will be in `output/` directory

## Single Photo Workflow

For processing individual photos:

```bash
# Translate and caption a specific photo
python test_single_photo.py screenshots/chat_with_maria.png

# Output will be saved as: output/captioned_chat_with_maria.png
```

## Tips

- **Image Quality**: Use clear screenshots for better OCR accuracy
- **Font Size**: Adjust `--font-size` based on image resolution
- **Manual Edits**: The pipeline saves translations before applying them, allowing for corrections
- **API Costs**: Each image translation uses one GPT-4 Vision API call
- **Supported Format**: Currently optimized for PNG files

## Troubleshooting

**"OPENAI_API_KEY not found"**
- Ensure `.env` file exists with your API key
- Check that python-dotenv is installed

**"No PNG files found"**
- Place screenshots in the `photos/` directory
- Ensure files have `.png` extension

**Translation errors**
- Verify your OpenAI API key has GPT-4 Vision access
- Check API quota and billing status
- Ensure images are clear and readable

**Font issues**
- The system will fall back to default font if Arial is unavailable
- You can change the font in `config.py`

## How It Works

1. **Image Analysis**: OpenAI's GPT-4 Vision model analyzes the WhatsApp screenshot
2. **Translation**: The model extracts and translates the conversation from Spanish to English
3. **Dynamic Sizing**: The system calculates required caption space based on text length
4. **Caption Addition**: A white caption area is added below the original image
5. **Text Rendering**: The translation is rendered onto the caption area
6. **File Output**: The captioned image is saved to the output directory

## License

This project is provided as-is for personal and educational use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Future Enhancements

Potential improvements for future versions:
- Support for more languages beyond Spanish
- Batch editing interface for translations
- Support for more image formats (JPEG, WEBP)
- Automatic language detection
- Custom styling templates
- Progress bars for batch processing
- Integration with cloud storage services