#!/usr/bin/env python3
"""
Dedicated GitHub Codespaces launcher for MUSCLE5 Sequence Alignment Tool
Ensures compatibility with various Gradio versions in the Codespaces environment
"""

import os
import sys
import subprocess
import time
import platform
from datetime import datetime

def print_header():
    """Print a colorful header"""
    colors = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "blue": "\033[94m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m"
    }
    
    print(f"{colors['bold']}{colors['blue']}==============================================={colors['reset']}")
    print(f"{colors['bold']}{colors['green']}    MUSCLE5 SEQUENCE ALIGNMENT TOOL - CODESPACES{colors['reset']}")
    print(f"{colors['bold']}{colors['blue']}==============================================={colors['reset']}")
    print(f"Python: {colors['yellow']}{platform.python_version()}{colors['reset']}")
    print(f"OS: {colors['yellow']}{platform.system()} {platform.release()}{colors['reset']}")
    print(f"Date: {colors['yellow']}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{colors['reset']}")
    print()

def get_gradio_version():
    """Get the installed Gradio version"""
    try:
        import gradio
        return getattr(gradio, "__version__", "unknown")
    except ImportError:
        return "not installed"

def check_requirements():
    """Check for required packages and compatibility"""
    print("Checking environment...")
    
    # Check for Gradio
    gradio_version = get_gradio_version()
    print(f"- Gradio version: {gradio_version}")
    
    if gradio_version == "not installed":
        print("  ❌ Gradio is not installed!")
        print("  Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=False)
        gradio_version = get_gradio_version()
        print(f"  - Installed Gradio version: {gradio_version}")
    
    # Check for MUSCLE5
    import os
    from app import check_and_setup_muscle
    
    print("- Checking MUSCLE5 installation...")
    check_result = check_and_setup_muscle()
    if check_result:
        print("  ✅ MUSCLE5 is properly configured")
    else:
        print("  ⚠️ MUSCLE5 setup may not be complete")

def run_application():
    """Run the application using the best method for this environment"""
    gradio_version = get_gradio_version()
    
    print("\nStarting MUSCLE5 Sequence Alignment Tool...")
    print("The web interface will be accessible via the Codespaces port forwarding.")
    print("If prompted to open a browser tab, select 'Open in Browser'\n")
    
    if gradio_version.startswith("4."):
        print(f"Using launch method for Gradio 4.x (detected {gradio_version})")
        print("Command: python simple_app.py\n")
        subprocess.run([sys.executable, "simple_app.py"])
    else:
        print(f"Using launch method for Gradio 3.x (detected {gradio_version})")
        print("Command: python run_simple.py\n")
        subprocess.run([sys.executable, "run_simple.py"])

def main():
    print_header()
    check_requirements()
    run_application()

if __name__ == "__main__":
    main()
