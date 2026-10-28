import cv2
import numpy as np
from PIL import Image

src_path = r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\traditional_sweet_maker_kadai_1793176239547.jpg'
img = cv2.imread(src_path)
h, w, c = img.shape

# 1. Create precise mask for the ladle bowl and handle
# Ladle bowl is in x: 380..540, y: 340..490
# Center of bowl is approx (465, 415)
# Neck is at (535, 385)
# Handle runs from (535, 385) to (790, 275)

# Let's verify mask
mask_bowl = np.zeros((h, w), dtype=np.uint8)
cv2.ellipse(mask_bowl, (465, 415), (75, 70), -15, 0, 360, 255, -1)

# Handle mask
pts_handle = np.array([
    [520, 400], [550, 370],
    [800, 260], [780, 290]
], np.int32)
cv2.fillPoly(mask_bowl, [pts_handle], 255)

# Clean inpainting of the sweet mixture underneath the ladle
# We inpaint the ladle bowl area so we have a clean background plate with only sweet mixture
inpaint_mask = cv2.dilate(mask_bowl, np.ones((11, 11), np.uint8))
bg_plate = cv2.inpaint(img, inpaint_mask, 21, cv2.INPAINT_TELEA)

# Texture patch blending: take rich sweet mixture texture from x: 550..750, y: 360..520
# and blend it into the inpainted area with seamless Poisson / alpha blending
sample_sweet = img[380:480, 580:680].copy()
sh_h, sh_w, _ = sample_sweet.shape

# Blend texture into the bowl area
patch_y1, patch_y2 = 360, 460
patch_x1, patch_x2 = 415, 515
alpha_blend = (mask_bowl[patch_y1:patch_y2, patch_x1:patch_x2].astype(np.float32) / 255.0)[:, :, None]
bg_plate[patch_y1:patch_y2, patch_x1:patch_x2] = (
    bg_plate[patch_y1:patch_y2, patch_x1:patch_x2] * (1.0 - alpha_blend * 0.7) +
    sample_sweet * (alpha_blend * 0.7)
).astype(np.uint8)

cv2.imwrite("debug_bg_plate.jpg", bg_plate)
print("Saved debug_bg_plate.jpg")

