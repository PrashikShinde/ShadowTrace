# backend/app/api/reverse_search.py

from fastapi import APIRouter # type: ignore
from app.services.playwright_browser import restart_browser_if_needed

router = APIRouter()

@router.post("/reverse-search")
async def reverse_search():
    page = await restart_browser_if_needed()
    current_url = page.url
    return {"current_page": current_url}
