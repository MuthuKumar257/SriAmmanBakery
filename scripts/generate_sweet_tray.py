import math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

def make_sweet_tray():
    w, h = 1300, 1100
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    cx, cy = 650, 640
    rx, ry = 520, 220
    
    # 1. Soft atmospheric ground shadow under the tray
    for r in range(560, 0, -20):
        alpha = int(75 * (1 - r / 560.0)**1.4)
        d.ellipse([cx - r, cy + 120 - int(r * 0.35), cx + r, cy + 120 + int(r * 0.35)], fill=(15, 7, 3, alpha))

    # 2. Outer Brass Rim (Thick cast brass lip)
    d.ellipse([cx - rx - 16, cy - ry - 16, cx + rx + 16, cy + ry + 16], fill=(160, 115, 48, 255))
    d.ellipse([cx - rx - 10, cy - ry - 10, cx + rx + 10, cy + ry + 10], fill=(215, 175, 95, 255))
    d.ellipse([cx - rx - 4, cy - ry - 4, cx + rx + 4, cy + ry + 4], fill=(130, 85, 30, 255))
    
    # Rim highlights (specular arcs on top-left)
    d.arc([cx - rx - 8, cy - ry - 8, cx + rx + 8, cy + ry + 8], 195, 330, fill=(255, 245, 190, 220), width=6)
    d.arc([cx - rx - 12, cy - ry - 12, cx + rx + 12, cy + ry + 12], 210, 310, fill=(255, 255, 230, 250), width=3)
    
    # 3. Fluted Inner Wall
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(110, 70, 25, 255))
    d.ellipse([cx - rx + 18, cy - ry + 12, cx + rx - 18, cy + ry - 12], fill=(175, 130, 55, 255))
    
    # 4. Sunken Platter Bed (Mirror-polished brass floor)
    d.ellipse([cx - rx + 32, cy - ry + 22, cx + rx - 32, cy + ry - 22], fill=(85, 50, 18, 255))
    
    # Concentric lathed brass rings
    for step in range(40, 420, 45):
        rrx = rx - step
        rry = int(rrx * (ry / rx))
        if rrx > 50 and rry > 20:
            d.ellipse([cx - rrx, cy - rry, cx + rrx, cy + rry], outline=(150, 105, 40, 90), width=2)
            
    # Soft golden radial glow in the center of tray
    for gr in range(320, 0, -20):
        galpha = int(45 * (1 - gr / 320.0))
        d.ellipse([cx - gr, cy - int(gr * 0.4), cx + gr, cy + int(gr * 0.4)], fill=(230, 180, 80, galpha))

    # 5. Place the 6 Sweets gracefully inside the tray
    # Load garnishes / sweets
    sweets = [Image.open(f'public/garnishes/{i}.png') for i in range(1, 7)]
    
    # Helper to paste with drop shadow
    def paste_sweet(sweet_img, pos_x, pos_y, target_w, target_h):
        sw = sweet_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        # create small shadow under sweet
        shadow = Image.new('RGBA', (target_w + 40, target_h + 40), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.ellipse([20, target_h * 0.5, target_w + 20, target_h + 20], fill=(20, 10, 5, 140))
        shadow = shadow.filter(ImageFilter.GaussianBlur(10))
        img.paste(shadow, (pos_x - 20, pos_y + 10), shadow)
        img.paste(sw, (pos_x, pos_y), sw)

    # 1. Mysore Pak on rear-left
    paste_sweet(sweets[1], cx - 360, cy - 110, 260, 260)
    
    # 2. Boost Burfi on rear-right
    paste_sweet(sweets[4], cx + 110, cy - 110, 250, 250)
    
    # 3. Badam Burfi on mid-left
    paste_sweet(sweets[3], cx - 410, cy - 10, 250, 250)
    
    # 4. Horlicks Burfi on mid-right
    paste_sweet(sweets[5], cx + 180, cy - 10, 240, 240)
    
    # 5. Golden Crisp Jalebi in front-left
    paste_sweet(sweets[2], cx - 250, cy + 30, 280, 280)
    
    # 6. Crownpiece Royal Motichoor Laddu elevated in center
    paste_sweet(sweets[0], cx - 180, cy - 190, 390, 390)
    
    # Enhance sharpness and contrast
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=3))
    
    img.save('public/sweet_tray.png', 'PNG')
    print("Successfully generated public/sweet_tray.png!")

if __name__ == '__main__':
    make_sweet_tray()
