import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://localhost:3000', wait_until='networkidle')
    time.sleep(1)

    # Click intro button to skip
    page.evaluate("() => { const b = document.querySelector('button'); if(b) b.click(); }")
    time.sleep(1)

    # Dispatch click event directly to button
    btn = page.locator("#sweets .sweet-sheet").first.locator("button:has-text('View Sweet Profile')")
    print("Button count:", btn.count())
    btn.dispatch_event('click')
    time.sleep(1)

    modal = page.locator("[role='dialog']")
    print("Modal visible?", modal.is_visible())
    if modal.is_visible():
        print("Modal title:", modal.locator("#sweet-modal-title").inner_text())

    b.close()

