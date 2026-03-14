# Dunlap Daily RSS Newsletter

An automated RSS newsletter system that fetches daily content from OneDrive .docx files and publishes to GitHub Pages.

## Features

- 📄 Fetches content from OneDrive .docx files
- 📰 Generates RSS feed automatically
- 🌐 Creates beautiful HTML pages for GitHub Pages
- 🤖 Automated daily updates via GitHub Actions
- 📱 Responsive design for mobile and desktop
- 🗂️ Archive system for past newsletters

## Quick Setup

### 1. Repository Setup

1. Fork or clone this repository
2. Enable GitHub Pages in repository settings (source: GitHub Actions)
3. Update the configuration in `config.json`

### 2. Azure App Registration (for OneDrive integration)

1. Go to [Azure Portal](https://portal.azure.com) > Azure Active Directory > App registrations
2. Click "New registration"
3. Set up your app:
   - **Name**: `Dunlap Daily Newsletter`
   - **Supported account types**: Accounts in any organizational directory and personal Microsoft accounts
   - **Redirect URI**: `http://localhost:8080/callback` (for setup) and your GitHub Pages URL
4. Note down:
   - Application (client) ID
   - Tenant ID
5. Go to "Certificates & secrets" > "New client secret"
   - Note down the secret value (only shown once!)
6. Go to "API permissions" > "Add permission" > "Microsoft Graph" > "Delegated permissions"
   - Add: `Files.Read`
   - Click "Grant admin consent"

### 3. OneDrive Authentication Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up OneDrive authentication
python onedrive_helper.py --setup
```

Follow the prompts to authenticate with your Microsoft account.

### 4. GitHub Secrets Configuration

In your GitHub repository, go to Settings > Secrets and variables > Actions, and add:

- `ONEDRIVE_CLIENT_ID`: Your Azure app client ID
- `ONEDRIVE_CLIENT_SECRET`: Your Azure app client secret  
- `ONEDRIVE_TENANT_ID`: Your Azure tenant ID
- `ONEDRIVE_FILE_PATH`: Path to your .docx file in OneDrive (e.g., `/Documents/daily-content.docx`)
- `ONEDRIVE_REFRESH_TOKEN`: Generated during setup (check config.json)

### 5. Configuration

Edit `config.json` to customize your newsletter:

```json
{
  "newsletter": {
    "title": "Your Newsletter Name",
    "description": "Your newsletter description", 
    "author": "Your Name",
    "link": "https://yourusername.github.io/dunlap_daily",
    "language": "en-US"
  }
}
```

### 6. Content Format

Your OneDrive .docx file should follow this format:

```
Daily Update - February 28, 2026

HIGHLIGHTS
• Important update 1
• Important update 2

NEWS
Lorem ipsum dolor sit amet, consectetur adipiscing elit.

ANNOUNCEMENTS  
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
```

## Usage

### Manual Generation

```bash
# Generate newsletter locally
python dunlap_daily.py

# Force update (even if today's entry exists)
python dunlap_daily.py --force

# Use custom config file
python dunlap_daily.py --config my-config.json
```

### Automated Generation

The system runs automatically via GitHub Actions:
- **Schedule**: Daily at 9 AM UTC (configurable)
- **Manual**: Trigger via GitHub Actions tab
- **On Push**: Runs when you push to main branch

### Testing OneDrive Connection

```bash
python onedrive_helper.py --test
```

## File Structure

```
dunlap_daily/
├── dunlap_daily.py          # Main generator script
├── onedrive_helper.py       # OneDrive integration
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── docs/                    # GitHub Pages output
│   ├── index.html          # Homepage
│   ├── archive.html        # Archive page
│   ├── feed.xml            # RSS feed
│   ├── style.css           # Stylesheet
│   └── archive/            # Individual posts
│       └── 2026-02-28.html
└── .github/workflows/       # GitHub Actions
    └── newsletter.yml
```

## Customization

### Styling

Edit `docs/style.css` to customize the appearance. The design uses CSS variables for easy theming:

```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --accent-color: #e74c3c;
    /* ... */
}
```

### Content Parsing

Modify the `parse_content()` method in `dunlap_daily.py` to change how your .docx content is processed.

### Newsletter Template

Update the HTML templates in the `generate_*_page()` methods to change the layout and structure.

## Troubleshooting

### Common Issues

1. **OneDrive Authentication Fails**
   - Check your Azure app permissions
   - Verify redirect URLs match
   - Ensure tenant ID is correct

2. **GitHub Actions Fail**
   - Verify all secrets are set correctly
   - Check the Actions logs for specific errors
   - Make sure repository has Pages enabled

3. **No Content Generated**
   - Verify OneDrive file path is correct
   - Check file permissions
   - Test connection with `python onedrive_helper.py --test`

4. **CSS/Styling Issues**
   - Clear browser cache
   - Check that `style.css` is in the `docs/` directory
   - Verify relative paths in HTML

### Debug Mode

Enable debug logging by setting the environment variable:

```bash
export LOG_LEVEL=DEBUG
python dunlap_daily.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Search existing GitHub issues
3. Create a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Error messages (if any)
   - Your configuration (remove sensitive data)

---

**Happy Newsletter Building! 📰✨**