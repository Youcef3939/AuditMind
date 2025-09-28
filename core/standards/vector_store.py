import json
from pathlib import Path

EMBEDDED_FILE = Path("data/standards/embedded_standards.json")

class VectorStore:
    def __init__(self):
        self.vectors = []

    def load_embeddings(self):
        print("Loading embedded standards...")
        with open(EMBEDDED_FILE, "r", encoding="utf-8") as f:
            standards_data = json.load(f)  

        if not isinstance(standards_data, dict):
            raise ValueError("Standards data should be a dictionary of standards.")

        for standard_code, paragraphs in standards_data.items():
            for para in paragraphs:
                self.vectors.append({
                    "standard_code": standard_code,
                    "paragraph": para["paragraph"],
                    "text": para["text"],
                    "embedding": para["embedding"]
                })

        print(f"Loaded {len(self.vectors)} paragraph embeddings.")

# test
if __name__ == "__main__":
    store = VectorStore()
    store.load_embeddings()
    print("First item:", store.vectors[0])