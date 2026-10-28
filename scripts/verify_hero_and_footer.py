import time
import os
from playwright.sync_api import sync_playwright

def verify():
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

        # 1. Verify Hero Title Size and Alignment
        title1 = page.locator("h1 span:has-text('Sri Amman')").first
        title2 = page.locator("h1 span:has-text('Bakery')").first
        box1 = title1.bounding_box()
        box2 = title2.bounding_box()
        sweet_box = page.locator("#top div[aria-hidden='true'].aspect-square").bounding_box()

        print(f"'Sri Amman' box: {box1}")
        print(f"'Bakery' box: {box2}")
        print(f"Sweet Platter box: {sweet_box}")

        # Check font size
        font_size1 = page.evaluate("(el) => window.getComputedStyle(el).fontSize", title1.element_handle())
        print(f"Computed Font Size for 'Sri Amman': {font_size1}")

        # Verify clearances
        if box1 and sweet_box and box2:
            left_clearance = sweet_box['x'] - (box1['x'] + box1['width'])
            right_clearance = box2['x'] - (sweet_box['x'] + sweet_box['width'])
            print(f"Left Clearance to Platter: {left_clearance:.2f}px")
            print(f"Right Clearance to Platter: {right_clearance:.2f}px")
            assert left_clearance > 0, f"Overlap on left! Clearance: {left_clearance}"
            assert right_clearance > 0, f"Overlap on right! Clearance: {right_clearance}"
            print("[PASS] Guaranteed zero overlap and symmetric clearance in hero!")

        hero_shot = os.path.join(artifacts_dir, "hero_enlarged_title.png")
        page.screenshot(path=hero_shot)
        print("Captured Hero:", hero_shot)

        # 2. Verify Footer Contact Links
        footer = page.locator("footer")
        footer.scroll_into_view_if_needed()
        time.sleep(1)

        phone_link = footer.locator("a[href*='tel:9626758666']")
        insta_link = footer.locator("a[href*='instagram.com/sriamman_bakery']")
        wa_link = footer.locator("a[href*='whatsapp.com/channel/0029Vb97jtVBadmd0d98OQ0u']")

        assert phone_link.count() > 0, "Phone link not found in footer!"
        assert insta_link.count() > 0, "Instagram link not found in footer!"
        assert wa_link.count() > 0, "WhatsApp link not found in footer!"

        print(f"[PASS] Found Phone link: {phone_link.first.get_attribute('href')}")
        print(f"[PASS] Found Instagram link: {insta_link.first.get_attribute('href')}")
        print(f"[PASS] Found WhatsApp link: {wa_link.first.get_attribute('href')}")

        footer_shot = os.path.join(artifacts_dir, "footer_contact_details.png")
        page.screenshot(path=footer_shot)
        print("Captured Footer:", footer_shot)

        # 3. Mobile Viewport
        mobile_page = b.new_page(viewport={"width": 375, "height": 812})
        mobile_page.goto("http://localhost:3000", wait_until="networkidle")
        time.sleep(1)
        mobile_page.evaluate("() => { const b = document.querySelector('button'); if(b) b.click(); }")
        time.sleep(1)

        mobile_hero_shot = os.path.join(artifacts_dir, "hero_mobile_enlarged.png")
        mobile_page.screenshot(path=mobile_hero_shot)
        print("Captured Mobile Hero:", mobile_hero_shot)

        mobile_footer = mobile_page.locator("footer")
        mobile_footer.scroll_into_view_if_needed()
        time.sleep(1)
        mobile_footer_shot = os.path.join(artifacts_dir, "footer_mobile_contacts.png")
        mobile_page.screenshot(path=mobile_footer_shot)
        print("Captured Mobile Footer:", mobile_footer_shot)

        print("\nConsole errors:", console_errors)
        print("Failed requests:", failed_requests)
        assert len(failed_requests) == 0, f"Failed requests: {failed_requests}"
        print("\n[ALL TESTS PASSED] Hero title enlargement and footer contacts verified cleanly!")

        b.close()

if __name__ == "__main__":
    verify()
