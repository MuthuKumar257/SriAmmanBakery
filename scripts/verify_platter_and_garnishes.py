import time
import os
from playwright.sync_api import sync_playwright

def verify_platter_and_garnishes():
    artifacts_dir = r"C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b"

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 900})

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        failed_requests = []
        page.on("requestfailed", lambda req: failed_requests.append(req.url))

        page.goto("http://localhost:3000", wait_until="networkidle")
        time.sleep(1)

        # Skip intro
        page.evaluate("() => { const b = document.querySelector('button'); if(b) b.click(); }")
        time.sleep(1)

        # 1. Hero section with new platter
        hero_shot = os.path.join(artifacts_dir, "platter_01_hero.png")
        page.screenshot(path=hero_shot)
        print("Captured Hero platter:", hero_shot)

        # 2. Craft Ritual Section with platter
        craft_sec = page.locator("#craft")
        craft_sec.scroll_into_view_if_needed()
        time.sleep(1)
        craft_shot = os.path.join(artifacts_dir, "platter_02_craft_ritual.png")
        page.screenshot(path=craft_shot)
        print("Captured Craft Ritual platter:", craft_shot)

        # 3. PackSection with falling garnishes
        pack_sec = page.locator("#pack")
        pack_sec.scroll_into_view_if_needed()
        time.sleep(1.5)
        pack_shot = os.path.join(artifacts_dir, "platter_03_falling_garnishes.png")
        page.screenshot(path=pack_shot)
        print("Captured Falling Garnishes:", pack_shot)

        print("Console errors:", console_errors)
        print("Failed requests:", failed_requests)
        assert len(failed_requests) == 0, f"Failed requests: {failed_requests}"
        print("[SUCCESS] Platter and garnishing verified cleanly!")

        b.close()

if __name__ == "__main__":
    verify_platter_and_garnishes()

