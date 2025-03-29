#!/usr/bin/env python3
"""
Verification script for MUSCLE5 Sequence Alignment Tool
Checks if everything is set up correctly
"""

import os
import sys
import platform
import subprocess
import importlib

def check_mark(condition):
    """Return a check mark or X based on condition"""
    return "✅" if condition else "❌"

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def check_muscle():
    """Check if MUSCLE5 is installed and accessible"""
    if not os.path.exists("muscle_config.txt"):
        return False, None
        
    with open("muscle_config.txt", "r") as f:
        muscle_path = f.read().strip()
        
    if not os.path.exists(muscle_path):
        return False, muscle_path
        
    try:
        result = subprocess.run([muscle_path, "-version"], 
                               capture_output=True, text=True,
                               timeout=5)
        if result.returncode == 0:
            return True, muscle_path
    except Exception:
        pass
        
    return False, muscle_path

def main():
    """Run verification checks"""
    print("\n=== MUSCLE5 Sequence Alignment Tool: System Verification ===\n")
    
    # 1. Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    python_ok = sys.version_info.major == 3 and sys.version_info.minor >= 8
    print(f"{check_mark(python_ok)} Python version: {python_version}")
    
    # 2. Check required packages
    packages = ["gradio", "numpy", "biopython"]
    for package in packages:
        has_package = check_package(package)
        print(f"{check_mark(has_package)} {package} package")
    
    # 3. Check MUSCLE5
    muscle_ok, muscle_path = check_muscle()
    print(f"{check_mark(muscle_ok)} MUSCLE5 executable", end="")
    if muscle_path:
        print(f": {muscle_path}")
    else:
        print()
    
    # 4. Check if we're in Codespaces
    in_codespaces = "CODESPACES" in os.environ or "CODESPACE_NAME" in os.environ
    print(f"{check_mark(True)} Running in Codespaces: {'Yes' if in_codespaces else 'No'}")
    
    # Summary
    all_ok = python_ok and all(check_package(pkg) for pkg in packages) and muscle_ok
    print("\n" + "=" * 60)
    
    if all_ok:
        print("✨ Everything looks good! You can run the application with:")
        print("\n   python launch.py\n")
    else:
        print("⚠️ Some issues were detected. Try running:")
        print("\n   python setup_muscle.py --force")
        print("   pip install -r requirements.txt")
        print("   python launch.py\n")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
