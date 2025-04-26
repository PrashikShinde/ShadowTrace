# app/api/scrape_results.py

from fastapi import APIRouter # type: ignore
from app.services.playwright_browser import restart_browser_if_needed
from app.services.google_scraper import scrape_google_results

router = APIRouter()

@router.get("/scrape-results")
async def scrape_results():
    try:
        page = await restart_browser_if_needed()

        # 🧠 Page already opened Google Images in startup

        results = await scrape_google_results(page)

        return {"status": "success", "data": {"results": results}}

    except Exception as e:
        print("Error during scrape-results:", e)
        return {"status": "error", "message": str(e)}
