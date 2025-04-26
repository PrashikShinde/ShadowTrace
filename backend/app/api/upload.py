from fastapi import APIRouter, UploadFile, File # type: ignore
from app.services.playwright_browser import restart_browser_if_needed
import os
import shutil

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    page = await restart_browser_if_needed()

    # Save file to server
    uploads_folder = "uploads"
    os.makedirs(uploads_folder, exist_ok=True)
    file_location = os.path.join(uploads_folder, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Open Google Images
    await page.goto("https://images.google.com")
    await page.wait_for_timeout(3000)  # give 3 seconds to load properly

    # Find the "camera" icon button and click it
    try:
        upload_image_button = await page.wait_for_selector('div[aria-label="Search by image"]', timeout=5000)
        await upload_image_button.click()
    except Exception as e:
        print("Couldn't find camera button:", e)
        return {"message": "Failed to find upload button on Google Images."}

    await page.wait_for_timeout(2000)

    # Now find the upload input field
    input_elem = await page.query_selector('input[type="file"]')

    if input_elem:
        await input_elem.set_input_files(file_location)
        return {"message": "Image uploaded successfully"}
    else:
        return {"message": "Failed to find file input to upload image."}
