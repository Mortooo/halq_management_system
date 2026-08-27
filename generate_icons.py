import os
from PIL import Image, ImageDraw, ImageFont

ICONS_DIR = r"d:\Projects\Halaqa_managment_system\Galaxy\halq_management_system\static\icons"
os.makedirs(ICONS_DIR, exist_ok=True)

def draw_quran_icon(size):
    img = Image.new("RGBA", (size, size), (6, 95, 70, 255)) # Emerald-800
    draw = ImageDraw.Draw(img)
    
    # Border & circles
    margin = size // 10
    draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=size//6, fill=(4, 120, 87, 255), outline=(254, 240, 138, 120), width=max(2, size//60))
    
    # Book / Quran symbol geometry
    cx, cy = size // 2, size // 2
    w = size // 3
    h = size // 4
    
    # Left page
    draw.polygon([
        (cx - 4, cy - h),
        (cx - w, cy - h + 15),
        (cx - w, cy + h),
        (cx - 4, cy + h - 15)
    ], fill=(254, 240, 138, 255), outline=(245, 158, 11, 255))
    
    # Right page
    draw.polygon([
        (cx + 4, cy - h),
        (cx + w, cy - h + 15),
        (cx + w, cy + h),
        (cx + 4, cy + h - 15)
    ], fill=(254, 240, 138, 255), outline=(245, 158, 11, 255))
    
    # Spine center line
    draw.line([(cx, cy - h), (cx, cy + h - 15)], fill=(180, 83, 9, 255), width=max(2, size//80))
    
    return img

def create_screenshot(width, height, is_mobile=False):
    img = Image.new("RGBA", (width, height), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)
    
    # Top navbar
    draw.rectangle([0, 0, width, height // 10], fill=(6, 95, 70, 255))
    
    # Hero section
    draw.rectangle([0, height // 10, width, height // 2], fill=(4, 120, 87, 255))
    
    # Text / Card placeholders
    cx, cy = width // 2, height // 4
    draw.rounded_rectangle([cx - width//3, cy - 20, cx + width//3, cy + 20], radius=10, fill=(254, 240, 138, 240))
    
    # Cards
    card_y = int(height * 0.55)
    draw.rounded_rectangle([width//10, card_y, width - width//10, height - height//10], radius=16, fill=(255, 255, 255, 255), outline=(229, 231, 235, 255), width=3)
    
    return img

# Generate all required icons
draw_quran_icon(192).save(os.path.join(ICONS_DIR, "icon-192.png"))
draw_quran_icon(512).save(os.path.join(ICONS_DIR, "icon-512.png"))
draw_quran_icon(512).save(os.path.join(ICONS_DIR, "icon-maskable.png"))

# Generate screenshots
create_screenshot(1280, 720, False).save(os.path.join(ICONS_DIR, "screenshot-desktop.png"))
create_screenshot(720, 1280, True).save(os.path.join(ICONS_DIR, "screenshot-mobile.png"))

print("Successfully generated PNG icons and screenshots!")
