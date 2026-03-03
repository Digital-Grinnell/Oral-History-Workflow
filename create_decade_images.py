#!/usr/bin/env python3
"""
Create decade-specific images (1940s-2020s) from a base image.
Superimposes decade text over the center with varying color schemes.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Define decades and their accent colors
DECADES = [
    ("1940's", "#81312F"),  # dark red
    ("1950's", "#FF8F1C"),  # orange
    ("1960's", "#FFE1A0"),  # light yellow
    ("1970's", "#006A52"),  # dark green
    ("1980's", "#00B388"),  # teal/green
    ("1990's", "#DAF6D0"),  # light green
    ("2000's", "#003B5C"),  # dark blue
    ("2010's", "#418FDE"),  # light blue
    ("2020's", "#3F2A56"),  # dark purple
]

RED_COLOR = "#DA291C"
BLACK_COLOR = "#000000"

def get_contrasting_text_color(bg_color):
    """Determine if text should be black or red based on background brightness."""
    # Convert hex to RGB
    r = int(bg_color[1:3], 16)
    g = int(bg_color[3:5], 16)
    b = int(bg_color[5:7], 16)
    
    # Calculate brightness (perception-based formula)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    
    # Return black for light backgrounds, red for dark backgrounds
    return BLACK_COLOR if brightness > 180 else RED_COLOR

def create_decade_image(base_image_path, decade_text, accent_color, output_path):
    """Create a decade-specific image with text overlay."""
    
    # Open the base image
    img = Image.open(base_image_path).convert("RGBA")
    width, height = img.size
    
    # Create a transparent overlay for text
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Try to load a font, fall back to default if not available
    try:
        # Try different common font locations
        font_size = int(height * 0.15)  # 15% of image height
        font_paths = [
            "/System/Library/Fonts/Supplemental/Impact.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                break
        
        if font is None:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
    
    # Calculate text position (center of image)
    # Get preliminary bbox to calculate dimensions
    temp_bbox = draw.textbbox((0, 0), decade_text, font=font)
    text_width = temp_bbox[2] - temp_bbox[0]
    text_height = temp_bbox[3] - temp_bbox[1]
    
    # Calculate centered position
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Get actual bbox at the drawing position for accurate background
    actual_bbox = draw.textbbox((x, y), decade_text, font=font)
    
    # Determine text color based on accent color
    text_color = get_contrasting_text_color(accent_color)
    
    # Create semi-transparent background for text using accent color
    padding = 30
    bg_rect = [
        actual_bbox[0] - padding,
        actual_bbox[1] - padding,
        actual_bbox[2] + padding,
        actual_bbox[3] + padding
    ]
    
    # Convert hex to RGBA with transparency
    r = int(accent_color[1:3], 16)
    g = int(accent_color[3:5], 16)
    b = int(accent_color[5:7], 16)
    bg_color_rgba = (r, g, b, 200)  # 200/255 opacity
    
    # Draw rounded rectangle background
    draw.rounded_rectangle(bg_rect, radius=20, fill=bg_color_rgba)
    
    # Draw text with outline for better visibility
    outline_width = 3
    for adj_x in range(-outline_width, outline_width + 1):
        for adj_y in range(-outline_width, outline_width + 1):
            if adj_x != 0 or adj_y != 0:
                outline_color = BLACK_COLOR if text_color == RED_COLOR else "#FFFFFF"
                draw.text((x + adj_x, y + adj_y), decade_text, font=font, fill=outline_color)
    
    # Draw main text
    draw.text((x, y), decade_text, font=font, fill=text_color)
    
    # Composite the overlay onto the original image
    result = Image.alpha_composite(img, overlay)
    
    # Convert back to RGB for saving as JPEG
    result_rgb = result.convert("RGB")
    result_rgb.save(output_path, "JPEG", quality=95)
    print(f"Created: {output_path}")

def main():
    """Generate all decade images."""
    base_image = "oral-history-base.jpg"
    output_dir = "decade-images"
    
    if not os.path.exists(base_image):
        print(f"Error: Base image '{base_image}' not found.")
        print("Please save the provided image as 'oral-history-base.jpg' in this directory.")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating decade images...")
    for decade, accent_color in DECADES:
        output_filename = decade.replace("'", "") + ".jpg"
        output_path = os.path.join(output_dir, output_filename)
        create_decade_image(base_image, decade, accent_color, output_path)
    
    print(f"\nAll {len(DECADES)} decade images created successfully!")
    print(f"Images saved in: {output_dir}/")

if __name__ == "__main__":
    main()
