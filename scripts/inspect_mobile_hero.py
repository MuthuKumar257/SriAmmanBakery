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
        time.sleep(2.5)
    page.screenshot(path='verification_shots/debug_mobile_hero.png')
    
    # Check mobile title
    title = page.locator('h1').first.bounding_box()
    sweet = page.locator('#top img[alt*="Sweets"]').first.bounding_box()
    print('Mobile Title:', title)
    print('Mobile Sweet:', sweet)
    if title and sweet:
        gap = sweet['y'] - (title['y'] + title['height'])
        print(f'Mobile vertical gap between title and sweet: {gap}px (positive means clear space!)')
    browser.close()

