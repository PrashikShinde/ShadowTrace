from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
import json
import numpy as np
from utils.embedding import generate_embedding, cosine_similarity

router = APIRouter()

UPLOAD_DIR = "uploads"
EMBEDDING_DB = "embeddings.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_embeddings():
    if not os.path.exists(EMBEDDING_DB):
        return []
    with open(EMBEDDING_DB, "r") as f:
        return json.load(f)

@router.post("/")
async def scan_face(file: UploadFile = File(...)):
    try:
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{str(uuid.uuid4())}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        vector = generate_embedding(file_path)
        if isinstance(vector, list):
            vector = np.array(vector)

        stored = load_embeddings()

        best_match = None
        highest_score = 0.0
        for item in stored:
            stored_vector = np.array(item["vector"])
            similarity = cosine_similarity(vector, stored_vector)
            if similarity > highest_score:
                highest_score = similarity
                best_match = item

        if best_match and highest_score > 0.75:
            return {
                "message": "Scan successful",
                "match": {
                    "filename": best_match["filename"],
                    "similarity": highest_score
                },
                "scanned_filename": filename,
                "vector": vector.tolist()
            }
        else:
            return {
                "message": "Scan successful, but no match found",
                "scanned_filename": filename,
                "vector": vector.tolist()
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
