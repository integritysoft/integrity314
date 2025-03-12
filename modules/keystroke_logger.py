"""
Keystroke Logger Module

Manages system-wide keystroke logging with timestamps.
"""
import threading
from pynput import keyboard
import time

class KeystrokeLogger:
    """Manages logging of keystrokes throughout the system."""
    
    def __init__(self):
        self.running = False
        self.listener = None
        self.callback = None
        self.buffer = ""
        self.last_timestamp = time.time()
        
        # List of sensitive field identifiers - could be expanded
        self.sensitive_prefixes = ["password", "passwd", "pwd", "pin", "credit", "card", 
                                  "cvv", "ssn", "social", "secret"]
        self.sensitive_mode = False
    
    def start(self, callback_function):
        """Start the keystroke logger."""
        if self.running:
            return
            
        self.running = True
        self.callback = callback_function
        
        # Start keyboard listener in a separate thread
        self.listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.listener.start()
    
    def _on_key_press(self, key):
        """Handle key press events."""
        if not self.running:
            return

        try:
            # Check if we're in a potential sensitive field
            self._check_sensitive_context()
            
            # Convert key to string representation
            key_str = ""
            if hasattr(key, 'char') and key.char:
                key_str = key.char
            else:
                # Handle special keys
                key_str = f"[{str(key).replace('Key.', '')}]"
            
            # Skip if in sensitive mode
            if self.sensitive_mode:
                key_str = "*"
                
            # Update buffer
            self.buffer += key_str
            
            # Check if it's time to flush the buffer (word or special key)
            current_time = time.time()
            if (current_time - self.last_timestamp > 1.0 or 
                key_str.startswith('[') or 
                len(self.buffer) > 20):
                self._flush_buffer()
                
        except Exception as e:
            print(f"Error processing keystroke: {e}")
    
    def _on_key_release(self, key):
        """Handle key release events."""
        # For certain keys like Enter, we want to flush immediately
        if key == keyboard.Key.enter or key == keyboard.Key.tab:
            self._flush_buffer()
            
        # Exit sensitive mode on shift+tab
        if key == keyboard.Key.tab and keyboard.Key.shift in self._active_keys():
            self.sensitive_mode = False
    
    def _active_keys(self):
        """Get list of currently active keys (implementation placeholder)."""
        # This is a simplified version, would need platform-specific implementation
        return []
    
    def _check_sensitive_context(self):
        """Check if current context might be a sensitive field."""
        # Look for words like 'password' in the recent buffer
        lower_buffer = self.buffer.lower()
        for prefix in self.sensitive_prefixes:
            if prefix in lower_buffer:
                self.sensitive_mode = True
                return
    
    def _flush_buffer(self):
        """Send the current buffer to the callback and reset."""
        if self.buffer and self.callback:
            self.callback(self.buffer)
        
        # Reset buffer and timestamp
        self.buffer = ""
        self.last_timestamp = time.time()
    
    def stop(self):
        """Stop the keystroke logger."""
        self.running = False
        if self.listener:
            self.listener.stop()
            
        # Flush any remaining buffer
        if self.buffer:
            self._flush_buffer() 