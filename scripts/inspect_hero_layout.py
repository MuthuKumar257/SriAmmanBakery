from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless=True
    )
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:3000', wait_until='networkidle')
    skip_btn = page.query_selector("button:has-text('Skip intro')")
    if skip_btn:
        skip_btn.click()
        time.sleep(2.5)
    page.screenshot(path='verification_shots/debug_current_hero.png')
    
    # Get bounding rects of word1, word2, and the sweet centerpiece
    spans = page.locator('h1 span').all()
    if len(spans) >= 2:
        w1 = spans[0].bounding_box()
        w2 = spans[1].bounding_box()
        print('Word 1 (Sri Amman):', w1)
        print('Word 2 (Bakery):', w2)
    
    sweet_el = page.locator('#top img[alt*="Sweets"]').first
    if sweet_el:
        cup = sweet_el.bounding_box()
        print('Centerpiece:', cup)
        
        # Calculate overlap!
        if w1 and cup:
            w1_right = w1['x'] + w1['width']
            cup_left = cup['x']
            overlap_w1 = w1_right - cup_left
            print(f'Overlap with Word 1: {overlap_w1}px (positive means cup covers text!)')
            
        if w2 and cup:
            w2_left = w2['x']
            cup_right = cup['x'] + cup['width']
            overlap_w2 = cup_right - w2_left
            print(f'Overlap with Word 2: {overlap_w2}px (positive means cup covers text!)')
    
    # Check nav text
    nav_el = page.locator('nav').first
    if nav_el:
        print('Nav text:', repr(nav_el.inner_text()))
        
    browser.close()

