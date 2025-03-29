#!/usr/bin/env python3
"""
Requirements installer script that properly handles environment-specific dependencies.
"""

import os
import sys
import subprocess

def is_codespaces():
    """Check if running in GitHub Codespaces environment"""
    return "CODESPACES" in os.environ or "CODESPACE_NAME" in os.environ

def main():
    """Install requirements based on the current environment"""
    print("Installing dependencies...")
    
    # Basic requirements without environment-specific packages
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt",
        "--no-cache-dir", "--upgrade", "--use-pep517"
    ], check=True)
    
    # Install additional Codespaces-specific packages if needed
    if is_codespaces():
        print("Detected GitHub Codespaces environment, installing specific versions...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "gradio==3.50.2", 
            "--no-cache-dir", "--upgrade"
        ], check=True)
    
    print("Dependency installation completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
