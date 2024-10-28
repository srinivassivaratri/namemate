# Namemate

## Task
CLI tool that intelligently renames files based on their content using OCR and AI. Extracts text from images, PDFs, audio, and video files to generate meaningful single-word names.

## Spec
- OCR text extraction from images using Tesseract
- PDF text extraction using PyPDF2 
- Audio transcription using SpeechRecognition
- Video transcription (extracts audio first)
- AI filename generation using Groq API
- Batch processing with preview mode
- Cross-platform (Linux/WSL)
- Handles duplicates with auto-numbering

## Plan

1. Install Dependencies
```bash
pip install pillow pytesseract torch groq python-dotenv speech_recognition PyPDF2
sudo apt install tesseract-ocr ffmpeg    # Linux/WSL
brew install tesseract ffmpeg            # macOS
```

2. Configure
```bash
# Create .env with your Groq API key
GROQ_API_KEY=your_key_here
```

3. Usage
```bash
# Test mode (first 10 files)
python rename_tool.py -d "/path/to/files" -t

# Process all files with confirmation
python rename_tool.py -d "/path/to/files"

# Process all files without confirmation
python rename_tool.py -d "/path/to/files" -y
```

## Code

Key Components:
- File type detection and text extraction
- OCR with preprocessing for better results
- Smart filename generation using Groq LLM
- Duplicate name handling
- Cross-platform path conversion
- Comprehensive logging

Dependencies:
- pillow: Image processing
- pytesseract: OCR engine
- groq: AI API client
- python-dotenv: Environment config
- speech_recognition: Audio transcription
- PyPDF2: PDF text extraction
- ffmpeg: Video processing

---

Feel free to contribute to the project or suggest improvements!
