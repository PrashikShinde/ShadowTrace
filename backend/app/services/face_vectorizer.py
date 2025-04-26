from deepface import DeepFace # type: ignore
from pathlib import Path

def extract_face_vectors(image_path: Path):
    """
    Extracts embeddings for all detected faces in the image using Facenet512.
    Returns a list of vectors.
    """
    try:
        embeddings = DeepFace.represent(
            img_path=str(image_path),
            model_name="Facenet512",
            enforce_detection=False  # Allow side faces, blurry faces, etc.
        )
        return [e["embedding"] for e in embeddings]
    except Exception as e:
        print(f"[DeepFace Error] {e}")
        return []
