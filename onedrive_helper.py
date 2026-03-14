#!/usr/bin/env python3
"""
OneDrive Integration Helper

This script helps set up OAuth2 authentication with Microsoft OneDrive
and provides methods to download .docx files from OneDrive.
"""

import json
import os
import webbrowser
from urllib.parse import urlencode, parse_qs
import requests
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class OneDriveClient:
    """Client for interacting with OneDrive API."""
    
    def __init__(self, client_id: str, client_secret: str, tenant_id: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.base_url = "https://graph.microsoft.com/v1.0"
        self.auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0"
        self.redirect_uri = "http://localhost:8080/callback"  # For local testing
        self.scopes = ["https://graph.microsoft.com/Files.Read"]
        
    def get_auth_url(self) -> str:
        """Generate the authorization URL for OAuth2 flow."""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "state": "random_state_string"
        }
        return f"{self.auth_url}/authorize?" + urlencode(params)
    
    def get_token_from_code(self, auth_code: str) -> dict:
        """Exchange authorization code for access token."""
        token_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes)
        }
        
        response = requests.post(f"{self.auth_url}/token", data=token_data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Token exchange failed: {response.text}")
    
    def refresh_token(self, refresh_token: str) -> dict:
        """Refresh the access token using refresh token."""
        token_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "scope": " ".join(self.scopes)
        }
        
        response = requests.post(f"{self.auth_url}/token", data=token_data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Token refresh failed: {response.text}")
    
    def download_file(self, file_path: str, access_token: str) -> bytes:
        """Download a file from OneDrive."""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Get file metadata first
        file_url = f"{self.base_url}/me/drive/root:{file_path}"
        response = requests.get(file_url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"File not found: {response.text}")
        
        file_info = response.json()
        download_url = file_info.get("@microsoft.graph.downloadUrl")
        
        if not download_url:
            raise Exception("Download URL not available")
        
        # Download the file
        download_response = requests.get(download_url)
        
        if download_response.status_code == 200:
            return download_response.content
        else:
            raise Exception(f"Download failed: {download_response.text}")

def setup_onedrive_auth():
    """Interactive setup for OneDrive authentication."""
    print("OneDrive Authentication Setup")
    print("="*40)
    
    # Get credentials
    client_id = input("Enter your Azure App Client ID: ").strip()
    client_secret = input("Enter your Azure App Client Secret: ").strip()
    tenant_id = input("Enter your Azure Tenant ID: ").strip()
    
    if not all([client_id, client_secret, tenant_id]):
        print("Error: All fields are required")
        return None
    
    client = OneDriveClient(client_id, client_secret, tenant_id)
    
    # Get authorization URL
    auth_url = client.get_auth_url()
    print(f"\\nOpening browser for authorization...")
    print(f"If browser doesn't open, visit: {auth_url}")
    
    webbrowser.open(auth_url)
    
    # Get authorization code from user
    print("\\nAfter authorization, copy the 'code' parameter from the callback URL")
    auth_code = input("Enter the authorization code: ").strip()
    
    try:
        # Get tokens
        token_response = client.get_token_from_code(auth_code)
        
        # Update config
        config_path = "config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
        else:
            config = {"onedrive": {}}
        
        config["onedrive"].update({
            "client_id": client_id,
            "client_secret": client_secret,
            "tenant_id": tenant_id,
            "refresh_token": token_response.get("refresh_token"),
            "access_token": token_response.get("access_token"),
            "token_expires": (datetime.now() + timedelta(seconds=token_response.get("expires_in", 3600))).isoformat()
        })
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("\\nAuthentication successful! Configuration saved to config.json")
        print("Don't forget to set your OneDrive file path in the config.")
        
        return config["onedrive"]
        
    except Exception as e:
        print(f"\\nError during authentication: {e}")
        return None

def test_onedrive_connection():
    """Test the OneDrive connection."""
    try:
        with open("config.json", 'r') as f:
            config = json.load(f)
        
        onedrive_config = config.get("onedrive", {})
        
        if not all(key in onedrive_config for key in ["client_id", "client_secret", "tenant_id", "refresh_token"]):
            print("Error: OneDrive configuration incomplete. Run setup first.")
            return False
        
        client = OneDriveClient(
            onedrive_config["client_id"],
            onedrive_config["client_secret"],
            onedrive_config["tenant_id"]
        )
        
        # Refresh token to get current access token
        token_response = client.refresh_token(onedrive_config["refresh_token"])
        access_token = token_response["access_token"]
        
        # Test by listing root drive
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{client.base_url}/me/drive", headers=headers)
        
        if response.status_code == 200:
            drive_info = response.json()
            print(f"Connection successful! Connected to: {drive_info.get('name', 'OneDrive')}")
            return True
        else:
            print(f"Connection failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing connection: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OneDrive Integration Helper")
    parser.add_argument("--setup", action="store_true", help="Set up OneDrive authentication")
    parser.add_argument("--test", action="store_true", help="Test OneDrive connection")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_onedrive_auth()
    elif args.test:
        test_onedrive_connection()
    else:
        print("Use --setup to configure OneDrive authentication or --test to test connection")