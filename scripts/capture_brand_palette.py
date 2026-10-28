from playwright.sync_api import sync_playwright
import time
import os

os.makedirs('verification_shots/brand_palette', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless=True
    )
    # Desktop 1440x900
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:3000', wait_until='networkidle')
    
    # Skip intro
    skip_btn = page.query_selector("button:has-text('Skip intro')")
    if skip_btn:
        skip_btn.click()
        time.sleep(2.0)
        
    # 1. Hero
    page.screenshot(path='verification_shots/brand_palette/01_hero_palette.png')
    print("Captured 01_hero_palette.png")
    
    # 2. Craft Ritual
    craft_sec = page.locator('#craft')
    craft_sec.scroll_into_view_if_needed()
    time.sleep(1.0)
    page.screenshot(path='verification_shots/brand_palette/02_craft_palette.png')
    print("Captured 02_craft_palette.png")
    
    # 3. Sweets Showcase (Warm Ivory background with maroon headings)
    sweets_sec = page.locator('#sweets')
    sweets_sec.scroll_into_view_if_needed()
    time.sleep(1.0)
    page.screenshot(path='verification_shots/brand_palette/03_sweets_palette.png')
    print("Captured 03_sweets_palette.png")
    
    # 4. Pack Section (Warm Ivory with Deep Forest Green buttons & Heritage Gold lines)
    pack_sec = page.locator('#pack')
    pack_sec.scroll_into_view_if_needed()
    time.sleep(1.5)
    page.screenshot(path='verification_shots/brand_palette/04_pack_palette.png')
    print("Captured 04_pack_palette.png")
    
    # 5. Estate / Our Story (Deep Forest Green with photorealistic stir)
    estate_sec = page.locator('#heritage')
    estate_sec.scroll_into_view_if_needed()
    time.sleep(1.0)
    page.screenshot(path='verification_shots/brand_palette/05_heritage_palette.png')
    print("Captured 05_heritage_palette.png")
    
    # 6. Footer (Deep Forest Green & Gold)
    footer_sec = page.locator('footer')
    footer_sec.scroll_into_view_if_needed()
    time.sleep(1.0)
    page.screenshot(path='verification_shots/brand_palette/06_footer_palette.png')
    print("Captured 06_footer_palette.png")
    
    # 7. Modal (Click first sweet card)
    card = page.locator('#sweets div[role="button"]').first
    if card:
        card.scroll_into_view_if_needed()
        time.sleep(0.5)
        card.click()
        time.sleep(1.0)
        page.screenshot(path='verification_shots/brand_palette/07_modal_palette.png')
        print("Captured 07_modal_palette.png")
        
    browser.close()

