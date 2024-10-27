# Namemate

## Task
A CLI tool that automatically renames screenshot files based on their content using OCR and AI. Perfect for organizing messy screenshot folders with meaningless names like "Screenshot_20240126.png".

## Spec
- Reads text from screenshots using OCR.
- Uses AI to generate meaningful single-word names.
- Handles batch processing.
- Supports test mode for safe previews.
- Works on Windows (via WSL) and Linux.

## Plan

1. **Install Dependencies**

   Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt   ```

   Or install them manually:
   ```bash
   pip install pillow pytesseract torch groq python-dotenv   ```

   **Note:** You also need to have Tesseract OCR installed on your system.

   - For Ubuntu/Debian:
     ```bash
     sudo apt-get install tesseract-ocr     ```

   - For macOS (using Homebrew):
     ```bash
     brew install tesseract     ```

2. **Set Up Environment Variables**

   Create a `.env` file in the project directory with your GROQ API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here   ```

3. **Usage**

   - **Test Mode (Processes First 10 Files Only):**
     ```bash
     python rename_tool.py -d "path/to/your/screenshots" -t     ```

     This will process the first 10 files in the specified directory as a test run.

   - **Process All Files with Confirmation:**
     ```bash
     python rename_tool.py -d "path/to/your/screenshots"     ```

     You'll be prompted to confirm before renaming the files.

   - **Process All Files without Confirmation:**
     ```bash
     python rename_tool.py -d "path/to/your/screenshots" -y     ```

     This will rename all files in the directory without asking for confirmation.

4. **Example**

   Before:

   - `Screenshot_20240126.png`
   - `image_001.jpg`
   - `screen_capture_2024.png`

   After:

   - `netconfig.png`
   - `docker.png`
   - `apitest.png`

5. **Recreating the Virtual Environment (Optional)**

   If you need to set up a virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   pip install -r requirements.txt   ```

## Code

The main script is `rename_tool.py`. It performs the following steps:

- **Extract Text from Images:**
  - Uses `pytesseract` for OCR to extract meaningful text from images.
  - Applies preprocessing to improve text extraction accuracy.

- **Generate Filenames with AI:**
  - Sends the extracted text to an AI model using the GROQ API.
  - Generates concise, single-word filenames based on the content.

- **Rename Files:**
  - Renames the image files using the generated filenames.
  - Ensures filenames are unique within the directory.

- **Preview and Confirmation:**
  - Displays a preview of the proposed changes.
  - Asks for user confirmation before proceeding (unless `-y` flag is used).

### **Features**

- **Cross-Platform Compatibility:**
  - Supports Windows paths (converted for WSL if necessary).
  - Works seamlessly on Linux systems.

- **Batch Processing:**
  - Can process all files in a directory.
  - Test mode (`-t` flag) allows you to run on a subset of files.

- **Logging:**
  - Uses Python's `logging` module for informative messages.
  - Errors and important events are logged for troubleshooting.

- **Customizable:**
  - The script can be modified to adjust naming conventions or processing logic.
  - Adjust the OCR confidence threshold or filename length limits as needed.

### **Dependencies**

- `pillow` (PIL): Image processing.
- `pytesseract`: OCR engine.
- `torch`: Required by some AI models.
- `groq`: For AI interactions via GROQ API.
- `python-dotenv`: Load environment variables from a `.env` file.

---

Feel free to contribute to the project or suggest improvements!
