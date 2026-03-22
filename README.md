# Dunlap Daily RSS Newsletter

A local newsletter generator that creates RSS feeds and HTML pages from daily content.

## 🌟 Features

- **Local Hosting**: No need for GitHub Pages or Azure setup
- **Auto-refresh**: Automatically regenerates content when files change
- **Scheduled Publishing**: Schedule posts for future dates and times
- **OneDrive Integration**: Fetch content from OneDrive .docx files (optional)
- **Local Fallback**: Works with local .docx or .txt files
- **RSS Feed**: Generates valid RSS feeds for newsletter subscriptions
- **Web Interface**: Clean, responsive HTML pages

## 📋 Prerequisites

### Install Python
1. **Download Python**: Visit [python.org/downloads](https://python.org/downloads)
2. **Install Python 3.8+**: Make sure to check "Add Python to PATH" during installation
3. **Verify Installation**: Open Command Prompt and run `python --version`

### Install Dependencies (Automatic)
The batch file will automatically install required packages, or run manually:
```bash
pip install python-docx feedgen pytz requests
```

## 🚀 Quick Start (Local Server)

### Option 1: Double-click to run (Easiest)
1. **Double-click** `run_local.bat` on Windows
2. **Auto-setup**: Will check for Python and install dependencies
3. **Auto-open**: Your browser will open automatically to `http://localhost:8000`

### Option 2: Command line
```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Run the local server
python run_local.py
```

## 📅 Scheduling Posts (NEW!)

### Schedule Tomorrow's Issue for Noon
```bash
python dunlap_daily.py --config config_local.json --schedule "tomorrow noon" --force
```

### Other Scheduling Options
```bash
# Tomorrow at 3 PM
python dunlap_daily.py --schedule "tomorrow 3pm" --force

# Specific date and time
python dunlap_daily.py --schedule "2026-03-19 12:00" --force

# Specific date (defaults to noon)
python dunlap_daily.py --schedule "2026-03-20" --force
```

### Supported Schedule Formats:
- **`"tomorrow noon"`** - Tomorrow at 12:00 PM
- **`"tomorrow 3pm"`** - Tomorrow at 3:00 PM
- **`"tomorrow midnight"`** - Tomorrow at 12:00 AM
- **`"2026-03-19 12:00"`** - Specific date and time (24-hour format)
- **`"2026-03-19"`** - Specific date (defaults to noon)

## 🎯 Use Case: Replace February 28th Content

Your current newsletter shows content from February 28, 2026. To publish tomorrow's first real issue:

1. **Edit Content**: Update `daily_content.txt` with your new content
2. **Schedule**: Run `python dunlap_daily.py --schedule "tomorrow noon" --force`
3. **Verify**: Check `http://localhost:8000` to see the updated newsletter

### Method 1: Local File (Recommended for local hosting)
1. Create or edit `daily_content.txt` or `daily_content.docx` in the project root
2. Write your daily content (first line becomes the title)
3. Save the file - the server will auto-detect changes and regenerate

**Content Format Example:**
```
Welcome to Today's Newsletter!

HIGHLIGHTS
• First bullet point
• Second bulletin point

NEWS
Your main news content goes here...

ANNOUNCEMENTS
Any announcements for today
```

## 📁 File Structure

```
├── dunlap_daily.py         # Main application
├── config_local.json       # Local configuration  
├── run_local.py           # Quick local server launcher
├── run_local.bat          # Windows batch file launcher
├── requirements.txt       # Python dependencies
├── daily_content.txt      # Place your daily content here
└── docs/                 # Generated website files
    ├── index.html        # Main page
    ├── feed.xml          # RSS feed
    ├── style.css         # Styling
    └── archive/          # Individual day pages
```

## 🔧 Full Command Line Options

```bash
python dunlap_daily.py [options]

Options:
  --serve              Start local web server
  --port PORT          Server port (default: 8000)  
  --no-open            Don't auto-open browser
  --no-watch           Disable file watching
  --force              Force regeneration 
  --schedule WHEN      Schedule for specific time (e.g., "tomorrow noon")
  --config FILE        Use custom config file
```

## 📝 Adding Content

### Method 1: Local File (Recommended for local hosting)
1. Create or edit `daily_content.docx` in the project root
2. Write your daily content (first line becomes the title)
3. Save the file - the server will auto-detect changes and regenerate

### Method 2: OneDrive Integration (Optional)
1. Configure OneDrive settings in `config_local.json`:
```json
{
  "onedrive": {
    "client_id": "your-app-id",
    "client_secret": "your-app-secret", 
    "tenant_id": "your-tenant-id",
    "file_path": "/path/to/daily-content.docx"
  }
}
```

## ⚙️ Configuration

Edit `config_local.json` to customize:

```json
{
  "newsletter": {
    "title": "Your Newsletter Name",
    "description": "Your newsletter description",
    "author": "Your Name",
    "link": "http://localhost:8000"
  },
  "local_server": {
    "port": 8000,           // Server port
    "auto_open": true,      // Auto-open browser
    "watch_files": true     // Auto-regenerate on changes
  }
}
```

## 🔧 Command Line Options

```bash
python dunlap_daily.py [options]

Options:
  --serve              Start local web server
  --port PORT          Server port (default: 8000)  
  --no-open            Don't auto-open browser
  --no-watch           Disable file watching
  --force              Force regeneration 
  --config FILE        Use custom config file
```

## 🎯 Benefits of Local Hosting

✅ **No External Dependencies**: No need to configure GitHub Pages, Azure, or other hosting services  
✅ **Instant Updates**: See changes immediately as you edit content  
✅ **Offline Access**: Works completely offline  
✅ **Easy Setup**: Just run one command to start  
✅ **File Watching**: Automatically regenerates when content changes  
✅ **Local Control**: Full control over your newsletter without external services

## 🏗️ How It Works

1. **Content Input**: Reads from `daily_content.docx` or OneDrive
2. **Generation**: Creates HTML pages and RSS feed in `docs/` folder  
3. **Local Server**: Serves the content on `http://localhost:8000`
4. **Auto-watch**: Monitors file changes and regenerates content automatically
5. **Browser**: Opens your newsletter in your default browser

## 📧 Accessing Your Newsletter

- **Main Page**: http://localhost:8000
- **RSS Feed**: http://localhost:8000/feed.xml  
- **Archive**: http://localhost:8000/archive.html

## 🆘 Troubleshooting

**Port already in use?**
```bash
python dunlap_daily.py --serve --port 9000
```

**Content not updating?**
- Ensure `daily_content.docx` exists
- Check the console for error messages
- Try running with `--force` flag

**Dependencies missing?**
```bash
pip install -r requirements.txt
```

## 🔄 Migration from GitHub Pages

Your existing content and setup will work with minimal changes:
1. Your existing `docs/` folder structure remains the same
2. All HTML and RSS files are generated identically  
3. Simply use the local server instead of pushing to GitHub Pages

This local setup gives you the same functionality as GitHub Pages but with immediate feedback and no external dependencies!

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