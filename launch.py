#!/usr/bin/env python3
"""
Universal Launcher for MUSCLE5 Sequence Alignment Tool
Works consistently in local environment and GitHub Codespaces
"""

import os
import sys
import platform
import subprocess
from datetime import datetime
import importlib.util

def print_banner():
    """Print a welcome banner with basic info"""
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
    print(f"System: {platform.system()} {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

def is_codespaces():
    """Check if running in GitHub Codespaces environment"""
    return "CODESPACES" in os.environ or "CODESPACE_NAME" in os.environ

def setup_muscle():
    """Set up MUSCLE5 executable if needed"""
    # Check if muscle_config.txt exists and has valid content
    muscle_path = None
    try:
        if os.path.exists("muscle_config.txt"):
            with open("muscle_config.txt", "r") as f:
                muscle_path = f.read().strip()
                
            # Verify the path exists and is executable
            if not os.path.exists(muscle_path):
                muscle_path = None
    except:
        muscle_path = None
    
    # If not configured, run setup
    if not muscle_path:
        print("MUSCLE5 executable not configured. Running setup...")
        try:
            subprocess.run([sys.executable, "setup_muscle.py", "--force"], check=True)
            print("MUSCLE5 setup completed successfully.")
        except Exception as e:
            print(f"Error setting up MUSCLE5: {e}")
            print("Please run 'python setup_muscle.py --force' manually.")

def get_gradio_version():
    """Get installed Gradio version"""
    try:
        import gradio
        return gradio.__version__
    except ImportError:
        return None

def start_application():
    """Start the main application"""
    print("\nStarting MUSCLE5 Sequence Alignment Tool...")
    
    # Set environment variable to indicate we're launched from the unified launcher
    os.environ["MUSCLE5_LAUNCHER"] = "1"
    
    # In Codespaces, we need to ensure the app runs with the right server name
    if is_codespaces():
        os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"
        print("Running in GitHub Codespaces mode")
        
    # Use main app.py if it exists, otherwise fall back to simple_app.py
    if os.path.exists("app.py"):
        print("Launching main application (app.py)...")
        subprocess.run([sys.executable, "app.py"])
    else:
        print("Main app.py not found, launching simple app...")
        subprocess.run([sys.executable, "simple_app.py"])
    
    print("\nApplication terminated.")

def main():
    """Main function"""
    print_banner()
    
    # First, ensure MUSCLE5 is set up
    setup_muscle()
    
    # Start the main application
    start_application()
    
    # Print access instructions for Codespaces
    if is_codespaces():
        print("\nAccessing in GitHub Codespaces:")
        print("1. Look for the 'PORTS' tab at the bottom panel of VS Code")
        print("2. Find port 7860, right-click and select 'Open in Browser'")
        print("3. If you only see a welcome message, try refreshing the browser page")

if __name__ == "__main__":
    main()
