from playwright.sync_api import sync_playwright
import time
import os

os.makedirs('verification_shots/sweets_12', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless=True
    )
    # 1. Desktop test
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:3000', wait_until='networkidle')
    skip_btn = page.query_selector("button:has-text('Skip intro')")
    if skip_btn:
        skip_btn.click()
        time.sleep(1.5)
        
    # Scroll to sweets section
    sweets_sec = page.locator('#sweets')
    sweets_sec.scroll_into_view_if_needed()
    time.sleep(1.0)
    
    # Check all cards
    cards = page.locator('#sweets div[role="button"]').all()
    print(f"Total sweet cards found in showcase: {len(cards)}")
    
    # Collect titles and subtitles
    for i, c in enumerate(cards):
        h3 = c.locator('h3').inner_text()
        subtitle_el = c.locator('p.italic')
        subtitle = subtitle_el.inner_text() if subtitle_el.count() > 0 else None
        bbox = c.bounding_box()
        print(f"Card {i+1}: {h3} | Subtitle: {subtitle} | Dimensions: w={bbox['width']:.1f}, h={bbox['height']:.1f}")
        
    # Capture showcase screenshots (row 1, row 2, row 3)
    page.screenshot(path='verification_shots/sweets_12/01_showcase_top.png')
    
    page.evaluate("window.scrollBy(0, 500)")
    time.sleep(0.5)
    page.screenshot(path='verification_shots/sweets_12/02_showcase_mid.png')
    
    page.evaluate("window.scrollBy(0, 500)")
    time.sleep(0.5)
    page.screenshot(path='verification_shots/sweets_12/03_showcase_bottom.png')
    
    # 2. Click Milk Laddu card to inspect modal
    milk_laddu_card = page.locator('#sweets div[role="button"]:has-text("Milk Laddu")').first
    if milk_laddu_card:
        milk_laddu_card.scroll_into_view_if_needed()
        time.sleep(0.4)
        milk_laddu_card.click()
        time.sleep(1.0)
        
        # Verify modal elements
        modal = page.locator('div[role="dialog"]')
        modal_title = modal.locator('#sweet-modal-title').inner_text()
        modal_sub = modal.locator('p.italic').inner_text()
        modal_desc = modal.locator('div.flex-col > div > p').first.inner_text()
        print(f"\nModal opened successfully:")
        print(f"  Title: {modal_title}")
        print(f"  Subtitle: {modal_sub}")
        print(f"  Description: {modal_desc[:70]}...")
        
        page.screenshot(path='verification_shots/sweets_12/04_milk_laddu_modal.png')
        
        # Close modal
        close_btn = modal.locator('button[aria-label="Close sweet description"]')
        close_btn.click()
        time.sleep(0.5)
        
    # 3. Mobile test
    page_mobile = browser.new_page(viewport={'width': 390, 'height': 844})
    page_mobile.goto('http://localhost:3000', wait_until='networkidle')
    skip_btn = page_mobile.query_selector("button:has-text('Skip intro')")
    if skip_btn:
        skip_btn.click()
        time.sleep(1.5)
    page_mobile.locator('#sweets').scroll_into_view_if_needed()
    time.sleep(1.0)
    page_mobile.screenshot(path='verification_shots/sweets_12/05_mobile_sweets.png')
    print("Mobile sweets screenshot captured.")
    
    browser.close()
    print("\nVerification completed successfully!")

