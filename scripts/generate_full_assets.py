import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

os.makedirs('public/beans', exist_ok=True)
os.makedirs('public/frames', exist_ok=True)

# -------------------------------------------------------------------
# Helper: Draw an ornate Indian Brass Thali / Urli
# -------------------------------------------------------------------
def draw_brass_thali(d, cx, cy, rx, ry):
    # Outer scalloped / embossed rim
    steps = 72
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        r_out = rx + 14 * math.sin(i * 6)
        x = cx + r_out * math.cos(angle)
        y = cy + (ry * r_out / rx) * math.sin(angle)
        d.ellipse([x - 7, y - 5, x + 7, y + 5], fill=(210, 165, 85, 230))

    # Outer brass rim rings with specular highlights
    d.ellipse([cx - rx - 10, cy - ry - 8, cx + rx + 10, cy + ry + 8], outline=(155, 110, 50, 255), width=6)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(185, 140, 65, 255), outline=(245, 215, 145, 255), width=8)
    d.ellipse([cx - rx + 15, cy - ry + 12, cx + rx - 15, cy + ry - 12], fill=(130, 90, 40, 255), outline=(215, 175, 95, 255), width=4)
    # Inner thali floor with warm reflection
    d.ellipse([cx - rx + 25, cy - ry + 20, cx + rx - 25, cy + ry - 20], fill=(95, 60, 25, 255))
    # Specular rim highlight on top-left
    d.arc([cx - rx, cy - ry, cx + rx, cy + ry], 190, 310, fill=(255, 245, 200, 240), width=5)

# -------------------------------------------------------------------
# Helper: Draw Motichoor Laddu (Sphere of glistening boondi pearls)
# -------------------------------------------------------------------
def draw_motichoor_laddu(d, cx, cy, radius, with_vark=True, with_garnish=True):
    # Base warm gradient
    for r in range(radius, 0, -5):
        factor = 1.0 - (r / radius) * 0.45
        r_col = int(min(255, 235 * factor + 35 * (1 - factor)))
        g_col = int(min(255, 130 * factor + 20 * (1 - factor)))
        b_col = int(min(255, 15 * factor))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(r_col, g_col, b_col, 255))

    # Dense layer of golden glistening boondi spheres
    rng = random.Random(42)
    pearl_count = int(radius * 3.8)
    for _ in range(pearl_count):
        # random position within circle
        ang = rng.uniform(0, 2 * math.pi)
        dist = radius * math.sqrt(rng.uniform(0.04, 0.96))
        px = cx + dist * math.cos(ang)
        py = cy + dist * math.sin(ang)
        pr = rng.uniform(5, 11) * (radius / 180.0)
        
        # 3D shading on pearl based on light source (top-left)
        dx = (px - (cx - radius * 0.35)) / radius
        dy = (py - (cy - radius * 0.35)) / radius
        light = max(0.2, min(1.3, 1.0 - (dx * 0.6 + dy * 0.7)))
        
        pr_r = int(min(255, 245 * light))
        pr_g = int(min(255, 150 * light))
        pr_b = int(min(255, 25 * light))
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(pr_r, pr_g, pr_b, 255))
        # Specular glint of ghee
        if rng.random() < 0.45:
            d.ellipse([px - pr * 0.4, py - pr * 0.4, px + pr * 0.1, py + pr * 0.1], fill=(255, 245, 190, 230))

    if with_garnish:
        # Green pistachios slivers
        for _ in range(int(radius * 0.22)):
            ang = rng.uniform(0, 2 * math.pi)
            dist = radius * math.sqrt(rng.uniform(0.1, 0.85))
            gx = cx + dist * math.cos(ang)
            gy = cy + dist * math.sin(ang)
            gw = rng.uniform(10, 22) * (radius / 180.0)
            gh = rng.uniform(4, 8) * (radius / 180.0)
            tilt = rng.uniform(0, 180)
            d.ellipse([gx - gw, gy - gh, gx + gw, gy + gh], fill=(110, 165, 55, 255), outline=(145, 205, 75, 255))
        
        # Melon seeds (magaj)
        for _ in range(int(radius * 0.12)):
            ang = rng.uniform(0, 2 * math.pi)
            dist = radius * math.sqrt(rng.uniform(0.15, 0.8))
            mx = cx + dist * math.cos(ang)
            my = cy + dist * math.sin(ang)
            mw = rng.uniform(12, 18) * (radius / 180.0)
            mh = rng.uniform(5, 7) * (radius / 180.0)
            d.ellipse([mx - mw, my - mh, mx + mw, my + mh], fill=(250, 240, 215, 255))

        # Saffron kesar strands
        for _ in range(int(radius * 0.18)):
            ang = rng.uniform(0, 2 * math.pi)
            dist = radius * math.sqrt(rng.uniform(0.1, 0.8))
            sx = cx + dist * math.cos(ang)
            sy = cy + dist * math.sin(ang)
            d.line([(sx, sy), (sx + rng.uniform(-15, 15), sy + rng.uniform(-15, 15))], fill=(185, 25, 10, 255), width=2)

    if with_vark:
        # Chandi ka Varq (Pure Silver Leaf patches)
        vark_patches = [
            [(cx - radius * 0.2, cy - radius * 0.25), (cx + radius * 0.1, cy - radius * 0.35), (cx + radius * 0.05, cy - radius * 0.05), (cx - radius * 0.25, cy - radius * 0.1)],
            [(cx + radius * 0.2, cy + radius * 0.05), (cx + radius * 0.38, cy - radius * 0.08), (cx + radius * 0.32, cy + radius * 0.2), (cx + radius * 0.15, cy + radius * 0.15)],
            [(cx - radius * 0.35, cy + radius * 0.12), (cx - radius * 0.18, cy + radius * 0.08), (cx - radius * 0.22, cy + radius * 0.28), (cx - radius * 0.38, cy + radius * 0.24)]
        ]
        for poly in vark_patches:
            d.polygon(poly, fill=(240, 245, 255, 235), outline=(255, 255, 255, 255))

# -------------------------------------------------------------------
# 3. GENERATE HERO SWEET (public/coffee.png -> 1254 x 1254)
# -------------------------------------------------------------------
def generate_hero_sweet():
    print("Generating hero sweet (public/coffee.png, 1254x1254)...")
    img = Image.new('RGBA', (1254, 1254), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    cx, cy = 627, 720
    # Soft ground shadow under thali
    for r in range(540, 0, -20):
        alpha = int(90 * (1 - r / 540.0)**1.5)
        d.ellipse([cx - r, cy + 90 - int(r * 0.3), cx + r, cy + 90 + int(r * 0.3)], fill=(20, 10, 4, alpha))
        
    # Draw ornate heavy brass thali (radius x=490, y=210)
    draw_brass_thali(d, cx, cy + 70, 490, 190)

    # Secondary background laddus in thali
    draw_motichoor_laddu(d, cx - 210, cy + 20, 140, with_vark=True, with_garnish=True)
    draw_motichoor_laddu(d, cx + 210, cy + 20, 140, with_vark=True, with_garnish=True)
    draw_motichoor_laddu(d, cx - 110, cy + 80, 135, with_vark=False, with_garnish=True)
    draw_motichoor_laddu(d, cx + 110, cy + 80, 135, with_vark=True, with_garnish=True)
    
    # Grand central Royal Motichoor Laddu (radiant and majestic)
    draw_motichoor_laddu(d, cx, cy - 80, 220, with_vark=True, with_garnish=True)

    # Warm golden desi ghee ambient aura / soft bloom
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=130, threshold=3))
    img.save('public/coffee.png', 'PNG')
    print("Saved public/coffee.png!")

# -------------------------------------------------------------------
# 4. GENERATE LUXURY SWEET BOX (public/package.png -> 926 x 1024)
# -------------------------------------------------------------------
def generate_package():
    print("Generating sweet gift box (public/package.png, 926x1024)...")
    img = Image.new('RGBA', (926, 1024), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Perspective sweet box dimensions
    bx, by = 463, 560
    bw, bh = 340, 390
    
    # Ground shadow
    for i in range(160, 0, -10):
        alpha = int(120 * (1 - i / 160.0)**1.4)
        d.ellipse([bx - bw - 40, by + bh - 40 - i//3, bx + bw + 40, by + bh + 40 + i//3], fill=(15, 6, 2, alpha))

    # Box Body (deep royal crimson / rich maroon gradient)
    rect = [bx - bw, by - bh, bx + bw, by + bh]
    # Draw bevel & outer edge
    d.rounded_rectangle(rect, radius=24, fill=(110, 18, 28, 255), outline=(215, 175, 95, 255), width=6)
    
    # Inner border gold foil
    inset = 22
    d.rounded_rectangle([rect[0] + inset, rect[1] + inset, rect[2] - inset, rect[3] - inset],
                        radius=16, outline=(230, 191, 122, 230), width=3)
    
    # Intricate Indian corner motifs
    for x_c, y_c in [
        (rect[0] + inset + 15, rect[1] + inset + 15),
        (rect[2] - inset - 15, rect[1] + inset + 15),
        (rect[0] + inset + 15, rect[3] - inset - 15),
        (rect[2] - inset - 15, rect[3] - inset - 15)
    ]:
        for k in range(1, 4):
            d.ellipse([x_c - k * 8, y_c - k * 8, x_c + k * 8, y_c + k * 8], outline=(230, 191, 122, 160), width=1)

    # Central Royal Medallion
    mcx, mcy = bx, by - 60
    d.ellipse([mcx - 170, mcy - 170, mcx + 170, mcy + 170], outline=(230, 191, 122, 255), width=4)
    d.ellipse([mcx - 160, mcy - 160, mcx + 160, mcy + 160], fill=(85, 12, 20, 255), outline=(180, 135, 65, 200), width=2)
    # Mandala rays around medallion
    for angle in range(0, 360, 12):
        rad = math.radians(angle)
        x1 = mcx + 170 * math.cos(rad)
        y1 = mcy + 170 * math.sin(rad)
        x2 = mcx + 185 * math.cos(rad)
        y2 = mcy + 185 * math.sin(rad)
        d.line([(x1, y1), (x2, y2)], fill=(230, 191, 122, 200), width=2)

    # Window / Illustration inside medallion: glistening golden laddus
    draw_motichoor_laddu(d, mcx - 55, mcy + 25, 60, with_vark=True, with_garnish=True)
    draw_motichoor_laddu(d, mcx + 55, mcy + 25, 60, with_vark=True, with_garnish=True)
    draw_motichoor_laddu(d, mcx, mcy - 30, 75, with_vark=True, with_garnish=True)

    # Regal Gold Lettering on Box
    try:
        font_brand = ImageFont.truetype("times.ttf", 38)
        font_prod = ImageFont.truetype("times.ttf", 28)
        font_desc = ImageFont.truetype("arial.ttf", 16)
        font_wt = ImageFont.truetype("arial.ttf", 18)
    except:
        font_brand = ImageFont.load_default()
        font_prod = ImageFont.load_default()
        font_desc = ImageFont.load_default()
        font_wt = ImageFont.load_default()

    brand = "TRIPATHI LADDU"
    prod = "SHAHI MOTICHOOR"
    desc = "HANDCRAFTED IN 100% PURE DESI GHEE"
    wt = "500 g · LUXURY SWEET BOX"

    for (txt, fnt, y_pos, color) in [
        (brand, font_brand, by + 130, (245, 215, 145, 255)),
        (prod, font_prod, by + 185, (230, 191, 122, 255)),
        (desc, font_desc, by + 235, (246, 234, 214, 200)),
        (wt, font_wt, by + 285, (230, 191, 122, 235))
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        w = bbox[2] - bbox[0]
        # subtle shadow
        d.text((bx - w // 2 + 1, y_pos + 1), txt, font=fnt, fill=(20, 5, 5, 220))
        d.text((bx - w // 2, y_pos), txt, font=fnt, fill=color)

    # Gold ribbon / band along bottom
    d.rectangle([rect[0] + inset, rect[3] - 70, rect[2] - inset, rect[3] - 50], fill=(230, 191, 122, 255))
    d.line([(rect[0] + inset, rect[3] - 70), (rect[2] - inset, rect[3] - 70)], fill=(255, 245, 205, 255), width=2)

    img.save('public/package.png', 'PNG')
    print("Saved public/package.png!")

# -------------------------------------------------------------------
# 5. GENERATE ESTATE & SEAL ASSETS
# -------------------------------------------------------------------
def generate_estate_assets():
    print("Generating heritage craft & seal assets...")
    
    # 1. public/estate.png (1536 x 1024) - Artisanal Sweet Hearth
    img = Image.new('RGB', (1536, 1024), (20, 10, 5))
    d = ImageDraw.Draw(img)
    # Warm atmospheric background: deep terracotta, hearth glow
    for y in range(1024):
        f = y / 1024.0
        # Warm golden hearth glow in lower center
        r = int(min(255, 45 + f * 55 + math.sin(f * math.pi) * 60))
        g = int(min(255, 22 + f * 28 + math.sin(f * math.pi) * 35))
        b = int(min(255, 8 + f * 12))
        d.line([(0, y), (1536, y)], fill=(r, g, b))

    # Traditional copper and brass kadhais simmering
    for kx, ky, kr in [(450, 750, 240), (1080, 750, 240), (768, 620, 290)]:
        # kadhai body
        d.arc([kx - kr, ky - kr//2, kx + kr, ky + kr//2], 0, 180, fill=(185, 120, 50), width=18)
        # simmering golden ghee
        d.ellipse([kx - kr + 15, ky - kr//3, kx + kr - 15, ky + kr//3], fill=(235, 155, 30))
        # Ghee bubbles & shimmer
        for _ in range(35):
            bx = random.uniform(kx - kr * 0.7, kx + kr * 0.7)
            by = random.uniform(ky - kr * 0.2, ky + kr * 0.2)
            br = random.uniform(4, 12)
            d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 225, 120, 220))

    # Hanging brass bells / lamps
    for lx in [250, 768, 1280]:
        d.line([(lx, 0), (lx, 260)], fill=(180, 140, 70), width=4)
        d.polygon([(lx, 320), (lx - 45, 260), (lx + 45, 260)], fill=(215, 175, 85))
        # Warm lantern glow
        for gr in range(90, 0, -10):
            d.ellipse([lx - gr, 310 - gr//2, lx + gr, 310 + gr//2], outline=(255, 215, 110, 40), width=3)

    img = img.filter(ImageFilter.GaussianBlur(2.0))
    img.save('public/estate.png', 'PNG')
    print("Saved public/estate.png!")

    # 2. public/estate labor.jpg (1000 x 1500) - Artisan Hands Rolling Laddus
    img2 = Image.new('RGB', (1000, 1500), (28, 14, 7))
    d2 = ImageDraw.Draw(img2)
    for y in range(1500):
        f = y / 1500.0
        d2.line([(0, y), (1000, y)], fill=(int(35 + f * 50), int(18 + f * 25), int(8 + f * 10)))
    # Central brass thali
    draw_brass_thali(d2, 500, 950, 420, 210)
    # Piled golden motichoor laddus
    draw_motichoor_laddu(d2, 500, 780, 180, with_vark=True, with_garnish=True)
    draw_motichoor_laddu(d2, 320, 860, 130, with_vark=True, with_garnish=True)
    draw_motichoor_laddu(d2, 680, 860, 130, with_vark=True, with_garnish=True)
    # Master halwai hands shaping laddu
    d2.ellipse([420, 520, 580, 680], outline=(230, 191, 122, 180), width=4)
    img2 = img2.filter(ImageFilter.GaussianBlur(1.0))
    img2.save('public/estate labor.jpg', 'JPEG', quality=92)
    print("Saved public/estate labor.jpg!")

    # 3. public/coorg.jpg (554 x 554) - Rotating Seal Medallion
    img3 = Image.new('RGB', (554, 554), (24, 11, 4))
    d3 = ImageDraw.Draw(img3)
    # Circular gold frame
    d3.ellipse([20, 20, 534, 534], fill=(45, 20, 8), outline=(230, 191, 122), width=10)
    draw_motichoor_laddu(d3, 277, 277, 180, with_vark=True, with_garnish=True)
    img3.save('public/coorg.jpg', 'JPEG', quality=95)
    print("Saved public/coorg.jpg!")

# -------------------------------------------------------------------
# 6. GENERATE 127 CANVAS FRAMES (public/frames/frame_000001.png to 127)
# -------------------------------------------------------------------
def generate_frames():
    print("Generating 127 scroll-scrubbed canvas frames (1248x1080)...")
    # Base background color: #170b05 -> rgb(23, 11, 5)
    # The reference site extracts background color dynamically:
    # try { let r = img.naturalHeight/2; n.drawImage(e, 0, r, 8, 8, 0, 0, 8, 8); ... }
    
    # Pre-render a master thali and laddu to composite smoothly
    cx, cy = 624, 620
    
    for i in range(1, 128):
        progress = (i - 1) / 126.0  # 0.0 to 1.0
        
        img = Image.new('RGB', (1248, 1080), (23, 11, 5))
        d = ImageDraw.Draw(img)
        
        # In frame 1, the thali & laddu match the exact hero position & scale!
        # As progress advances:
        # Chapter 1 (0.0 to 0.20 - Lift): Sweet gently elevates, golden steam rises
        # Chapter 2 (0.20 to 0.40 - Tilt): Saffron syrup pours from golden jhari
        # Chapter 3 (0.40 to 0.86 - Pour & Roll): Pearls bind, pistachios fold in
        # Chapter 4 (0.86 to 1.00 - Crown): Silver vark settles, glorious presentation
        
        # Vertical elevation of laddu
        lift_y = 0
        if progress < 0.25:
            p_lift = progress / 0.25
            lift_y = -int(math.sin(p_lift * math.pi * 0.5) * 80)
        elif progress < 0.85:
            lift_y = -80 + int(math.sin((progress - 0.25) / 0.6 * math.pi) * 30)
        else:
            p_down = (progress - 0.85) / 0.15
            lift_y = -int(80 * (1 - p_down))
            
        # Draw brass thali
        draw_brass_thali(d, cx, cy + 120, 480, 180)
        
        # Surrounding laddus in thali
        draw_motichoor_laddu(d, cx - 210, cy + 70, 130, with_vark=True, with_garnish=True)
        draw_motichoor_laddu(d, cx + 210, cy + 70, 130, with_vark=True, with_garnish=True)
        
        # Central Sweet undergoing the ritual
        laddu_y = cy + lift_y
        
        # If pouring chapter (0.20 <= progress <= 0.80), draw golden ribbon of saffron syrup!
        if 0.18 <= progress <= 0.75:
            # Stream of golden kesar chashni pouring from top right into the sweet
            stream_p = min(1.0, (progress - 0.18) / 0.15)
            pour_start_x = cx + 280
            pour_start_y = 120
            pour_end_x = cx + 15
            pour_end_y = laddu_y - 80
            
            # Bezier-like golden syrup ribbon
            points = []
            for t_step in range(25):
                t = t_step / 24.0 * stream_p
                px = (1 - t)**2 * pour_start_x + 2 * (1 - t) * t * (cx + 80) + t**2 * pour_end_x
                py = (1 - t)**2 * pour_start_y + 2 * (1 - t) * t * (laddu_y - 180) + t**2 * pour_end_y
                points.append((px, py))
            if len(points) > 1:
                d.line(points, fill=(245, 185, 35), width=14)
                d.line(points, fill=(255, 245, 170), width=6)
                
            # Golden brass jhari pouring at top right
            d.polygon([(pour_start_x + 30, pour_start_y - 50),
                       (pour_start_x - 15, pour_start_y),
                       (pour_start_x + 60, pour_start_y + 20)], fill=(215, 175, 95))
                       
        # Draw main laddu with progress-dependent vark and garnish
        has_vark = progress >= 0.70
        has_garnish = progress >= 0.35
        draw_motichoor_laddu(d, cx, laddu_y, 210, with_vark=has_vark, with_garnish=has_garnish)
        
        # Ambient golden ghee steam particles
        if 0.05 <= progress <= 0.95:
            for s_i in range(12):
                steam_ang = (s_i * 30 + progress * 720) % 360
                rad = math.radians(steam_ang)
                sx = cx + math.cos(rad) * (180 + s_i * 15)
                sy = laddu_y - 120 - (s_i * 22 + int(progress * 160)) % 180
                alpha = int(45 * (1 - (sy / 800.0)))
                d.ellipse([sx - 18, sy - 8, sx + 18, sy + 8], fill=(230, 191, 122, alpha))
                
        frame_name = f'public/frames/frame_{i:06d}.png'
        img.save(frame_name, 'PNG')
        if i % 25 == 0 or i == 127:
            print(f"Generated frame {i}/127")

    print("All 127 frames generated successfully!")

if __name__ == '__main__':
    generate_hero_sweet()
    generate_package()
    generate_estate_assets()
    generate_frames()
