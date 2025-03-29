#!/usr/bin/env python3
"""
MUSCLE5 Setup Script
Downloads and configures MUSCLE5 executable for this application
Works in both local and Codespaces environments
"""

import os
import sys
import platform
import subprocess
import tempfile
import urllib.request
import shutil
import zipfile
import stat
from pathlib import Path

def print_step(message):
    """Print a step in the setup process"""
    print(f"\n[SETUP] {message}")

def is_codespaces():
    """Check if running in GitHub Codespaces environment"""
    return "CODESPACES" in os.environ or "CODESPACE_NAME" in os.environ

def download_file(url, output_path):
    """Download a file from URL to output path with progress"""
    print(f"Downloading from {url} to {output_path}")
    try:
        with urllib.request.urlopen(url) as response, open(output_path, 'wb') as out_file:
            total_size = int(response.info().get('Content-Length', 0))
            downloaded = 0
            block_size = 8192
            
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                    
                downloaded += len(buffer)
                out_file.write(buffer)
                
                # Simple progress indicator
                progress = int(50 * downloaded / total_size) if total_size > 0 else 0
                sys.stdout.write(f"\r[{'#' * progress}{' ' * (50-progress)}] {downloaded/1024/1024:.1f}MB")
                sys.stdout.flush()
                
        print("\nDownload completed successfully.")
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

def make_executable(path):
    """Make a file executable"""
    current_mode = os.stat(path).st_mode
    os.chmod(path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def get_muscle5_download_url():
    """Get the appropriate MUSCLE5 download URL for the current platform"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "https://drive5.com/muscle5/muscle5.1.win64.exe", "muscle5.exe"
    elif system == "darwin":  # macOS
        if "arm" in machine or "aarch64" in machine:
            return "https://drive5.com/muscle5/muscle5.1.macos_arm64", "muscle5"
        else:
            return "https://drive5.com/muscle5/muscle5.1.macos_intel64", "muscle5"
    elif system == "linux":
        if "aarch64" in machine or "arm" in machine:
            return "https://drive5.com/muscle5/muscle5.1.linux_arm64", "muscle5"
        else:
            return "https://drive5.com/muscle5/muscle5.1.linux_intel64", "muscle5"
    else:
        raise RuntimeError(f"Unsupported platform: {system} {machine}")

def setup_muscle5(force=False):
    """Set up MUSCLE5 executable"""
    print_step("Setting up MUSCLE5 executable")
    
    # Define the target directory
    if is_codespaces():
        # In Codespaces, store in workspace
        target_dir = os.path.abspath("bin")
    else:
        # Locally, use a user-specific location
        target_dir = os.path.join(os.path.expanduser("~"), ".muscle5")
    
    # Create directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Check if already configured
    config_path = os.path.abspath("muscle_config.txt")
    if os.path.exists(config_path) and not force:
        with open(config_path, "r") as f:
            muscle_path = f.read().strip()
            if os.path.exists(muscle_path):
                print(f"MUSCLE5 already configured at: {muscle_path}")
                return muscle_path
    
    # Get platform-specific download URL and executable name
    try:
        url, exe_name = get_muscle5_download_url()
    except RuntimeError as e:
        print(f"Error: {e}")
        print("You'll need to manually download MUSCLE5 for your platform from: https://drive5.com/muscle5/")
        return None
    
    # Download MUSCLE5
    with tempfile.TemporaryDirectory() as tmp_dir:
        download_path = os.path.join(tmp_dir, exe_name)
        
        if download_file(url, download_path):
            # Make executable if needed (for Unix)
            if platform.system() != "Windows":
                make_executable(download_path)
            
            # Move to target directory
            target_path = os.path.join(target_dir, exe_name)
            shutil.move(download_path, target_path)
            
            # Make executable again after moving (just to be sure)
            if platform.system() != "Windows":
                make_executable(target_path)
            
            # Save the path to config file
            with open(config_path, "w") as f:
                f.write(target_path)
            
            print(f"MUSCLE5 installed at: {target_path}")
            return target_path
    
    return None

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Set up MUSCLE5 for the alignment tool")
    parser.add_argument("--force", action="store_true", help="Force re-download even if already configured")
    args = parser.parse_args()
    
    muscle_path = setup_muscle5(force=args.force)
    
    if muscle_path:
        print("\n✅ MUSCLE5 setup completed successfully!")
        
        # Test MUSCLE5
        try:
            if platform.system() == "Windows":
                result = subprocess.run([muscle_path, "-version"], capture_output=True, text=True)
            else:
                result = subprocess.run([muscle_path, "-version"], capture_output=True, text=True)
                
            print(f"\nMUSCLE5 version information:")
            print(result.stdout.strip())
        except Exception as e:
            print(f"\nWarning: Could not verify MUSCLE5 installation: {e}")
    else:
        print("\n❌ MUSCLE5 setup failed. Please try again or install manually.")
        sys.exit(1)

if __name__ == "__main__":
    main()
