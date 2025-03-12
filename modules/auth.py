"""
Authentication Module

Handles Supabase authentication and user session management.
"""
import os
import json
import time
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseAuth:
    """Handles authentication with Supabase."""
    
    def __init__(self):
        """Initialize Supabase client and session data."""
        self.supabase_url = os.environ.get("SUPABASE_URL", "")
        self.supabase_key = os.environ.get("SUPABASE_KEY", "")
        self.client = None
        self.session = None
        self.user_id = None
        
        # Path to store session data
        self.app_data_dir = self._get_app_data_dir()
        self.session_file = os.path.join(self.app_data_dir, "session.json")
        
        # Initialize Supabase client if credentials are available
        self._init_client()
        
        # Try to load existing session
        self._load_session()
    
    def _get_app_data_dir(self):
        """Get or create application data directory."""
        if os.name == 'nt':  # Windows
            app_data = os.path.join(os.environ.get('APPDATA', ''), 'IntegrityAssistant')
        else:  # macOS / Linux
            app_data = os.path.join(os.path.expanduser('~'), '.integrity_assistant')
            
        # Create directory if it doesn't exist
        if not os.path.exists(app_data):
            os.makedirs(app_data)
            
        return app_data
    
    def _init_client(self):
        """Initialize the Supabase client."""
        if self.supabase_url and self.supabase_key:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
            except Exception as e:
                print(f"Failed to initialize Supabase client: {e}")
    
    def _load_session(self):
        """Try to load saved session data."""
        if not os.path.exists(self.session_file):
            return False
            
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
                
            # Check if session contains required fields
            if 'access_token' in session_data and 'refresh_token' in session_data and 'user_id' in session_data:
                self.session = session_data
                self.user_id = session_data['user_id']
                
                # Check if token is expired and try to refresh
                if self._is_token_expired() and not self.refresh_token():
                    return False
                    
                return True
                
        except Exception as e:
            print(f"Failed to load session: {e}")
            
        return False
    
    def _save_session(self):
        """Save session data to file."""
        if not self.session:
            return False
            
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.session, f)
            return True
        except Exception as e:
            print(f"Failed to save session: {e}")
            return False
    
    def _is_token_expired(self):
        """Check if the current access token is expired."""
        if not self.session or 'expires_at' not in self.session:
            return True
            
        # Check if current time is past expiration
        return time.time() > self.session['expires_at']
    
    def login(self, email, password):
        """
        Log in with email and password.
        
        Args:
            email (str): User's email address
            password (str): User's password
            
        Returns:
            bool: True if login successful, False otherwise
        """
        if not self.client:
            return False
            
        try:
            # Attempt to sign in
            response = self.client.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
            
            # Extract session data
            self.session = {
                'access_token': response.session.access_token,
                'refresh_token': response.session.refresh_token,
                'user_id': response.user.id,
                'expires_at': time.time() + 3600  # Assuming 1-hour expiry
            }
            
            self.user_id = response.user.id
            
            # Save session to file
            self._save_session()
            
            return True
            
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def refresh_token(self):
        """
        Refresh the authentication token.
        
        Returns:
            bool: True if refresh successful, False otherwise
        """
        if not self.client or not self.session or 'refresh_token' not in self.session:
            return False
            
        try:
            # Attempt to refresh the token
            response = self.client.auth.refresh_session(self.session['refresh_token'])
            
            # Update session data
            self.session = {
                'access_token': response.session.access_token,
                'refresh_token': response.session.refresh_token,
                'user_id': self.user_id,
                'expires_at': time.time() + 3600  # Assuming 1-hour expiry
            }
            
            # Save updated session
            self._save_session()
            
            return True
            
        except Exception as e:
            print(f"Token refresh failed: {e}")
            return False
    
    def logout(self):
        """
        Log out the current user.
        
        Returns:
            bool: True if logout successful, False otherwise
        """
        if not self.client or not self.session:
            return False
            
        try:
            # Sign out with Supabase
            self.client.auth.sign_out()
            
            # Clear local session data
            self.session = None
            self.user_id = None
            
            # Remove session file
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
                
            return True
            
        except Exception as e:
            print(f"Logout failed: {e}")
            return False
    
    def get_auth_token(self):
        """
        Get the current authentication token.
        
        Returns:
            str: The current access token or None if not authenticated
        """
        if not self.session:
            return None
            
        # Check if token is expired and try to refresh
        if self._is_token_expired() and not self.refresh_token():
            return None
            
        return self.session.get('access_token')
    
    def get_user_id(self):
        """
        Get the current user ID.
        
        Returns:
            str: The current user ID or None if not authenticated
        """
        return self.user_id
    
    def is_authenticated(self):
        """
        Check if the user is currently authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        return self.get_auth_token() is not None 