#!/usr/bin/env python3
"""
Simple Launcher for MUSCLE5 Sequence Alignment Tool
Compatible with newer versions of Gradio (4.x+)
"""

import os
import sys
import platform
from datetime import datetime

def print_banner():
    """Print a welcome banner"""
    banner = """
    __  ___                __     ______     _____                                  
   /  |/  /_  _________  / /__  / ____/____/ ___/___  _____  __  _____ ____  ______
  / /|_/ / / / / ___/ _ \/ / _ \/___ \/ ___/\__ \/ _ \/ __ \/ / / / _ \\_  / / / / /
 / /  / / /_/ (__  )  __/ /  __/___/ / /__ ___/ /  __/ / / / /_/ /  __// /_/ /_/ / 
/_/  /_/\\__,_/____/\\___/_/\\___/_____/\\___//____/\\___/_/ /_/\\__, /\\___/___/\\__, /  
                                                          /____/         /____/   
    """
    print(banner)
    print("MUSCLE5 Sequence Alignment Tool")
    print(f"Starting application at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Web interface will be available shortly...\n")

def is_codespaces():
    """Check if running in GitHub Codespaces environment"""
    return "CODESPACES" in os.environ or "CODESPACE_NAME" in os.environ

def main():
    print_banner()
    
    print("Loading application modules...")
    
    # Import app creation and check functions
    from app import create_ui, check_and_setup_muscle
    import gradio as gr
    
    # Check Gradio version
    gradio_version = getattr(gr, "__version__", "unknown")
    print(f"Detected Gradio version: {gradio_version}")
    
    # Check and setup MUSCLE5
    print("Checking MUSCLE5 installation...")
    check_and_setup_muscle()
    
    # Create the app interface
    print("Creating user interface...")
    app = create_ui()
    
    # Launch with settings compatible with both Gradio 3.x and 4.x
    print("Starting Gradio server...")
    
    # Always use these basic settings that work across Gradio versions
    launch_kwargs = {
        "server_name": "0.0.0.0",
        "share": True
    }
    
    # For Codespaces, we need specific settings
    if is_codespaces():
        print("Running in GitHub Codespaces environment")
    else:
        print("Running in local environment")
    
    try:
        # Simplest launch approach that should work across Gradio versions
        app.launch(**launch_kwargs)
    except Exception as e:
        print(f"\nError launching application with standard settings: {str(e)}")
        print("Trying alternative launch method...")
        
        try:
            # Remove any problematic parameters that might not be supported
            if "prevent_thread_lock" in launch_kwargs:
                del launch_kwargs["prevent_thread_lock"]
            if "quiet" not in launch_kwargs:
                launch_kwargs["quiet"] = True
                
            app.launch(**launch_kwargs)
        except Exception as e2:
            print(f"Failed to launch application: {str(e2)}")
            print("\nPlease try one of these alternative commands:")
            print("  python run_simple.py")
            print("  gradio app.py")
            sys.exit(1)

if __name__ == "__main__":
    main()
