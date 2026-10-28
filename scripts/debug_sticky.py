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
    
    page.evaluate("window.scrollTo(0, 2200)")
    page.wait_for_timeout(500)
    
    info = page.evaluate("""() => {
        const stage = document.querySelector('#ritual > div');
        const stageRect = stage ? stage.getBoundingClientRect() : null;
        const centerEl = document.elementFromPoint(720, 450);
        const topEl = document.elementFromPoint(720, 100);
        return {
            stageRect,
            stagePosition: stage ? window.getComputedStyle(stage).position : null,
            stageTop: stage ? window.getComputedStyle(stage).top : null,
            centerTag: centerEl ? centerEl.tagName + '.' + centerEl.className : 'null',
            topTag: topEl ? topEl.tagName + '.' + topEl.className : 'null',
            scrollY: window.scrollY
        };
    }""")
    print("Element and stage info at scroll 2200:")
    import json
    print(json.dumps(info, indent=2))
    
    browser.close()

