import json
from pathlib import Path

DB_FILE = Path("data/embeddings.json")
DB_FILE.parent.mkdir(exist_ok=True)

def load_embeddings():
    if not DB_FILE.exists():
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_embedding(filename: str, vector):
    data = load_embeddings()
    data.append({
        "filename": filename,
        "embedding": vector
    })
    with open(DB_FILE, "w") as f:
        json.dump(data, f)
