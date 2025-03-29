#!/usr/bin/env python3
"""
Diagnostic tool for checking GitHub Codespaces compatibility and debugging issues.
Run this script to verify your environment and identify potential problems.
"""

import os
import sys
import platform
import subprocess
import importlib.util
import json
import socket
from datetime import datetime

def print_header(text):
    """Print a section header with formatting"""
    print("\n" + "=" * 80)
    print(f" {text}")
    print("=" * 80)

def is_codespaces():
    """Check if running in GitHub Codespaces environment"""
    return "CODESPACES" in os.environ or "CODESPACE_NAME" in os.environ or "MUSCLE5_CODESPACES_MODE" in os.environ

def check_network_port(port=7860):
    """Check if the specified port is available or in use"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", port))
            return True, None
    except socket.error as e:
        return False, str(e)

def get_package_version(package_name):
    """Get the version of an installed package"""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            return None
        
        package = importlib.import_module(package_name)
        return getattr(package, "__version__", "Unknown version")
    except ImportError:
        return None

def check_muscle5():
    """Check if MUSCLE5 is installed and accessible."""
    status = {"installed": False, "path": None, "version": None, "error": None}
    
    try:
        # Check if config file exists
        if not os.path.exists("muscle_config.txt"):
            status["error"] = "Config file not found"
            return status
            
        # Read the path from config file
        with open("muscle_config.txt", "r") as f:
            muscle_path = f.read().strip()
        
        status["path"] = muscle_path
        
        # Check if the file exists
        if not os.path.exists(muscle_path):
            # Try to find muscle5 in PATH
            try:
                result = subprocess.run(["muscle5", "-version"], capture_output=True, check=False, text=True)
                if result.returncode == 0:
                    status["installed"] = True
                    status["path"] = "muscle5"
                    status["version"] = result.stdout.strip()
                else:
                    status["error"] = "Found in PATH but execution failed"
            except FileNotFoundError:
                status["error"] = "Not found in PATH"
        else:
            # Check if it's runnable
            try:
                result = subprocess.run([muscle_path, "-version"], capture_output=True, check=False, text=True)
                if result.returncode == 0:
                    status["installed"] = True
                    status["version"] = result.stdout.strip()
                else:
                    status["error"] = f"Execution failed: {result.stderr.strip()}"
            except Exception as e:
                status["error"] = str(e)
    except Exception as e:
        status["error"] = str(e)
    
    return status

def check_environment_variables():
    """Check for Codespaces environment variables"""
    codespaces_vars = {}
    relevant_vars = [
        "CODESPACES", "CODESPACE_NAME", "GITHUB_CODESPACES", 
        "CODESPACES_PORT", "GITHUB_USER", "GITHUB_SERVER_URL",
        "MUSCLE5_CODESPACES_MODE"
    ]
    
    for var in relevant_vars:
        if var in os.environ:
            codespaces_vars[var] = os.environ[var]
    
    return codespaces_vars

def check_gradio():
    """Check Gradio installation and compatibility"""
    status = {"installed": False, "version": None, "compatible": False, "error": None}
    
    try:
        gradio_spec = importlib.util.find_spec("gradio")
        if gradio_spec:
            import gradio as gr
            status["installed"] = True
            status["version"] = gr.__version__
            
            gradio_version = gr.__version__.split('.')
            major_version = int(gradio_version[0])
            
            # Check compatibility with Codespaces
            if major_version >= 4:
                status["compatible"] = True
            elif major_version == 3:
                status["compatible"] = True
                status["note"] = "Compatible but older version"
            else:
                status["compatible"] = False
                status["error"] = "Gradio version too old for reliable Codespaces operation"
        else:
            status["error"] = "Gradio not installed"
    except Exception as e:
        status["error"] = str(e)
        
    return status

def print_diagnostic_result(title, result, success_indicator=None):
    """Print a diagnostic result with formatting"""
    if isinstance(result, dict):
        print(f"\n{title}:")
        
        # Determine status indicator
        if success_indicator is not None:
            status = success_indicator
        elif "installed" in result and result["installed"]:
            status = "✅"
        elif "error" in result and result["error"]:
            status = "❌"
        else:
            status = "⚠️"
            
        print(f"{status} ", end="")
        
        # Print details
        for key, value in result.items():
            if value is not None and key != "installed":
                print(f"{key}: {value}")
    else:
        print(f"\n{title}: {result}")

def print_env_var_instructions():
    """Print platform-specific instructions for setting environment variables"""
    system = platform.system()
    print("\nTo simulate Codespaces environment locally:")
    
    if system == "Windows":
        print("\nIn Command Prompt:")
        print("   set MUSCLE5_CODESPACES_MODE=1")
        print("\nIn PowerShell:")
        print("   $env:MUSCLE5_CODESPACES_MODE = 1")
        print("\nTo set permanently in PowerShell:")
        print("   [Environment]::SetEnvironmentVariable('MUSCLE5_CODESPACES_MODE', '1', 'User')")
    elif system == "Darwin":  # macOS
        print("\nIn Terminal (bash/zsh):")
        print("   export MUSCLE5_CODESPACES_MODE=1")
        print("\nTo set permanently, add to ~/.zshrc or ~/.bash_profile:")
        print("   echo 'export MUSCLE5_CODESPACES_MODE=1' >> ~/.zshrc")
    else:  # Linux and others
        print("\nIn Terminal (bash):")
        print("   export MUSCLE5_CODESPACES_MODE=1")
        print("\nTo set permanently, add to ~/.bashrc:")
        print("   echo 'export MUSCLE5_CODESPACES_MODE=1' >> ~/.bashrc")
    
    print("\nAfter setting the environment variable, restart your terminal or run:")
    if system == "Windows":
        print("   python codespaces_diagnostics.py")
    else:
        print("   python3 codespaces_diagnostics.py")

def run_diagnostics():
    """Run all diagnostics and print results"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_header("MUSCLE5 CODESPACES DIAGNOSTICS")
    
    # Basic information
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {platform.python_version()}")
    print(f"System: {platform.system()} {platform.release()} {platform.machine()}")
    
    # Check if running in Codespaces
    in_codespaces = is_codespaces()
    print_diagnostic_result("Running in GitHub Codespaces", 
                           "Yes" if in_codespaces else "No", 
                           "✅" if in_codespaces else "⚠️")
    
    # Check environment variables
    env_vars = check_environment_variables()
    print_diagnostic_result("Codespaces Environment Variables", 
                           env_vars if env_vars else "None found",
                           "✅" if env_vars else "⚠️")
    
    # Check Gradio
    gradio_status = check_gradio()
    print_diagnostic_result("Gradio Status", gradio_status)
    
    # Check MUSCLE5
    muscle_status = check_muscle5()
    print_diagnostic_result("MUSCLE5 Status", muscle_status)
    
    # Check port availability
    port_available, port_error = check_network_port(7860)
    print_diagnostic_result("Port 7860 Available", 
                           "Yes" if port_available else f"No - {port_error}",
                           "✅" if port_available else "❌")
    
    # Check other dependencies
    print("\nOther Dependencies:")
    for package in ["numpy", "scipy", "matplotlib", "requests", "biopython"]:
        version = get_package_version(package)
        print(f"{'✅' if version else '❌'} {package}: {version if version else 'Not installed'}")
    
    # Provide troubleshooting advice
    print_header("TROUBLESHOOTING ADVICE")
    
    if not in_codespaces:
        print("\n⚠️ Not running in GitHub Codespaces environment")
        print_env_var_instructions()
    
    if not gradio_status["installed"] or not gradio_status["compatible"]:
        print("\n❌ Gradio issues detected")
        print("   - Install/update with: pip install -U gradio")
        print("   - For Codespaces compatibility, use Gradio 3.x or 4.x")
    
    if not muscle_status["installed"]:
        print("\n❌ MUSCLE5 not properly installed or configured")
        print("   - Run: python setup_muscle.py --force")
        print("   - Check permissions: chmod +x <muscle_path>")
    
    if not port_available:
        print("\n❌ Port 7860 is already in use")
        if platform.system() == "Windows":
            print("   - Find and stop the process: Get-Process -Id (Get-NetTCPConnection -LocalPort 7860).OwningProcess")
            print("   - Alternative: Restart computer or use a different port")
        else:
            print("   - Stop other running instances: pkill -f 'python app.py'")
            print("   - Find process using: lsof -i :7860")
        print("   - Or modify the port number in app.py or codespaces_start.py")
    
    # Full startup instructions
    print_header("STARTUP INSTRUCTIONS")
    
    print("\nTo properly start the application in Codespaces:")
    print("1. Run: python codespaces_start.py")
    print("2. Look for the public URL in the terminal output")
    print("3. Open the URL in a browser, or use the 'Open in Browser' button in PORTS tab")
    
    print("\nIf issues persist:")
    print("1. Check GITHUB_CODESPACES.md for troubleshooting steps")
    print("2. Run: python setup_muscle.py --force && python codespaces_start.py")
    print("3. If only a basic page appears, use 'Open in Browser' from PORTS tab")

def main():
    """Main function"""
    run_diagnostics()
    return 0

if __name__ == "__main__":
    sys.exit(main())
