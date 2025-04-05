from playwright.sync_api import sync_playwright
import os
import uuid

def perform_search(filename):
    img_path = os.path.join("uploads", filename)
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Example using Bing (can add DuckDuckGo here too)
        page.goto("https://www.bing.com/images")

        upload_input = page.locator('input[type="file"]')
        upload_input.set_input_files(img_path)

        page.wait_for_timeout(5000)

        links = page.query_selector_all('a.iusc')
        for link in links[:5]:
            href = link.get_attribute("href")
            if href:
                results.append({
                    "source": "Bing",
                    "url": href,
                    "image_path": img_path  # This will be replaced with actual downloaded image
                })

        browser.close()

    return results
