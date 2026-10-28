import cv2
import numpy as np

img = cv2.imread(r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\traditional_sweet_maker_kadai_1793176239547.jpg')

# Probe points from (300, 600) to (800, 300)
p1 = np.array([250, 630])
p2 = np.array([850, 270])

vis = img.copy()
for t in np.linspace(0, 1, 13):
    pt = (p1 * (1 - t) + p2 * t).astype(int)
    cv2.circle(vis, tuple(pt), 6, (0, 255, 255), -1)
    cv2.putText(vis, f"{pt[0]},{pt[1]}", (pt[0] + 8, pt[1] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

cv2.imwrite("debug_probe_line.jpg", vis)
print("Saved debug_probe_line.jpg")

