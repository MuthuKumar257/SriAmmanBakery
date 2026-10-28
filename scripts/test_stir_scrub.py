import time
import os
import shutil
from playwright.sync_api import sync_playwright

os.makedirs('verification_shots', exist_ok=True)
artifact_dir = r"C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b"

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            headless=True
        )
        
        # 1. Desktop Test (1440 x 900)
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        
        failed_requests = []
        page.on("requestfailed", lambda req: failed_requests.append(f"{req.method} {req.url}: {req.failure}"))
        
        print("Navigating to Sri Amman Bakery site...")
        page.goto("http://localhost:3000", wait_until="networkidle")
        
        # Skip intro
        skip_btn = page.query_selector("button:has-text('Skip intro')")
        if skip_btn:
            skip_btn.click()
            time.sleep(2.5)
            
        print("Scrolling to #heritage (Our Story sweet-making section)...")
        page.evaluate("document.getElementById('heritage').scrollIntoView()")
        time.sleep(1.2)
        
        # Capture scroll position 1: Entrance / Arch Expansion (p ~ 0.05)
        page.screenshot(path="verification_shots/stir_01_entrance.png")
        print("Captured stir_01_entrance.png (p ~ 0.05)")
        
        # Scroll forward: p ~ 0.35 (ladle scooping forward into golden batter)
        page.evaluate("window.scrollBy(0, 750)")
        time.sleep(1.0)
        page.screenshot(path="verification_shots/stir_02_scoop_center.png")
        print("Captured stir_02_scoop_center.png (p ~ 0.35)")
        
        # Scroll forward: p ~ 0.65 (ladle folding sweet mixture, camera zooming in)
        page.evaluate("window.scrollBy(0, 900)")
        time.sleep(1.0)
        page.screenshot(path="verification_shots/stir_03_fold_right.png")
        print("Captured stir_03_fold_right.png (p ~ 0.65)")
        
        # Scroll forward: p ~ 0.95 (close-up on prepared sweet mixture)
        page.evaluate("window.scrollBy(0, 950)")
        time.sleep(1.0)
        page.screenshot(path="verification_shots/stir_04_closeup_finish.png")
        print("Captured stir_04_closeup_finish.png (p ~ 0.95)")
        
        # TEST REVERSE PLAYBACK: Scroll BACKWARD to p ~ 0.50
        print("Testing backward scroll (reverse playback)...")
        page.evaluate("window.scrollBy(0, -1000)")
        time.sleep(1.0)
        page.screenshot(path="verification_shots/stir_05_reverse_mid.png")
        print("Captured stir_05_reverse_mid.png (reversed back to p ~ 0.50)")
        
        # Scroll all the way back up to entrance
        page.evaluate("window.scrollBy(0, -1600)")
        time.sleep(1.0)
        page.screenshot(path="verification_shots/stir_06_reverse_start.png")
        print("Captured stir_06_reverse_start.png (reversed back to entrance)")
        
        # 2. Mobile Responsive Test (390 x 844)
        print("\nTesting on Mobile (390 x 844)...")
        context_mobile = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True)
        page_m = context_mobile.new_page()
        page_m.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page_m.on("requestfailed", lambda req: failed_requests.append(f"{req.method} {req.url}: {req.failure}"))
        
        page_m.goto("http://localhost:3000", wait_until="networkidle")
        skip_btn_m = page_m.query_selector("button:has-text('Skip intro')")
        if skip_btn_m:
            skip_btn_m.click()
            time.sleep(2.5)
            
        page_m.evaluate("document.getElementById('heritage').scrollIntoView()")
        time.sleep(1.2)
        page_m.evaluate("window.scrollBy(0, 1000)")
        time.sleep(1.0)
        page_m.screenshot(path="verification_shots/stir_07_mobile_stir.png")
        print("Captured stir_07_mobile_stir.png")
        
        browser.close()
        
        # Copy shots to artifact dir
        for f in os.listdir("verification_shots"):
            if f.startswith("stir_") and f.endswith(".png"):
                shutil.copy2(os.path.join("verification_shots", f), os.path.join(artifact_dir, f))
        print("Copied all stir screenshots to artifact directory.")
        
        print("\n=== STIR SCRUBBING AUDIT RESULTS ===")
        print(f"Total console errors: {len(console_errors)}")
        if console_errors:
            for e in console_errors:
                print(f"  • {e}")
        print(f"Total failed requests: {len(failed_requests)}")
        if failed_requests:
            for fr in failed_requests:
                print(f"  • {fr}")
        print("Verification completed successfully!")

if __name__ == "__main__":
    run_test()

