#!/usr/bin/env python3
"""
Simple launcher for MUSCLE5 Sequence Alignment Tool
This version uses the compatibility module to handle different environments.
"""

import os
import sys
from datetime import datetime

# Add helpful banner when starting
def print_banner():
    """Print an informative banner when starting the application"""
    banner = """
    __  ___                __     ______     _____                                  
   /  |/  /_  _________  / /__  / ____/____/ ___/___  _____  __  _____ ____  ______
  / /|_/ / / / / ___/ _ \/ / _ \/___ \/ ___/\__ \/ _ \/ __ \/ / / / _ \_  / / / / /
 / /  / / /_/ (__  )  __/ /  __/___/ / /__ ___/ /  __/ / / / /_/ /  __// /_/ /_/ / 
/_/  /_/\\__,_/____/\\___/_/\\___/_____/\\___//____/\\___/_/ /_/\\__, /\\___/___/\\__, /  
                                                          /____/         /____/   
    """
    print(banner)
    print("MUSCLE5 Sequence Alignment Tool")
    print(f"Starting application at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Web interface will be available shortly...")
    print("Press Ctrl+C to stop the application\n")

def main():
    print_banner()
    
    # Import modules after banner to show something quickly
    from app import create_ui, check_and_setup_muscle
    from utils.compatibility import launch_app, is_codespaces
    
    # Check and setup MUSCLE5
    check_and_setup_muscle()
    
    # Create the app interface
    app = create_ui()
    
    # Launch the app using our compatibility wrapper
    try:
        launch_app(app, quiet=True)
    except Exception as e:
        print(f"Error launching application: {str(e)}")
        print("\nTrying alternative launch method...")
        
        # Alternative launch method as fallback
        try:
            if is_codespaces():
                app.launch(server_name="0.0.0.0", share=True, quiet=True)
            else:
                app.launch(share=False)
        except Exception as e2:
            print(f"Failed to launch application: {str(e2)}")
            sys.exit(1)

if __name__ == "__main__":
    main()
