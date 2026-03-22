#!/usr/bin/env python3
"""
Schedule tomorrow's newsletter from OneDrive.
"""

import sys
from pathlib import Path
import datetime

def main():
    print("📅 Scheduling Tomorrow's Newsletter for Noon")
    print("=" * 50)
    
    # Add current directory to path
    sys.path.insert(0, str(Path(__file__).parent))
    
    from dunlap_daily import DunlapDailyGenerator, parse_schedule_string
    
    try:
        # Create generator with local config (includes OneDrive path)
        generator = DunlapDailyGenerator("config_local.json")
        
        # Parse tomorrow noon
        scheduled_date = parse_schedule_string("tomorrow noon")
        print(f"📆 Target date: {scheduled_date.strftime('%B %d, %Y at %I:%M %p')}")
        
        # Expected file path (for info)
        tomorrow_date = datetime.datetime.now().strftime("%m_%d_%y").replace("0", "").replace("_", "_")
        expected_path = f"/Market/Dunlap Daily/Dunlap Daily 3_19_26.docx"
        print(f"📄 Expected OneDrive file: {expected_path}")
        
        # Check OneDrive configuration
        onedrive_config = generator.config.get("onedrive", {})
        if not onedrive_config.get("client_id"):
            print("⚠️  OneDrive not configured - will look for local fallback file")
            
            # Check for local files
            local_docx = generator.base_dir / "daily_content.docx" 
            local_txt = generator.base_dir / "daily_content.txt"
            
            if local_txt.exists():
                print(f"✅ Found local content: {local_txt}")
            elif local_docx.exists():
                print(f"✅ Found local content: {local_docx}")
            else:
                print("❌ No local content found!")
                print("   Create 'daily_content.txt' with tomorrow's content")
                return
        else:
            print("✅ OneDrive configured - will try to fetch from cloud")
        
        print("\n🚀 Generating scheduled newsletter...")
        
        # Run with scheduled date
        generator.run(force_update=True, scheduled_date=scheduled_date)
        
        print("\n✅ Tomorrow's newsletter scheduled successfully!")
        print(f"🌐 Start server with: python run_fresh.py")
        print(f"📱 Or use: python dunlap_daily.py --serve --port 8001")
        
    except Exception as e:
        print(f"❌ Error scheduling newsletter: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()