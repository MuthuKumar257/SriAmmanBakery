from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        headless=True
    )
    page = browser.new_page()
    failed = []
    page.on("response", lambda res: failed.append((res.status, res.url)) if res.status >= 400 else None)
    page.goto("http://localhost:3000", wait_until="networkidle")
    
    skip = page.query_selector("button:has-text('Skip intro')")
    if skip:
        skip.click()
    page.wait_for_timeout(3000)
    
    # Scroll through entire page to check all assets
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    
    print("Failed requests:")
    for f in failed:
        print(f)
        
    browser.close()

