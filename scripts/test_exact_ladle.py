import cv2
import numpy as np

img = cv2.imread(r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\traditional_sweet_maker_kadai_1793176239547.jpg')
h, w, _ = img.shape

# Let's draw an ellipse at y: 580, x: 350
test_vis = img.copy()
cv2.ellipse(test_vis, (340, 580), (60, 60), 0, 0, 360, (0, 0, 255), 3)

# Handle line from (340, 580) to (760, 310)
cv2.line(test_vis, (340, 580), (760, 310), (0, 255, 0), 3)

cv2.imwrite("debug_exact_ladle.jpg", test_vis)
print("Saved debug_exact_ladle.jpg")

