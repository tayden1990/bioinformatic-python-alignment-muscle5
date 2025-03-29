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
    import gradio as gr
    
    # Check and setup MUSCLE5
    check_and_setup_muscle()
    
    # Create the app interface
    app = create_ui()
    
    # Launch the app with simplified approach
    try:
        print("Starting application...")
        # Set server_name to 0.0.0.0 to ensure proper binding in Codespaces
        result = app.launch(server_name="0.0.0.0", share=True)
        
        # Try to safely access share_url if it exists
        try:
            if hasattr(result, 'share_url') and result.share_url:
                print("\n" + "=" * 60)
                print(f"🌎 PUBLIC SHARING URL: {result.share_url}")
                print("=" * 60 + "\n")
        except:
            # If we can't access share_url attribute, just continue silently
            pass
            
    except Exception as e:
        print(f"Error launching application: {str(e)}")
        print("\nTrying alternative launch method...")
        
        # Simplest possible approach as final fallback
        try:
            app.launch(server_name="0.0.0.0", share=True, prevent_thread_lock=True)
        except Exception as e2:
            print(f"Failed to launch application: {str(e2)}")
            sys.exit(1)

if __name__ == "__main__":
    main()
