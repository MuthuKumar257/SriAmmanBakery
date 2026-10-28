import time
import os
from playwright.sync_api import sync_playwright

def verify():
    artifacts_dir = r"C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b"
    os.makedirs(artifacts_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        failed_requests = []
        page.on("requestfailed", lambda req: failed_requests.append(req.url))

        print("Navigating to http://localhost:3000...")
        page.goto("http://localhost:3000", wait_until="networkidle")
        time.sleep(1)

        # Skip intro if playing
        page.evaluate("() => { const b = document.querySelector('button'); if(b) b.click(); }")
        time.sleep(1)

        # Locate section
        sec = page.locator("#signature-collection")
        print("Section count:", sec.count())
        assert sec.count() > 0, "Section #signature-collection not found!"

        # Scroll to section start
        sec.scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=os.path.join(artifacts_dir, "sig_01_veil_entry.png"))
        print("Captured veil entry.")

        # Scroll into cards
        sheets = page.locator(".sweet-sheet")
        count = sheets.count()
        print(f"Found {count} sweet sheets.")
        assert count == 4, f"Expected 4 sweet sheets, got {count}"

        # Scroll through each sweet card
        for i in range(count):
            sheets.nth(i).scroll_into_view_if_needed()
            time.sleep(1)
            shot_path = os.path.join(artifacts_dir, f"sig_0{i+2}_card_{i}.png")
            page.screenshot(path=shot_path)
            title = sheets.nth(i).locator(".sweet-title").inner_text()
            print(f"Card {i} Title: '{title}', screenshot: {shot_path}")

        # Check Mobile Viewport
        print("\nTesting mobile viewport 375x812...")
        mobile_page = context.new_page()
        mobile_page.set_viewport_size({"width": 375, "height": 812})
        mobile_page.goto("http://localhost:3000", wait_until="networkidle")
        time.sleep(1)
        mobile_sec = mobile_page.locator("#signature-collection")
        mobile_sec.scroll_into_view_if_needed()
        time.sleep(1)
        mobile_shot = os.path.join(artifacts_dir, "sig_06_mobile_stack.png")
        mobile_page.screenshot(path=mobile_shot)
        print("Mobile view captured:", mobile_shot)

        print("\nConsole errors:", console_errors)
        print("Failed requests:", failed_requests)
        assert len(failed_requests) == 0, f"Failed requests found: {failed_requests}"
        print("\n[SUCCESS] Signature Sweets Collection verified cleanly!")

        browser.close()

if __name__ == "__main__":
    verify()
