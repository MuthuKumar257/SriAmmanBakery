from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        headless=True
    )
    page = browser.new_page()
    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    
    failed = []
    page.on("response", lambda res: failed.append((res.status, res.url)) if res.status >= 400 else None)
    
    page.goto("http://localhost:3000", wait_until="networkidle")
    
    skip = page.query_selector("button:has-text('Skip intro')")
    if skip:
        skip.click()
    page.wait_for_timeout(2500)
    
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    
    print("Console errors count:", len(console_errors))
    if console_errors:
        print("Console errors:", console_errors)
    print("Failed requests count:", len(failed))
    if failed:
        print("Failed requests:", failed)
        
    browser.close()

