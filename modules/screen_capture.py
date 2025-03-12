"""
Screen Capture Module

Handles screen capture and OCR text extraction at 2 frames per second.
"""
import os
import time
import pytesseract
from PIL import Image, ImageGrab
import io

class ScreenCapture:
    """Manages screen capture and OCR text extraction."""
    
    def __init__(self):
        # Set path to Tesseract OCR if not in system PATH
        if os.name == 'nt':  # Windows
            tesseract_path = os.environ.get('TESSERACT_PATH', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def capture(self):
        """Capture the entire screen and return the image."""
        try:
            # Capture the entire screen
            screenshot = ImageGrab.grab()
            return screenshot
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
    
    def extract_text(self, image):
        """Extract text from the captured image using OCR."""
        if image is None:
            return ""
            
        try:
            # Extract text using pytesseract
            text = pytesseract.image_to_string(image)
            
            # Clean up the text (remove extra whitespace)
            text = ' '.join(text.split())
            
            # Dispose of the image to preserve privacy
            image = None
            
            return text
        except Exception as e:
            print(f"Error extracting text: {e}")
            return "" 