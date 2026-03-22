#!/usr/bin/env python3
"""
Helper script to kill existing server and start fresh.
"""

import subprocess
import sys
import time
from pathlib import Path

def kill_existing_servers():
    """Kill any existing python servers on common ports."""
    ports_to_check = [8000, 8001, 8002, 8080]
    
    for port in ports_to_check:
        try:
            # Windows command to find processes using the port
            result = subprocess.run(
                f'netstat -ano | findstr :{port}',
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout:
                print(f"🔍 Found process using port {port}")
                
                # Extract PID from netstat output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'LISTENING' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1]
                            try:
                                # Kill the process
                                subprocess.run(f'taskkill /F /PID {pid}', shell=True, check=True)
                                print(f"✅ Killed process {pid} on port {port}")
                            except subprocess.CalledProcessError:
                                print(f"❌ Could not kill process {pid}")
                                
        except Exception as e:
            # Ignore errors, just try next port
            pass

def main():
    print("🧹 Cleaning up existing servers...")
    kill_existing_servers()
    
    print("\n⏳ Waiting 2 seconds for cleanup...")
    time.sleep(2)
    
    print("🚀 Starting fresh newsletter server...")
    
    # Import and run the newsletter server
    sys.path.insert(0, str(Path(__file__).parent))
    from dunlap_daily import DunlapDailyGenerator
    
    try:
        generator = DunlapDailyGenerator("config_local.json")
        generator.serve_local()
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()