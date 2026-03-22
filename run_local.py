#!/usr/bin/env python3
"""
Simple script to run Dunlap Daily locally.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dunlap_daily import DunlapDailyGenerator

def main():
    """Run the newsletter server locally."""
    print("🚀 Starting Dunlap Daily Local Server...")
    print("=" * 50)
    
    try:
        generator = DunlapDailyGenerator("config_local.json")
        generator.serve_local()
    except KeyboardInterrupt:
        print("\n👋 Thanks for using Dunlap Daily!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()