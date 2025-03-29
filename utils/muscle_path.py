"""Utility module for handling MUSCLE5 executable path detection and validation."""

import os
import platform
import subprocess
from pathlib import Path

def get_default_muscle_path():
    """Returns the default muscle path based on operating system"""
    if platform.system() == "Windows":
        # Check common Windows locations
        paths = [
            os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "muscle", "muscle.exe"),
            os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), "muscle", "muscle.exe"),
            "muscle.exe",  # If in PATH or current directory
            "muscle-win64.v5.3.exe"  # Common downloaded name
        ]
    elif platform.system() == "Darwin":  # macOS
        paths = [
            "/usr/local/bin/muscle",
            "/opt/homebrew/bin/muscle",
            "muscle"  # If in PATH or current directory
        ]
    else:  # Linux and others
        paths = [
            "/usr/bin/muscle",
            "/usr/local/bin/muscle",
            "muscle"  # If in PATH or current directory
        ]
    
    # Check if any path exists
    for path in paths:
        if os.path.exists(path):
            return path
    
    # Return a default that will be checked later
    return "muscle"

def get_configured_muscle_path():
    """
    Get the MUSCLE5 path from configuration file or environment
    
    Returns:
        Path to MUSCLE5 executable
    """
    # First check configuration file
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "muscle_config.txt")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                muscle_path = f.read().strip()
                if os.path.exists(muscle_path):
                    return muscle_path
        except:
            pass
    
    # Then check environment variable
    muscle_path = os.environ.get("MUSCLE5_PATH")
    if muscle_path and os.path.exists(muscle_path):
        return muscle_path
    
    # Finally use default path
    return get_default_muscle_path()

def validate_muscle_executable(executable_path):
    """
    Validates that the provided path is a valid MUSCLE5 executable
    
    Args:
        executable_path: Path to the potential MUSCLE5 executable
    
    Returns:
        Tuple of (is_valid, message)
    """
    if not os.path.exists(executable_path):
        return False, f"File does not exist: {executable_path}"
    
    if not os.access(executable_path, os.X_OK) and not executable_path.endswith('.exe'):
        return False, f"File is not executable: {executable_path}"
    
    try:
        # Try running with -version to see if it's actually MUSCLE
        process = subprocess.run(
            [executable_path, "-version"], 
            capture_output=True, 
            text=True,
            check=False,
            timeout=3  # Add a timeout to avoid hanging
        )
        
        # Check for common MUSCLE version strings in output
        output = process.stdout + process.stderr
        if "MUSCLE" in output or "muscle" in output:
            return True, f"Valid MUSCLE executable detected: {os.path.basename(executable_path)}"
        else:
            return False, f"File does not appear to be a MUSCLE executable: {executable_path}"
    
    except Exception as e:
        return False, f"Error validating executable: {str(e)}"

def save_muscle_path(path):
    """
    Save the MUSCLE5 path to configuration file
    
    Args:
        path: Path to MUSCLE5 executable
    
    Returns:
        True if successful, False otherwise
    """
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "muscle_config.txt")
        with open(config_path, "w") as f:
            f.write(path)
        return True
    except:
        return False
