from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None
src = os.path.abspath('public/logo.png')
dst = os.path.abspath('public/favicon.ico')
tmp = os.path.abspath('public/favicon_new.ico')

with Image.open(src) as img:
    # Resize first to a sensible size e.g. 256x256 with square pad
    w, h = img.size
    max_dim = max(w, h)
    sq = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
    sq.paste(img, ((max_dim - w) // 2, (max_dim - h) // 2))
    sq_resized = sq.resize((64, 64), Image.Resampling.LANCZOS)
    sq_resized.save(tmp, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

if os.path.exists(tmp):
    if os.path.exists(dst):
        os.remove(dst)
    os.rename(tmp, dst)
    print(f"Optimized favicon.ico successfully! New size: {os.path.getsize(dst)} bytes")

