#!/usr/bin/env python3
"""
GitHub Codespaces Setup Notice
This script displays a welcome message and instructions when a Codespace is created.
"""

import os
import platform
import sys
import subprocess
from datetime import datetime

def print_colored(text, color):
    """Print colored text to the terminal"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
        "bold": "\033[1m"
    }
    
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

def check_muscle_installation():
    """Check if MUSCLE5 is installed and configured"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "muscle_config.txt")
    
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            muscle_path = f.read().strip()
            if os.path.exists(muscle_path):
                return True, muscle_path
    
    return False, None

def main():
    """Display setup notice and environment information"""
    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Check if this is a GitHub Codespaces environment
    in_codespaces = "CODESPACES" in os.environ
    
    # ASCII Art banner
    banner = """
    __  ___                __     ______     _____                                  
   /  |/  /_  _________  / /__  / ____/____/ ___/___  _____  __  _____ ____  ______
  / /|_/ / / / / ___/ _ \/ / _ \/___ \/ ___/\__ \/ _ \/ __ \/ / / / _ \\_  / / / / /
 / /  / / /_/ (__  )  __/ /  __/___/ / /__ ___/ /  __/ / / / /_/ /  __// /_/ /_/ / 
/_/  /_/\\__,_/____/\\___/_/\\___/_____/\\___//____/\\___/_/ /_/\\__, /\\___/___/\\__, /  
                                                          /____/         /____/   
    """
    
    print_colored(banner, "cyan")
    
    if in_codespaces:
        print_colored("🚀 WELCOME TO MUSCLE5 SEQUENCE ALIGNMENT TOOL 🚀", "green")
        print_colored("Running in GitHub Codespaces environment\n", "green")
    else:
        print_colored("🚀 MUSCLE5 SEQUENCE ALIGNMENT TOOL 🚀", "blue")
        print_colored("Running in local environment\n", "blue")
    
    # Check MUSCLE5 installation
    muscle_installed, muscle_path = check_muscle_installation()
    
    if muscle_installed:
        print_colored("✅ MUSCLE5 executable is configured:", "green")
        print_colored(f"   Path: {muscle_path}\n", "white")
    else:
        print_colored("⚠️  MUSCLE5 executable is not configured yet", "yellow")
        print_colored("   Run 'python setup_muscle.py --force' to download and configure it\n", "white")
    
    # Show system info
    print_colored("System Information:", "magenta")
    print_colored(f"  • Python: {platform.python_version()}", "white")
    print_colored(f"  • OS: {platform.system()} {platform.release()}", "white")
    print_colored(f"  • Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", "white")
    
    # Startup instructions
    print_colored("To start the application:", "yellow")
    print_colored("  Run: python app.py", "white")
    print_colored("  The web interface will be available at http://127.0.0.1:7860\n", "white")
    
    print_colored("For more information:", "blue")
    print_colored("  • View README.md for usage instructions", "white")
    print_colored("  • See GITHUB_CODESPACES.md for Codespaces-specific guidance", "white")
    print_colored("  • Visit https://github.com/tayden1990/bioinformatic-python-alignment-muscle5 for updates\n", "white")
    
    print_colored("Happy aligning! 🧬🔬✨\n", "green")

if __name__ == "__main__":
    main()
