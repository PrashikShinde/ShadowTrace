from deepface import DeepFace

MODELS = ["Facenet", "VGG-Face", "ArcFace", "DeepFace"]

def compare_faces(uploaded_path, candidate_path):
    results = []
    for model in MODELS:
        try:
            result = DeepFace.verify(
                img1_path=uploaded_path,
                img2_path=candidate_path,
                model_name=model,
                detector_backend='opencv',  # you can test with mtcnn too
                enforce_detection=True
            )
            results.append(result["distance"])
        except Exception as e:
            print(f"Error with {model}: {str(e)}")

    if not results:
        return None

    avg_distance = sum(results) / len(results)
    match = avg_distance < 0.4  # tune this threshold
    return {
        "average_distance": avg_distance,
        "match": match
    }
