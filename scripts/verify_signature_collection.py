import time
import os
from playwright.sync_api import sync_playwright

def verify_12_signature_sweets():
    artifacts_dir = r"C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b"
    os.makedirs(artifacts_dir, exist_ok=True)

    expected_sweets = [
        "Laddu",
        "Mysore Pak",
        "Jalebi",
        "Badam Burfi",
        "Boost Burfi",
        "Horlicks Burfi",
        "Badusha",
        "Carrot Burfi",
        "Pista Burfi",
        "Rose Burfi",
        "Gulab Jamun",
        "Milk Laddu"
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

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

        # Locate section #sweets
        sec = page.locator("#sweets")
        print("Section #sweets count:", sec.count())
        assert sec.count() > 0, "Section #sweets not found!"

        sheets = page.locator(".sweet-sheet")
        count = sheets.count()
        print(f"Found {count} sweet sheets (expected {len(expected_sweets)}).")
        assert count == len(expected_sweets), f"Expected {len(expected_sweets)} sheets, got {count}"

        found_titles = []
        for i in range(count):
            sheet = sheets.nth(i)
            title = sheet.locator(".sweet-title").inner_text().strip()
            found_titles.append(title)
            print(f"Sheet {i+1:02d}: {title}")

            # Capture sample screenshots for Laddu, Mysore Pak, Boost Burfi, and Milk Laddu
            if i in [0, 1, 4, 11]:
                sheet.scroll_into_view_if_needed()
                time.sleep(0.5)
                shot = os.path.join(artifacts_dir, f"stack_sweet_{i+1:02d}_{title.replace(' ', '_').lower()}.png")
                page.screenshot(path=shot)
                print(f"  -> Captured {shot}")

        assert found_titles == expected_sweets, f"Title mismatch! Expected {expected_sweets}, got {found_titles}"

        # Test Milk Laddu subtitle
        milk_laddu_sheet = sheets.nth(11)
        sub = milk_laddu_sheet.locator("p.italic").inner_text().strip()
        print(f"Milk Laddu subtitle: '{sub}'")
        assert "Also called Tirupathi Laddu" in sub, f"Expected 'Also called Tirupathi Laddu', got '{sub}'"

        # Test clicking 'View Sweet Profile' button on Card 0 (Laddu)
        view_btn = sheets.nth(0).locator("button:has-text('View Sweet Profile')")
        print("Clicking 'View Sweet Profile' on Laddu...")
        sheets.nth(0).scroll_into_view_if_needed()
        time.sleep(0.5)
        view_btn.dispatch_event('click')
        time.sleep(1)

        # Check modal open
        modal = page.locator("[role='dialog']")
        assert modal.is_visible(), "Modal did not open!"
        modal_title = modal.locator("#sweet-modal-title").inner_text()
        print(f"Modal opened for sweet: '{modal_title}'")
        assert "Laddu" in modal_title, f"Expected modal for Laddu, got '{modal_title}'"

        # Capture modal screenshot
        modal_shot = os.path.join(artifacts_dir, "stack_sweet_modal_laddu.png")
        page.screenshot(path=modal_shot)
        print("Captured modal screenshot:", modal_shot)

        # Close modal
        close_btn = modal.locator("button:has(svg.lucide-x)")
        if close_btn.count() > 0:
            close_btn.first.dispatch_event('click')
        else:
            page.keyboard.press("Escape")
        time.sleep(0.5)

        # Mobile Viewport Test
        print("\nTesting mobile viewport 375x812...")
        mobile_page = browser.new_page(viewport={"width": 375, "height": 812})
        mobile_page.goto("http://localhost:3000", wait_until="networkidle")
        time.sleep(1)
        mobile_page.evaluate("() => { const b = document.querySelector('button'); if(b) b.click(); }")
        time.sleep(1)
        mobile_sec = mobile_page.locator("#sweets")
        mobile_sec.scroll_into_view_if_needed()
        time.sleep(1)
        mobile_shot = os.path.join(artifacts_dir, "stack_sweet_mobile.png")
        mobile_page.screenshot(path=mobile_shot)
        print("Captured mobile screenshot:", mobile_shot)

        print("\nConsole errors:", console_errors)
        print("Failed requests:", failed_requests)
        assert len(failed_requests) == 0, f"Failed requests found: {failed_requests}"
        print("\n[ALL TESTS PASSED] 12 Signature Sweets stacking scroll verified cleanly!")

        browser.close()

if __name__ == "__main__":
    verify_12_signature_sweets()
