from PIL import Image, ImageFilter, ImageDraw
import numpy as np

def process_royal_platter():
    input_path = r"C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\royal_brass_sweet_platter_1793195738853.jpg"
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    arr = np.array(img, dtype=np.float32)

    # Estimate background from corners
    corners = np.vstack([arr[0:20, 0:20], arr[0:20, -20:], arr[-20:, 0:20], arr[-20:, -20:]])
    bg_color = np.median(corners.reshape(-1, 4), axis=0)[:3]
    print("Detected background color:", bg_color)

    # Color difference from background
    diff = np.linalg.norm(arr[:, :, :3] - bg_color, axis=2)

    # Threshold with smooth transition
    low_thresh = 18.0
    high_thresh = 36.0
    alpha = np.clip((diff - low_thresh) / (high_thresh - low_thresh), 0.0, 1.0) * 255.0

    # Also clean up stray pixels far outside platter ellipse
    cy, cx = h / 2, w / 2
    y, x = np.ogrid[:h, :w]
    # Elliptical distance
    ry, rx = h * 0.46, w * 0.49
    dist_ellipse = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
    outer_falloff = np.clip(1.0 - (dist_ellipse - 0.98) / 0.04, 0.0, 1.0)
    alpha = alpha * outer_falloff

    # Smooth the alpha mask
    mask_img = Image.fromarray(alpha.astype(np.uint8), mode="L")
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(1.2))

    # Decontaminate edge fringe
    edge_mask = np.array(mask_img, dtype=np.float32) / 255.0
    rgb = arr[:, :, :3].copy()
    # Where edge is semi-transparent, neutralize toward platter tone
    fringe = (edge_mask > 0.05) & (edge_mask < 0.95)
    rgb[fringe] = rgb[fringe] * 0.9

    isolated = Image.fromarray(np.dstack([rgb.astype(np.uint8), mask_img]), mode="RGBA")

    # Composite onto standard 1300x1100 tray canvas
    canvas_w, canvas_h = 1300, 1100
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)

    # Subtle warm contact ground shadow
    tray_cx, tray_cy = canvas_w // 2, canvas_h // 2 + 50
    shadow_rx, shadow_ry = 540, 220
    for r in range(shadow_rx, 0, -20):
        frac = 1.0 - (r / shadow_rx)
        s_alpha = int(90 * (frac ** 1.5))
        d.ellipse([tray_cx - r, tray_cy - int(r * (shadow_ry / shadow_rx)),
                   tray_cx + r, tray_cy + int(r * (shadow_ry / shadow_rx))],
                  fill=(15, 8, 4, s_alpha))

    # Resize platter to fit gracefully on canvas
    target_w = 1180
    target_h = int(h * target_w / w)
    resized_platter = isolated.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Paste platter centered
    paste_x = (canvas_w - target_w) // 2
    paste_y = (canvas_h - target_h) // 2 + 10
    canvas.paste(resized_platter, (paste_x, paste_y), resized_platter)

    # Sharpen slightly for crisp specular highlights on brass and sweets
    canvas = canvas.filter(ImageFilter.UnsharpMask(radius=1.8, percent=115, threshold=3))

    out_path = r"d:\Bakery\Website\public\sweet_tray.png"
    canvas.save(out_path, "PNG", optimize=True)
    import os
    print(f"Saved {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)")

if __name__ == "__main__":
    process_royal_platter()
