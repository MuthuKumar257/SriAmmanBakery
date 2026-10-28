from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless=True
    )
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://localhost:3000', wait_until='networkidle')
    
    skip_btn = page.query_selector("button:has-text('Skip intro')")
    if skip_btn:
        skip_btn.click()
        time.sleep(2.0)
        
    page.screenshot(path='verification_shots/brand_palette/mobile_01_hero.png')
    
    sweets = page.locator('#sweets')
    sweets.scroll_into_view_if_needed()
    time.sleep(1.0)
    page.screenshot(path='verification_shots/brand_palette/mobile_02_sweets.png')
    
    browser.close()
    print("Captured mobile screenshots successfully.")

