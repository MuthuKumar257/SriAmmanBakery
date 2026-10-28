import cv2
import numpy as np
from scipy.interpolate import RBFInterpolator
import os
import math
import time

src_path = r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\traditional_sweet_maker_kadai_1793176239547.jpg'
orig = cv2.imread(src_path)
h, w, c = orig.shape

out_dir = r"public/stir_frames"
os.makedirs(out_dir, exist_ok=True)

TOTAL_FRAMES = 55
OUT_W, OUT_H = 1920, 1080

print(f"Generating {TOTAL_FRAMES} photorealistic stirring frames...")
print(f"Source size: {w}x{h}, Output size: {OUT_W}x{OUT_H}")

# 1. Base fixed control points
fixed_points = []
# Borders
for x in np.linspace(0, w, 9):
    fixed_points.append([x, 0])
    fixed_points.append([x, h])
for y in np.linspace(0, h, 7):
    fixed_points.append([0, y])
    fixed_points.append([w, y])

# Kadai handles & outer rim
fixed_points.extend([
    [100, 480], [140, 520], [170, 560], # Left handle & rim
    [210, 680], [350, 720], [550, 740], [750, 730], [900, 710], # Kadai bottom
    [990, 580], [1030, 480], # Right rim
    [520, 260], [680, 240], # Background behind kadai
    [1180, 70], [1320, 180], [1320, 500], # Craftsman torso & right side
    [180, 180], [380, 130], [780, 130], # Background pots
    [260, 420], [860, 390], # Mixture far edges
])

# 2. Moving control points on the original image
# Ladle bowl center: (450, 510)
# Handle neck: (535, 455)
# Mid-handle: (650, 385)
# Hand grip: (780, 320)
# Wrist wrap: (880, 240)
# Forearm mid: (1020, 180)

# Sweet mixture points around the bowl
mixture_ring = [
    [380, 510], [420, 460], [480, 450], [520, 490],
    [510, 560], [450, 570], [390, 560]
]

# Stove fire region control points (for subtle organic flicker)
fire_points = [
    [550, 710], [640, 690], [720, 700], [800, 715]
]

# Center and radius of the stirring elliptical orbit
C_x, C_y = 525, 500
R_x, R_y = 75, 32
theta_0 = math.atan2(510 - C_y, 450 - C_x)

grid_y, grid_x = np.mgrid[0:h:3, 0:w:3]
eval_pts = np.column_stack([grid_x.ravel(), grid_y.ravel()])

start_time = time.time()

for f in range(TOTAL_FRAMES):
    p = f / (TOTAL_FRAMES - 1)
    
    # Smooth continuous stirring cycle (1.25 complete revolutions)
    # Start at left, scoop deep through center-bottom, lift right, sweep back top
    theta = theta_0 + 2.0 * math.pi * (1.2 * p)
    
    # Target bowl position
    x_bowl = C_x + R_x * math.cos(theta)
    y_bowl = C_y + R_y * math.sin(theta)
    
    # Bowl displacement
    dx_bowl = x_bowl - 450
    dy_bowl = y_bowl - 510
    
    # Hand displacement (lever action with natural lag)
    hand_lag_theta = theta - 0.22
    x_hand_target = 780 + 35 * math.cos(hand_lag_theta)
    y_hand_target = 320 + 16 * math.sin(hand_lag_theta)
    dx_hand = x_hand_target - 780
    dy_hand = y_hand_target - 320
    
    # Build control point pairs
    src_pts = []
    dst_pts = []
    
    # Add fixed points
    for pt in fixed_points:
        src_pts.append(pt)
        dst_pts.append(pt)
        
    # Moving ladle points
    src_pts.append([450, 510])
    dst_pts.append([x_bowl, y_bowl])
    
    src_pts.append([535, 455])
    dst_pts.append([535 + dx_bowl * 0.75 + dx_hand * 0.25, 455 + dy_bowl * 0.75 + dy_hand * 0.25])
    
    src_pts.append([650, 385])
    dst_pts.append([650 + dx_bowl * 0.35 + dx_hand * 0.65, 385 + dy_bowl * 0.35 + dy_hand * 0.65])
    
    # Moving hand & arm
    src_pts.append([780, 320])
    dst_pts.append([x_hand_target, y_hand_target])
    
    src_pts.append([880, 240])
    dst_pts.append([880 + dx_hand * 0.65, 240 + dy_hand * 0.65])
    
    src_pts.append([1020, 180])
    dst_pts.append([1020 + dx_hand * 0.25, 180 + dy_hand * 0.25])
    
    # Moving sweet mixture points (viscous fluid drag)
    for mpt in mixture_ring:
        src_pts.append(mpt)
        dst_pts.append([mpt[0] + dx_bowl * 0.82, mpt[1] + dy_bowl * 0.82])
        
    # Fire flicker control
    flame_flicker = 3.5 * math.sin(2.0 * math.pi * 3.5 * p)
    for fpt in fire_points:
        src_pts.append(fpt)
        dst_pts.append([fpt[0] + flame_flicker * 0.5, fpt[1] + flame_flicker])
        
    src_arr = np.array(src_pts, dtype=np.float32)
    dst_arr = np.array(dst_pts, dtype=np.float32)
    
    # Compute smooth inverse deformation map
    rbf_x = RBFInterpolator(dst_arr, src_arr[:, 0], kernel='thin_plate_spline', smoothing=0.8)
    rbf_y = RBFInterpolator(dst_arr, src_arr[:, 1], kernel='thin_plate_spline', smoothing=0.8)
    
    map_x_coarse = rbf_x(eval_pts).reshape(grid_y.shape).astype(np.float32)
    map_y_coarse = rbf_y(eval_pts).reshape(grid_y.shape).astype(np.float32)
    
    map_x = cv2.resize(map_x_coarse, (w, h), interpolation=cv2.INTER_CUBIC)
    map_y = cv2.resize(map_y_coarse, (w, h), interpolation=cv2.INTER_CUBIC)
    
    warped = cv2.remap(orig, map_x, map_y, interpolation=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    
    # Subtle thermal color breathing on the firewood embers
    fire_glow = 1.0 + 0.06 * math.sin(2.0 * math.pi * 4.0 * p) + 0.03 * math.cos(2.0 * math.pi * 8.0 * p)
    fire_mask = np.zeros((h, w), dtype=np.float32)
    cv2.ellipse(fire_mask, (650, 710), (160, 45), 0, 0, 360, 1.0, -1)
    fire_mask = cv2.GaussianBlur(fire_mask, (41, 41), 0)[:, :, None]
    
    warped_f = warped.astype(np.float32)
    # Warm up fire region
    warped_f[:, :, 2] = np.clip(warped_f[:, :, 2] * (1.0 + fire_mask[:, :, 0] * (fire_glow - 1.0) * 1.4), 0, 255) # Red
    warped_f[:, :, 1] = np.clip(warped_f[:, :, 1] * (1.0 + fire_mask[:, :, 0] * (fire_glow - 1.0) * 0.7), 0, 255) # Green
    warped = warped_f.astype(np.uint8)
    
    # 3. Camera motion (smooth progressive push-in / zoom toward the mixture)
    # At p = 0.0: zoom = 1.0 (wide view showing full stove, embers, kadai)
    # At p = 1.0: zoom = 1.34 (close-up on rich bubbling golden halwa mixture & ladle)
    zoom = 1.0 + 0.34 * math.pow(p, 1.08)
    
    # Pan focus point: from center (w/2, h/2) smoothly tracking toward kadai center (560, 470)
    focus_x = w / 2.0 * (1.0 - p) + 570.0 * p
    focus_y = h / 2.0 * (1.0 - p) + 470.0 * p
    
    # Compute crop box based on zoom and focus
    crop_w = w / zoom
    crop_h = h / zoom
    
    x1 = int(round(focus_x - crop_w / 2.0))
    y1 = int(round(focus_y - crop_h / 2.0))
    x2 = int(round(x1 + crop_w))
    y2 = int(round(y1 + crop_h))
    
    # Clamp to image boundaries
    if x1 < 0:
        x2 -= x1
        x1 = 0
    if y1 < 0:
        y2 -= y1
        y1 = 0
    if x2 > w:
        x1 -= (x2 - w)
        x2 = w
    if y2 > h:
        y1 -= (y2 - h)
        y2 = h
        
    cropped = warped[y1:y2, x1:x2]
    final_frame = cv2.resize(cropped, (OUT_W, OUT_H), interpolation=cv2.INTER_CUBIC)
    
    # Save as high-quality WebP frame
    out_file = os.path.join(out_dir, f"frame_{f:03d}.webp")
    # Also save as JPEG for maximum fallback compatibility
    cv2.imwrite(out_file, final_frame, [cv2.IMWRITE_WEBP_QUALITY, 85])
    
    if f % 12 == 0 or f == TOTAL_FRAMES - 1:
        elapsed = time.time() - start_time
        print(f"Generated frame {f:02d}/{TOTAL_FRAMES} (p={p:.2f}, zoom={zoom:.2f}x) in {elapsed:.1f}s")

print(f"Successfully generated all {TOTAL_FRAMES} frames in {time.time() - start_time:.1f}s")

