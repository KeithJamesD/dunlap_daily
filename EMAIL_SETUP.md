# Email Setup Instructions for Dunlap Daily

## Quick Start

1. **Configure Email Settings**
   Edit `email_config.json`:
   ```json
   {
     "email": {
       "enabled": true,
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "username": "your-email@gmail.com",
       "password": "your-app-password",
       "from_name": "Dunlap Daily",
       "from_email": "your-email@gmail.com",
       "subject_template": "{title} - {date}",
       "subscribers_file": "subscribers.json"
     }
   }
   ```

2. **Add Subscribers**
   ```bash
   python dunlap_daily.py --email-add "subscriber@example.com"
   ```

3. **Send Newsletter**
   ```bash
   python dunlap_daily.py --force  # Generates and sends automatically
   ```

## Commands

### Subscriber Management
- `--email-add EMAIL` - Add subscriber
- `--email-remove EMAIL` - Remove subscriber  
- `--email-list` - List all subscribers
- `--email-test EMAIL` - Send test email

### Examples
```bash
# Add subscriber
python dunlap_daily.py --email-add "john@example.com"

# Send test email
python dunlap_daily.py --email-test "test@example.com"

# List subscribers
python dunlap_daily.py --email-list

# Generate newsletter and send to all subscribers
python dunlap_daily.py --force
```

## Email Provider Setup

### Gmail Setup
1. Enable 2-factor authentication
2. Generate App Password:
   - Go to Google Account Settings → Security → 2-Step Verification
   - At bottom, click "App passwords"
   - Select "Mail" and "Other (Custom name)"
   - Use generated password in config

### Outlook/Hotmail Setup
```json
{
  "smtp_server": "smtp-mail.outlook.com",
  "smtp_port": 587
}
```

### Other Providers
- **Yahoo**: smtp.mail.yahoo.com:587
- **iCloud**: smtp.mail.me.com:587

## Automatic Email Sending

When you run `python dunlap_daily.py --force`:
1. Newsletter is generated
2. HTML email is created
3. Sent to all active subscribers
4. Both HTML and plain text versions included

## Security Notes

- Never commit email passwords to git
- Use App Passwords, not main account passwords
- Consider environment variables for credentials:
  ```bash
  export EMAIL_PASSWORD="your-app-password"
  ```

## Troubleshooting

**"Authentication failed"**
- Check username/password
- Ensure App Password enabled (Gmail)
- Verify SMTP settings

**"Email functionality not available"**
- Run: `pip install smtplib email`
- Check newsletter_email.py exists

**No emails sent**
- Verify `"enabled": true` in config
- Check subscriber list: `--email-list`
- Test with: `--email-test your-email@domain.com`