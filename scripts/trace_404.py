from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        headless=True
    )
    page = browser.new_page()
    page.on("requestfailed", lambda req: print("Request failed:", req.url, req.failure))
    page.on("response", lambda res: print("Status:", res.status, res.url) if res.status >= 400 else None)
    page.goto("http://localhost:3000", wait_until="networkidle")
    browser.close()

