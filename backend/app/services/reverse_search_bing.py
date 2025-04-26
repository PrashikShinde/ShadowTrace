from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def search_bing_reverse(image_path: Path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # Directly go to Bing Image Search with camera button
        page.goto("https://www.bing.com/images")
        page.wait_for_timeout(3000)

        # Click on the camera icon button
        camera_icon = page.locator('div[title="Image Match"]')
        camera_icon.click()
        page.wait_for_timeout(2000)

        # Upload file
        file_input = page.locator('input[type="file"]').first
        file_input.set_input_files(str(image_path))

        # Wait for results
        page.wait_for_timeout(6000)

        # Collect result URLs
        links = page.locator('a').all()
        urls = [link.get_attribute('href') for link in links if link.get_attribute('href')]

        browser.close()
        return urls
