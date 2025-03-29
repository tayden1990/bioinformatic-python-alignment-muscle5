#!/usr/bin/env python3
"""
Script to install missing dependencies identified by codespaces_diagnostics.py
"""

import sys
import subprocess
import importlib.util
import platform
from datetime import datetime

def print_colored(text, color):
    """Print colored text to the terminal"""
    colors = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m"
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

def check_package(package_name):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package_name):
    """Install a package using pip"""
    print_colored(f"Installing {package_name}...", "yellow")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"Error installing {package_name}: {e}", "red")
        return False

def main():
    """Main function to install missing dependencies"""
    print_colored("\n=== MUSCLE5 MISSING DEPENDENCIES INSTALLER ===", "cyan")
    print_colored(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "white")
    print_colored(f"Python: {platform.python_version()}", "white")
    print_colored(f"System: {platform.system()} {platform.release()} {platform.machine()}\n", "white")
    
    # Define required packages
    missing_packages = []
    
    # Check for missing packages
    if not check_package("scipy"):
        missing_packages.append("scipy")
    if not check_package("biopython"):
        missing_packages.append("biopython")
    
    # Install missing packages
    if missing_packages:
        print_colored(f"Found {len(missing_packages)} missing dependencies: {', '.join(missing_packages)}", "yellow")
        print_colored("Starting installation...\n", "blue")
        
        successfully_installed = []
        failed_to_install = []
        
        for package in missing_packages:
            if install_package(package):
                successfully_installed.append(package)
            else:
                failed_to_install.append(package)
        
        print()
        if successfully_installed:
            print_colored(f"✅ Successfully installed: {', '.join(successfully_installed)}", "green")
        if failed_to_install:
            print_colored(f"❌ Failed to install: {', '.join(failed_to_install)}", "red")
    else:
        print_colored("✅ All required dependencies are already installed!", "green")
    
    print_colored("\nNext steps:", "magenta")
    print_colored("1. Run 'python codespaces_diagnostics.py' to verify all dependencies", "white")
    print_colored("2. Start the application with 'python codespaces_start.py'", "white")
    print_colored("\n==============================================\n", "cyan")

if __name__ == "__main__":
    main()
