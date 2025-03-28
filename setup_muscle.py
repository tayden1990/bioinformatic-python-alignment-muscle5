#!/usr/bin/env python3
"""
MUSCLE5 Setup Script
This script automates the download and setup of the MUSCLE5 executable
for different operating systems.
"""

import os
import sys
import platform
import subprocess
import shutil
import argparse
from pathlib import Path
import urllib.request

# MUSCLE5 download URLs
MUSCLE_URLS = {
    "Windows": "https://github.com/rcedgar/muscle/releases/download/v5.3/muscle-win64.v5.3.exe",
    "Darwin": "https://github.com/rcedgar/muscle/releases/download/v5.3/muscle-osx-x86.v5.3",
    "Linux": "https://github.com/rcedgar/muscle/releases/download/v5.3/muscle-linux-x86.v5.3"
}

def get_system_info():
    """Detect the operating system and architecture."""
    system = platform.system()
    architecture = platform.machine()
    
    print(f"Detected system: {system} ({architecture})")
    
    if system not in MUSCLE_URLS:
        print(f"Error: Unsupported operating system: {system}")
        print("MUSCLE5 is available for Windows, macOS (Darwin), and Linux")
        return None
    
    return system

def download_muscle(system, destination=None):
    """Download the appropriate MUSCLE5 executable for the system."""
    url = MUSCLE_URLS[system]
    
    # Default destination directory is the current script directory
    if destination is None:
        destination = os.path.dirname(os.path.abspath(__file__))
    
    # Create destination directory if it doesn't exist
    os.makedirs(destination, exist_ok=True)
    
    # Set appropriate filename
    if system == "Windows":
        filename = "muscle5.exe"
    else:
        filename = "muscle5"
    
    file_path = os.path.join(destination, filename)
    
    print(f"Downloading MUSCLE5 from {url}")
    print(f"Saving to {file_path}")
    
    try:
        # Download the file
        urllib.request.urlretrieve(url, file_path)
        
        # Make executable on Unix-like systems
        if system != "Windows":
            os.chmod(file_path, 0o755)
        
        print("Download completed successfully.")
        return file_path
    
    except Exception as e:
        print(f"Error downloading MUSCLE5: {e}")
        return None

def verify_installation(file_path):
    """Verify that the downloaded MUSCLE5 executable works."""
    print("Verifying MUSCLE5 installation...")
    
    try:
        # Try running with -version to see if it's actually MUSCLE
        result = subprocess.run(
            [file_path, "-version"], 
            capture_output=True, 
            text=True,
            check=False,
            timeout=5  # Add a timeout to avoid hanging
        )
        
        # Check if the output contains MUSCLE
        output = result.stdout + result.stderr
        if "MUSCLE" in output or "muscle" in output:
            print("✅ MUSCLE5 installation verified!")
            print(f"Version information: {output.strip()}")
            return True
        else:
            print("❌ Verification failed: The executable doesn't appear to be MUSCLE5")
            print(f"Output: {output}")
            return False
    
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def configure_environment(file_path):
    """Configure the environment to use the MUSCLE5 executable."""
    abs_path = os.path.abspath(file_path)
    
    # Save the path to the configuration file
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "muscle_config.txt")
    try:
        with open(config_path, "w") as f:
            f.write(abs_path)
        print(f"Saved MUSCLE5 path to configuration file: {config_path}")
    except Exception as e:
        print(f"Warning: Failed to save configuration file: {e}")
    
    # Suggest setting environment variable
    if platform.system() == "Windows":
        print("\nTo set the environment variable permanently, run this in Command Prompt:")
        print(f'setx MUSCLE5_PATH "{abs_path}"')
    else:
        print("\nTo set the environment variable permanently, add this to your shell profile (~/.bashrc, ~/.zshrc, etc.):")
        print(f'export MUSCLE5_PATH="{abs_path}"')
    
    # Set for current process
    os.environ["MUSCLE5_PATH"] = abs_path
    print(f"\nMUSCLE5_PATH is now set to: {abs_path}")
    print("This will work for this session, but you should set it permanently as suggested above.")

def main():
    parser = argparse.ArgumentParser(description="Setup MUSCLE5 executable for sequence alignment")
    parser.add_argument("--destination", help="Destination directory for the MUSCLE5 executable", default=None)
    parser.add_argument("--force", action="store_true", help="Force download even if executable already exists")
    args = parser.parse_args()
    
    # Detect the operating system
    system = get_system_info()
    if not system:
        return 1
    
    destination = args.destination
    
    # Determine the expected file path
    if destination is None:
        destination = os.path.dirname(os.path.abspath(__file__))
    
    filename = "muscle5.exe" if system == "Windows" else "muscle5"
    file_path = os.path.join(destination, filename)
    
    # Check if the executable already exists
    if os.path.exists(file_path) and not args.force:
        print(f"MUSCLE5 executable already exists at {file_path}")
        print("To download again, use the --force option")
        
        # Verify the existing executable
        if verify_installation(file_path):
            configure_environment(file_path)
            return 0
        else:
            print("Existing executable failed verification. Consider using --force to download again.")
            return 1
    
    # Download MUSCLE5
    file_path = download_muscle(system, destination)
    if not file_path:
        return 1
    
    # Verify the installation
    if not verify_installation(file_path):
        return 1
    
    # Configure the environment
    configure_environment(file_path)
    
    print("\n✨ MUSCLE5 setup completed successfully! ✨")
    print(f"You can now run the alignment tool: python app.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
