import cv2
import numpy as np

src_path = r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\traditional_sweet_maker_kadai_1793176239547.jpg'
img = cv2.imread(src_path)
h, w, _ = img.shape

# Mask for the ladle bowl and lower handle
mask = np.zeros((h, w), dtype=np.uint8)

# Ladle head bowl
cv2.circle(mask, (355, 575), 65, 255, -1)
cv2.ellipse(mask, (370, 570), (75, 60), 0, 0, 360, 255, -1)

# Lower handle near bowl
pts = np.array([[380, 570], [450, 530], [530, 480], [545, 500], [460, 555], [390, 595]], np.int32)
cv2.fillPoly(mask, [pts], 255)

# Inpaint using Telea and Navier-Stokes
inpaint_telea = cv2.inpaint(img, mask, 15, cv2.INPAINT_TELEA)

# Also let's synthesize organic sweet texture from the surrounding mixture
# Sample authentic mixture from x: 480..680, y: 520..640
sample_texture = img[520:640, 480:600]
h_t, w_t, _ = sample_texture.shape

# Seamless clone or texture synthesis onto the mask area
blend = inpaint_telea.copy()

# Add subtle ghee gloss and micro-texture
noise = np.random.normal(0, 3, (h, w, 3)).astype(np.float32)
blend_f = np.clip(blend.astype(np.float32) + noise * (mask[:, :, None] / 255.0), 0, 255).astype(np.uint8)

cv2.imwrite("debug_inpainted_mixture.jpg", blend_f)
print("Saved debug_inpainted_mixture.jpg")

