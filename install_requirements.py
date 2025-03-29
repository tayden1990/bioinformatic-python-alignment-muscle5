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
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt",
            "--no-cache-dir", "--upgrade", "--use-pep517"
        ], check=True)
    except subprocess.CalledProcessError:
        # If the marker syntax in requirements.txt causes issues, fall back to manual installation
        print("Error with requirements.txt, falling back to manual installation...")
        
        # Install base requirements without problematic markers
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "gradio>=3.40.1,<5.0.0", "biopython>=1.81,<2.0.0", "plotly>=5.14.1,<6.0.0",
            "pandas>=2.0.0,<3.0.0", "numpy>=1.24.0,<2.0.0", "psutil>=5.9.0,<6.0.0",
            "Pillow>=9.0.0,<10.0.0", "matplotlib>=3.5.0,<4.0.0", "requests>=2.28.0,<3.0.0",
            "packaging>=21.0,<24.0", "tqdm>=4.64.0,<5.0.0",
            "--no-cache-dir", "--upgrade"
        ], check=True)
        
        # Install platform-specific packages
        if sys.platform == "win32":
            subprocess.run([
                sys.executable, "-m", "pip", "install", "pywin32>=305",
                "--no-cache-dir", "--upgrade"
            ], check=True)
        elif sys.platform == "darwin":
            subprocess.run([
                sys.executable, "-m", "pip", "install", "pyobjc-framework-Cocoa>=9.0",
                "--no-cache-dir", "--upgrade"
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
