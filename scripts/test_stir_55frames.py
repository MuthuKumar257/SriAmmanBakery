from playwright.sync_api import sync_playwright
import time
import os

os.makedirs('verification_shots/stir_55', exist_ok=True)

missing_frames = []
loaded_frames = []

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless=True
    )
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    
    # Listen to network requests
    def on_response(response):
        if '/stir_frames/' in response.url:
            if response.status == 200:
                loaded_frames.append(response.url.split('/')[-1])
            elif response.status == 404:
                missing_frames.append(response.url)
                
    page.on('response', on_response)
    
    page.goto('http://localhost:3000', wait_until='networkidle')
    skip_btn = page.query_selector("button:has-text('Skip intro')")
    if skip_btn:
        skip_btn.click()
        time.sleep(1.5)
        
    # Scroll to #heritage section
    heritage = page.locator('#heritage')
    heritage.scroll_into_view_if_needed()
    time.sleep(1.0)
    
    # Get bounding rect of #heritage
    box = heritage.bounding_box()
    print("Heritage section bbox:", box)
    
    # Scrub smoothly through the 55-frame animation
    steps = [0.0, 0.25, 0.5, 0.75, 1.0]
    for idx, s in enumerate(steps):
        target_y = box['y'] + (box['height'] - 900) * s
        page.evaluate(f"window.scrollTo(0, {target_y})")
        time.sleep(0.6)
        page.screenshot(path=f'verification_shots/stir_55/step_{idx}_{int(s*100)}pct.png')
        print(f"Scrubbed to {int(s*100)}%, captured step_{idx}_{int(s*100)}pct.png")
        
    # Reverse scrubbing test
    for idx, s in enumerate([0.7, 0.3, 0.0]):
        target_y = box['y'] + (box['height'] - 900) * s
        page.evaluate(f"window.scrollTo(0, {target_y})")
        time.sleep(0.4)
        
    time.sleep(1.0)
    browser.close()

print(f"Total frames loaded: {len(set(loaded_frames))}")
print(f"Sample loaded: {sorted(list(set(loaded_frames)))[:5]} ... {sorted(list(set(loaded_frames)))[-3:]}")
print(f"Missing (404) frames: {len(missing_frames)}")
if missing_frames:
    print("404 errors:", missing_frames[:5])

