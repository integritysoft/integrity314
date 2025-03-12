#!/usr/bin/env python3
"""
Integrity Assistant 1.0.2 - Main Application

This is the entry point for the Integrity Assistant application.
"""
import sys
import os
import json
import threading
import time
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication

# Load environment variables from .env file
load_dotenv()

# Import internal modules
from modules.screen_capture import ScreenCapture
from modules.keystroke_logger import KeystrokeLogger
from modules.gui import ChatOverlay
from modules.api_client import ApiClient
from modules.auth import SupabaseAuth
from modules.login_dialog import LoginDialog

class IntegrityAssistant:
    """Main application class that coordinates all components."""
    
    def __init__(self):
        self.running = False
        self.auth = SupabaseAuth()
        self.api_client = ApiClient(self.auth)
        self.screen_capture = ScreenCapture()
        self.keystroke_logger = KeystrokeLogger()
        self.gui = None  # Will be initialized after login
        
        # Data storage
        self.screen_texts = []
        self.keystrokes = []
    
    def authenticate(self):
        """Show login dialog and authenticate user."""
        login_dialog = LoginDialog(self.auth)
        login_dialog.login_successful.connect(self.on_auth_success)
        
        # Show the dialog and wait for it to complete
        result = login_dialog.exec_()
        
        # Return True if login was successful, False otherwise
        return result == login_dialog.Accepted
    
    def on_auth_success(self):
        """Handle successful authentication."""
        print(f"Authenticated as user: {self.auth.get_user_id()}")
    
    def start(self):
        """Start all components of the application."""
        if self.running:
            return
            
        print("Starting Integrity Assistant...")
        self.running = True
        
        # Initialize GUI if not already done
        if not self.gui:
            self.gui = ChatOverlay(self.submit_query)
        
        # Start screen capture thread
        self.screen_capture_thread = threading.Thread(
            target=self.run_screen_capture, 
            daemon=True
        )
        self.screen_capture_thread.start()
        
        # Start keystroke logger
        self.keystroke_logger.start(self.on_keystroke)
        
        # Show GUI
        self.gui.show()
    
    def run_screen_capture(self):
        """Run the screen capture loop at 2 FPS."""
        while self.running:
            try:
                # Capture screen and extract text
                image = self.screen_capture.capture()
                text = self.screen_capture.extract_text(image)
                
                # Only store if text was found
                if text:
                    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    self.screen_texts.append({
                        "timestamp": timestamp,
                        "text": text
                    })
                    
                    # Keep only the last 30 entries (approximately 15 seconds at 2 FPS)
                    if len(self.screen_texts) > 30:
                        self.screen_texts.pop(0)
                
                # Sleep to maintain 2 FPS
                time.sleep(0.5)
            except Exception as e:
                print(f"Error in screen capture: {e}")
                time.sleep(1)
    
    def on_keystroke(self, key_event):
        """Handle keystroke events from the logger."""
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.keystrokes.append({
            "timestamp": timestamp,
            "content": key_event
        })
        
        # Keep only the last 100 keystrokes
        if len(self.keystrokes) > 100:
            self.keystrokes.pop(0)
    
    def submit_query(self, query_text):
        """Submit a query to the API with context data."""
        try:
            # Prepare data block
            data_block = {
                "user_query": query_text,
                "context": {
                    "screen_texts": self.screen_texts,
                    "recent_keystrokes": self.keystrokes,
                    "metadata": {
                        "user_id": self.auth.get_user_id(),
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    }
                }
            }
            
            # Send to API
            response = self.api_client.send_query(data_block)
            
            # Update UI with response
            if response:
                self.gui.display_response(response)
            else:
                self.gui.display_response("Sorry, I couldn't process your request.")
                
        except Exception as e:
            self.gui.display_response(f"Error: {str(e)}")
    
    def stop(self):
        """Stop all application components."""
        print("Stopping Integrity Assistant...")
        self.running = False
        self.keystroke_logger.stop()
        if self.gui:
            self.gui.hide()

def main():
    """Application entry point."""
    # Initialize QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Integrity Assistant")
    
    # Create the assistant
    assistant = IntegrityAssistant()
    
    # Authenticate user
    if not assistant.authenticate():
        print("Authentication failed or cancelled.")
        sys.exit(1)
    
    # Start the assistant
    assistant.start()
    
    # Start event loop
    exit_code = app.exec_()
    
    # Clean up
    assistant.stop()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 