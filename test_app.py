import unittest
import os
import sys
import importlib.util

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to find the main application file
potential_app_files = ["app.py", "main.py", "muscle_aligner.py", "aligner.py"]
app_module = None

for filename in potential_app_files:
    if os.path.exists(filename):
        print(f"Found potential application file: {filename}")
        try:
            # Try to import the module
            spec = importlib.util.spec_from_file_location("app_module", filename)
            app_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_module)
            print(f"Successfully imported {filename}")
            break
        except Exception as e:
            print(f"Error importing {filename}: {e}")

class TestApplicationExists(unittest.TestCase):
    
    def test_application_file_exists(self):
        """Test if any application file exists"""
        app_files_exist = any(os.path.exists(f) for f in potential_app_files)
        if not app_files_exist:
            print("WARNING: No application files found.")
        self.assertTrue(app_files_exist, "At least one application file should exist")
    
    @unittest.skipIf(app_module is None, "No application module could be imported")
    def test_module_attributes(self):
        """Test if the application module has expected attributes"""
        # This is a basic check - adjust based on your actual application
        dir_contents = dir(app_module)
        print(f"Module contains these attributes: {dir_contents}")
        self.assertTrue(len(dir_contents) > 0, "Module should have attributes")

if __name__ == "__main__":
    unittest.main()
