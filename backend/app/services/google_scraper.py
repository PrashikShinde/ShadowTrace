# app/services/google_scraper.py

import asyncio

async def scrape_google_results(page):
    try:
        print("Waiting for search results...")

        # 🛑 Stay on SAME tab, don't open new!
        await page.wait_for_selector('div.N54PNb', timeout=20000)

        print("Results loaded, scraping...")

        results = []

        image_divs = await page.query_selector_all('div.N54PNb')

        for div in image_divs:
            try:
                img = await div.query_selector('img')
                src = await img.get_attribute('src') if img else None

                link_tag = await div.query_selector('a.LBcIee')
                href = await link_tag.get_attribute('href') if link_tag else None

                if src and href:
                    results.append({
                        "image_src": src,
                        "page_link": href
                    })
            except Exception as e:
                print(f"Error scraping one result: {e}")
                continue

        print(f"Scraped {len(results)} results!")
        return results

    except Exception as e:
        print("Error while scraping results:", e)
        return []
