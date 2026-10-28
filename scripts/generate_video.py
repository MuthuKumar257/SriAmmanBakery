import imageio.v3 as iio
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFilter

def make_video():
    print("Generating cinematic sweets intro video (public/drone zoom.mp4)...")
    frames = []
    w, h = 1280, 720
    total_frames = 120 # 4 seconds at 30 fps
    
    # We will generate a camera slow zoom through warm golden mist, golden embers and pure desi ghee reflections
    for f in range(total_frames):
        t = f / float(total_frames)
        zoom = 1.0 + t * 0.25
        
        # Base deep roast to golden amber radial gradient
        base = Image.new('RGB', (w, h), (18, 9, 4))
        d = ImageDraw.Draw(base)
        
        # Multiple ambient warm light centers that drift slowly
        cx1 = int(w * 0.5 + math.sin(t * math.pi * 2) * 50)
        cy1 = int(h * 0.45 + math.cos(t * math.pi * 2) * 30)
        
        for r in range(int(520 * zoom), 0, -25):
            factor = (1.0 - r / (520.0 * zoom))**1.4
            red = int(22 + 130 * factor)
            green = int(10 + 65 * factor)
            blue = int(4 + 18 * factor)
            d.ellipse([cx1 - r, cy1 - r//2, cx1 + r, cy1 + r//2], fill=(red, green, blue))
            
        # Simmering golden boondi pearls / ghee bubbles glistening in bokeh
        rng = np.random.RandomState(f * 100)
        for b_i in range(35):
            bx = int((rng.uniform(0.1, 0.9) * w - w*0.5) * zoom + w*0.5)
            by = int((rng.uniform(0.2, 0.8) * h - h*0.5) * zoom + h*0.5)
            br = int(rng.uniform(8, 28) * zoom)
            alpha_b = rng.uniform(0.2, 0.7)
            d.ellipse([bx - br, by - br, bx + br, by + br],
                      fill=(int(240 * alpha_b), int(160 * alpha_b), int(40 * alpha_b)))
            d.ellipse([bx - br//3, by - br//3, bx + br//4, by + br//4],
                      fill=(int(255 * alpha_b), int(240 * alpha_b), int(180 * alpha_b)))

        # Soft atmospheric blur
        blurred = base.filter(ImageFilter.GaussianBlur(1.8))
        frames.append(np.array(blurred))
        if f % 30 == 0:
            print(f"Rendered video frame {f}/{total_frames}")

    iio.imwrite('public/drone zoom.mp4', frames, fps=30, codec='libx264')
    print("Video public/drone zoom.mp4 created successfully!")

if __name__ == '__main__':
    make_video()

