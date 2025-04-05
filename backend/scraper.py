import asyncio
from playwright.async_api import async_playwright
import os
import uuid
import requests

async def scrape_google_images(query, save_dir="./scraped"):
    os.makedirs(save_dir, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"https://www.google.com/search?tbm=isch&q={query}")

        await page.wait_for_timeout(3000)

        img_elements = await page.query_selector_all("img")

        image_paths = []
        for index, img in enumerate(img_elements[:10]):
            src = await img.get_attribute("src")
            if src and src.startswith("http"):
                try:
                    image_data = requests.get(src).content
                    filename = os.path.join(save_dir, f"{uuid.uuid4()}.jpg")
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    image_paths.append(filename)
                except:
                    pass

        await browser.close()
        return image_paths

# test run
# asyncio.run(scrape_google_images("face"))
