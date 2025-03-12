"""
API Client Module

Handles communication with the Railway server via secure REST API.
"""
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ApiClient:
    """Handles API communication with the Railway server."""
    
    def __init__(self, auth_manager):
        """Initialize with auth manager for authentication."""
        self.auth = auth_manager
        self.api_base_url = os.environ.get("RAILWAY_API_URL", "https://integrity-api.railway.app")
        self.query_endpoint = "/api/query"
    
    def send_query(self, data_block):
        """
        Send a query to the Railway server.
        
        Args:
            data_block (dict): The structured JSON data block containing user query and context.
            
        Returns:
            str: The response from the API or error message.
        """
        try:
            # Get authentication token
            token = self.auth.get_auth_token()
            if not token:
                return "Authentication error: Please log in to your account."
            
            # Prepare headers with authentication
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            # Send request to the API
            response = requests.post(
                f"{self.api_base_url}{self.query_endpoint}", 
                headers=headers,
                json=data_block,
                timeout=30  # 30 second timeout
            )
            
            # Check for successful response
            if response.status_code == 200:
                return response.json().get("response", "No response content")
            elif response.status_code == 401:
                return "Authentication error: Your session has expired. Please log in again."
            elif response.status_code == 429:
                return "Rate limit exceeded: You've reached your daily query limit (100 queries)."
            else:
                return f"Server error ({response.status_code}): {response.text}"
                
        except requests.RequestException as e:
            return f"Connection error: Could not connect to the server. {str(e)}"
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    def check_rate_limit(self):
        """
        Check the user's current rate limit status.
        
        Returns:
            dict: Dictionary with quota information or None on error.
        """
        try:
            # Get authentication token
            token = self.auth.get_auth_token()
            if not token:
                return None
            
            # Prepare headers with authentication
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            # Send request to the API
            response = requests.get(
                f"{self.api_base_url}/api/quota", 
                headers=headers,
                timeout=10
            )
            
            # Check for successful response
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception:
            return None 