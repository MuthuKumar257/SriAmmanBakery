from playwright.sync_api import sync_playwright
import time, shutil

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
    
    page.evaluate("document.getElementById('sweets').scrollIntoView()")
    time.sleep(0.5)
    page.evaluate("window.scrollBy(0, 1600)")
    time.sleep(1)
    page.screenshot(path='verification_shots/07_local_sweets_row2.png')
    shutil.copy2('verification_shots/07_local_sweets_row2.png', r'C:\Users\muthu\.gemini\antigravity\brain\53599524-1e90-4507-9ca7-00bb3cc8156b\07_local_sweets_row2.png')
    browser.close()
print('Captured and copied 07_local_sweets_row2.png')

