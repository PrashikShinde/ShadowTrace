from fastapi import FastAPI # type: ignore
from app.api import upload, reverse_search
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from app.services.playwright_browser import start_browser_persistent
from app.api import scrape_results

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await start_browser_persistent()

app.include_router(upload.router)
app.include_router(reverse_search.router)
app.include_router(scrape_results.router)
