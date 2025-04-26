# app/services/playwright_browser.py

from playwright.async_api import async_playwright

playwright = None
browser_context = None
page = None

async def start_browser_persistent():
    global playwright, browser_context, page

    if playwright is None:
        playwright = await async_playwright().start()

    if browser_context is None:
        browser_context = await playwright.chromium.launch_persistent_context(
            user_data_dir="./user_data",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )

    if page is None or page.is_closed():
        page = await browser_context.new_page()
        await page.goto("https://images.google.com")  # Go to Google Images immediately

    return page

async def get_browser_context():
    global browser_context
    if browser_context is None:
        await start_browser_persistent()
    return browser_context

async def restart_browser_if_needed():
    global browser_context, page

    if browser_context is None or page is None or page.is_closed():
        print("Restarting browser or page...")
        await start_browser_persistent()
    
    return page

async def close_browser():
    global playwright, browser_context, page
    if page and not page.is_closed():
        await page.close()
    if browser_context:
        await browser_context.close()
    if playwright:
        await playwright.stop()
    playwright = None
    browser_context = None
    page = None
