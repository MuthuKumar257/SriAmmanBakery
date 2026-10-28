import time
import os
from playwright.sync_api import sync_playwright

def capture_iris_steps():
    artifacts_dir = r"C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("http://localhost:3000", wait_until="networkidle")
        time.sleep(1)

        # Skip intro
        page.evaluate("() => { const b = document.querySelector('button'); if(b) b.click(); }")
        time.sleep(1)

        # Get top position of #signature-collection
        top = page.evaluate("() => document.getElementById('signature-collection').offsetTop")
        print("Signature collection offsetTop:", top)

        # Scroll to veil start
        page.evaluate(f"() => window.scrollTo(0, {top})")
        time.sleep(1)
        page.screenshot(path=os.path.join(artifacts_dir, "iris_01_start.png"))

        # Scroll through the 100vh scrub
        vh = 900
        for step_i, frac in enumerate([0.25, 0.5, 0.75, 1.0], start=2):
            scroll_pos = top + int(vh * frac)
            page.evaluate(f"() => window.scrollTo(0, {scroll_pos})")
            time.sleep(0.8)
            shot_path = os.path.join(artifacts_dir, f"iris_0{step_i}_step_{int(frac*100)}pct.png")
            page.screenshot(path=shot_path)
            print(f"Captured iris step {int(frac*100)}%: {shot_path}")

        browser.close()

if __name__ == "__main__":
    capture_iris_steps()

