"""
GUI Module

Provides a minimalist chat overlay for user interaction.
"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QLineEdit, QPushButton, QLabel, 
                             QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette

class ChatOverlay(QWidget):
    """A minimalist, floating chat overlay window."""
    
    def __init__(self, submit_callback):
        super().__init__()
        self.submit_callback = submit_callback
        self.is_visible = False
        self.shortcut_key = "Alt+Space"  # Default shortcut
        
        # Window setup
        self.setup_window()
        
        # Set up UI components
        self.init_ui()
        
        # Set up keyboard shortcut
        # In a real implementation, would use global hotkey library
        # For now, just a placeholder notification
        print(f"Press {self.shortcut_key} to activate Integrity Assistant")
        
        # Simulate the shortcut for demonstration
        QTimer.singleShot(500, self.toggle_visibility)
    
    def setup_window(self):
        """Configure window properties."""
        # Make window frameless and stay on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set initial size and position
        screen_geometry = QApplication.desktop().availableGeometry()
        self.window_width = 400
        self.window_height = 500
        x = screen_geometry.width() - self.window_width - 20
        y = 100
        self.setGeometry(x, y, self.window_width, self.window_height)
        
        # Track mouse for dragging
        self.old_pos = None
        self.setMouseTracking(True)
    
    def init_ui(self):
        """Initialize the user interface components."""
        # Set dark theme
        self.set_dark_theme()
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title bar
        title_bar = self.create_title_bar()
        main_layout.addLayout(title_bar)
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D30;
                color: #FFFFFF;
                border: 1px solid #3E3E42;
                border-radius: 5px;
            }
        """)
        self.chat_display.setFont(QFont("Segoe UI", 10))
        self.chat_display.setAcceptRichText(True)
        main_layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask anything...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #3E3E42;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.input_field.setFont(QFont("Segoe UI", 10))
        self.input_field.returnPressed.connect(self.submit_query)
        
        self.submit_btn = QPushButton("Send")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #1C97EA;
            }
            QPushButton:pressed {
                background-color: #0063B1;
            }
        """)
        self.submit_btn.clicked.connect(self.submit_query)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_btn)
        
        main_layout.addLayout(input_layout)
        
        # Add welcome message
        self.display_response("Welcome to Integrity Assistant 1.0.2! How can I help you today?")
        
        # Set layout
        self.setLayout(main_layout)
    
    def create_title_bar(self):
        """Create a custom title bar."""
        title_layout = QHBoxLayout()
        
        # Title
        title = QLabel("Integrity Assistant")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF;")
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #AAAAAA;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                color: #FF5555;
            }
        """)
        close_btn.clicked.connect(self.toggle_visibility)
        
        # Minimize button
        min_btn = QPushButton("_")
        min_btn.setFixedSize(20, 20)
        min_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #AAAAAA;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                color: #FFFFFF;
            }
        """)
        min_btn.clicked.connect(self.toggle_visibility)
        
        # Add to layout
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(min_btn)
        title_layout.addWidget(close_btn)
        
        return title_layout
    
    def set_dark_theme(self):
        """Apply dark theme to the entire widget."""
        self.setStyleSheet("""
            QWidget {
                background-color: #252526;
                color: #FFFFFF;
            }
        """)
    
    def submit_query(self):
        """Handle query submission."""
        query_text = self.input_field.text().strip()
        if not query_text:
            return
            
        # Add user query to display
        self.chat_display.append(f"<div style='color:#AAAAFF;'><b>You:</b> {query_text}</div>")
        
        # Clear input field
        self.input_field.clear()
        
        # Temporary "thinking" message
        self.chat_display.append("<div style='color:#888888;'><i>Processing...</i></div>")
        
        # Call the callback
        if self.submit_callback:
            self.submit_callback(query_text)
    
    def display_response(self, response_text):
        """Display the assistant's response in the chat."""
        # Remove the temporary "thinking" message if it exists
        current_html = self.chat_display.toHtml()
        if "<i>Processing...</i>" in current_html:
            current_html = current_html.replace("<div style='color:#888888;'><i>Processing...</i></div>", "")
            self.chat_display.setHtml(current_html)
        
        # Add the response
        self.chat_display.append(f"<div style='color:#88FF88;'><b>Assistant:</b> {response_text}</div>")
        
        # Scroll to bottom
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def toggle_visibility(self):
        """Toggle the visibility of the overlay."""
        if self.is_visible:
            self._animate_hide()
        else:
            self._animate_show()
    
    def _animate_show(self):
        """Animate the window appearing."""
        self.show()
        self.is_visible = True
        
        # Give focus to input field
        self.input_field.setFocus()
    
    def _animate_hide(self):
        """Animate the window disappearing."""
        self.hide()
        self.is_visible = False
    
    def mousePressEvent(self, event):
        """Track mouse press for dragging the window."""
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        """Handle window dragging."""
        if self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()
    
    def mouseReleaseEvent(self, event):
        """Handle end of dragging."""
        if event.button() == Qt.LeftButton:
            self.old_pos = None
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        # Escape key closes the window
        if event.key() == Qt.Key_Escape:
            self.toggle_visibility()
        else:
            super().keyPressEvent(event) 