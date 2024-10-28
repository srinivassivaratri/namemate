#!/usr/bin/env python3

import os
import argparse
import platform
from datetime import datetime
from PIL import Image
import pytesseract
import torch
from collections import Counter
import re
from groq import Groq
from dotenv import load_dotenv
import logging
from pathlib import Path
import speech_recognition as sr
import PyPDF2

# Load environment variables
load_dotenv()

# Set up basic logging
logging.basicConfig(level=logging.INFO)

def convert_windows_path_to_wsl(path):
    if platform.system() == "Linux":
        if ':' in path:
            drive, rest = path.split(':', 1)
            wsl_path = f"/mnt/{drive.lower()}{rest.replace('\\', '/')}"
            return wsl_path
    return path

def extract_text_from_image(image_path):
    """Extract text from image using OCR with better preprocessing."""
    try:
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get multiple text blocks for better context
        text_blocks = pytesseract.image_to_data(
            image,
            config='--psm 6 --oem 3 -l eng',
            output_type=pytesseract.Output.DICT
        )
        
        # Combine text with confidence scores
        meaningful_text = []
        for i, conf in enumerate(text_blocks['conf']):
            if conf > 30:  # Filter low confidence text
                text = text_blocks['text'][i].strip()
                if text and len(text) > 1:  # Skip single characters
                    meaningful_text.append(text)
        
        if meaningful_text:
            # Join all meaningful text for better context
            full_text = ' '.join(meaningful_text)
            # Clean up the text
            clean_text = re.sub(r'[^\w\s-]', ' ', full_text)  # Keep hyphens
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            return clean_text
            
        return None
    except Exception as e:
        logging.error(f"Error extracting text from {image_path}: {e}")
        return None

def extract_text_from_file(file_path):
    """Extract text from various file types."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']:
        # Image files
        return extract_text_from_image(file_path)
    elif ext in ['.txt', '.md', '.py', '.java', '.html', '.csv', '.json', '.xml', '.pdf']:
        # Text and PDF files
        if ext == '.pdf':
            return extract_text_from_pdf(file_path)
        else:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Clean up the text
                    clean_text = re.sub(r'[^\w\s-]', ' ', content)
                    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                    return clean_text
            except Exception as e:
                logging.error(f"Error reading {file_path}: {e}")
                return None
    elif ext in ['.mp3', '.wav', '.ogg', '.flac']:
        # Audio files
        return extract_text_from_audio(file_path)
    elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
        # Video files
        return extract_text_from_video(file_path)
    else:
        # Other file types
        return None

def clean_filename(text):
    """Clean and format text for use as filename."""
    if not text:
        return None
    
    # Convert to lowercase and replace spaces with underscores
    text = text.lower().replace(' ', '_')
    
    # Remove any non-alphanumeric characters except underscores
    text = re.sub(r'[^a-z0-9_]', '', text)
    
    # Limit length to 50 characters
    text = text[:50]
    
    # Remove multiple consecutive underscores
    text = re.sub(r'_+', '_', text)
    
    # Remove leading/trailing underscores
    text = text.strip('_')
    
    return text if text else None

def get_smart_name_llm(content):
    """Get filename suggestion from LLM with single-word naming."""
    prompt = f"""Generate a single-word filename that best describes this screenshot content.

    Content: "{content}"

    Rules:
    1. Return ONLY ONE WORD (no underscores)
    2. Maximum 15 characters
    3. Must be descriptive and meaningful
    4. Use common abbreviations if needed:
       - config
       - auth
       - admin
       - docs
       - dev
       - prod
       - api
       - db
       - app
       - sys
       - net
       - log
       - ui
       - cli

    Examples based on content:
    - Terminal showing ports -> "ports"
    - User authentication error -> "authfail"
    - Network configuration -> "netconfig"
    - Database backup screen -> "dbbackup"
    - System logs -> "syslog"
    - API documentation -> "apidocs"
    - Git merge conflict -> "gitmerge"
    - Docker settings -> "docker"
    - User interface -> "interface"
    - Build process -> "build"

    Return ONLY the filename (without extension), nothing else."""
    
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",
            temperature=0.1,
        )
        suggestion = response.choices[0].message.content.strip()
        
        # Post-process the suggestion
        clean_name = clean_filename(suggestion)
        if clean_name:
            # Remove any underscores
            clean_name = clean_name.replace('_', '')
            
            # Limit length
            clean_name = clean_name[:15]
            
            # Ensure name is meaningful
            if len(clean_name) < 3 or clean_name in ['error', 'unknown', 'image', 'screenshot']:
                # Try to extract meaningful word from original filename
                original_name = os.path.splitext(os.path.basename(content))[0]
                if original_name and not original_name.startswith('screenshot'):
                    words = re.findall(r'[a-z]+', original_name.lower())
                    if words:
                        return words[0][:15]
                return None
                
            return clean_name
        return None
    except Exception as e:
        logging.error(f"Error getting LLM suggestion: {e}")
        return None

def generate_unique_name(base_name, ext, name_counter):
    """Generate unique filename with counter if needed, preserving the original extension."""
    if name_counter[base_name] > 1:
        return f"{base_name}_{name_counter[base_name]}{ext}"
    return f"{base_name}{ext}"

def rename_files(directory='.', confirm=True, batch_size=10):
    """Rename files in the specified directory based on content."""
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        if not files:
            print("No files found in the directory.")
            return
        
        total_files = len(files)
        print(f"\nFound {total_files} files.")
        
        if batch_size:
            files = files[:batch_size]
            print(f"Processing first {batch_size} files as a test batch...")
        
        name_counter = Counter()
        new_names = []
        preview_data = []
        
        for idx, filename in enumerate(files, 1):
            file_path = os.path.join(directory, filename)
            print(f"\nProcessing file {idx}/{len(files)}: {filename}")
            
            content = extract_text_from_file(file_path)
            if not content:
                print(f"No content extracted from {filename}")
                continue
            
            try:
                # Generate name using LLM
                base_name = get_smart_name_llm(content)
                if not base_name:
                    print(f"Could not generate name for {filename}")
                    continue
                
                # Generate unique name
                _, ext = os.path.splitext(filename)
                new_name = generate_unique_name(base_name, ext, name_counter)
                name_counter[base_name] += 1
                
                print(f"Generated name: {base_name}")
                new_names.append(new_name)
                
                preview_data.append({
                    'old_name': filename,
                    'new_name': new_name,
                    'content': content[:100]
                })
                
            except Exception as e:
                logging.error(f"Error processing {filename}: {e}")
                continue
        
        if not preview_data:
            print("No files could be processed successfully.")
            return
        
        if confirm:
            print("\nPreview of changes:")
            for data in preview_data:
                print(f"\nOld name: {data['old_name']}")
                print(f"New name: {data['new_name']}")
                print(f"Content: {data['content']}")
            
            proceed = input("\nProceed with renaming? (Y/n): ").lower().strip() != 'n'
            if not proceed:
                print("Renaming cancelled.")
                return
        
        # Perform renaming
        for data in preview_data:
            old_path = os.path.join(directory, data['old_name'])
            new_path = os.path.join(directory, data['new_name'])
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {data['old_name']} -> {data['new_name']}")
            except OSError as e:
                print(f"Could not rename {data['old_name']}: {e}")
        
        print("\nRenaming completed.")
        if batch_size:
            print(f"\nThis was a test run with {batch_size} files.")
            print("If you're satisfied with the results, run without --test flag to process all files.")
            
    except Exception as e:
        logging.error(f"Error in rename_files: {e}")
        print(f"An error occurred: {e}")

def extract_text_from_pdf(file_path):
    """Extract text from PDF files with improved handling."""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            
            if reader.is_encrypted:
                try:
                    reader.decrypt('')
                except Exception as e:
                    logging.error(f"Cannot decrypt PDF {file_path}: {e}")
                    return None
            
            text = ''
            max_pages = 10  # Limit to first 10 pages
            for i, page in enumerate(reader.pages):
                if i >= max_pages:
                    break
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                except Exception as e:
                    logging.error(f"Error extracting text from page {i+1} of {file_path}: {e}")
                    continue  # Skip to the next page
            
            clean_text = re.sub(r'[^\w\s-]', ' ', text)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            return clean_text if clean_text else None
    except Exception as e:
        logging.error(f"Error extracting text from PDF {file_path}: {e}")
        return None

def extract_text_from_audio(file_path):
    """Extract text from audio files using speech recognition."""
    try:
        r = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            clean_text = re.sub(r'[^\w\s-]', ' ', text)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            return clean_text if clean_text else None
    except Exception as e:
        logging.error(f"Error extracting text from audio {file_path}: {e}")
        return None

def extract_text_from_video(file_path):
    """Extract text from video files by extracting audio and performing speech recognition."""
    temp_audio = "temp_audio.wav"
    try:
        # Extract audio using ffmpeg
        os.system(f"ffmpeg -i \"{file_path}\" -q:a 0 -map a {temp_audio} -y")
        # Extract text from audio
        text = extract_text_from_audio(temp_audio)
        # Remove temporary audio file
        os.remove(temp_audio)
        return text
    except Exception as e:
        logging.error(f"Error extracting text from video {file_path}: {e}")
        if os.path.exists(temp_audio):
            os.remove(temp_audio)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A file renamer that generates filenames based on image content."
    )
    parser.add_argument('-d', '--directory', default='.', 
                        help='Directory to rename files in. Default is current directory.')
    parser.add_argument('-y', '--yes', action='store_true', 
                        help='Do not ask for confirmation before renaming')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Run on first 10 files only as a test')
    args = parser.parse_args()
    
    directory = convert_windows_path_to_wsl(args.directory)
    rename_files(directory, confirm=not args.yes, batch_size=10 if args.test else None)

