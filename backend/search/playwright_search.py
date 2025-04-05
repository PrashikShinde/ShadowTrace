from playwright.sync_api import sync_playwright
from typing import List, Dict
import time

SEARCH_ENGINES = {
    "Google": "https://images.google.com/",
    "Yandex": "https://yandex.com/images/",
    "Bing": "https://www.bing.com/images",
    "DuckDuckGo": "https://duckduckgo.com/",
    "Pinterest": "https://www.pinterest.com/",
    "TinEye": "https://tineye.com/",
    "Baidu": "https://image.baidu.com/"
}

def search_google(image_path: str) -> List[Dict]:
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(SEARCH_ENGINES["Google"])
            page.click('button[aria-label="Search by image"]')
            page.click("text=Upload a file")
            page.set_input_files('input[type="file"]', image_path)
            page.wait_for_timeout(6000)
            links = page.locator('a:has(img)').element_handles()
            for link in links[:10]:
                href = link.get_attribute("href")
                if href:
                    results.append({"source": "Google", "url": href, "match_confidence": 85})
            browser.close()
    except Exception as e:
        print("Google search error:", e)
    return results

def search_yandex(image_path: str) -> List[Dict]:
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(SEARCH_ENGINES["Yandex"])
            page.click('button[aria-label="Search by image"]')
            page.set_input_files('input[type="file"]', image_path)
            page.wait_for_timeout(6000)
            links = page.locator('a:has(img)').element_handles()
            for link in links[:10]:
                href = link.get_attribute("href")
                if href:
                    results.append({"source": "Yandex", "url": href, "match_confidence": 82})
            browser.close()
    except Exception as e:
        print("Yandex search error:", e)
    return results

def search_bing(image_path: str) -> List[Dict]:
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(SEARCH_ENGINES["Bing"])
            page.click("text=Search using an image")
            page.set_input_files('input[type="file"]', image_path)
            page.wait_for_timeout(6000)
            links = page.locator('a:has(img)').element_handles()
            for link in links[:10]:
                href = link.get_attribute("href")
                if href:
                    results.append({"source": "Bing", "url": href, "match_confidence": 80})
            browser.close()
    except Exception as e:
        print("Bing search error:", e)
    return results

def search_duckduckgo(image_path: str) -> List[Dict]:
    return [{
        "source": "DuckDuckGo",
        "url": "https://duckduckgo.com/?q=reverse+image+search&ia=images",
        "match_confidence": 60,
        "note": "DuckDuckGo doesn’t support direct upload."
    }]

def search_pinterest_fallback() -> List[Dict]:
    return [{
        "source": "Pinterest",
        "url": SEARCH_ENGINES["Pinterest"] + "search/pins/?q=reverse+image+search",
        "match_confidence": 50,
        "note": "Pinterest doesn't support auto reverse search."
    }]

def search_tineye(image_path: str) -> List[Dict]:
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(SEARCH_ENGINES["TinEye"])
            page.set_input_files('input[type="file"]', image_path)
            page.click('input[type="submit"]')
            page.wait_for_timeout(6000)
            links = page.locator('a.result__link').element_handles()
            for link in links[:10]:
                href = link.get_attribute("href")
                if href:
                    results.append({"source": "TinEye", "url": href, "match_confidence": 75})
            browser.close()
    except Exception as e:
        print("TinEye error:", e)
    return results

def search_baidu(image_path: str) -> List[Dict]:
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(SEARCH_ENGINES["Baidu"])
            page.click('span.soutu-btn')  # Open upload box
            page.set_input_files('input.upload-pic', image_path)
            page.wait_for_timeout(6000)
            links = page.locator('a:has(img)').element_handles()
            for link in links[:10]:
                href = link.get_attribute("href")
                if href:
                    results.append({"source": "Baidu", "url": href, "match_confidence": 78})
            browser.close()
    except Exception as e:
        print("Baidu error:", e)
    return results

def run_all_searches(image_path: str) -> List[Dict]:
    results = []
    results.extend(search_google(image_path))
    results.extend(search_yandex(image_path))
    results.extend(search_bing(image_path))
    results.extend(search_tineye(image_path))
    results.extend(search_baidu(image_path))
    results.extend(search_duckduckgo(image_path))
    results.extend(search_pinterest_fallback())
    return results
