#!/usr/bin/env python3
"""
GitHub Codespaces starter script for MUSCLE5 Sequence Alignment Tool
Handles compatibility with Gradio versions and Codespaces environment
"""

import os
import sys
import platform
from datetime import datetime
import time
import subprocess

def print_banner():
    """Print a colorful header for Codespaces environment"""
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
    print(f"Starting application at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 80)
    print(f"System: {platform.system()} {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    print("-" * 80)
    print()

def check_muscle_installation():
    """Check if MUSCLE5 is installed and setup if needed"""
    from app import check_and_setup_muscle
    
    print("Checking MUSCLE5 installation...")
    result = check_and_setup_muscle()
    
    if result:
        print("✅ MUSCLE5 is ready to use")
    else:
        print("⚠️ MUSCLE5 setup issue - will attempt to fix during startup")
    
    print()
    return result

def get_gradio_version():
    """Get the installed Gradio version"""
    try:
        import gradio
        version = getattr(gradio, "__version__", "unknown")
        print(f"Detected Gradio version: {version}")
        return version
    except ImportError:
        print("WARNING: Gradio not installed. Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        import gradio
        version = getattr(gradio, "__version__", "unknown")
        print(f"Installed Gradio version: {version}")
        return version

def launch_application():
    """Launch the application with the best method for Codespaces"""
    gradio_version = get_gradio_version()
    
    print("\nStarting MUSCLE5 Sequence Alignment Tool...")
    print("The application will be accessible in your browser shortly.\n")
    
    # For Gradio 4.x, use a different launch approach
    if gradio_version.startswith("4."):
        print("Using launch method for Gradio 4.x")
        
        # Import and create the application
        from app import create_ui
        app = create_ui()
        
        # Launch with settings compatible with Codespaces and Gradio 4.x
        try:
            # First attempt: Use server_name parameter
            print("Launching with Codespaces-compatible settings...")
            result = app.launch(
                server_name="0.0.0.0",
                share=True,
                quiet=False
            )
            
            # Display public URL if available
            if hasattr(result, 'share_url') and result.share_url:
                print("\n" + "=" * 60)
                print(f"🌎 PUBLIC SHARING URL: {result.share_url}")
                print("=" * 60 + "\n")
                
            return True
            
        except Exception as e:
            print(f"First launch attempt failed: {str(e)}")
            print("Trying alternative launch method...")
            
            try:
                # Second attempt: Simplified parameters
                result = app.launch(server_name="0.0.0.0", share=True)
                return True
            except Exception as e2:
                print(f"Second launch attempt failed: {str(e2)}")
                print("Falling back to direct module execution...")
                
                # Third attempt: Execute app.py directly
                subprocess.run([sys.executable, "app.py"])
                return True
    else:
        # For Gradio 3.x or other versions
        print("Using compatibility mode for Gradio 3.x")
        subprocess.run([sys.executable, "run_simple.py"])
        return True

def main():
    print_banner()
    check_muscle_installation()
    success = launch_application()
    
    if not success:
        print("\n⚠️ Application failed to start properly.")
        print("Try running one of these commands manually:")
        print("  python app.py")
        print("  python run_simple.py")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
