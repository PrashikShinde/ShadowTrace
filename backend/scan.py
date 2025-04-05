from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from search.playwright_search import run_all_searches

router = APIRouter()

class ScanRequest(BaseModel):
    filename: str
    vector: list

@router.post("/scan")
async def scan_face(data: ScanRequest):
    try:
        image_path = f"uploads/{data.filename}"  # assuming uploads/ stores files
        matches = run_all_searches(image_path)
        return {
            "message": "Scan initiated",
            "filename": data.filename,
            "matches": matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
