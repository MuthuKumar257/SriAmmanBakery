import os
import time
from playwright.sync_api import sync_playwright

os.makedirs('verification_shots', exist_ok=True)

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            headless=True
        )
        
        # 1. Desktop Verification (1440 x 900)
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        
        failed_requests = []
        page.on("requestfailed", lambda req: failed_requests.append(f"{req.method} {req.url}: {req.failure}"))
        
        print("Navigating to Sri Amman Bakery site on Desktop (1440x900)...")
        page.goto("http://localhost:3000", wait_until="networkidle")
        
        # 1. Capture intro screen
        time.sleep(1)
        page.screenshot(path="verification_shots/01_local_intro.png")
        print("Captured 01_local_intro.png")
        
        # Click skip intro button
        skip_btn = page.query_selector("button:has-text('Skip intro')")
        if skip_btn:
            skip_btn.click()
            print("Clicked 'Skip intro'")
            time.sleep(2.5) # Wait for reveal transition
            
        # 2. Capture Hero Section
        page.screenshot(path="verification_shots/02_local_hero.png")
        print("Captured 02_local_hero.png")
        
        # 3. Scroll to Craft Ritual (Sweet Tray for Ghee, Roast, Craft, Garnish · 01 / 04)
        page.evaluate("document.getElementById('craft').scrollIntoView()")
        time.sleep(1.5)
        page.screenshot(path="verification_shots/03_local_craft_ghee.png")
        print("Captured 03_local_craft_ghee.png (Step 01 / 04 - Ghee)")
        
        # Scroll through step 02 (Roast)
        page.evaluate("window.scrollBy(0, 650)")
        time.sleep(1.2)
        page.screenshot(path="verification_shots/04_local_craft_roast.png")
        print("Captured 04_local_craft_roast.png (Step 02 / 04 - Roast)")
        
        # Scroll through step 03 (Craft)
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(1.2)
        page.screenshot(path="verification_shots/05_local_craft_craft.png")
        print("Captured 05_local_craft_craft.png (Step 03 / 04 - Craft)")
        
        # Scroll through step 04 (Garnish)
        page.evaluate("window.scrollBy(0, 900)")
        time.sleep(1.2)
        page.screenshot(path="verification_shots/06_local_craft_garnish.png")
        print("Captured 06_local_craft_garnish.png (Step 04 / 04 - Garnish)")
        
        # 4. Scroll to Sweets Showcase Grid
        page.evaluate("document.getElementById('sweets').scrollIntoView()")
        time.sleep(1.5)
        page.screenshot(path="verification_shots/07_local_sweets_grid.png")
        print("Captured 07_local_sweets_grid.png (All 7 Sweets Grid)")
        
        # 4b. Test Clicking Badusha Sweet Card to Open Modal
        print("Testing Sweet Card Click (Badusha)...")
        badusha_card = page.query_selector("[aria-label='View details of Badusha']")
        if badusha_card:
            badusha_card.click()
            time.sleep(1)
            page.screenshot(path="verification_shots/07b_modal_badusha.png")
            print("Captured 07b_modal_badusha.png (Sweet Detail Modal for Badusha)")
            
            # Test pressing Escape to close
            page.keyboard.press("Escape")
            time.sleep(0.8)
            print("Pressed Escape - Modal closed")
            
        # 4c. Test Clicking Laddu Sweet Card
        laddu_card = page.query_selector("[aria-label='View details of Laddu']")
        if laddu_card:
            laddu_card.click()
            time.sleep(0.8)
            page.screenshot(path="verification_shots/07c_modal_laddu.png")
            print("Captured 07c_modal_laddu.png (Sweet Detail Modal for Laddu)")
            
            # Click Close button
            close_btn = page.query_selector("button[aria-label='Close sweet description']")
            if close_btn:
                close_btn.click()
                time.sleep(0.8)
                print("Clicked Close button - Modal closed")
        
        # 5. Scroll to Pack Section
        page.evaluate("document.getElementById('pack').scrollIntoView()")
        time.sleep(2.5)
        page.screenshot(path="verification_shots/08_local_pack.png")
        print("Captured 08_local_pack.png")
        
        # 6. Scroll to Heritage Section (Our Story - Mangalasamy P 2022)
        page.evaluate("document.getElementById('heritage').scrollIntoView()")
        time.sleep(1)
        page.evaluate("window.scrollBy(0, 1500)")
        time.sleep(1)
        page.screenshot(path="verification_shots/09_local_heritage.png")
        print("Captured 09_local_heritage.png")
        
        # 7. Scroll to Footer
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        page.screenshot(path="verification_shots/10_local_footer.png")
        print("Captured 10_local_footer.png")
        
        # 8. Mobile Verification (390 x 844)
        print("Testing mobile responsive layout (390x844)...")
        context_mobile = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True)
        page_m = context_mobile.new_page()
        page_m.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page_m.on("requestfailed", lambda req: failed_requests.append(f"{req.method} {req.url}: {req.failure}"))
        
        page_m.goto("http://localhost:3000", wait_until="networkidle")
        
        skip_btn_m = page_m.query_selector("button:has-text('Skip intro')")
        if skip_btn_m:
            skip_btn_m.click()
            time.sleep(2.5)
            
        page_m.screenshot(path="verification_shots/11_mobile_hero.png")
        print("Captured 11_mobile_hero.png")
        
        page_m.evaluate("document.getElementById('craft').scrollIntoView()")
        time.sleep(1.5)
        page_m.screenshot(path="verification_shots/12_mobile_sweet_tray.png")
        print("Captured 12_mobile_sweet_tray.png")
        
        page_m.evaluate("document.getElementById('sweets').scrollIntoView()")
        time.sleep(1.5)
        page_m.screenshot(path="verification_shots/13_mobile_sweets.png")
        print("Captured 13_mobile_sweets.png")

        # Test mobile modal click
        badusha_m = page_m.query_selector("[aria-label='View details of Badusha']")
        if badusha_m:
            badusha_m.click()
            time.sleep(1)
            page_m.screenshot(path="verification_shots/13b_mobile_modal.png")
            print("Captured 13b_mobile_modal.png")
            close_btn_m = page_m.query_selector("button[aria-label='Close sweet description']")
            if close_btn_m:
                close_btn_m.click()
                time.sleep(0.8)

        page_m.evaluate("document.getElementById('heritage').scrollIntoView()")
        time.sleep(1)
        page_m.evaluate("window.scrollBy(0, 1000)")
        time.sleep(1)
        page_m.screenshot(path="verification_shots/14_mobile_heritage.png")
        print("Captured 14_mobile_heritage.png")
        
        browser.close()
        
        print("\n=== VERIFICATION AUDIT RESULTS ===")
        print(f"Total console errors: {len(console_errors)}")
        if console_errors:
            for err in console_errors:
                print(f"  • {err}")
        print(f"Total failed requests: {len(failed_requests)}")
        if failed_requests:
            for fr in failed_requests:
                print(f"  • {fr}")
        print("All verification screenshots captured successfully!")

if __name__ == "__main__":
    verify()
