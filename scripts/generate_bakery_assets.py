import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

os.makedirs('public/garnishes', exist_ok=True)
os.makedirs('public/beans', exist_ok=True)
os.makedirs('public/frames', exist_ok=True)

# -------------------------------------------------------------------
# 1. GENERATE THE SIX SWEETS (public/garnishes/1.png to 6.png)
# -------------------------------------------------------------------
def generate_six_sweets():
    print("Generating the six specific sweets...")
    
    # ---------------------------------------------------------------
    # 1. LADDU (Golden, round traditional Indian sweet)
    # ---------------------------------------------------------------
    img1 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(img1)
    cx, cy, radius = 160, 160, 125
    
    # Base warm golden gradient
    for r in range(radius, 0, -4):
        f = 1.0 - (r / radius) * 0.45
        d1.ellipse([cx - r, cy - r, cx + r, cy + r],
                   fill=(int(240 * f + 15 * (1 - f)), int(145 * f + 10 * (1 - f)), int(20 * f), 255))
                   
    # Boondi spheres
    rng = random.Random(101)
    for _ in range(450):
        ang = rng.uniform(0, 2 * math.pi)
        dist = radius * math.sqrt(rng.uniform(0.04, 0.95))
        px = cx + dist * math.cos(ang)
        py = cy + dist * math.sin(ang)
        pr = rng.uniform(5, 10)
        
        dx = (px - (cx - radius * 0.35)) / radius
        dy = (py - (cy - radius * 0.35)) / radius
        light = max(0.25, min(1.3, 1.0 - (dx * 0.6 + dy * 0.7)))
        d1.ellipse([px - pr, py - pr, px + pr, py + pr],
                   fill=(int(min(255, 250 * light)), int(min(255, 160 * light)), int(min(255, 30 * light)), 255))
        if rng.random() < 0.4:
            d1.ellipse([px - pr * 0.4, py - pr * 0.4, px + pr * 0.1, py + pr * 0.1],
                       fill=(255, 250, 205, 230))
                       
    # Garnish: green pistachios & melon seeds
    for _ in range(30):
        ang = rng.uniform(0, 2 * math.pi)
        dist = radius * math.sqrt(rng.uniform(0.1, 0.82))
        gx = cx + dist * math.cos(ang)
        gy = cy + dist * math.sin(ang)
        d1.ellipse([gx - 9, gy - 4, gx + 9, gy + 4], fill=(110, 175, 55, 255))
    for _ in range(15):
        ang = rng.uniform(0, 2 * math.pi)
        dist = radius * math.sqrt(rng.uniform(0.15, 0.8))
        mx = cx + dist * math.cos(ang)
        my = cy + dist * math.sin(ang)
        d1.ellipse([mx - 10, my - 4, mx + 10, my + 4], fill=(250, 240, 215, 255))
        
    img1 = img1.filter(ImageFilter.GaussianBlur(0.8))
    img1.save('public/garnishes/1.png', 'PNG')
    img1.save('public/beans/1.png', 'PNG')
    print("Saved 1. Laddu")

    # ---------------------------------------------------------------
    # 2. MYSORE PAK (Rich, golden, traditional gram-flour sweet)
    # ---------------------------------------------------------------
    img2 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(img2)
    # 3D cuboid block in isometric perspective
    # Top face (golden roasted crust with crumbly pores)
    top_face = [(160, 55), (265, 110), (160, 165), (55, 110)]
    d2.polygon(top_face, fill=(245, 195, 75, 255), outline=(225, 170, 50, 255))
    
    # Left face (rich darker caramelized ghee center)
    left_face = [(55, 110), (160, 165), (160, 265), (55, 210)]
    d2.polygon(left_face, fill=(195, 120, 40, 255), outline=(170, 100, 30, 255))
    
    # Right face (medium warm ghee crumb)
    right_face = [(160, 165), (265, 110), (265, 210), (160, 265)]
    d2.polygon(right_face, fill=(225, 155, 55, 255), outline=(195, 130, 45, 255))
    
    # Porous honeycomb crumb texture
    rng = random.Random(202)
    for _ in range(80):
        px = rng.uniform(70, 250)
        py = rng.uniform(70, 150)
        d2.ellipse([px - 2, py - 1, px + 2, py + 1], fill=(180, 115, 35, 180))
    for _ in range(90):
        px = rng.uniform(65, 155)
        py = rng.uniform(120, 250)
        d2.ellipse([px - 3, py - 2, px + 3, py + 2], fill=(145, 80, 20, 190))
    for _ in range(90):
        px = rng.uniform(165, 255)
        py = rng.uniform(120, 250)
        d2.ellipse([px - 3, py - 2, px + 3, py + 2], fill=(175, 105, 35, 190))
        
    # Specular ghee glint on top edge
    d2.line([(160, 55), (265, 110)], fill=(255, 240, 175, 240), width=3)
    d2.line([(55, 110), (160, 165)], fill=(255, 230, 150, 220), width=3)
    
    img2 = img2.filter(ImageFilter.GaussianBlur(0.8))
    img2.save('public/garnishes/2.png', 'PNG')
    img2.save('public/beans/2.png', 'PNG')
    print("Saved 2. Mysore Pak")

    # ---------------------------------------------------------------
    # 3. JALEBI (Bright orange, syrup-soaked spiral sweet)
    # ---------------------------------------------------------------
    img3 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d3 = ImageDraw.Draw(img3)
    # Spiral loops of crisp pretzel-coil
    loops = 3.6
    steps = 400
    points = []
    for step in range(steps):
        theta = step * (loops * 2 * math.pi) / steps
        r_spiral = 18 + 95 * (step / steps)
        # add wavy variation for handmade batter look
        r_spiral += 7 * math.sin(theta * 5.0)
        jx = 160 + r_spiral * math.cos(theta)
        jy = 160 + r_spiral * math.sin(theta) * 0.92
        points.append((jx, jy))
        
    # Draw thicker base coil in bright saffron orange
    for i in range(len(points) - 1):
        d3.line([points[i], points[i + 1]], fill=(250, 105, 5, 255), width=24)
    # Inner body highlight
    for i in range(len(points) - 1):
        d3.line([points[i], points[i + 1]], fill=(255, 145, 20, 255), width=16)
    # Glistening sugar syrup glossy sheen
    for i in range(len(points) - 1):
        p1 = (points[i][0] - 2, points[i][1] - 3)
        p2 = (points[i+1][0] - 2, points[i+1][1] - 3)
        d3.line([p1, p2], fill=(255, 230, 150, 230), width=6)
        
    # Saffron strands
    d3.line([(140, 130), (155, 145)], fill=(180, 20, 10, 255), width=2)
    d3.line([(175, 160), (190, 175)], fill=(180, 20, 10, 255), width=2)
    
    img3 = img3.filter(ImageFilter.GaussianBlur(0.8))
    img3.save('public/garnishes/3.png', 'PNG')
    img3.save('public/beans/3.png', 'PNG')
    print("Saved 3. Jalebi")

    # ---------------------------------------------------------------
    # 4. BADAM BURFI (Almond-based diamond sweet with silver vark)
    # ---------------------------------------------------------------
    img4 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d4 = ImageDraw.Draw(img4)
    # Isometric diamond / lozenge cut
    # Top face
    top_diamond = [(160, 50), (265, 125), (160, 200), (55, 125)]
    d4.polygon(top_diamond, fill=(245, 235, 215, 255), outline=(220, 205, 180, 255))
    
    # Left cut edge (showing granular badam texture)
    left_edge = [(55, 125), (160, 200), (160, 260), (55, 185)]
    d4.polygon(left_edge, fill=(215, 195, 165, 255), outline=(190, 170, 140, 255))
    
    # Right cut edge
    right_edge = [(160, 200), (265, 125), (265, 185), (160, 260)]
    d4.polygon(right_edge, fill=(230, 210, 180, 255), outline=(205, 185, 155, 255))
    
    # Almond skin specks & granularity
    rng = random.Random(404)
    for _ in range(120):
        bx = rng.uniform(70, 250)
        by = rng.uniform(70, 180)
        d4.ellipse([bx - 1.5, by - 1, bx + 1.5, by + 1], fill=(160, 95, 45, 190))
        
    # Pure Silver Vark (Chandi ka Varq) foil patch on top
    vark_poly = [(125, 95), (205, 75), (225, 140), (150, 165), (115, 135)]
    d4.polygon(vark_poly, fill=(240, 248, 255, 240), outline=(255, 255, 255, 255))
    
    # Sliced almond slivers on top
    d4.ellipse([165, 110, 195, 125], fill=(210, 150, 85, 255))
    d4.ellipse([168, 112, 192, 123], fill=(255, 245, 225, 255))
    
    img4 = img4.filter(ImageFilter.GaussianBlur(0.8))
    img4.save('public/garnishes/4.png', 'PNG')
    img4.save('public/beans/4.png', 'PNG')
    print("Saved 4. Badam Burfi")

    # ---------------------------------------------------------------
    # 5. BOOST BURFI (Chocolate-brown / malt-colored burfi)
    # ---------------------------------------------------------------
    img5 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d5 = ImageDraw.Draw(img5)
    # 3D diamond square block
    top_boost = [(160, 50), (265, 125), (160, 200), (55, 125)]
    d5.polygon(top_boost, fill=(105, 48, 22, 255), outline=(85, 36, 15, 255))
    
    left_boost = [(55, 125), (160, 200), (160, 260), (55, 185)]
    d5.polygon(left_boost, fill=(75, 32, 14, 255), outline=(58, 24, 10, 255))
    
    right_boost = [(160, 200), (265, 125), (265, 185), (160, 260)]
    d5.polygon(right_boost, fill=(90, 40, 18, 255), outline=(70, 30, 12, 255))
    
    # Chocolate-malt granular texture & golden roasted nuts
    rng = random.Random(505)
    for _ in range(110):
        px = rng.uniform(70, 250)
        py = rng.uniform(70, 180)
        d5.ellipse([px - 2, py - 1, px + 2, py + 1], fill=(135, 68, 32, 190))
    # Embedded cashew nut pieces on top
    for (kx, ky) in [(130, 115), (190, 105), (160, 155)]:
        d5.ellipse([kx - 12, ky - 7, kx + 12, ky + 7], fill=(235, 220, 185, 255), outline=(195, 160, 110, 200))
        
    # Specular gloss on edge
    d5.line([(160, 50), (265, 125)], fill=(155, 85, 45, 220), width=3)
    d5.line([(55, 125), (160, 200)], fill=(145, 75, 35, 200), width=3)
    
    img5 = img5.filter(ImageFilter.GaussianBlur(0.8))
    img5.save('public/garnishes/5.png', 'PNG')
    img5.save('public/beans/5.png', 'PNG')
    print("Saved 5. Boost Burfi")

    # ---------------------------------------------------------------
    # 6. HORLICKS BURFI (Malt-flavored golden-cream burfi)
    # ---------------------------------------------------------------
    img6 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d6 = ImageDraw.Draw(img6)
    # Clean, attractive square diamond block in warm malted-cream
    top_horlicks = [(160, 50), (265, 125), (160, 200), (55, 125)]
    d6.polygon(top_horlicks, fill=(238, 205, 145, 255), outline=(215, 180, 115, 255))
    
    left_horlicks = [(55, 125), (160, 200), (160, 260), (55, 185)]
    d6.polygon(left_horlicks, fill=(198, 155, 95, 255), outline=(175, 135, 80, 255))
    
    right_horlicks = [(160, 200), (265, 125), (265, 185), (160, 260)]
    d6.polygon(right_horlicks, fill=(218, 175, 115, 255), outline=(195, 155, 95, 255))
    
    # Fine malt grain texture
    rng = random.Random(606)
    for _ in range(120):
        px = rng.uniform(70, 250)
        py = rng.uniform(70, 180)
        d6.ellipse([px - 2, py - 1, px + 2, py + 1], fill=(210, 170, 110, 180))
        
    # Pistachio & almond sliver garnish
    for (gx, gy) in [(140, 110), (180, 125), (160, 85)]:
        d6.ellipse([gx - 8, gy - 3, gx + 8, gy + 3], fill=(110, 175, 55, 255))
    for (ax, ay) in [(155, 140), (200, 95)]:
        d6.ellipse([ax - 9, ay - 4, ax + 9, ay + 4], fill=(255, 245, 220, 255), outline=(190, 140, 80, 200))
        
    # Specular gloss line
    d6.line([(160, 50), (265, 125)], fill=(255, 240, 195, 240), width=3)
    d6.line([(55, 125), (160, 200)], fill=(255, 235, 180, 220), width=3)
    
    img6 = img6.filter(ImageFilter.GaussianBlur(0.8))
    img6.save('public/garnishes/6.png', 'PNG')
    img6.save('public/beans/6.png', 'PNG')
    print("Saved 6. Horlicks Burfi")

# -------------------------------------------------------------------
# 2. GENERATE HERO SWEET THALI (Featuring the 6 sweets)
# -------------------------------------------------------------------
def draw_brass_thali(d, cx, cy, rx, ry):
    steps = 72
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        r_out = rx + 14 * math.sin(i * 6)
        x = cx + r_out * math.cos(angle)
        y = cy + (ry * r_out / rx) * math.sin(angle)
        d.ellipse([x - 7, y - 5, x + 7, y + 5], fill=(210, 165, 85, 230))

    d.ellipse([cx - rx - 10, cy - ry - 8, cx + rx + 10, cy + ry + 8], outline=(155, 110, 50, 255), width=6)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(185, 140, 65, 255), outline=(245, 215, 145, 255), width=8)
    d.ellipse([cx - rx + 15, cy - ry + 12, cx + rx - 15, cy + ry - 12], fill=(130, 90, 40, 255), outline=(215, 175, 95, 255), width=4)
    d.ellipse([cx - rx + 25, cy - ry + 20, cx + rx - 25, cy + ry - 20], fill=(95, 60, 25, 255))
    d.arc([cx - rx, cy - ry, cx + rx, cy + ry], 190, 310, fill=(255, 245, 200, 240), width=5)

def generate_hero_assortment():
    print("Generating hero sweets assortment on brass thali (public/sweet.png)...")
    img = Image.new('RGBA', (1254, 1254), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    cx, cy = 627, 720
    # Soft ground shadow under thali
    for r in range(540, 0, -20):
        alpha = int(90 * (1 - r / 540.0)**1.5)
        d.ellipse([cx - r, cy + 90 - int(r * 0.3), cx + r, cy + 90 + int(r * 0.3)], fill=(20, 10, 4, alpha))
        
    draw_brass_thali(d, cx, cy + 70, 490, 190)

    # Paste the 6 handcrafted sweets artfully arranged inside the thali
    # Load each of the 6 sweets
    sweets = [Image.open(f'public/garnishes/{i}.png') for i in range(1, 7)]
    
    # Positions and sizes for each sweet on the brass platter:
    # 1. Mysore Pak on left rear
    s2 = sweets[1].resize((260, 260), Image.Resampling.LANCZOS)
    img.paste(s2, (cx - 380, cy - 80), s2)
    
    # 2. Boost Burfi on right rear
    s5 = sweets[4].resize((250, 250), Image.Resampling.LANCZOS)
    img.paste(s5, (cx + 120, cy - 80), s5)
    
    # 3. Horlicks Burfi on far right
    s6 = sweets[5].resize((240, 240), Image.Resampling.LANCZOS)
    img.paste(s6, (cx + 190, cy + 10), s6)
    
    # 4. Badam Burfi on far left
    s4 = sweets[3].resize((240, 240), Image.Resampling.LANCZOS)
    img.paste(s4, (cx - 410, cy + 10), s4)
    
    # 5. Jalebi in front center-left
    s3 = sweets[2].resize((270, 270), Image.Resampling.LANCZOS)
    img.paste(s3, (cx - 240, cy + 50), s3)

    # 6. Grand Golden Laddu prominently crowned at center
    s1 = sweets[0].resize((390, 390), Image.Resampling.LANCZOS)
    img.paste(s1, (cx - 195, cy - 190), s1)

    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=125, threshold=3))
    img.save('public/sweet.png', 'PNG')
    img.save('public/coffee.png', 'PNG')
    print("Saved public/sweet.png and public/coffee.png!")

# -------------------------------------------------------------------
# 3. GENERATE LUXURY SWEET BOX (public/package.png)
# -------------------------------------------------------------------
def generate_sweet_box():
    print("Generating Sri Amman Bakery sweet box (public/package.png)...")
    img = Image.new('RGBA', (926, 1024), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    bx, by = 463, 560
    bw, bh = 340, 390
    
    # Ground shadow
    for i in range(160, 0, -10):
        alpha = int(120 * (1 - i / 160.0)**1.4)
        d.ellipse([bx - bw - 40, by + bh - 40 - i//3, bx + bw + 40, by + bh + 40 + i//3], fill=(15, 6, 2, alpha))

    # Box Body (deep royal burgundy / rich maroon)
    rect = [bx - bw, by - bh, bx + bw, by + bh]
    d.rounded_rectangle(rect, radius=24, fill=(110, 18, 28, 255), outline=(215, 175, 95, 255), width=6)
    
    # Inner gold border
    inset = 22
    d.rounded_rectangle([rect[0] + inset, rect[1] + inset, rect[2] - inset, rect[3] - inset],
                        radius=16, outline=(230, 191, 122, 230), width=3)
    
    # Corner ornaments
    for x_c, y_c in [
        (rect[0] + inset + 15, rect[1] + inset + 15),
        (rect[2] - inset - 15, rect[1] + inset + 15),
        (rect[0] + inset + 15, rect[3] - inset - 15),
        (rect[2] - inset - 15, rect[3] - inset - 15)
    ]:
        for k in range(1, 4):
            d.ellipse([x_c - k * 8, y_c - k * 8, x_c + k * 8, y_c + k * 8], outline=(230, 191, 122, 160), width=1)

    # Medallion
    mcx, mcy = bx, by - 65
    d.ellipse([mcx - 170, mcy - 170, mcx + 170, mcy + 170], outline=(230, 191, 122, 255), width=4)
    d.ellipse([mcx - 160, mcy - 160, mcx + 160, mcy + 160], fill=(85, 12, 20, 255), outline=(180, 135, 65, 200), width=2)
    
    # Rays
    for angle in range(0, 360, 12):
        rad = math.radians(angle)
        x1 = mcx + 170 * math.cos(rad)
        y1 = mcy + 170 * math.sin(rad)
        x2 = mcx + 185 * math.cos(rad)
        y2 = mcy + 185 * math.sin(rad)
        d.line([(x1, y1), (x2, y2)], fill=(230, 191, 122, 200), width=2)

    # Inside medallion: collage of the sweets (Laddu, Jalebi, Mysore Pak)
    s1 = Image.open('public/garnishes/1.png').resize((130, 130), Image.Resampling.LANCZOS)
    s2 = Image.open('public/garnishes/2.png').resize((100, 100), Image.Resampling.LANCZOS)
    s3 = Image.open('public/garnishes/3.png').resize((110, 110), Image.Resampling.LANCZOS)
    img.paste(s2, (mcx - 110, mcy - 40), s2)
    img.paste(s3, (mcx + 10, mcy - 40), s3)
    img.paste(s1, (mcx - 65, mcy - 70), s1)

    # Brand typography on box
    try:
        font_brand = ImageFont.truetype("times.ttf", 36)
        font_prod = ImageFont.truetype("times.ttf", 26)
        font_desc = ImageFont.truetype("arial.ttf", 15)
        font_wt = ImageFont.truetype("arial.ttf", 17)
    except:
        font_brand = ImageFont.load_default()
        font_prod = ImageFont.load_default()
        font_desc = ImageFont.load_default()
        font_wt = ImageFont.load_default()

    brand = "SRI AMMAN BAKERY"
    prod = "SIGNATURE SWEETS ASSORTMENT"
    desc = "LADDU · MYSORE PAK · JALEBI · BURFI"
    wt = "PURE GHEE · 6 HERITAGE SWEETS"

    for (txt, fnt, y_pos, color) in [
        (brand, font_brand, by + 125, (245, 215, 145, 255)),
        (prod, font_prod, by + 180, (230, 191, 122, 255)),
        (desc, font_desc, by + 230, (246, 234, 214, 200)),
        (wt, font_wt, by + 280, (230, 191, 122, 235))
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        w = bbox[2] - bbox[0]
        d.text((bx - w // 2 + 1, y_pos + 1), txt, font=fnt, fill=(20, 5, 5, 220))
        d.text((bx - w // 2, y_pos), txt, font=fnt, fill=color)

    # Gold ribbon band
    d.rectangle([rect[0] + inset, rect[3] - 70, rect[2] - inset, rect[3] - 50], fill=(230, 191, 122, 255))
    d.line([(rect[0] + inset, rect[3] - 70), (rect[2] - inset, rect[3] - 70)], fill=(255, 245, 205, 255), width=2)

    img.save('public/package.png', 'PNG')
    print("Saved public/package.png!")

# -------------------------------------------------------------------
# 4. GENERATE ROTATING SEAL (public/seal_sweet.jpg)
# -------------------------------------------------------------------
def generate_seal():
    print("Generating rotating seal medallion (public/seal_sweet.jpg)...")
    img = Image.new('RGB', (554, 554), (24, 11, 4))
    d = ImageDraw.Draw(img)
    d.ellipse([20, 20, 534, 534], fill=(45, 20, 8), outline=(230, 191, 122), width=10)
    
    # Collage of sweets inside seal
    s1 = Image.open('public/garnishes/1.png').resize((240, 240), Image.Resampling.LANCZOS)
    s2 = Image.open('public/garnishes/2.png').resize((170, 170), Image.Resampling.LANCZOS)
    s3 = Image.open('public/garnishes/3.png').resize((180, 180), Image.Resampling.LANCZOS)
    img.paste(s2, (80, 200), s2)
    img.paste(s3, (280, 200), s3)
    img.paste(s1, (157, 100), s1)
    
    img.save('public/seal_sweet.jpg', 'JPEG', quality=95)
    img.save('public/coorg.jpg', 'JPEG', quality=95)
    print("Saved public/seal_sweet.jpg!")

# -------------------------------------------------------------------
# 5. GENERATE 127 CANVAS FRAMES (public/frames/frame_000001.png to 127)
# -------------------------------------------------------------------
def generate_canvas_frames():
    print("Generating 127 canvas frames with Sri Amman Bakery sweets...")
    cx, cy = 624, 620
    
    # Load sweets
    s1 = Image.open('public/garnishes/1.png') # Laddu
    s2 = Image.open('public/garnishes/2.png') # Mysore Pak
    s3 = Image.open('public/garnishes/3.png') # Jalebi
    s4 = Image.open('public/garnishes/4.png') # Badam Burfi
    s5 = Image.open('public/garnishes/5.png') # Boost Burfi
    s6 = Image.open('public/garnishes/6.png') # Horlicks Burfi

    for i in range(1, 128):
        progress = (i - 1) / 126.0
        
        img = Image.new('RGB', (1248, 1080), (23, 11, 5))
        d = ImageDraw.Draw(img)
        
        # Draw brass thali base
        draw_brass_thali(d, cx, cy + 120, 480, 180)
        
        # Surround with sweets
        mp = s2.resize((210, 210), Image.Resampling.LANCZOS)
        bb = s5.resize((200, 200), Image.Resampling.LANCZOS)
        jal = s3.resize((210, 210), Image.Resampling.LANCZOS)
        hb = s6.resize((190, 190), Image.Resampling.LANCZOS)
        bad = s4.resize((190, 190), Image.Resampling.LANCZOS)
        
        img.paste(mp, (cx - 380, cy + 30), mp)
        img.paste(bb, (cx + 170, cy + 30), bb)
        img.paste(bad, (cx - 390, cy + 110), bad)
        img.paste(hb, (cx + 200, cy + 110), hb)
        img.paste(jal, (cx - 240, cy + 130), jal)
        
        # Central Laddu elevation
        lift_y = 0
        if progress < 0.25:
            p_lift = progress / 0.25
            lift_y = -int(math.sin(p_lift * math.pi * 0.5) * 80)
        elif progress < 0.85:
            lift_y = -80 + int(math.sin((progress - 0.25) / 0.6 * math.pi) * 30)
        else:
            p_down = (progress - 0.85) / 0.15
            lift_y = -int(80 * (1 - p_down))
            
        laddu_center_y = cy + lift_y - 20
        
        # Golden saffron syrup pour in chapter 2/3
        if 0.18 <= progress <= 0.75:
            stream_p = min(1.0, (progress - 0.18) / 0.15)
            pour_start_x = cx + 280
            pour_start_y = 120
            pour_end_x = cx + 15
            pour_end_y = laddu_center_y - 50
            
            points = []
            for t_step in range(25):
                t = t_step / 24.0 * stream_p
                px = (1 - t)**2 * pour_start_x + 2 * (1 - t) * t * (cx + 80) + t**2 * pour_end_x
                py = (1 - t)**2 * pour_start_y + 2 * (1 - t) * t * (laddu_center_y - 160) + t**2 * pour_end_y
                points.append((px, py))
            if len(points) > 1:
                d.line(points, fill=(245, 185, 35), width=14)
                d.line(points, fill=(255, 245, 170), width=6)
                
            d.polygon([(pour_start_x + 30, pour_start_y - 50),
                       (pour_start_x - 15, pour_start_y),
                       (pour_start_x + 60, pour_start_y + 20)], fill=(215, 175, 95))
                       
        # Center Laddu paste
        lad = s1.resize((360, 360), Image.Resampling.LANCZOS)
        img.paste(lad, (cx - 180, laddu_center_y - 180), lad)
        
        frame_name = f'public/frames/frame_{i:06d}.png'
        img.save(frame_name, 'PNG')
        if i % 30 == 0 or i == 127:
            print(f"Generated frame {i}/127")

    print("All 127 frames updated successfully!")

if __name__ == '__main__':
    generate_six_sweets()
    generate_hero_assortment()
    generate_sweet_box()
    generate_seal()
    generate_canvas_frames()
