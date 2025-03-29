#!/usr/bin/env python3
"""
GitHub Codespaces starter script for MUSCLE5 Sequence Alignment Tool
Handles compatibility with Gradio versions and Codespaces environment
"""

import os
import sys
import platform
import datetime
import subprocess
import importlib.util

def print_banner():
    """Print a fancy ASCII banner for the application."""
    banner = """
    __  ___                __     ______     _____                                  
   /  |/  /_  _________  / /__  / ____/____/ ___/___  _____  __  _____ ____  ______
  / /|_/ / / / / ___/ _ \/ / _ \/___ \/ ___/\__ \/ _ \/ __ \/ / / / _ \\_  / / / / /
 / /  / / /_/ (__  )  __/ /  __/___/ / /__ ___/ /  __/ / / / /_/ /  __// /_/ /_/ / 
/_/  /_/\\__,_/____/\\___/_/\\___/_____/\\___//____/\\___/_/ /_/\\__, /\\___/___/\\__, /  
                                                          /____/         /____/   
    """
    print(banner)
    print("MUSCLE5 Sequence Alignment Tool - GitHub Codespaces Edition")
    print(f"Starting application at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 80)
    print(f"System: {platform.system()} {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    print("-" * 80)
    print()

def check_muscle5():
    """Check if MUSCLE5 is installed and accessible."""
    print("Checking MUSCLE5 installation...")
    try:
        # Read the path from config file
        with open("muscle_config.txt", "r") as f:
            muscle_path = f.read().strip()
        
        # Check if the file exists
        if not os.path.exists(muscle_path):
            print("⚠️ MUSCLE5 path not found at configured location")
            print(f"   Path: {muscle_path}")
            print("   Attempting to find MUSCLE5 in PATH...")
            
            # Try to find muscle5 in PATH
            try:
                subprocess.run(["muscle5", "-version"], capture_output=True, check=False)
                print("✅ Found MUSCLE5 in PATH")
                # Update config file
                with open("muscle_config.txt", "w") as f:
                    f.write("muscle5")
                return True
            except FileNotFoundError:
                print("❌ MUSCLE5 not found in PATH")
                print("Please download MUSCLE5 and set the path in the application.")
                return False
        else:
            # Check if it's runnable
            try:
                subprocess.run([muscle_path, "-version"], capture_output=True, check=False)
                print("✅ MUSCLE5 is ready to use")
                return True
            except Exception as e:
                print(f"❌ Error running MUSCLE5: {str(e)}")
                return False
    except Exception as e:
        print(f"❌ Error checking MUSCLE5: {str(e)}")
        return False

def main():
    """Main function to start the application in Codespaces."""
    print_banner()
    check_muscle5()
    
    # Check Gradio version for compatibility
    try:
        gradio_spec = importlib.util.find_spec("gradio")
        if gradio_spec:
            import gradio as gr
            print(f"\nDetected Gradio version: {gr.__version__}")
            
            print("\nStarting MUSCLE5 Sequence Alignment Tool...")
            print("The application will be accessible in your browser shortly.\n")
            
            # Import and run the main application
            # Make sure we're using correct launch parameters for GitHub Codespaces
            gradio_version = gr.__version__.split('.')
            major_version = int(gradio_version[0])
            
            if major_version >= 4:
                print("Using launch method for Gradio 4.x")
                # Import main app module and run it with Codespaces-compatible settings
                from app import create_app
                demo = create_app()
                demo.launch(
                    server_name="0.0.0.0",  # Listen on all interfaces
                    server_port=7860,       # Use the default Gradio port
                    share=True,             # Enable public sharing
                    inbrowser=False,        # Don't try to open a browser
                    debug=False             # Disable debug mode for production
                )
            else:
                print("Using launch method for Gradio 3.x")
                # Import main app module and run it with Codespaces-compatible settings
                import app
                app.main(
                    server_name="0.0.0.0",  # Listen on all interfaces
                    server_port=7860,       # Use the default Gradio port
                    share=True,             # Enable public sharing
                    inbrowser=False,        # Don't try to open a browser
                    debug=False             # Disable debug mode for production
                )
        else:
            print("❌ Gradio not installed. Please install with: pip install gradio")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
