import math
import random
from PIL import Image, ImageDraw, ImageFilter

def generate_more_garnishes():
    print("Generating expanded garnishes 7 to 14...")

    # ---------------------------------------------------------------
    # 7. GULAB JAMUN (Glossy dark golden-amber syrup sphere)
    # ---------------------------------------------------------------
    img7 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d7 = ImageDraw.Draw(img7)
    cx, cy, radius = 160, 160, 120
    
    # Deep warm brown-amber sphere with rich glossy syrup shading
    for r in range(radius, 0, -3):
        f = 1.0 - (r / radius) * 0.5
        d7.ellipse([cx - r, cy - r, cx + r, cy + r],
                   fill=(int(95 * f + 25 * (1 - f)), int(45 * f + 10 * (1 - f)), int(18 * f + 5 * (1 - f)), 255))
    
    # Specular glossy syrup highlights
    d7.ellipse([cx - 55, cy - 65, cx - 15, cy - 25], fill=(255, 230, 180, 160))
    d7.ellipse([cx - 45, cy - 55, cx - 25, cy - 35], fill=(255, 255, 240, 220))
    # Cardamom & saffron specks
    rng = random.Random(707)
    for _ in range(18):
        px = cx + rng.uniform(-70, 70)
        py = cy + rng.uniform(-70, 70)
        d7.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(40, 60, 30, 200)) # cardamom
    for _ in range(8):
        sx = cx + rng.uniform(-60, 60)
        sy = cy + rng.uniform(-60, 60)
        d7.line([sx, sy, sx + rng.uniform(8, 16), sy + rng.uniform(-4, 6)], fill=(210, 45, 20, 230), width=2) # saffron
    
    img7 = img7.filter(ImageFilter.GaussianBlur(0.7))
    img7.save('public/garnishes/7.png', 'PNG')
    print("Saved 7. Gulab Jamun")

    # ---------------------------------------------------------------
    # 8. PISTA BURFI (Pastel emerald diamond with crushed pistachios)
    # ---------------------------------------------------------------
    img8 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d8 = ImageDraw.Draw(img8)
    # Isometric Diamond
    top = (160, 45)
    right = (275, 130)
    bottom = (160, 275)
    left = (45, 190)
    center = (160, 160)
    
    # Top face
    d8.polygon([top, right, center, left], fill=(135, 190, 120, 255))
    # Right beveled side
    d8.polygon([center, right, (275, 155), (160, 290)], fill=(100, 150, 90, 255))
    # Left beveled side
    d8.polygon([left, center, (160, 290), (45, 215)], fill=(115, 165, 105, 255))
    
    # Pistachio nut granules
    rng = random.Random(808)
    for _ in range(80):
        nx = rng.uniform(70, 250)
        ny = rng.uniform(65, 175)
        d8.ellipse([nx - 4, ny - 3, nx + 4, ny + 3], fill=(60, 115, 45, 220))
    # Slivered almonds on top
    for _ in range(12):
        ax = rng.uniform(90, 230)
        ay = rng.uniform(75, 160)
        d8.ellipse([ax - 8, ay - 3, ax + 8, ay + 3], fill=(250, 240, 220, 240))
        
    img8 = img8.filter(ImageFilter.GaussianBlur(0.6))
    img8.save('public/garnishes/8.png', 'PNG')
    print("Saved 8. Pista Burfi")

    # ---------------------------------------------------------------
    # 9. CARROT BURFI (Vibrant garden carrot-orange diamond)
    # ---------------------------------------------------------------
    img9 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d9 = ImageDraw.Draw(img9)
    d9.polygon([top, right, center, left], fill=(235, 115, 40, 255))
    d9.polygon([center, right, (275, 155), (160, 290)], fill=(185, 80, 25, 255))
    d9.polygon([left, center, (160, 290), (45, 215)], fill=(205, 95, 30, 255))
    
    # Grated carrot grain & cashews
    rng = random.Random(909)
    for _ in range(110):
        cx1 = rng.uniform(65, 255)
        cy1 = rng.uniform(60, 180)
        d9.ellipse([cx1 - 3, cy1 - 2, cx1 + 3, cy1 + 2], fill=(255, 145, 60, 220))
    for _ in range(10):
        kx = rng.uniform(85, 235)
        ky = rng.uniform(70, 165)
        d9.ellipse([kx - 9, ky - 5, kx + 9, ky + 5], fill=(245, 235, 205, 240))
        
    img9 = img9.filter(ImageFilter.GaussianBlur(0.6))
    img9.save('public/garnishes/9.png', 'PNG')
    print("Saved 9. Carrot Burfi")

    # ---------------------------------------------------------------
    # 10. ROSE BURFI (Soft floral pink diamond with rose petals)
    # ---------------------------------------------------------------
    img10 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d10 = ImageDraw.Draw(img10)
    d10.polygon([top, right, center, left], fill=(240, 165, 185, 255))
    d10.polygon([center, right, (275, 155), (160, 290)], fill=(195, 120, 145, 255))
    d10.polygon([left, center, (160, 290), (45, 215)], fill=(215, 140, 165, 255))
    
    # Edible dried rose petals
    rng = random.Random(1010)
    for _ in range(16):
        rx1 = rng.uniform(80, 240)
        ry1 = rng.uniform(70, 170)
        d10.ellipse([rx1 - 7, ry1 - 4, rx1 + 7, ry1 + 4], fill=(160, 35, 65, 230))
    for _ in range(14):
        ax = rng.uniform(90, 230)
        ay = rng.uniform(75, 160)
        d10.ellipse([ax - 7, ay - 3, ax + 7, ay + 3], fill=(110, 170, 85, 220)) # pistachio fleck
        
    img10 = img10.filter(ImageFilter.GaussianBlur(0.6))
    img10.save('public/garnishes/10.png', 'PNG')
    print("Saved 10. Rose Burfi")

    # ---------------------------------------------------------------
    # 11. WHOLE ROASTED CASHEW NUT (Kidney curved, golden toast)
    # ---------------------------------------------------------------
    img11 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d11 = ImageDraw.Draw(img11)
    
    # Draw curved crescent cashew
    for r in range(80, 0, -2):
        frac = r / 80.0
        c_fill = (int(245 - 20 * frac), int(225 - 40 * frac), int(175 - 70 * frac), 255)
        d11.arc([60 + r * 0.4, 70 + r * 0.3, 260 - r * 0.4, 250 - r * 0.3], 20, 260, fill=c_fill, width=22)
    # Toast marks
    d11.arc([90, 95, 230, 225], 60, 180, fill=(180, 115, 45, 180), width=8)
    d11.arc([110, 115, 210, 205], 90, 160, fill=(145, 85, 30, 200), width=5)
    
    img11 = img11.filter(ImageFilter.GaussianBlur(0.8))
    img11.save('public/garnishes/11.png', 'PNG')
    print("Saved 11. Whole Roasted Cashew")

    # ---------------------------------------------------------------
    # 12. WHOLE CALIFORNIA ALMOND (Oval pointed, golden brown skin)
    # ---------------------------------------------------------------
    img12 = Image.new('RGBA', (320, 320), (0, 0, 0, 0))
    d12 = ImageDraw.Draw(img12)
    
    # Pointed almond shape
    points = [
        (160, 45), (210, 95), (235, 165), (220, 235),
        (160, 275), (100, 235), (85, 165), (110, 95)
    ]
    d12.polygon(points, fill=(165, 95, 45, 255))
    # Inner woodgrain almond striations
    for off in range(-35, 40, 12):
        d12.line([(160 + off * 0.6, 75), (160 + off, 245)], fill=(125, 65, 25, 180), width=3)
    # Specular rim
    d12.line([(110, 105), (85, 165), (105, 235)], fill=(210, 145, 85, 160), width=4)
    
    img12 = img12.filter(ImageFilter.GaussianBlur(0.8))
    img12.save('public/garnishes/12.png', 'PNG')
    print("Saved 12. Whole Almond")

if __name__ == '__main__':
    generate_more_garnishes()

