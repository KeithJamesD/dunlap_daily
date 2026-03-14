#!/usr/bin/env python3
"""
Dunlap Daily RSS Newsletter Generator

This script fetches daily content from a OneDrive .doc file,
generates an RSS feed, and creates HTML pages for GitHub Pages hosting.
"""

import os
import sys
import json
import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional
import requests
import zipfile
import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging
import argparse
import pytz

try:
    from docx import Document
except ImportError:
    print("python-docx not installed. Installing...")
    os.system("pip install python-docx")
    from docx import Document

try:
    import feedgen.feed
except ImportError:
    print("feedgen not installed. Installing...")
    os.system("pip install feedgen")
    import feedgen.feed

from feedgen.feed import FeedGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DunlapDailyGenerator:
    """Main class for generating the Dunlap Daily RSS newsletter."""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self.load_config(config_path)
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "docs"  # GitHub Pages directory
        self.rss_file = self.output_dir / "feed.xml"
        self.archive_dir = self.output_dir / "archive"
        
        # Create necessary directories
        self.output_dir.mkdir(exist_ok=True)
        self.archive_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "newsletter": {
                "title": "Dunlap Daily",
                "description": "Daily insights and updates from Dunlap",
                "author": "Dunlap Team",
                "link": "https://your-username.github.io/dunlap_daily",
                "language": "en-US"
            },
            "onedrive": {
                "client_id": "",
                "client_secret": "",
                "tenant_id": "",
                "file_path": "/path/to/your/daily-content.docx"
            },
            "github": {
                "repository": "your-username/dunlap_daily",
                "pages_url": "https://your-username.github.io/dunlap_daily"
            }
        }
    
    def fetch_onedrive_content(self) -> Optional[str]:
        """Fetch content from OneDrive .doc file."""
        try:
            # Try OneDrive integration first
            if self._has_onedrive_config():
                content = self._fetch_from_onedrive()
                if content:
                    return content
            
            # Fallback to local file
            local_doc_path = self.base_dir / "daily_content.docx"
            
            if not local_doc_path.exists():
                logger.warning(f"Local document not found at {local_doc_path}")
                return None
            
            # Read the Word document
            doc = Document(local_doc_path)
            content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    content.append(paragraph.text.strip())
            
            return "\n\n".join(content)
            
        except Exception as e:
            logger.error(f"Error fetching OneDrive content: {e}")
            return None
    
    def _has_onedrive_config(self) -> bool:
        """Check if OneDrive configuration is available."""
        onedrive_config = self.config.get("onedrive", {})
        required_keys = ["client_id", "client_secret", "tenant_id", "refresh_token"]
        return all(key in onedrive_config and onedrive_config[key] for key in required_keys)
    
    def _fetch_from_onedrive(self) -> Optional[str]:
        """Fetch content directly from OneDrive using API."""
        try:
            from onedrive_helper import OneDriveClient
            
            onedrive_config = self.config["onedrive"]
            client = OneDriveClient(
                onedrive_config["client_id"],
                onedrive_config["client_secret"], 
                onedrive_config["tenant_id"]
            )
            
            # Refresh token to get current access token
            token_response = client.refresh_token(onedrive_config["refresh_token"])
            access_token = token_response["access_token"]
            
            # Update refresh token if provided
            if "refresh_token" in token_response:
                self.config["onedrive"]["refresh_token"] = token_response["refresh_token"]
                self._save_config()
            
            # Download file
            file_path = onedrive_config.get("file_path")
            if not file_path:
                logger.error("OneDrive file path not configured")
                return None
            
            file_content = client.download_file(file_path, access_token)
            
            # Save to local file for backup
            local_doc_path = self.base_dir / "daily_content.docx"
            with open(local_doc_path, 'wb') as f:
                f.write(file_content)
            
            # Parse the downloaded content
            doc = Document(local_doc_path)
            content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    content.append(paragraph.text.strip())
            
            logger.info("Successfully fetched content from OneDrive")
            return "\n\n".join(content)
            
        except Exception as e:
            logger.warning(f"Failed to fetch from OneDrive: {e}")
            return None
    
    def _save_config(self):
        """Save updated configuration."""
        try:
            config_path = self.base_dir / "config.json"
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save config: {e}")
    
    def parse_content(self, raw_content: str) -> Dict:
        """Parse the raw content into structured newsletter data."""
        if not raw_content:
            return {}
        
        lines = raw_content.split('\n')
        title = ""
        content_sections = []
        current_section = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # First non-empty line is typically the title
            if not title:
                title = line
                continue
            
            # Look for section headers (lines that might be in all caps or have special formatting)
            if line.isupper() and len(line) > 3:
                if current_section:
                    content_sections.append(current_section)
                current_section = f"<h3>{line}</h3>\n"
            else:
                current_section += f"<p>{line}</p>\n"
        
        if current_section:
            content_sections.append(current_section)
        
        return {
            "title": title or f"Daily Update - {datetime.date.today().strftime('%B %d, %Y')}",
            "content": "\n".join(content_sections),
            "date": datetime.datetime.now(pytz.UTC),
            "permalink": f"/archive/{datetime.date.today().strftime('%Y-%m-%d')}.html"
        }
    
    def generate_rss_feed(self, entries: List[Dict]) -> None:
        """Generate RSS feed from entries."""
        fg = FeedGenerator()
        
        # Set feed metadata
        fg.title(self.config["newsletter"]["title"])
        fg.description(self.config["newsletter"]["description"])
        fg.link(href=self.config["newsletter"]["link"], rel="alternate")
        fg.link(href=f"{self.config['newsletter']['link']}/feed.xml", rel="self")
        fg.author(name=self.config["newsletter"]["author"])
        fg.language(self.config["newsletter"]["language"])
        fg.lastBuildDate(datetime.datetime.now(pytz.UTC))
        
        # Add entries to feed
        for entry in entries[:10]:  # Limit to 10 most recent entries
            fe = fg.add_entry()
            fe.title(entry["title"])
            fe.description(entry["content"])
            fe.link(href=f"{self.config['newsletter']['link']}{entry['permalink']}")
            fe.pubDate(entry["date"])
            fe.guid(f"{self.config['newsletter']['link']}{entry['permalink']}", permalink=True)
        
        # Write RSS feed
        fg.rss_file(str(self.rss_file))
        logger.info(f"RSS feed generated: {self.rss_file}")
    
    def generate_html_page(self, entry: Dict) -> None:
        """Generate HTML page for a single entry."""
        date_str = entry["date"].strftime("%Y-%m-%d")
        html_file = self.archive_dir / f"{date_str}.html"
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{entry['title']} - {self.config['newsletter']['title']}</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header>
        <h1><a href="../">{self.config['newsletter']['title']}</a></h1>
        <nav>
            <a href="../">Home</a> | 
            <a href="../feed.xml">RSS Feed</a> | 
            <a href="../archive.html">Archive</a>
        </nav>
    </header>
    
    <main>
        <article>
            <h2>{entry['title']}</h2>
            <time datetime="{entry['date'].isoformat()}">{entry['date'].strftime('%B %d, %Y')}</time>
            <div class="content">
                {entry['content']}
            </div>
        </article>
    </main>
    
    <footer>
        <p>&copy; {datetime.date.today().year} {self.config['newsletter']['author']}. All rights reserved.</p>
    </footer>
</body>
</html>
"""
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML page generated: {html_file}")
    
    def load_existing_entries(self) -> List[Dict]:
        """Load existing entries from archive files."""
        entries = []
        entries_file = self.output_dir / "entries.json"
        
        if entries_file.exists():
            try:
                with open(entries_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        item["date"] = datetime.datetime.fromisoformat(item["date"])
                        entries.append(item)
            except Exception as e:
                logger.error(f"Error loading existing entries: {e}")
        
        return entries
    
    def save_entries(self, entries: List[Dict]) -> None:
        """Save entries to JSON file."""
        entries_file = self.output_dir / "entries.json"
        
        # Convert datetime objects to strings for JSON serialization
        serializable_entries = []
        for entry in entries:
            entry_copy = entry.copy()
            entry_copy["date"] = entry["date"].isoformat()
            serializable_entries.append(entry_copy)
        
        with open(entries_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_entries, f, indent=2, ensure_ascii=False)
    
    def generate_index_page(self, entries: List[Dict]) -> None:
        """Generate the main index page."""
        index_file = self.output_dir / "index.html"
        
        # Generate recent entries HTML
        recent_entries_html = ""
        for entry in entries[:5]:  # Show 5 most recent
            date_str = entry["date"].strftime("%B %d, %Y")
            recent_entries_html += f"""
            <article class="entry-preview">
                <h3><a href="{entry['permalink']}">{entry['title']}</a></h3>
                <time>{date_str}</time>
                <div class="excerpt">
                    {entry['content'][:200]}...
                </div>
                <a href="{entry['permalink']}" class="read-more">Read more</a>
            </article>
            """
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config['newsletter']['title']}</title>
    <meta name="description" content="{self.config['newsletter']['description']}">
    <link rel="stylesheet" href="style.css">
    <link rel="alternate" type="application/rss+xml" title="RSS Feed" href="feed.xml">
</head>
<body>
    <header>
        <h1>{self.config['newsletter']['title']}</h1>
        <p class="tagline">{self.config['newsletter']['description']}</p>
        <nav>
            <a href="feed.xml">RSS Feed</a> | 
            <a href="archive.html">Archive</a>
        </nav>
    </header>
    
    <main>
        <section class="recent-entries">
            <h2>Recent Updates</h2>
            {recent_entries_html}
        </section>
    </main>
    
    <footer>
        <p>&copy; {datetime.date.today().year} {self.config['newsletter']['author']}. All rights reserved.</p>
        <p><a href="feed.xml">Subscribe to RSS</a></p>
    </footer>
</body>
</html>
"""
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Index page generated: {index_file}")
    
    def generate_archive_page(self, entries: List[Dict]) -> None:
        """Generate the archive page."""
        archive_file = self.output_dir / "archive.html"
        
        # Generate archive entries HTML
        archive_entries_html = ""
        for entry in entries:
            date_str = entry["date"].strftime("%B %d, %Y")
            archive_entries_html += f"""
            <li>
                <time>{date_str}</time>
                <a href="{entry['permalink']}">{entry['title']}</a>
            </li>
            """
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Archive - {self.config['newsletter']['title']}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1><a href="./">{self.config['newsletter']['title']}</a></h1>
        <nav>
            <a href="./">Home</a> | 
            <a href="feed.xml">RSS Feed</a> | 
            <a href="archive.html">Archive</a>
        </nav>
    </header>
    
    <main>
        <h2>Archive</h2>
        <ul class="archive-list">
            {archive_entries_html}
        </ul>
    </main>
    
    <footer>
        <p>&copy; {datetime.date.today().year} {self.config['newsletter']['author']}. All rights reserved.</p>
    </footer>
</body>
</html>
"""
        
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Archive page generated: {archive_file}")
    
    def run(self, force_update: bool = False) -> None:
        """Main execution method."""
        logger.info("Starting Dunlap Daily generation...")
        
        # Load existing entries
        entries = self.load_existing_entries()
        
        # Check if we need to add a new entry today
        today = datetime.date.today()
        has_today_entry = any(
            entry["date"].date() == today for entry in entries
        )
        
        if not has_today_entry or force_update:
            # Fetch new content
            raw_content = self.fetch_onedrive_content()
            
            if raw_content:
                # Parse content
                new_entry = self.parse_content(raw_content)
                
                # Add to entries list
                entries.append(new_entry)
                
                # Sort entries by date (newest first)
                entries.sort(key=lambda x: x["date"], reverse=True)
                
                # Generate HTML page for new entry
                self.generate_html_page(new_entry)
                
                logger.info(f"New entry added: {new_entry['title']}")
            else:
                logger.warning("No new content found")
        else:
            logger.info("Today's entry already exists")
        
        # Generate RSS feed
        self.generate_rss_feed(entries)
        
        # Generate pages
        self.generate_index_page(entries)
        self.generate_archive_page(entries)
        
        # Save entries
        self.save_entries(entries)
        
        logger.info("Dunlap Daily generation complete!")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate Dunlap Daily RSS Newsletter")
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Force update even if today's entry exists"
    )
    parser.add_argument(
        "--config", 
        default="config.json", 
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    try:
        generator = DunlapDailyGenerator(args.config)
        generator.run(force_update=args.force)
    except Exception as e:
        logger.error(f"Error running generator: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
