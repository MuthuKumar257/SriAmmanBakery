import cv2
import numpy as np
from scipy.interpolate import RBFInterpolator
import time

src_path = r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\traditional_sweet_maker_kadai_1793176239547.jpg'
orig = cv2.imread(src_path)
h, w, c = orig.shape

# Downscale slightly for fast test, or full res
# Let's test on full res or 0.5x
print(f"Testing RBF / MLS kinematic deformation on {w}x{h} image...")

# Define anchor points that must NEVER move:
# - Boundaries of the image
# - Outer kadai rim & handles
# - Distant background
# - Stove & firewood base
# - Craftsman's upper body / shoulder

fixed_points = []
# Borders
for x in np.linspace(0, w, 8):
    fixed_points.append([x, 0])
    fixed_points.append([x, h])
for y in np.linspace(0, h, 6):
    fixed_points.append([0, y])
    fixed_points.append([w, y])

# Kadai handles & outer rim
fixed_points.extend([
    [120, 480], [160, 520], [180, 560], # Left handle & rim
    [220, 680], [380, 720], [600, 730], [800, 710], # Kadai bottom
    [1000, 560], [1020, 480], # Right rim
    [580, 280], [650, 260], # Background behind kadai
    [1200, 80], [1300, 200], [1300, 500], # Craftsman torso & right side
    [200, 200], [400, 150], [800, 150], # Background pots
])

# Moving control points:
# In the original image:
# Ladle bowl center: (450, 510)
# Ladle bowl left: (390, 520)
# Ladle bowl right: (500, 490)
# Ladle neck: (540, 460)
# Ladle mid-handle: (650, 390)
# Hand grip: (780, 320)
# Wrist wrap: (880, 240)
# Forearm mid: (1020, 180)

# Sweet mixture points that swirl with the ladle:
# Nearby mixture points around the bowl
mix_points = [
    [400, 460], [480, 440], [540, 520], [460, 570], [380, 560]
]

# Let's test a stirring displacement:
# Suppose the ladle moves down and right by dx = +60, dy = +25 (plowing forward into the batter)
dx_stir = 60
dy_stir = 25

# Hand moves in sync, but smaller displacement due to lever arm:
dx_hand = dx_stir * 0.45
dy_hand = dy_stir * 0.45

src_pts = []
dst_pts = []

# Add fixed points
for pt in fixed_points:
    src_pts.append(pt)
    dst_pts.append(pt)

# Moving ladle points
ladle_pts = [
    [450, 510], [390, 520], [500, 490], [540, 460], [650, 390]
]
for pt in ladle_pts:
    src_pts.append(pt)
    dst_pts.append([pt[0] + dx_stir, pt[1] + dy_stir])

# Moving sweet mixture points (swirling alongside)
for pt in mix_points:
    src_pts.append(pt)
    dst_pts.append([pt[0] + dx_stir * 0.85, pt[1] + dy_stir * 0.85])

# Moving hand & wrist
src_pts.append([780, 320])
dst_pts.append([780 + dx_hand, 320 + dy_hand])

src_pts.append([880, 240])
dst_pts.append([880 + dx_hand * 0.6, 240 + dy_hand * 0.6])

src_pts.append([1020, 180])
dst_pts.append([1020 + dx_hand * 0.2, 180 + dy_hand * 0.2])

src_pts = np.array(src_pts, dtype=np.float32)
dst_pts = np.array(dst_pts, dtype=np.float32)

print(f"Total control points: {len(src_pts)}")

# Using Thin-Plate Spline or RBF
# We want mapping: (x_dst, y_dst) -> (x_src, y_src)
# So for every pixel in the destination image, we lookup the corresponding pixel in the source image!
rbf_x = RBFInterpolator(dst_pts, src_pts[:, 0], kernel='thin_plate_spline', smoothing=1.0)
rbf_y = RBFInterpolator(dst_pts, src_pts[:, 1], kernel='thin_plate_spline', smoothing=1.0)

# Create meshgrid
grid_y, grid_x = np.mgrid[0:h:2, 0:w:2]
eval_pts = np.column_stack([grid_x.ravel(), grid_y.ravel()])

print("Evaluating RBF interpolation on grid...")
t0 = time.time()
map_x_coarse = rbf_x(eval_pts).reshape(grid_y.shape).astype(np.float32)
map_y_coarse = rbf_y(eval_pts).reshape(grid_y.shape).astype(np.float32)
print(f"RBF eval time: {time.time() - t0:.2f}s")

# Upsample displacement map to full resolution
map_x = cv2.resize(map_x_coarse, (w, h), interpolation=cv2.INTER_CUBIC)
map_y = cv2.resize(map_y_coarse, (w, h), interpolation=cv2.INTER_CUBIC)

# Remap image
warped = cv2.remap(orig, map_x, map_y, interpolation=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)

cv2.imwrite("debug_rbf_stir_test.jpg", warped)
print("Saved debug_rbf_stir_test.jpg")

