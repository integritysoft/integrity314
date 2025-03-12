"""
Login Dialog Module

Provides a login dialog for Supabase authentication.
"""
import os
import webbrowser
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

class LoginDialog(QDialog):
    """Dialog for user authentication."""
    
    login_successful = pyqtSignal()
    
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth = auth_manager
        self.setWindowTitle("Integrity Assistant - Login")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #252526;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QLineEdit {
                background-color: #3E3E42;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1C97EA;
            }
            QPushButton:pressed {
                background-color: #0063B1;
            }
            QPushButton#create_account_btn {
                background-color: transparent;
                color: #0078D7;
                text-decoration: underline;
                border: none;
            }
            QPushButton#create_account_btn:hover {
                color: #1C97EA;
            }
        """)
        
        # Set up UI components
        self.init_ui()
        
        # Check if already authenticated
        if self.auth.is_authenticated():
            self.accept()
            self.login_successful.emit()
    
    def init_ui(self):
        """Initialize the UI components."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel("Login to Integrity Assistant")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Access your account to use the assistant")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #AAAAAA;")
        main_layout.addWidget(subtitle)
        
        # Spacer
        main_layout.addSpacing(10)
        
        # Email input
        email_label = QLabel("Email")
        email_label.setFont(QFont("Segoe UI", 10))
        main_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setFont(QFont("Segoe UI", 10))
        main_layout.addWidget(self.email_input)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 10))
        main_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 10))
        main_layout.addWidget(self.password_input)
        
        # Login button
        self.login_btn = QPushButton("Log In")
        self.login_btn.setFont(QFont("Segoe UI", 10))
        self.login_btn.clicked.connect(self.attempt_login)
        main_layout.addWidget(self.login_btn)
        
        # Create account link
        account_layout = QHBoxLayout()
        account_layout.addStretch()
        
        account_label = QLabel("Don't have an account?")
        account_label.setFont(QFont("Segoe UI", 9))
        account_label.setStyleSheet("color: #AAAAAA;")
        
        create_account_btn = QPushButton("Create one")
        create_account_btn.setObjectName("create_account_btn")
        create_account_btn.setFont(QFont("Segoe UI", 9))
        create_account_btn.clicked.connect(self.open_signup_page)
        
        account_layout.addWidget(account_label)
        account_layout.addWidget(create_account_btn)
        account_layout.addStretch()
        
        main_layout.addLayout(account_layout)
        
        # Daily quota note
        quota_note = QLabel("Note: Free accounts are limited to 100 queries per day")
        quota_note.setFont(QFont("Segoe UI", 8))
        quota_note.setStyleSheet("color: #888888;")
        quota_note.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(quota_note)
        
        # Set layout
        self.setLayout(main_layout)
    
    def attempt_login(self):
        """Attempt to log in with provided credentials."""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both email and password.")
            return
        
        # Show wait cursor
        self.setCursor(Qt.WaitCursor)
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Logging in...")
        
        # Attempt login
        success = self.auth.login(email, password)
        
        # Reset cursor
        self.setCursor(Qt.ArrowCursor)
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Log In")
        
        if success:
            self.login_successful.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", 
                               "Invalid email or password. Please try again.")
    
    def open_signup_page(self):
        """Open the web browser to the signup page."""
        # This URL would be replaced with the actual signup page
        webbrowser.open("https://integrity-web.vercel.app/signup")
        
        QMessageBox.information(self, "Create Account", 
                              "Please create an account on the website, then return here to log in.") 