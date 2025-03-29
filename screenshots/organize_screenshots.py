#!/usr/bin/env python3
"""
Screenshot Organization Tool

This script helps organize screenshots in the repository by:
1. Renaming files according to naming conventions
2. Optimizing image sizes
3. Generating thumbnails for README preview
4. Updating the screenshots README.md
"""

import os
import re
from pathlib import Path
import argparse
from datetime import datetime
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("WARNING: Pillow library not found. Image optimization will be skipped.")
    print("Install with: pip install Pillow")

# Constants
MAX_IMAGE_WIDTH = 1200  # Maximum width for full-size images
THUMB_WIDTH = 400       # Width for thumbnails
SCREENSHOTS_DIR = Path(__file__).parent

def create_thumbnail(image_path, quality=85):
    """Create a thumbnail version of an image"""
    if not PILLOW_AVAILABLE:
        return None
    
    thumb_path = image_path.parent / f"{image_path.stem}_thumb{image_path.suffix}"
    
    try:
        with Image.open(image_path) as img:
            # Calculate aspect ratio
            width, height = img.size
            aspect = height / width
            new_height = int(THUMB_WIDTH * aspect)
            
            # Resize image
            resized = img.resize((THUMB_WIDTH, new_height), Image.Resampling.LANCZOS)
            
            # Save with optimized quality
            resized.save(thumb_path, optimize=True, quality=quality)
            print(f"Created thumbnail: {thumb_path}")
            
            return thumb_path
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        return None

def optimize_image(image_path, quality=85):
    """Optimize image size while maintaining quality"""
    if not PILLOW_AVAILABLE:
        return
    
    try:
        with Image.open(image_path) as img:
            # Check if resizing is needed
            width, height = img.size
            if width > MAX_IMAGE_WIDTH:
                aspect = height / width
                new_height = int(MAX_IMAGE_WIDTH * aspect)
                img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)
                print(f"Resized image from {width}x{height} to {MAX_IMAGE_WIDTH}x{new_height}")
            
            # Save with optimized quality
            img.save(image_path, optimize=True, quality=quality)
            print(f"Optimized: {image_path}")
    except Exception as e:
        print(f"Error optimizing {image_path}: {e}")

def normalize_filename(filename):
    """Convert filename to lowercase with underscores"""
    # Remove file extension
    name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1].lower()
    
    # Replace spaces and hyphens with underscores
    name = name.replace(' ', '_').replace('-', '_')
    
    # Remove any special characters
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    
    # Convert to lowercase
    name = name.lower()
    
    # Add extension back
    return f"{name}{ext}"

def rename_screenshots():
    """Rename all screenshots according to naming convention"""
    renamed_files = []
    
    for file in os.listdir(SCREENSHOTS_DIR):
        # Skip Python files and directories
        if file.endswith('.py') or file == 'README.md' or os.path.isdir(os.path.join(SCREENSHOTS_DIR, file)):
            continue
            
        # Check if file is an image
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            old_path = os.path.join(SCREENSHOTS_DIR, file)
            new_filename = normalize_filename(file)
            new_path = os.path.join(SCREENSHOTS_DIR, new_filename)
            
            # Skip if already normalized
            if old_path == new_path:
                continue
                
            # Check if destination exists
            if os.path.exists(new_path):
                print(f"Skipping {file}: Destination {new_filename} already exists")
                continue
                
            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {file} -> {new_filename}")
            renamed_files.append((file, new_filename))
    
    return renamed_files

def update_screenshots_readme():
    """Update the screenshots README.md with current screenshots"""
    readme_path = os.path.join(SCREENSHOTS_DIR, "README.md")
    
    # Get list of screenshots
    screenshots = []
    for file in os.listdir(SCREENSHOTS_DIR):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Skip thumbnail files
            if "_thumb" in file:
                continue
            screenshots.append(file)
    
    # Group screenshots by type
    ui_screenshots = [s for s in screenshots if any(kw in s for kw in ['app', 'ui', 'screen', 'interface', 'window'])]
    env_screenshots = [s for s in screenshots if any(kw in s for kw in ['env', 'setup', 'install', 'config', 'windows', 'mac', 'linux'])]
    other_screenshots = [s for s in screenshots if s not in ui_screenshots and s not in env_screenshots]
    
    # Backup existing README if it exists
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            old_content = f.read()
        backup_path = f"{readme_path}.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        with open(backup_path, 'w') as f:
            f.write(old_content)
        print(f"Created backup of README at {backup_path}")
    
    # Build new README content
    content = """# Screenshots Gallery

This directory contains screenshots of the application's UI and various environments.

## UI Screenshots

"""
    
    for s in sorted(ui_screenshots):
        desc = s.replace('_', ' ').replace('.png', '').replace('.jpg', '').title()
        content += f"- `{s}` - {desc}\n"
    
    content += "\n## Environment Screenshots\n\n"
    
    for s in sorted(env_screenshots):
        desc = s.replace('_', ' ').replace('.png', '').replace('.jpg', '').title()
        content += f"- `{s}` - {desc}\n"
    
    if other_screenshots:
        content += "\n## Other Screenshots\n\n"
        for s in sorted(other_screenshots):
            desc = s.replace('_', ' ').replace('.png', '').replace('.jpg', '').title()
            content += f"- `{s}` - {desc}\n"
    
    content += """
## Adding New Screenshots

To add new screenshots:
1. Place them in this directory
2. Update this README.md file
3. Reference them in the main repository README.md as needed

Example markdown to include a screenshot in documentation:
```markdown
![Screenshot description](screenshots/screenshot_name.png)
```

## Naming Convention

Please follow this naming convention for screenshots:
- Use lowercase letters and underscores
- Use descriptive names that indicate content
- Include platform/environment information when relevant
- Example: `windows_muscle_config.png`
"""
    
    # Write new README
    with open(readme_path, 'w') as f:
        f.write(content)
    
    print(f"Updated {readme_path} with {len(screenshots)} screenshots")

def main():
    parser = argparse.ArgumentParser(description="Organize repository screenshots")
    parser.add_argument("--rename", action="store_true", help="Rename screenshots to follow naming convention")
    parser.add_argument("--optimize", action="store_true", help="Optimize image sizes")
    parser.add_argument("--thumbnails", action="store_true", help="Generate thumbnails")
    parser.add_argument("--update-readme", action="store_true", help="Update screenshots README.md")
    parser.add_argument("--all", action="store_true", help="Perform all operations")
    
    args = parser.parse_args()
    
    # If no args provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Process based on arguments
    if args.rename or args.all:
        rename_screenshots()
    
    if args.optimize or args.all:
        if PILLOW_AVAILABLE:
            for file in os.listdir(SCREENSHOTS_DIR):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    optimize_image(os.path.join(SCREENSHOTS_DIR, file))
        else:
            print("Image optimization skipped: Pillow library not available")
    
    if args.thumbnails or args.all:
        if PILLOW_AVAILABLE:
            for file in os.listdir(SCREENSHOTS_DIR):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')) and not "_thumb" in file:
                    create_thumbnail(Path(SCREENSHOTS_DIR) / file)
        else:
            print("Thumbnail generation skipped: Pillow library not available")
    
    if args.update_readme or args.all:
        update_screenshots_readme()
    
    print("Screenshot organization completed!")

if __name__ == "__main__":
    main()
