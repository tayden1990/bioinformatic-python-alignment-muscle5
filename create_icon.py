from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Create a simple icon for the application"""
    # Create a 256x256 image with transparent background
    img = Image.new('RGBA', (256, 256), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a circle background
    draw.ellipse((16, 16, 240, 240), fill=(0, 100, 200, 255))
    
    # Draw a DNA-like symbol
    for i in range(5):
        # Calculate position
        y_offset = 20 * i
        
        # Draw first horizontal line
        draw.line((64, 84 + y_offset, 192, 84 + y_offset), 
                 fill=(255, 255, 255, 255), width=8)
        
        # Draw second horizontal line
        draw.line((64, 172 - y_offset, 192, 172 - y_offset), 
                 fill=(255, 255, 255, 255), width=8)
        
        # Draw connectors between lines
        if i % 2 == 0:
            draw.line((80 + 30 * i, 84 + y_offset, 110 + 30 * i, 172 - y_offset), 
                     fill=(0, 255, 0, 255), width=6)
        else:
            draw.line((80 + 30 * i, 172 - y_offset, 110 + 30 * i, 84 + y_offset), 
                     fill=(255, 100, 0, 255), width=6)
    
    # Draw text "M5" for Muscle5
    try:
        # Try to find a font that works on most systems
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        # Fall back to default font
        font = ImageFont.load_default()
    
    # Add the text at the bottom
    draw.text((100, 190), "M5", fill=(255, 255, 255, 255), font=font)
    
    # Save as PNG and ICO
    img.save('icon.png')
    
    # Convert to ICO format (for Windows)
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save('icon.ico', sizes=sizes)
    
    print(f"Icon created: {os.path.abspath('icon.ico')}")
    return os.path.abspath('icon.ico')

if __name__ == "__main__":
    create_app_icon()
