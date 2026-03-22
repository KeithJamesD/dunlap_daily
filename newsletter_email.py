#!/usr/bin/env python3
"""
Email module for Dunlap Daily Newsletter
Handles email subscription and sending functionality
"""

import json
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Dict, Optional
import datetime

logger = logging.getLogger(__name__)

class NewsletterEmailer:
    """Handles email distribution for the newsletter."""
    
    def __init__(self, config_path: str = "config.json", email_config_path: str = "email_config.json"):
        self.config = self.load_config(config_path)
        self.email_config = self.load_email_config(email_config_path)
        self.subscribers_file = Path(self.email_config.get("subscribers_file", "subscribers.json"))
        
    def load_config(self, config_path: str) -> Dict:
        """Load main configuration."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found")
            return {}
    
    def load_email_config(self, email_config_path: str) -> Dict:
        """Load email configuration."""
        try:
            with open(email_config_path, 'r') as f:
                return json.load(f).get("email", {})
        except FileNotFoundError:
            logger.warning(f"Email config file {email_config_path} not found")
            return {}
    
    def load_subscribers(self) -> List[Dict]:
        """Load subscriber list."""
        try:
            if self.subscribers_file.exists():
                with open(self.subscribers_file, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            logger.error(f"Error loading subscribers: {e}")
            return []
    
    def save_subscribers(self, subscribers: List[Dict]) -> None:
        """Save subscriber list."""
        try:
            with open(self.subscribers_file, 'w') as f:
                json.dump(subscribers, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving subscribers: {e}")
    
    def add_subscriber(self, email: str, name: str = None) -> bool:
        """Add a new subscriber."""
        subscribers = self.load_subscribers()
        
        # Check if already subscribed
        for sub in subscribers:
            if sub["email"].lower() == email.lower():
                logger.info(f"Email {email} already subscribed")
                return False
        
        # Add new subscriber
        new_subscriber = {
            "email": email,
            "name": name or email.split("@")[0],
            "subscribed_date": datetime.datetime.now().isoformat(),
            "active": True
        }
        subscribers.append(new_subscriber)
        self.save_subscribers(subscribers)
        logger.info(f"Added subscriber: {email}")
        return True
    
    def remove_subscriber(self, email: str) -> bool:
        """Remove/unsubscribe an email address."""
        subscribers = self.load_subscribers()
        
        for sub in subscribers:
            if sub["email"].lower() == email.lower():
                sub["active"] = False
                sub["unsubscribed_date"] = datetime.datetime.now().isoformat()
                self.save_subscribers(subscribers)
                logger.info(f"Unsubscribed: {email}")
                return True
        
        logger.warning(f"Email not found: {email}")
        return False
    
    def get_active_subscribers(self) -> List[str]:
        """Get list of active subscriber email addresses."""
        subscribers = self.load_subscribers()
        return [sub["email"] for sub in subscribers if sub.get("active", True)]
    
    def create_email_content(self, entry: Dict) -> str:
        """Create HTML email content from newsletter entry."""
        base_url = self.config.get("newsletter", {}).get("link", "http://localhost:8000")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{entry['title']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            line-height: 1.6;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .newsletter {{
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2c3e50;
            margin: 0;
            font-size: 2em;
        }}
        .date {{
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        .content {{
            color: #333;
        }}
        .content h3 {{
            color: #2c3e50;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 25px;
        }}
        .content p {{
            margin-bottom: 15px;
        }}
        .content img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 4px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 4px;
            font-size: 0.9em;
            color: #6c757d;
        }}
        .footer a {{
            color: #3498db;
            text-decoration: none;
        }}
        .unsubscribe {{
            font-size: 0.8em;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="newsletter">
        <div class="header">
            <h1>{self.config.get('newsletter', {}).get('title', 'Dunlap Daily')}</h1>
            <div class="date">{entry['date'].strftime('%B %d, %Y')}</div>
        </div>
        
        <div class="content">
            {entry['content']}
        </div>
        
        <div class="footer">
            <p>Thanks for reading {self.config.get('newsletter', {}).get('title', 'Dunlap Daily')}!</p>
            <p>
                <a href="{base_url}">View online</a> | 
                <a href="{base_url}/feed.xml">RSS Feed</a> | 
                <a href="{base_url}/archive.html">Archive</a>
            </p>
            <div class="unsubscribe">
                <p>To unsubscribe, reply to this email with "UNSUBSCRIBE" in the subject.</p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        return html_content
    
    def send_newsletter(self, entry: Dict, test_email: str = None) -> bool:
        """Send newsletter to subscribers or test email."""
        if not self.email_config.get("enabled", False):
            logger.info("Email sending is disabled in configuration")
            return False
        
        try:
            # Get recipients
            recipients = [test_email] if test_email else self.get_active_subscribers()
            if not recipients:
                logger.warning("No recipients found")
                return False
            
            # Create email content
            html_content = self.create_email_content(entry)
            subject = self.email_config.get("subject_template", "{title}").format(
                title=entry["title"],
                date=entry["date"].strftime("%m/%d/%Y")
            )
            
            # Setup SMTP
            smtp_server = smtplib.SMTP(
                self.email_config["smtp_server"], 
                self.email_config["smtp_port"]
            )
            smtp_server.starttls()
            smtp_server.login(
                self.email_config["username"], 
                self.email_config["password"]
            )
            
            # Send to each recipient
            sent_count = 0
            for recipient in recipients:
                try:
                    msg = MIMEMultipart("alternative")
                    msg["Subject"] = subject
                    msg["From"] = f"{self.email_config['from_name']} <{self.email_config['from_email']}>"
                    msg["To"] = recipient
                    
                    # Create plain text version
                    text_content = f"""
{entry['title']}
{entry['date'].strftime('%B %d, %Y')}

{entry['content']}

---
View online: {self.config.get('newsletter', {}).get('link', '')}
RSS Feed: {self.config.get('newsletter', {}).get('link', '')}/feed.xml
                    """
                    
                    # Attach both versions
                    part1 = MIMEText(text_content, "plain")
                    part2 = MIMEText(html_content, "html")
                    
                    msg.attach(part1)
                    msg.attach(part2)
                    
                    # Send email
                    smtp_server.send_message(msg)
                    sent_count += 1
                    logger.info(f"Email sent to {recipient}")
                    
                except Exception as e:
                    logger.error(f"Failed to send to {recipient}: {e}")
            
            smtp_server.quit()
            logger.info(f"Newsletter sent to {sent_count} recipients")
            return True
            
        except Exception as e:
            logger.error(f"Error sending newsletter: {e}")
            return False

def main():
    """Command line interface for email management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage newsletter email subscribers")
    parser.add_argument("--add", type=str, help="Add subscriber email")
    parser.add_argument("--remove", type=str, help="Remove subscriber email")
    parser.add_argument("--list", action="store_true", help="List all active subscribers")
    parser.add_argument("--test", type=str, help="Send test email to address")
    
    args = parser.parse_args()
    
    emailer = NewsletterEmailer()
    
    if args.add:
        success = emailer.add_subscriber(args.add)
        print(f"{'Added' if success else 'Failed to add'} subscriber: {args.add}")
    
    elif args.remove:
        success = emailer.remove_subscriber(args.remove)
        print(f"{'Removed' if success else 'Failed to remove'} subscriber: {args.remove}")
    
    elif args.list:
        subscribers = emailer.get_active_subscribers()
        print(f"Active subscribers ({len(subscribers)}):")
        for email in subscribers:
            print(f"  - {email}")
    
    elif args.test:
        # Create a test entry
        test_entry = {
            "title": "Test Newsletter",
            "content": "<p>This is a test email from your Dunlap Daily newsletter system.</p>",
            "date": datetime.datetime.now()
        }
        success = emailer.send_newsletter(test_entry, test_email=args.test)
        print(f"Test email {'sent' if success else 'failed'}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()