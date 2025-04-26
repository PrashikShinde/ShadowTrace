from playwright.sync_api import sync_playwright
from pathlib import Path
import time
from app.utils.stealth_patch import patch_stealth
from app.utils.clipboard import copy_image_to_clipboard
from threading import Event

resume_scraping = Event()

def search_google_reverse(image_path: Path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 800})
            page = context.new_page()

            patch_stealth(page)

            page.goto("https://images.google.com/")
            page.wait_for_timeout(3000)

            page.mouse.move(300, 400)
            page.mouse.move(320, 420)
            page.wait_for_timeout(1000)

            camera_icon = page.locator('div[aria-label="Search by image"]')
            camera_icon.click()
            page.wait_for_timeout(2000)

            copy_image_to_clipboard(image_path)
            page.keyboard.press("Control+V")

            print("Waiting for user to solve CAPTCHA...")
            resume_scraping.wait()
            print("User solved CAPTCHA, resuming scraping...")

            page.wait_for_timeout(5000)

            links = page.locator('a').all()
            urls = [link.get_attribute('href') for link in links if link.get_attribute('href')]

            return urls
        finally:
            print("Closing browser properly now...")
            browser.close()
