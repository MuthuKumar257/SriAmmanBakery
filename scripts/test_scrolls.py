from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        headless=True
    )
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:3000", wait_until="networkidle")
    
    skip = page.query_selector("button:has-text('Skip intro')")
    if skip:
        skip.click()
    page.wait_for_timeout(2500)
    
    for y in [1200, 2200, 3200, 4200]:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(800)
        page.screenshot(path=f"verification_shots/scroll_{y}.png")
        print(f"Captured scroll_{y}.png")
        
    browser.close()

