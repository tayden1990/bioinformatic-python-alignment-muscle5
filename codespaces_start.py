#!/usr/bin/env python3
"""
Single-command starter for MUSCLE5 Sequence Alignment Tool in GitHub Codespaces.
Just run: python codespaces_start.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# ANSI color codes for terminal output
COLORS = {
    "blue": "\033[94m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "bold": "\033[1m",
    "reset": "\033[0m"
}

def print_header():
    """Print a simple welcome message"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{COLORS['bold']}{COLORS['blue']}======================================================{COLORS['reset']}")
    print(f"{COLORS['bold']}{COLORS['green']}   MUSCLE5 SEQUENCE ALIGNMENT TOOL - CODESPACES     {COLORS['reset']}")
    print(f"{COLORS['bold']}{COLORS['blue']}======================================================{COLORS['reset']}")
    print()
    print(f"{COLORS['yellow']}Starting the application in GitHub Codespaces...{COLORS['reset']}")
    print()

def setup_muscle():
    """Ensure MUSCLE5 is downloaded and configured"""
    print(f"{COLORS['blue']}➤ Checking MUSCLE5 installation...{COLORS['reset']}")
    
    muscle_config = Path("muscle_config.txt")
    if muscle_config.exists() and muscle_config.read_text().strip():
        muscle_path = muscle_config.read_text().strip()
        if Path(muscle_path).exists():
            print(f"{COLORS['green']}  ✓ MUSCLE5 is already configured{COLORS['reset']}")
            return True
    
    print(f"{COLORS['yellow']}  ⚙ Setting up MUSCLE5...{COLORS['reset']}")
    try:
        subprocess.run([sys.executable, "setup_muscle.py", "--force"], check=True)
        print(f"{COLORS['green']}  ✓ MUSCLE5 setup complete{COLORS['reset']}")
        return True
    except Exception as e:
        print(f"{COLORS['red']}  ✗ MUSCLE5 setup failed: {str(e)}{COLORS['reset']}")
        return False

def run_application():
    """Start the application with proper settings for Codespaces"""
    print(f"{COLORS['blue']}➤ Starting application server...{COLORS['reset']}")
    
    # Set required environment variables for Codespaces
    os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"
    os.environ["GRADIO_SERVER_PORT"] = "7860"
    
    # Start the actual application
    print(f"{COLORS['green']}  ✓ Application starting at http://127.0.0.1:7860{COLORS['reset']}")
    print(f"{COLORS['yellow']}  ⚙ When the browser tab opens, wait for the interface to fully load{COLORS['reset']}")
    print(f"{COLORS['yellow']}  ⚙ If no browser opens, click the 'PORTS' tab and the 'Open in Browser' icon{COLORS['reset']}")
    print()
    print(f"{COLORS['bold']}Press Ctrl+C to stop the application when finished{COLORS['reset']}")
    print()
    
    # Start the main app with parameters optimized for Codespaces
    try:
        subprocess.run([
            sys.executable, "app.py",
            "--server-name=0.0.0.0",
            "--server-port=7860", 
            "--share=true"
        ])
    except KeyboardInterrupt:
        print(f"\n{COLORS['yellow']}Application stopped by user{COLORS['reset']}")

def main():
    """Main entry point"""
    print_header()
    
    if setup_muscle():
        run_application()
    else:
        print(f"{COLORS['red']}Unable to start application due to MUSCLE5 setup failure.{COLORS['reset']}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
