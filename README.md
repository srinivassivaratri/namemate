# Namemate

## Task
A CLI tool that automatically renames screenshot files based on their content using OCR and AI. Perfect for organizing messy screenshot folders with meaningless names like "Screenshot_20240126.png".

## Spec
- Reads text from screenshots, PDFs, audio, and video files
- Uses AI to generate meaningful single-word names
- Handles batch processing
- Supports test mode for safe previews
- Works on Windows (via WSL) and Linux

## Plan

1. Install Dependencies

   Install the required Python packages using pip:
   ```bash
   pip install pillow pytesseract torch groq python-dotenv speech_recognition PyPDF2
   ```

   For Tesseract OCR:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr

   # macOS
   brew install tesseract
   ```

2. Set Up Environment Variables

   Create a .env file in the project directory with your GROQ API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. Usage

   Test Mode (Processes First 10 Files Only):
   ```bash
   python rename_tool.py -d "path/to/your/screenshots" -t
   ```

   This will process the first 10 files in the specified directory as a test run.

   Process All Files with Confirmation:
   ```bash
   python rename_tool.py -d "path/to/your/screenshots"
   ```

   You'll be prompted to confirm before renaming the files.

   Process All Files without Confirmation:
   ```bash
   python rename_tool.py -d "path/to/your/screenshots" -y
   ```

   This will rename all files in the directory without asking for confirmation.

4. Example

   Before:
   - Screenshot_20240126.png
   - image_001.jpg
   - screen_capture_2024.png

   After:
   - netconfig.png
   - docker.png
   - apitest.png

## Code

Main features:
- Extracts text from images, PDFs, audio and video files
- Generates filenames using GROQ API
- Handles batch renaming with preview
- Cross-platform support
- Comprehensive logging

Dependencies:
- pillow: Image processing
- pytesseract: OCR engine
- torch: AI model support
- groq: AI interactions
- python-dotenv: Environment variables
- speech_recognition: Audio processing
- PyPDF2: PDF text extraction

---

Feel free to contribute to the project or suggest improvements!
