import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# Create screenshots directory if it doesn't exist
screenshots_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(screenshots_dir, exist_ok=True)

# Create a placeholder screenshot for README
def create_placeholder_screenshot():
    # Create a blank image
    width, height = 800, 500
    image = Image.new('RGB', (width, height), color=(245, 245, 245))
    draw = ImageDraw.Draw(image)
    
    # Add some text
    text = "Muscle5 Tool Screenshot"
    try:
        # Try to find a font that works on most systems
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        # Fall back to default font
        font = ImageFont.load_default()
    
    text_width = draw.textlength(text, font=font) if hasattr(draw, 'textlength') else 400
    text_position = ((width - text_width) // 2, 150)
    draw.text(text_position, text, fill=(60, 60, 60), font=font)
    
    # Add a placeholder for DNA visualization
    draw.rectangle([(100, 250), (700, 400)], outline=(0, 120, 200), width=2)
    for i in range(5):
        y = 270 + i * 25
        draw.line([(120, y), (680, y)], fill=(0, 120, 200), width=1)
        
        # Add some colored circles to represent nucleotides
        colors = [(0, 170, 0), (0, 0, 200), (255, 160, 0), (200, 0, 0)]
        for j in range(20):
            x = 120 + j * 30
            color_idx = (i + j) % 4
            draw.ellipse([(x-5, y-5), (x+5, y+5)], fill=colors[color_idx])
    
    # Save the image
    screenshot_path = os.path.join(screenshots_dir, "app_screenshot.png")
    image.save(screenshot_path)
    print(f"Created placeholder screenshot at {screenshot_path}")
    return screenshot_path

if __name__ == "__main__":
    screenshot_path = create_placeholder_screenshot()
    
    # Display the image if running interactively
    try:
        img = plt.imread(screenshot_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    except:
        pass
