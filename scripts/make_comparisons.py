import os
import shutil
from PIL import Image, ImageDraw, ImageFont

artifact_dir = r"C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b"
os.makedirs(artifact_dir, exist_ok=True)

# 1. Copy all verification shots to artifact directory
for f in os.listdir("verification_shots"):
    if f.endswith(".png"):
        shutil.copy2(os.path.join("verification_shots", f), os.path.join(artifact_dir, f))
print("Copied verification shots to artifact directory.")

# 2. Side-by-side comparison images
pairs = [
    ("Intro Screen", "reference_dump/01_intro.png", "verification_shots/01_local_intro.png", "compare_intro.png"),
    ("Hero Section", "reference_dump/02_hero.png", "verification_shots/02_local_hero.png", "compare_hero.png"),
    ("Sweet Tray - Step 01 / 04 (Ghee)", "reference_dump/03_ritual_lift.png", "verification_shots/03_local_craft_ghee.png", "compare_sweet_tray_ghee.png"),
    ("Sweet Tray - Step 03 / 04 (Craft)", "reference_dump/05_ritual_pour.png", "verification_shots/05_local_craft_craft.png", "compare_sweet_tray_craft.png"),
    ("The Pack / Sweet Box", "reference_dump/07_pack.png", "verification_shots/08_local_pack.png", "compare_pack.png"),
    ("Heritage Craft", "reference_dump/09_estate_middle.png", "verification_shots/09_local_heritage.png", "compare_estate.png"),
    ("Footer", "reference_dump/10_footer.png", "verification_shots/10_local_footer.png", "compare_footer.png"),
    ("Mobile Layout (Sweet Tray 01/04)", "reference_dump/11_mobile_hero.png", "verification_shots/12_mobile_sweet_tray.png", "compare_mobile_sweet_tray.png"),
    ("Mobile Heritage Sweet-Making", "reference_dump/13_mobile_estate.png", "verification_shots/14_mobile_heritage.png", "compare_mobile_heritage.png"),
]

for title, ref_path, local_path, out_name in pairs:
    if not (os.path.exists(ref_path) and os.path.exists(local_path)):
        print(f"Skipping {title}: missing file")
        continue
        
    im_ref = Image.open(ref_path)
    im_loc = Image.open(local_path)
    
    h = 600
    w_ref = int(im_ref.width * h / im_ref.height)
    w_loc = int(im_loc.width * h / im_loc.height)
    
    im_ref_resized = im_ref.resize((w_ref, h), Image.Resampling.LANCZOS)
    im_loc_resized = im_loc.resize((w_loc, h), Image.Resampling.LANCZOS)
    
    header_h = 44
    combined = Image.new('RGB', (w_ref + w_loc + 10, h + header_h), (20, 10, 5))
    d = ImageDraw.Draw(combined)
    
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()
        
    d.text((20, 12), f"Reference: Filter Coffee ({title})", font=font, fill=(230, 191, 122))
    d.text((w_ref + 30, 12), f"Sri Amman Bakery: Recreated ({title})", font=font, fill=(230, 191, 122))
    
    combined.paste(im_ref_resized, (0, header_h))
    combined.paste(im_loc_resized, (w_ref + 10, header_h))
    
    out_path = os.path.join(artifact_dir, out_name)
    combined.save(out_path, "PNG")
    print(f"Created comparison: {out_name}")

print("All comparisons successfully created in artifact directory!")
