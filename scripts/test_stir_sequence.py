import cv2
import numpy as np
import math

src_path = r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\traditional_sweet_maker_kadai_1793176239547.jpg'
orig = cv2.imread(src_path)
h, w, c = orig.shape

# 1. Isolate the Ladle + Hand element from the original image
# Ladle bowl: center (450, 510), radius ~70
# Handle: from (500, 480) to (800, 300)
# Hand: around (750..920, 200..360)
# Forearm: around (880..1150, 120..280)

# Create a clean alpha mask for the moving component (ladle + hand + forearm)
mask_mover = np.zeros((h, w), dtype=np.float32)

# Bowl
cv2.circle(mask_mover, (450, 510), 68, 1.0, -1)
cv2.ellipse(mask_mover, (460, 510), (75, 65), -15, 0, 360, 1.0, -1)

# Handle
pts_handle = np.array([[480, 520], [520, 460], [820, 275], [780, 325]], np.int32)
cv2.fillPoly(mask_mover, [pts_handle], 1.0)

# Hand
pts_hand = np.array([
    [710, 340], [750, 280], [790, 230], [870, 190],
    [930, 220], [940, 260], [890, 320], [820, 380], [740, 390]
], np.int32)
cv2.fillPoly(mask_mover, [pts_hand], 1.0)

# Forearm
pts_forearm = np.array([
    [870, 190], [1050, 130], [1250, 100], [1280, 220],
    [1080, 240], [930, 260], [890, 320]
], np.int32)
cv2.fillPoly(mask_mover, [pts_forearm], 1.0)

# Soft feathering of the mover mask
mask_mover = cv2.GaussianBlur(mask_mover, (15, 15), 0)

# 2. Inpaint the background plate where the ladle was originally sitting
# Mask for inpainting: only the bowl and lower handle inside the sweet mixture
mask_inpaint = np.zeros((h, w), dtype=np.uint8)
cv2.circle(mask_inpaint, (450, 510), 80, 255, -1)
cv2.fillPoly(mask_inpaint, [np.array([[460, 540], [530, 450], [620, 410], [580, 480]], np.int32)], 255)
mask_inpaint = cv2.dilate(mask_inpaint, np.ones((7, 7), np.uint8))

bg_plate = cv2.inpaint(orig, mask_inpaint, 18, cv2.INPAINT_TELEA)

# Texture patch from adjacent authentic sweet mixture (x: 580..720, y: 460..580)
texture_patch = orig[460:580, 580:700].copy()
patch_mask = (mask_inpaint[460:580, 390:510].astype(np.float32) / 255.0)[:, :, None]
bg_plate[460:580, 390:510] = (
    bg_plate[460:580, 390:510] * (1.0 - patch_mask * 0.75) +
    texture_patch[0:120, 0:120] * (patch_mask * 0.75)
).astype(np.uint8)

cv2.imwrite("debug_clean_plate.jpg", bg_plate)
print("Saved debug_clean_plate.jpg")

