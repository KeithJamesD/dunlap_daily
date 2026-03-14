#!/usr/bin/env python3
"""
Setup script for Dunlap Daily Newsletter
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def main():
    print("🗞️  Dunlap Daily Newsletter Setup")
    print("="*50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print("✅ Python version check passed")
    
    # Install dependencies
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)
    
    # Create configuration
    config_path = Path("config.json")
    if not config_path.exists():
        print("\n⚙️  Creating configuration file...")
        
        print("\nEnter your newsletter details:")
        title = input("Newsletter title (default: Dunlap Daily): ").strip() or "Dunlap Daily"
        description = input("Description (default: Daily insights and updates): ").strip() or "Daily insights and updates"
        author = input("Author name: ").strip() or "Newsletter Author"
        
        print("\nEnter your GitHub details:")
        github_username = input("GitHub username: ").strip()
        repo_name = input("Repository name (default: dunlap_daily): ").strip() or "dunlap_daily"
        
        config = {
            "newsletter": {
                "title": title,
                "description": description,
                "author": author,
                "link": f"https://{github_username}.github.io/{repo_name}",
                "language": "en-US"
            },
            "onedrive": {
                "client_id": "",
                "client_secret": "",
                "tenant_id": "",
                "file_path": "",
                "refresh_token": ""
            },
            "github": {
                "repository": f"{github_username}/{repo_name}",
                "pages_url": f"https://{github_username}.github.io/{repo_name}"
            },
            "automation": {
                "run_time": "09:00",
                "timezone": "America/New_York"
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration file created")
    else:
        print("✅ Configuration file already exists")
    
    # Create docs directory
    docs_dir = Path("docs")
    if not docs_dir.exists():
        docs_dir.mkdir()
        print("✅ Created docs directory")
    
    # Test the generator
    print("\n🧪 Running test generation...")
    try:
        subprocess.run([sys.executable, "test_generator.py"], check=True)
        print("✅ Test generation completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Test generation failed: {e}")
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Set up Azure App Registration for OneDrive integration:")
    print("   - Go to https://portal.azure.com")
    print("   - Create a new App Registration") 
    print("   - Get Client ID, Client Secret, and Tenant ID")
    print("   - Run: python onedrive_helper.py --setup")
    print("")
    print("2. Create GitHub repository and enable Pages:")
    print("   - Create repository on GitHub")
    print("   - Enable GitHub Pages (Settings > Pages > Source: GitHub Actions)")
    print("   - Add repository secrets for OneDrive integration")
    print("")
    print("3. Test locally:")
    print("   - Place your daily content in daily_content.docx")
    print("   - Run: python dunlap_daily.py")
    print("   - Check the docs/ folder for generated files")
    print("")
    print("4. Deploy:")
    print("   - Push to GitHub")
    print("   - GitHub Actions will automatically build and deploy")
    print("")
    print("📁 Generated files are in the docs/ directory")
    print("🌐 Open docs/index.html in your browser to preview")

if __name__ == "__main__":
    main()