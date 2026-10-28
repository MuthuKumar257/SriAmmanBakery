from PIL import Image, ImageDraw, ImageFont

# Let's test the layout dimensions mathematically on 1440x900
W, H = 1440, 900
pad = 60
cup_w = 380 # clamp(260px, 26vw, 380px)

center_x = W / 2
cup_left = center_x - cup_w / 2 # 720 - 190 = 530
cup_right = center_x + cup_w / 2 # 720 + 190 = 910

clearance = 28
w1_right = cup_left - clearance # 530 - 28 = 502
w2_left = cup_right + clearance # 910 + 28 = 938

left_avail = w1_right - pad # 502 - 60 = 442px
right_avail = (W - pad) - w2_left # 1380 - 938 = 442px

print(f"Viewport: {W}x{H}")
print(f"Cup width: {cup_w}px (from {cup_left} to {cup_right})")
print(f"Left available space for 'Sri Amman': {left_avail}px (from {pad} to {w1_right})")
print(f"Right available space for 'Bakery': {right_avail}px (from {w2_left} to {W - pad})")
print(f"Symmetry: left_avail == right_avail -> {left_avail == right_avail}")

