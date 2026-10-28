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
    
    page.evaluate("window.scrollTo(0, 2000)")
    page.wait_for_timeout(1000)
    
    pixel_info = page.evaluate("""() => {
        const c = document.querySelector('canvas.ritual-canvas');
        if (!c) return 'No canvas';
        const ctx = c.getContext('2d');
        const data = ctx.getImageData(c.width/2, c.height/2, 1, 1).data;
        return {
            rgba: Array.from(data),
            styleOpacity: c.style.opacity,
            computedOpacity: window.getComputedStyle(c).opacity,
            display: window.getComputedStyle(c).display,
            mask: window.getComputedStyle(c).maskImage
        };
    }""")
    print("Canvas pixel and style info at scroll 2000:", pixel_info)
    
    canvas_el = page.query_selector("canvas.ritual-canvas")
    if canvas_el:
        canvas_el.screenshot(path="verification_shots/canvas_only.png")
        print("Saved verification_shots/canvas_only.png")
        
    browser.close()

