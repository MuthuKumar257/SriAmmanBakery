import math
import os
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import imageio.v3 as iio
import imageio_ffmpeg

def generate_video():
    print("=== Generating Traditional Sweet-Making Cinematic Animation ===")
    w, h = 1280, 854
    total_frames = 192  # 8.0 seconds at 24 fps (exact seamless loop)
    fps = 24
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"Using FFmpeg: {ffmpeg_exe}")
    
    # Pre-render stationary atmospheric background (workshop, stone walls, chulha structure)
    print("Pre-rendering background architecture...")
    bg = Image.new('RGBA', (w, h), (18, 9, 4, 255))
    bg_draw = ImageDraw.Draw(bg)
    
    # 1. Distant dark stone & brick wall
    for y in range(0, h, 28):
        offset = 18 if (y // 28) % 2 == 1 else 0
        for x in range(-20, w + 40, 60):
            # stone block
            tone = int(14 + ((x * 13 + y * 7) % 15))
            r = tone + 6
            g = tone
            b = tone - 4
            bg_draw.rectangle([x + offset, y, x + offset + 56, y + 25], fill=(r, g, b, 255))
            bg_draw.rectangle([x + offset, y, x + offset + 56, y + 25], outline=(10, 5, 2, 200), width=1)
            
    # Soft background lighting: antique brass vessels in the distant alcove
    # Shelf at y = 140
    bg_draw.rectangle([60, 170, 480, 185], fill=(26, 14, 6, 255))
    # Brass pots on shelf
    for bx, bw, bh in [(100, 50, 40), (180, 70, 55), (280, 45, 60), (360, 80, 45)]:
        bg_draw.ellipse([bx, 170 - bh, bx + bw, 170 + bh//3], fill=(70, 48, 18, 255), outline=(110, 80, 32, 255))
        bg_draw.ellipse([bx + bw//4, 170 - bh + 5, bx + bw*3//4, 170 - bh + 15], fill=(130, 95, 40, 255))
        
    # Stone floor at bottom
    floor_y = 660
    bg_draw.rectangle([0, floor_y, w, h], fill=(22, 12, 6, 255))
    for fx in range(-50, w + 100, 160):
        bg_draw.line([fx, floor_y, fx - 100, h], fill=(12, 6, 2, 255), width=2)
    for fy in range(floor_y, h, 45):
        bg_draw.line([0, fy, w, fy], fill=(14, 7, 3, 255), width=2)

    # 2. Traditional Terracotta Mud & Brick Chulha (Stove) Base
    # Center around cx = 520, cy = 600
    st_cx = 520
    # Clay hearth outer mound
    bg_draw.ellipse([st_cx - 360, 500, st_cx + 360, 740], fill=(55, 26, 12, 255), outline=(32, 14, 6, 255), width=4)
    bg_draw.ellipse([st_cx - 320, 530, st_cx + 320, 720], fill=(42, 19, 8, 255))
    
    # Fire combustion cavity opening (dark arch)
    bg_draw.ellipse([st_cx - 240, 560, st_cx + 240, 710], fill=(16, 7, 2, 255))
    
    # Firewood logs placed inside stove
    # Log 1: angled left
    bg_draw.line([st_cx - 200, 680, st_cx - 40, 610], fill=(30, 16, 8, 255), width=28)
    bg_draw.ellipse([st_cx - 215, 665, st_cx - 185, 695], fill=(45, 24, 12, 255), outline=(15, 8, 3, 255))
    # Log 2: angled right
    bg_draw.line([st_cx + 200, 680, st_cx + 40, 610], fill=(26, 14, 6, 255), width=26)
    bg_draw.ellipse([st_cx + 185, 665, st_cx + 215, 695], fill=(40, 20, 10, 255), outline=(15, 8, 3, 255))
    # Log 3: center cross log
    bg_draw.line([st_cx - 140, 640, st_cx + 150, 645], fill=(34, 18, 9, 255), width=24)
    # Charred wood ends
    for ch_x, ch_y in [(st_cx - 30, 615), (st_cx + 20, 620), (st_cx, 635)]:
        bg_draw.ellipse([ch_x - 12, ch_y - 8, ch_x + 12, ch_y + 8], fill=(12, 5, 2, 255))

    bg_blurred = bg.filter(ImageFilter.GaussianBlur(1.2))
    bg_np = np.array(bg_blurred)
    
    print("Synthesizing cinematic sweet-making animation frames...")
    frames_rgb = []
    
    kadai_cx = 520
    kadai_cy = 460
    kadai_rx = 340
    kadai_ry = 140
    
    for f in range(total_frames):
        tau = (2.0 * math.pi * f) / total_frames
        
        frame = Image.fromarray(bg_np.copy())
        d = ImageDraw.Draw(frame, 'RGBA')
        
        # -------------------------------------------------------------
        # 1. Fireplace Glow & Ember Bed (Harmonic breathing)
        # -------------------------------------------------------------
        ember_pulse = 0.82 + 0.14 * math.sin(2 * tau) + 0.08 * math.cos(5 * tau)
        
        # Deep glowing charcoal bed under the logs
        for er in range(180, 0, -18):
            efact = (1.0 - er / 180.0) * ember_pulse
            er_col = (int(255 * efact), int(80 * efact), int(10 * efact), int(120 * efact))
            d.ellipse([st_cx - er, 630 - int(er * 0.35), st_cx + er, 630 + int(er * 0.35)], fill=er_col)
            
        # Hot white-gold ember hotspots
        for hx, hy in [(st_cx - 60, 635), (st_cx + 50, 638), (st_cx - 10, 625), (st_cx + 20, 645)]:
            h_pulse = 0.7 + 0.3 * math.sin(tau * 3 + hx)
            d.ellipse([hx - 14, hy - 8, hx + 14, hy + 8], fill=(255, int(200 * h_pulse), int(60 * h_pulse), int(220 * h_pulse)))

        # -------------------------------------------------------------
        # 2. Dynamic Dancing Firewood Flames (Harmonic loops)
        # -------------------------------------------------------------
        flame_count = 14
        for fi in range(flame_count):
            fx_rel = (fi - flame_count / 2) / (flame_count / 2)
            fx_base = st_cx + fx_rel * 180
            fy_base = 635 - int(abs(fx_rel) * 20)
            
            # Harmonic height and lateral curl
            fh_base = 120 + 45 * math.cos(fx_rel * 2)
            fh = fh_base + 35 * math.sin(tau * 4 + fi * 1.3) + 20 * math.cos(tau * 7 + fi * 2.1)
            f_sway = 18 * math.sin(tau * 3 + fi * 0.9) + 10 * math.cos(tau * 6 + fi * 1.5)
            
            # Flame tongue curve
            tip_x = fx_base + f_sway
            tip_y = fy_base - fh
            
            # Flame outer envelope (amber-orange)
            d.polygon([
                (fx_base - 22, fy_base),
                (fx_base - 14, fy_base - fh * 0.45),
                (tip_x, tip_y),
                (fx_base + 14, fy_base - fh * 0.45),
                (fx_base + 22, fy_base)
            ], fill=(255, 95, 10, int(150 * ember_pulse)))
            
            # Flame bright inner core (white-yellow)
            d.polygon([
                (fx_base - 10, fy_base),
                (fx_base - 6, fy_base - fh * 0.3),
                (tip_x * 0.7 + fx_base * 0.3, tip_y + fh * 0.25),
                (fx_base + 6, fy_base - fh * 0.3),
                (fx_base + 10, fy_base)
            ], fill=(255, 230, 110, int(210 * ember_pulse)))

        # -------------------------------------------------------------
        # 3. Rising Fire Sparks / Embers
        # -------------------------------------------------------------
        for si in range(28):
            s_phase = (tau + si * (2.0 * math.pi / 28.0)) % (2.0 * math.pi)
            s_prog = s_phase / (2.0 * math.pi) # 0 to 1
            sx = st_cx + math.sin(s_prog * 4 + si * 1.7) * (140 + si * 6) + math.sin(tau * 2 + si) * 25
            sy = 630 - s_prog * 340
            s_alpha = int(240 * math.sin(s_prog * math.pi))
            sr = 2 + (si % 3)
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 180, 50, s_alpha))

        # -------------------------------------------------------------
        # 4. Massive Traditional Metal Kadai (Wok)
        # -------------------------------------------------------------
        # Kadai outer iron bowl
        d.ellipse([kadai_cx - kadai_rx, kadai_cy - kadai_ry, kadai_cx + kadai_rx, kadai_cy + kadai_ry],
                  fill=(22, 13, 7, 255), outline=(60, 36, 16, 255), width=6)
                  
        # Firelight reflection across curved bottom rim
        fire_spec_alpha = int(140 * ember_pulse)
        d.arc([kadai_cx - kadai_rx, kadai_cy - kadai_ry, kadai_cx + kadai_rx, kadai_cy + kadai_ry],
              20, 160, fill=(245, 140, 30, fire_spec_alpha), width=10)
        d.arc([kadai_cx - kadai_rx + 10, kadai_cy - kadai_ry + 10, kadai_cx + kadai_rx - 10, kadai_cy + kadai_ry - 10],
              35, 145, fill=(255, 195, 60, int(fire_spec_alpha * 0.8)), width=5)

        # Heavy forged metal ring handles
        # Left handle
        d.ellipse([kadai_cx - kadai_rx - 28, kadai_cy - 20, kadai_cx - kadai_rx + 12, kadai_cy + 30],
                  fill=(30, 18, 9, 255), outline=(80, 52, 22, 255), width=5)
        # Right handle
        d.ellipse([kadai_cx + kadai_rx - 12, kadai_cy - 20, kadai_cx + kadai_rx + 28, kadai_cy + 30],
                  fill=(30, 18, 9, 255), outline=(80, 52, 22, 255), width=5)

        # -------------------------------------------------------------
        # 5. Boiling & Simmering Sweet Mixture Inside the Kadai
        # -------------------------------------------------------------
        # Inner sweet pool (slow-simmering ghee, besan & saffron)
        sw_rx = kadai_rx - 22
        sw_ry = kadai_ry - 22
        d.ellipse([kadai_cx - sw_rx, kadai_cy - sw_ry, kadai_cx + sw_rx, kadai_cy + sw_ry],
                  fill=(135, 75, 16, 255))
                  
        # Concentric liquid heat gradients (golden-amber core)
        for step in range(30, 180, 25):
            crx = sw_rx - step
            cry = int(crx * (sw_ry / sw_rx))
            if crx > 20:
                c_alpha = 110 + int(35 * math.sin(tau * 3 + step))
                d.ellipse([kadai_cx - crx, kadai_cy - cry, kadai_cx + crx, kadai_cy + cry],
                          fill=(195, 115, 28, c_alpha))

        # Golden ghee shimmer ripples following the stirring vortex
        vortex_phase = tau * 4
        for vi in range(12):
            v_angle = vortex_phase + vi * (math.pi / 6)
            vr = 110 + 60 * math.sin(v_angle * 0.5)
            vx = kadai_cx + math.cos(v_angle) * vr
            vy = kadai_cy + math.sin(v_angle) * (vr * 0.4)
            d.arc([vx - 25, vy - 10, vx + 25, vy + 10], 0, 180, fill=(255, 210, 95, 160), width=3)

        # Simmering ghee bubbles
        for bi in range(18):
            b_phase = (tau * 3 + bi * 1.4) % (2.0 * math.pi)
            b_scale = math.sin(b_phase)
            if b_scale > 0:
                bx = kadai_cx + math.sin(bi * 2.3) * (sw_rx * 0.72)
                by = kadai_cy + math.cos(bi * 1.9) * (sw_ry * 0.65)
                br = int(4 + 8 * b_scale)
                d.ellipse([bx - br, by - br * 0.5, bx + br, by + br * 0.5],
                          fill=(245, 175, 50, int(180 * b_scale)), outline=(255, 240, 160, int(220 * b_scale)), width=1)

        # -------------------------------------------------------------
        # 6. The Sweet Maker (Halwai) & Ladle Stirring Kinematics
        # -------------------------------------------------------------
        # Stirring motion: 2 complete elliptical sweeps in 8 seconds
        stir_theta = tau * 2.0
        
        # Ladle contact point inside kadai
        ladle_tip_x = kadai_cx + math.cos(stir_theta) * (sw_rx * 0.62)
        ladle_tip_y = kadai_cy + math.sin(stir_theta) * (sw_ry * 0.55) - 10
        
        # Sweet maker hand position
        hand_x = 940 + math.cos(stir_theta) * 35
        hand_y = 380 + math.sin(stir_theta) * 25
        
        # Sweet maker body anatomy (standing beside the kadai)
        # Body sway
        body_sway_x = math.cos(stir_theta) * 8
        body_sway_y = math.sin(stir_theta) * 5
        
        # Artisan Torso (traditional cream cotton kurta)
        torso_x = 980 + body_sway_x
        torso_y = 340 + body_sway_y
        
        # Head / face profile
        d.ellipse([torso_x - 38, torso_y - 120, torso_x + 38, torso_y - 45], fill=(85, 48, 22, 255))
        # Hair / traditional cloth headwrap
        d.ellipse([torso_x - 42, torso_y - 132, torso_x + 36, torso_y - 95], fill=(30, 16, 8, 255))
        # Forehead & nose profile
        d.polygon([(torso_x - 30, torso_y - 90), (torso_x - 46, torso_y - 75), (torso_x - 30, torso_y - 65)], fill=(92, 54, 25, 255))
        
        # Warm firelight rim on face from below
        face_light = int(120 * ember_pulse)
        d.arc([torso_x - 38, torso_y - 118, torso_x + 38, torso_y - 45], 80, 190, fill=(245, 160, 60, face_light), width=4)

        # Torso & Shoulders
        d.polygon([
            (torso_x - 65, torso_y - 45),
            (torso_x + 75, torso_y - 40),
            (torso_x + 60, torso_y + 190),
            (torso_x - 55, torso_y + 190)
        ], fill=(165, 140, 105, 255)) # Cream khadi kurta
        
        # Saffron gamcha draped over left shoulder
        d.polygon([
            (torso_x - 68, torso_y - 45),
            (torso_x - 35, torso_y - 45),
            (torso_x - 25, torso_y + 150),
            (torso_x - 50, torso_y + 150)
        ], fill=(210, 95, 25, 255))
        
        # Firelight dynamic sheen on kurta
        d.polygon([
            (torso_x - 58, torso_y - 20),
            (torso_x - 20, torso_y - 15),
            (torso_x - 20, torso_y + 120),
            (torso_x - 50, torso_y + 120)
        ], fill=(235, 145, 50, int(75 * ember_pulse)))

        # Arms holding the long metal ladle
        # Right arm reaching forward
        d.line([torso_x - 45, torso_y + 5, hand_x - 20, hand_y + 10], fill=(85, 48, 22, 255), width=24)
        # Left arm bracing
        d.line([torso_x - 10, torso_y + 15, hand_x + 30, hand_y], fill=(78, 44, 20, 255), width=20)
        # Hands gripping the handle
        d.ellipse([hand_x - 28, hand_y - 8, hand_x + 38, hand_y + 26], fill=(95, 54, 25, 255), outline=(50, 28, 12, 255), width=2)
        
        # Firelight highlight on artisan hands
        d.arc([hand_x - 28, hand_y - 8, hand_x + 38, hand_y + 26], 100, 230, fill=(255, 185, 75, face_light), width=3)

        # -------------------------------------------------------------
        # 7. Long Forged Metal Ladle (Jhala / Palta)
        # -------------------------------------------------------------
        # Ladle handle extends from hands into the kadai
        d.line([hand_x + 120, hand_y - 90, ladle_tip_x, ladle_tip_y], fill=(75, 68, 62, 255), width=9)
        d.line([hand_x + 120, hand_y - 90, ladle_tip_x, ladle_tip_y], fill=(180, 160, 130, 200), width=2) # Specular ridge
        
        # Broad metal stirring paddle/blade at the tip
        paddle_angle = math.atan2(ladle_tip_y - hand_y, ladle_tip_x - hand_x) + math.pi / 2
        p_len = 36
        p_dx = math.cos(paddle_angle) * p_len
        p_dy = math.sin(paddle_angle) * p_len
        d.line([ladle_tip_x - p_dx, ladle_tip_y - p_dy, ladle_tip_x + p_dx, ladle_tip_y + p_dy], fill=(95, 88, 80, 255), width=18)
        
        # Viscous golden sweet batter cascading off the paddle as it folds
        cascade_lift = max(0, -math.sin(stir_theta)) # When paddle lifts
        if cascade_lift > 0.15:
            d_alpha = int(220 * cascade_lift)
            # Golden cascade stream
            d.line([ladle_tip_x, ladle_tip_y, ladle_tip_x - 15, ladle_tip_y + 35], fill=(245, 175, 45, d_alpha), width=7)
            d.ellipse([ladle_tip_x - 22, ladle_tip_y + 30, ladle_tip_x - 8, ladle_tip_y + 46], fill=(255, 215, 80, d_alpha))

        # -------------------------------------------------------------
        # 8. Delicate Wood Smoke & Cardamom Steam (Seamless harmonic advection)
        # -------------------------------------------------------------
        for smi in range(24):
            sm_phase = (tau + smi * (2.0 * math.pi / 24.0)) % (2.0 * math.pi)
            sm_prog = sm_phase / (2.0 * math.pi) # 0 to 1
            sm_x = kadai_cx - 60 + math.sin(sm_prog * 3 + smi * 1.5) * 85 - sm_prog * 80
            sm_y = 440 - sm_prog * 380
            sm_rad = int(30 + sm_prog * 120)
            sm_alpha = int(45 * math.sin(sm_prog * math.pi))
            
            d.ellipse([sm_x - sm_rad, sm_y - int(sm_rad * 0.45), sm_x + sm_rad, sm_y + int(sm_rad * 0.45)],
                      fill=(180, 160, 140, sm_alpha))

        # Final soft lens blur for cinematic warmth
        frame_blurred = frame.filter(ImageFilter.GaussianBlur(0.6))
        frames_rgb.append(np.array(frame_blurred.convert('RGB')))
        
        if f % 40 == 0:
            print(f"Rendered frame {f}/{total_frames} ({int(f/total_frames*100)}%)")

    # 1. Save Poster Image (frame 0)
    poster_path = 'public/estate_craft_poster.jpg'
    Image.fromarray(frames_rgb[0]).save(poster_path, 'JPEG', quality=92)
    print(f"Saved poster image: {poster_path}")
    
    # Also save as public/estate_craft.jpg for fallback
    Image.fromarray(frames_rgb[0]).save('public/estate_craft.jpg', 'JPEG', quality=92)

    # 2. Encode WebM Video (libvpx-vp9)
    webm_path = 'public/estate_craft.webm'
    print(f"Encoding seamless WebM video ({webm_path})...")
    # Use imageio to write frames to mp4 first then convert, or use ffmpeg directly via pipe
    # Direct ffmpeg pipe for optimal quality and small file size
    mp4_path = 'public/estate_craft.mp4'
    
    print("Writing MP4 with imageio...")
    iio.imwrite(mp4_path, frames_rgb, fps=fps, codec='libx264')
    print(f"Saved {mp4_path} ({os.path.getsize(mp4_path)} bytes)")
    
    # Convert MP4 to highly compressed WebM using the detected ffmpeg executable
    print(f"Converting to WebM with {ffmpeg_exe}...")
    cmd_webm = [
        ffmpeg_exe, '-y',
        '-i', mp4_path,
        '-c:v', 'libvpx-vp9',
        '-b:v', '1200k',
        '-crf', '32',
        '-pix_fmt', 'yuv420p',
        '-an', # no audio
        webm_path
    ]
    res = subprocess.run(cmd_webm, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Saved {webm_path} ({os.path.getsize(webm_path)} bytes)")
    else:
        print("WebM conversion warning, trying standard vp8...")
        cmd_vp8 = [
            ffmpeg_exe, '-y',
            '-i', mp4_path,
            '-c:v', 'libvpx',
            '-b:v', '1000k',
            '-pix_fmt', 'yuv420p',
            '-an',
            webm_path
        ]
        subprocess.run(cmd_vp8, capture_output=True)
        print(f"Saved {webm_path} via vp8 ({os.path.getsize(webm_path)} bytes)")

    print("=== Sweet-Making Animation Generation Complete! ===")

if __name__ == '__main__':
    generate_video()
