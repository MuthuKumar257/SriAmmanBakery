import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

os.makedirs('public/beans', exist_ok=True)
os.makedirs('public/frames', exist_ok=True)

# -------------------------------------------------------------------
# Helper: create metallic brass gradient
# -------------------------------------------------------------------
def brass_color(factor=1.0):
    # Base brass: #e6bf7a -> (230, 191, 122)
    r = int(min(255, max(0, 230 * factor)))
    g = int(min(255, max(0, 191 * factor)))
    b = int(min(255, max(0, 122 * factor)))
    return (r, g, b)

# -------------------------------------------------------------------
# 1. GENERATE BEANS / GARNISHES (public/beans/1.png to 6.png)
# -------------------------------------------------------------------
def generate_garnishes():
    print("Generating garnishes (dry fruits)...")
    
    # 1. Pistachio (Whole / Shelled Royal Pista)
    img = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Shell base
    d.ellipse([50, 40, 270, 280], fill=(225, 205, 170, 255))
    # Pistachio nut inside
    d.ellipse([80, 50, 240, 270], fill=(110, 155, 60, 255))
    d.ellipse([95, 70, 225, 250], fill=(135, 185, 70, 255))
    # Purple/brown skin blush
    d.ellipse([75, 120, 140, 220], fill=(130, 75, 95, 200))
    # Highlight
    d.ellipse([130, 80, 190, 150], fill=(180, 220, 95, 230))
    # Texture lines
    for i in range(15):
        y = 70 + i * 11
        d.arc([85, y, 235, y + 25], 30, 150, fill=(85, 125, 45, 180), width=2)
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    img.save('public/beans/1.png', 'PNG')
    
    # 2. Cardamom Pod (Chhoti Elaichi)
    img = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Pod shape (pointed oval)
    points = [
        (160, 30), (210, 80), (230, 160), (210, 240),
        (160, 290), (110, 240), (90, 160), (110, 80)
    ]
    d.polygon(points, fill=(105, 145, 75, 255))
    # Cardamom ribbed ridges
    d.line([(160, 30), (160, 290)], fill=(160, 205, 110, 255), width=5)
    d.arc([105, 50, 215, 270], 100, 260, fill=(75, 115, 50, 200), width=4)
    d.arc([105, 50, 215, 270], 280, 80, fill=(145, 190, 95, 220), width=4)
    # Crown tips
    d.polygon([(155, 30), (160, 15), (165, 30)], fill=(80, 100, 50, 255))
    img = img.filter(ImageFilter.GaussianBlur(1.5))
    img.save('public/beans/2.png', 'PNG')

    # 3. Kashmiri Almond (Badam)
    img = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Almond shape (teardrop)
    points = [
        (160, 35), (225, 100), (235, 190), (195, 270),
        (160, 285), (125, 270), (85, 190), (95, 100)
    ]
    d.polygon(points, fill=(165, 95, 45, 255))
    # Grain and skin texture
    for i in range(12):
        y = 60 + i * 18
        d.arc([105, y, 215, y + 40], 20, 160, fill=(130, 65, 25, 200), width=3)
    # Highlight ridge
    d.arc([120, 60, 200, 260], 270, 90, fill=(215, 145, 80, 220), width=5)
    img = img.filter(ImageFilter.GaussianBlur(1.5))
    img.save('public/beans/3.png', 'PNG')

    # 4. Golden Boondi / Saffron Pearl
    img = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Glistening sphere
    d.ellipse([60, 60, 260, 260], fill=(235, 140, 20, 255))
    d.ellipse([75, 75, 245, 245], fill=(250, 175, 35, 255))
    # Ghee glaze specular highlight
    d.ellipse([110, 85, 185, 145], fill=(255, 235, 140, 240))
    d.ellipse([130, 95, 160, 120], fill=(255, 255, 230, 255))
    # Saffron speck
    d.line([(180, 150), (200, 170)], fill=(180, 30, 15, 255), width=3)
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    img.save('public/beans/4.png', 'PNG')

    # 5. Crescent Cashew (Kaju)
    img = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Kidney / crescent curve
    d.ellipse([70, 70, 230, 250], fill=(245, 235, 205, 255))
    d.ellipse([140, 100, 270, 220], fill=(0, 0, 0, 0)) # carve crescent
    # Golden roasted blush
    d.arc([80, 80, 220, 240], 90, 270, fill=(215, 175, 120, 230), width=24)
    # Specular gloss
    d.arc([95, 95, 205, 225], 110, 230, fill=(255, 255, 240, 255), width=6)
    img = img.filter(ImageFilter.GaussianBlur(1.5))
    img.save('public/beans/5.png', 'PNG')

    # 6. Melon Seed (Magaj)
    img = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    points = [
        (160, 45), (195, 120), (190, 220), (160, 275),
        (130, 220), (125, 120)
    ]
    d.polygon(points, fill=(235, 225, 195, 255))
    d.polygon([(158, 55), (175, 120), (170, 210), (158, 260), (146, 210), (145, 120)], fill=(255, 250, 230, 255))
    d.line([(160, 50), (160, 270)], fill=(210, 190, 150, 200), width=2)
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    img.save('public/beans/6.png', 'PNG')
    print("Garnishes generated successfully!")

# -------------------------------------------------------------------
# 2. GENERATE BRAND LOGO (public/logo.png)
# -------------------------------------------------------------------
def generate_logo():
    print("Generating brand logo...")
    # Target size matching reference logo: 862 x 688
    img = Image.new('RGBA', (862, 688), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Check if user's logo exists in Logo/
    user_logo_path = 'Logo/logoWithOutBackground.png'
    has_user_logo = os.path.exists(user_logo_path)
    
    if has_user_logo:
        try:
            user_img = Image.open(user_logo_path).convert('RGBA')
            bbox = user_img.getbbox()
            if bbox:
                user_img = user_img.crop(bbox)
            # Scale to fit upper half
            user_img.thumbnail((540, 360), Image.Resampling.LANCZOS)
            # Center on canvas
            x = (862 - user_img.width) // 2
            y = 60
            img.paste(user_img, (x, y), user_img)
        except Exception as e:
            print("Error loading user logo:", e)
            has_user_logo = False

    if not has_user_logo:
        # Draw royal crest / Kalash emblem
        cx, cy = 431, 200
        # Outer golden radiant rays
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            x1 = cx + math.cos(rad) * 90
            y1 = cy + math.sin(rad) * 90
            x2 = cx + math.cos(rad) * 115
            y2 = cy + math.sin(rad) * 115
            d.line([(x1, y1), (x2, y2)], fill=(230, 191, 122, 190), width=3)
        # Royal crown / Kalash
        d.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], outline=(230, 191, 122, 255), width=4)
        d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], outline=(150, 101, 42, 220), width=2)
        # Inner emblem
        d.polygon([(cx, cy - 50), (cx + 40, cy + 30), (cx - 40, cy + 30)], fill=(230, 191, 122, 240))
        d.ellipse([cx - 15, cy - 10, cx + 15, cy + 20], fill=(255, 235, 180, 255))
        d.ellipse([cx - 8, cy - 60, cx + 8, cy - 44], fill=(230, 191, 122, 255))

    # Add elegant typography for brand
    # Draw ornate divider line
    d.line([(231, 440), (631, 440)], fill=(230, 191, 122, 220), width=2)
    d.polygon([(431, 435), (436, 440), (431, 445), (426, 440)], fill=(230, 191, 122, 255))
    
    # Load fonts or render crisp lettering
    # We can draw high-quality vector-like serif lettering
    try:
        font_large = ImageFont.truetype("times.ttf", 68)
        font_sub = ImageFont.truetype("arial.ttf", 22)
    except:
        font_large = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    brand_text = "TRIPATHI LADDU"
    sub_text = "SHUDDH DESI GHEE SWEETS · EST. 2001"
    
    bbox1 = d.textbbox((0, 0), brand_text, font=font_large)
    w1 = bbox1[2] - bbox1[0]
    # Draw drop shadow
    d.text(((862 - w1) // 2 + 2, 472), brand_text, font=font_large, fill=(35, 17, 8, 200))
    # Draw golden text
    d.text(((862 - w1) // 2, 470), brand_text, font=font_large, fill=(230, 191, 122, 255))
    
    bbox2 = d.textbbox((0, 0), sub_text, font=font_sub)
    w2 = bbox2[2] - bbox2[0]
    d.text(((862 - w2) // 2, 560), sub_text, font=font_sub, fill=(246, 234, 214, 185))

    img.save('public/logo.png', 'PNG')
    print("Logo saved to public/logo.png")

if __name__ == '__main__':
    generate_garnishes()
    generate_logo()

