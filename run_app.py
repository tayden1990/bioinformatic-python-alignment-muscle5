import os
import sys
import tempfile
import subprocess
import platform
import webbrowser
import time
import threading
import gradio as gr
from app import create_ui, check_and_setup_muscle

def is_frozen():
    """Check if the application is running as a PyInstaller frozen executable"""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def get_base_dir():
    """Get the base directory for the application, works for both script and frozen exe"""
    if is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def create_startup_message():
    """Create a simple startup message with ASCII art"""
    ascii_art = """
    __  ___                __     ______     _____                                  
   /  |/  /_  _________  / /__  / ____/____/ ___/___  _____  __  _____ ____  ______
  / /|_/ / / / / ___/ _ \/ / _ \/___ \/ ___/\__ \/ _ \/ __ \/ / / / _ \_  / / / / /
 / /  / / /_/ (__  )  __/ /  __/___/ / /__ ___/ /  __/ / / / /_/ /  __// /_/ /_/ / 
/_/  /_/\__,_/____/\___/_/\___/_____/\___//____/\___/_/ /_/\__, /\___/___/\__, /  
                                                          /____/         /____/   
    """
    
    message = f"{ascii_art}\n"
    message += "Muscle5 Sequence Alignment Tool is starting...\n"
    message += "A browser window should open automatically.\n\n"
    message += "If it doesn't, please navigate to: http://127.0.0.1:7860\n\n"
    message += "To stop the application, close this window or press Ctrl+C\n"
    
    return message

def open_browser():
    """Open browser after a short delay"""
    def _open_browser():
        time.sleep(2)  # Allow Gradio server to start
        webbrowser.open('http://127.0.0.1:7860')
    
    thread = threading.Thread(target=_open_browser)
    thread.daemon = True
    thread.start()

def main():
    # Change working directory to the correct location if frozen
    if is_frozen():
        os.chdir(get_base_dir())
    
    # Create and print startup message
    print(create_startup_message())
    
    # Check if MUSCLE5 is available
    muscle_setup_success = check_and_setup_muscle()
    if not muscle_setup_success:
        print("\nWARNING: MUSCLE5 executable not found or invalid.")
        print("You will need to configure it from within the application.")
    
    # Open browser automatically
    open_browser()
    
    # Create and start the Gradio interface
    app = create_ui()
    app.launch(share=True, inbrowser=False)

if __name__ == "__main__":
    main()
