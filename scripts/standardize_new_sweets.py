from PIL import Image
import os

images = {
    'carrot-burfi.jpg': 'Carrot-Barfi.jpg',
    'gulab-jamun.jpg': 'Gulab Jamun.jpg',
    'milk-laddu.jpg': 'Milk Laddu.png',
    'pista-burfi.jpg': 'Pista Barfi.jpg',
    'rose-burfi.jpg': 'Rose-Barfi-scaled.jpg',
}

sweets_dir = 'public/sweets'

for target_name, src_name in images.items():
    src_path = os.path.join(sweets_dir, src_name)
    dst_path = os.path.join(sweets_dir, target_name)
    with Image.open(src_path) as img:
        img = img.convert('RGB')
        # Center-crop to 4:3 ratio for perfectly balanced cards
        w, h = img.size
        target_ratio = 4.0 / 3.0
        current_ratio = w / h
        
        if current_ratio > target_ratio:
            # Too wide, crop left/right
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            img_cropped = img.crop((left, 0, left + new_w, h))
        else:
            # Too tall, crop top/bottom
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            img_cropped = img.crop((0, top, w, top + new_h))
            
        # Resize to standard 800x600
        final_img = img_cropped.resize((800, 600), Image.Resampling.LANCZOS)
        final_img.save(dst_path, 'JPEG', quality=92, optimize=True)
        print(f"Standardized {src_name} -> {target_name} (800x600)")

print("All 5 new sweets images standardized successfully!")

