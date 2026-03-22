# Dunlap Daily - Local Configuration

## 🔐 Security Setup

### Keep Credentials Local
Your sensitive credentials have been removed from the public config files for security.

### Local Configuration Files
Create these files locally (they're in .gitignore):

**`config_local.json`** (copy your real credentials here):
```json
{
  "newsletter": {
    "title": "Dunlap Daily",
    "description": "Daily insights and updates from Dunlap", 
    "author": "Dunlap Team",
    "link": "https://keithjamesd.github.io/dunlap_daily",
    "language": "en-US",
    "base_url": "https://keithjamesd.github.io/dunlap_daily"
  },
  "onedrive": {
    "client_id": "your-actual-client-id",
    "client_secret": "your-actual-client-secret",
    "tenant_id": "your-actual-tenant-id",
    "file_path": "/Market/Dunlap_Daily {date}.docx",
    "refresh_token": "your-refresh-token"
  },
  "github": {
    "repository": "KeithJamesD/dunlap_daily",
    "pages_url": "https://keithjamesd.github.io/dunlap_daily",
    "token": "your-github-token-if-needed"
  }
}
```

**`email_config_local.json`**:
```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your-actual-email@gmail.com",
    "password": "your-actual-app-password", 
    "from_name": "Dunlap Daily",
    "from_email": "your-actual-email@gmail.com",
    "subject_template": "{title} - {date}",
    "subscribers_file": "subscribers.json"
  }
}
```

### Usage with Local Config
```bash
# Use local config files
python dunlap_daily.py --config config_local.json --force

# Or modify the script to check for local configs first
```

### .gitignore Protection
These files are already in .gitignore:
- `config_local.json`
- `email_config_local.json` 
- `*.local.json`

## 🌍 GitHub Pages vs Local Development

### For GitHub Pages (Public)
- Use sanitized config files (no credentials)
- Focus on static content generation
- Commit and push safely

### For Local Development (Private)
- Use local config files with real credentials
- OneDrive integration works
- Email sending works

### Best Practice
1. **Develop locally** with full credentials
2. **Generate content** with local config
3. **Commit only** the generated content (docs/ folder)
4. **Keep credentials safe** in local files only