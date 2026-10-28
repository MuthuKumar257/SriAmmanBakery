import numpy as np
from PIL import Image, ImageFilter
import cv2

# Load original high-res photograph
src_path = r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\traditional_sweet_maker_kadai_1793176239547.jpg'
img = cv2.imread(src_path)
h, w, c = img.shape
print(f"Loaded image: {w}x{h}, {c} channels")

# Let's inspect the ladle head region:
# Ladle head is roughly in x: 370..550, y: 500..670
# Handle is in x: 500..850, y: 350..580
# Hand is in x: 740..980, y: 220..420
# Kadai sweet mixture is in x: 230..940, y: 400..690

# Let's create a mask of the ladle + hand to see its boundaries
mask_ladle = np.zeros((h, w), dtype=np.uint8)

# Polygon roughly around the ladle head and handle
pts_ladle_head = np.array([[380, 520], [420, 500], [530, 510], [560, 570], [550, 650], [450, 670], [380, 620]], np.int32)
cv2.fillPoly(mask_ladle, [pts_ladle_head], 255)

# Handle
pts_handle = np.array([[510, 560], [560, 520], [860, 320], [840, 360]], np.int32)
cv2.fillPoly(mask_ladle, [pts_handle], 255)

# Save mask visualization
vis = img.copy()
vis[mask_ladle > 0] = vis[mask_ladle > 0] * 0.5 + np.array([0, 0, 255]) * 0.5
cv2.imwrite("debug_ladle_mask.jpg", vis)
print("Saved debug_ladle_mask.jpg")

