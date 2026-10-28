from PIL import Image, ImageDraw
import numpy as np

img = Image.open(r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\traditional_sweet_maker_kadai_1793176239547.jpg')
w, h = img.size

# Let's mark reference points to locate the ladle head, handle, hand, and kadai
# We can draw crosshairs on a debug copy to precisely verify pixel positions
debug = img.copy()
d = ImageDraw.Draw(debug)

# Estimated points:
# Ladle head: (470, 480)
# Ladle neck: (560, 430)
# Hand wrist: (860, 280)
# Kadai center: (580, 520)
# Kadai left rim: (180, 500)
# Kadai right rim: (980, 520)
# Fire: (750, 700)

points = [
    ("Ladle Head", 470, 480, "red"),
    ("Ladle Neck", 560, 430, "yellow"),
    ("Hand/Wrist", 860, 280, "cyan"),
    ("Forearm Base", 1200, 150, "magenta"),
    ("Kadai Center", 580, 520, "green"),
    ("Kadai Left", 180, 500, "blue"),
    ("Kadai Right", 980, 520, "blue"),
]

for name, x, y, col in points:
    d.line([x - 20, y, x + 20, y], fill=col, width=3)
    d.line([x, y - 20, x, y + 20], fill=col, width=3)
    d.text((x + 10, y - 10), name, fill="white")

debug.save("debug_points.jpg", quality=90)
print("Saved debug_points.jpg")

