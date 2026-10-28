import cv2
import numpy as np

src_path = r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\traditional_sweet_maker_kadai_1793176239547.jpg'
img = cv2.imread(src_path)

# Draw 50px grid over x: 300..1100, y: 150..700
grid = img.copy()
for x in range(300, 1150, 50):
    cv2.line(grid, (x, 150), (x, 700), (0, 255, 0), 1)
    cv2.putText(grid, str(x), (x, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

for y in range(150, 750, 50):
    cv2.line(grid, (300, y), (1100, y), (0, 255, 0), 1)
    cv2.putText(grid, str(y), (310, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

cv2.imwrite("debug_grid.jpg", grid)
print("Saved debug_grid.jpg")

