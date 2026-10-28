import urllib.request
import os
from PIL import Image

os.makedirs('public/sweets', exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

candidates = {
    'laddu': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Laddu_3.jpg/800px-Laddu_3.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/A_view_of_Laddu.JPG/800px-A_view_of_Laddu.JPG',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Laddu%2C_a_famous_sweet_in_India.jpg/800px-Laddu%2C_a_famous_sweet_in_India.jpg'
    ],
    'mysore-pak': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Mysore_pak.jpg/800px-Mysore_pak.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Mysorepak.jpg/800px-Mysorepak.jpg'
    ],
    'jalebi': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/FOOD_Jalebi.jpg/800px-FOOD_Jalebi.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Jalebi_-_Closeup_View_of_Jalebis.JPG/800px-Jalebi_-_Closeup_View_of_Jalebis.JPG'
    ],
    'badam-burfi': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Badam_Barfi.jpg/800px-Badam_Barfi.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Barfi.JPG/800px-Barfi.JPG'
    ],
    'boost-burfi': [
        'https://shreemsweetsandbakery.com/wp-content/uploads/2021/02/Boost-Barfi-600x600.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Dodha_Burfi_-_Howrah_2016-01-26_9262.JPG/800px-Dodha_Burfi_-_Howrah_2016-01-26_9262.JPG'
    ],
    'horlicks-burfi': [
        'https://shreemsweetsandbakery.com/wp-content/uploads/2021/02/Horlicks-Barfi-600x600.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Besan_Ki_Barfi.JPG/800px-Besan_Ki_Barfi.JPG'
    ]
}

for name, urls in candidates.items():
    success = False
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                temp_file = f'public/sweets/{name}_raw.jpg'
                with open(temp_file, 'wb') as f:
                    f.write(data)
                
                # Verify and optimize image
                im = Image.open(temp_file)
                im = im.convert('RGB')
                
                # Resize to consistent 800x600 or 800x800 high quality
                w, h = im.size
                print(f"Downloaded {name} from {url} ({w}x{h})")
                
                # Crop to 4:3 or 1:1 aspect ratio
                target_w, target_h = 800, 600
                im_ratio = w / h
                target_ratio = target_w / target_h
                
                if im_ratio > target_ratio:
                    # wider than target
                    new_w = int(h * target_ratio)
                    left = (w - new_w) // 2
                    im = im.crop((left, 0, left + new_w, h))
                else:
                    new_h = int(w / target_ratio)
                    top = (h - new_h) // 2
                    im = im.crop((0, top, w, top + new_h))
                    
                im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
                final_path = f'public/sweets/{name}.jpg'
                im.save(final_path, 'JPEG', quality=90, optimize=True)
                print(f"Saved optimized {final_path} (800x600, {os.path.getsize(final_path)} bytes)")
                
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                success = True
                break
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    if not success:
        print(f"FAILED to fetch {name}!")

print("All sweets download check completed!")

