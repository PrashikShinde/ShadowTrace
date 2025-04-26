from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def search_yandex_reverse(image_path: Path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://yandex.com/images/")
        page.click('button[aria-label="Search by image"]')
        page.wait_for_timeout(2000)

        upload_input = page.locator('input[type="file"]').first
        upload_input.set_input_files(str(image_path))

        page.wait_for_timeout(6000)
        links = page.locator('a').all()
        urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]

        browser.close()
        return urls
