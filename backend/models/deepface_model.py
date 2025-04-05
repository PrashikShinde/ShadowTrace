from deepface import DeepFace
import numpy as np

def generate_embedding(image_path):
    embedding_obj = DeepFace.represent(img_path=image_path, model_name="Facenet")[0]
    return embedding_obj["embedding"]

def compare_with_results(uploaded_vector, results):
    matches = []
    for result in results:
        try:
            result_vector = generate_embedding(result["image_path"])
            distance = np.linalg.norm(np.array(uploaded_vector) - np.array(result_vector))
            confidence = max(0, 100 - distance * 10)
            if confidence > 85:
                matches.append({
                    "source": result["source"],
                    "url": result["url"],
                    "match_confidence": round(confidence, 2)
                })
        except Exception as e:
            continue
    return matches