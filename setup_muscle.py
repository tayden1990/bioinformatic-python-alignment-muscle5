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
    try:
        print(f"Downloading from {url} to {output_path}")
        
        # Create a request with a user agent to avoid 403 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
            total_size = int(response.info().get('Content-Length', 0))
            downloaded = 0
            chunk_size = 1024 * 1024  # 1MB chunks
            
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                downloaded += len(chunk)
                out_file.write(chunk)
                
                # Print progress
                if total_size > 0:
                    percent = int(downloaded * 100 / total_size)
                    sys.stdout.write(f"\rDownloading... {percent}% ({downloaded} / {total_size} bytes)")
                    sys.stdout.flush()
                else:
                    sys.stdout.write(f"\rDownloading... {downloaded} bytes")
                    sys.stdout.flush()
            
            print()  # New line after progress
            return True
    except urllib.error.HTTPError as e:
        print(f"Error downloading file: {e}")
        # Check if we need to provide specific advice based on the error
        if e.code == 403:
            print("Access forbidden. The server may be blocking automated downloads.")
            print("Please try manual download from the website.")
        return False
    except Exception as e:
        print(f"Unexpected error during download: {e}")
        return False

def make_executable(path):
    """Make a file executable"""
    current_mode = os.stat(path).st_mode
    os.chmod(path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def get_muscle5_download_url():
    """Get the appropriate MUSCLE5 download URL for the current platform"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Updated URLs for MUSCLE5 - now using the updated muscle website URLs
    base_url = "https://drive5.com/muscle5/"
    
    if system == "windows":
        return f"{base_url}muscle5.1.win64.exe", "muscle5.exe"
    elif system == "darwin":  # macOS
        if "arm" in machine or "aarch64" in machine:
            return f"{base_url}muscle5.1.macos_arm64", "muscle5"
        else:
            return f"{base_url}muscle5.1.macos_intel64", "muscle5"
    elif system == "linux":
        if "aarch64" in machine or "arm" in machine:
            return f"{base_url}muscle5.1.linux_arm64", "muscle5"
        else:
            return f"{base_url}muscle5.1.linux_intel64", "muscle5"
    else:
        raise RuntimeError(f"Unsupported platform: {system} {machine}")

def extract_tar_gz(tar_path, target_dir):
    """Extract a tar.gz file to the target directory"""
    try:
        import tarfile
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=target_dir)
        return True
    except Exception as e:
        print(f"Error extracting archive: {e}")
        return False

def find_muscle_executable(dir_path):
    """Find the MUSCLE executable in the extracted directory"""
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.lower().startswith("muscle") and (file.lower().endswith(".exe") or "." not in file):
                return os.path.join(root, file)
    return None

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
        print(f"Will download from: {url}")
    except RuntimeError as e:
        print(f"Error: {e}")
        print_manual_instructions()
        return None
    
    # Download MUSCLE5
    with tempfile.TemporaryDirectory() as tmp_dir:
        download_path = os.path.join(tmp_dir, exe_name)
        extract_dir = os.path.join(tmp_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        
        if download_file(url, download_path):
            # Check if the downloaded file is already an executable (not an archive)
            if not url.endswith('.tar.gz'):
                # It's a direct executable, no need to extract
                muscle_path = download_path
            else:
                # Extract the tar.gz file
                if not extract_tar_gz(download_path, extract_dir):
                    print_manual_instructions()
                    return None
                
                # Find the muscle executable in the extracted files
                muscle_path = find_muscle_executable(extract_dir)
                if not muscle_path:
                    print("Could not find MUSCLE executable in the extracted files.")
                    print_manual_instructions()
                    return None
            
            # Make executable if needed (for Unix)
            if platform.system() != "Windows":
                make_executable(muscle_path)
            
            # Move to target directory
            target_path = os.path.join(target_dir, exe_name)
            shutil.move(muscle_path, target_path)
            
            # Make executable again after moving (just to be sure)
            if platform.system() != "Windows":
                make_executable(target_path)
            
            # Save the path to config file
            with open(config_path, "w") as f:
                f.write(target_path)
            
            print(f"MUSCLE5 installed at: {target_path}")
            return target_path
        else:
            print_manual_instructions()
    
    return None

def print_manual_instructions():
    """Print instructions for manual download of MUSCLE"""
    print("\n== MANUAL DOWNLOAD INSTRUCTIONS ==")
    print("The automatic download failed. Please follow these steps to manually install MUSCLE:")
    print("1. Visit the official MUSCLE website: https://drive5.com/muscle5/")
    print("2. Download the appropriate version for your operating system")
    print("3. Save the executable file to a location on your computer")
    print("4. Make the file executable (chmod +x muscle5) on Mac/Linux")
    print("5. Update the muscle_config.txt file with the full path to the executable")
    print("\nAlternatively, you can download a pre-compiled binary from other sources:")
    print("- Bioconda: https://anaconda.org/bioconda/muscle")
    print("- Homebrew (Mac): brew install muscle")
    print("- Ubuntu/Debian: apt-get install muscle")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Set up MUSCLE5 for the alignment tool")
    parser.add_argument("--force", action="store_true", help="Force re-download even if already configured")
    args = parser.parse_args()
    
    muscle_path = setup_muscle5(force=args.force)
    
    if muscle_path:
        print("\n✓ MUSCLE5 setup completed successfully!")
        
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
        # Use ASCII symbol to avoid encoding issues on Windows
        print("\nX MUSCLE5 setup failed. Please try again or install manually.")
        sys.exit(1)

if __name__ == "__main__":
    main()
