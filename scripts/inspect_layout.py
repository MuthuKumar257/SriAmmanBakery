from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:3000", wait_until="networkidle")
    
    skip = page.query_selector("button:has-text('Skip intro')")
    if skip: skip.click()
    page.wait_for_timeout(3000)
    
    sections = page.evaluate("""() => {
        return ['top', 'ritual', 'pack', 'estate'].map(id => {
            const el = document.getElementById(id);
            if (!el) return { id, error: 'not found' };
            const rect = el.getBoundingClientRect();
            return {
                id,
                offsetTop: el.offsetTop,
                offsetHeight: el.offsetHeight,
                top: rect.top,
                bottom: rect.bottom,
                scrollHeight: document.body.scrollHeight
            };
        });
    }""")
    print("Section offsets and dimensions:")
    import json
    print(json.dumps(sections, indent=2))
    
    # Also inspect canvas styling & dimensions
    canvas_info = page.evaluate("""() => {
        const c = document.querySelector('canvas.ritual-canvas');
        if (!c) return 'No canvas found';
        const rect = c.getBoundingClientRect();
        return {
            width: c.width,
            height: c.height,
            clientWidth: c.clientWidth,
            clientHeight: c.clientHeight,
            opacity: window.getComputedStyle(c).opacity,
            visibility: window.getComputedStyle(c).visibility,
            top: rect.top,
            left: rect.left
        };
    }""")
    print("Canvas info on initial hero:", canvas_info)
    
    # Scroll to ritual midpoint
    page.evaluate("window.scrollTo(0, 2000)")
    page.wait_for_timeout(1000)
    canvas_mid = page.evaluate("""() => {
        const c = document.querySelector('canvas.ritual-canvas');
        if (!c) return 'No canvas';
        return {
            opacity: window.getComputedStyle(c).opacity,
            progress: document.querySelector('.rail-track')?.style.getPropertyValue('--progress'),
            activeDots: Array.from(document.querySelectorAll('.rail-dot')).map(d => d.getAttribute('data-active')),
            activeSteps: Array.from(document.querySelectorAll('.rail-step')).map(d => d.getAttribute('data-active'))
        };
    }""")
    print("Canvas info at scrollY=2000:", canvas_mid)
    
    browser.close()

