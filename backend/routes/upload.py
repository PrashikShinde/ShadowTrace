from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
import json
import numpy as np
from utils.embedding import generate_embedding

router = APIRouter()

UPLOAD_DIR = "uploads"
EMBEDDING_DB = "embeddings.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_embedding(filename, vector):
    data = []
    if os.path.exists(EMBEDDING_DB):
        with open(EMBEDDING_DB, "r") as f:
            data = json.load(f)
    data.append({
        "filename": filename,
        "vector": vector.tolist() if isinstance(vector, np.ndarray) else vector
    })
    with open(EMBEDDING_DB, "w") as f:
        json.dump(data, f)

@router.post("/")
async def upload_face(file: UploadFile = File(...)):
    try:
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{str(uuid.uuid4())}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        vector = generate_embedding(file_path)
        save_embedding(filename, vector)

        return {
            "message": "Upload successful",
            "filename": filename,
            "vector": vector.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
