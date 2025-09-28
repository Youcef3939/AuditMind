import json
from pathlib import Path
import numpy as np

EMBEDDED_FILE = Path("data/standards/embedded_standards.json")


class VectorStore:
    """Loads the paragraph embeddings from JSON."""
    def __init__(self):
        self.vectors = []

    def load_embeddings(self):
        print("Loading embedded standards...")
        with open(EMBEDDED_FILE, "r", encoding="utf-8") as f:
            standards_data = json.load(f)  # load as dict

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


class VectorSearch:
    """Vector search engine using cosine similarity (free mode)."""
    def __init__(self):
        self.vectors = []

    def load_embeddings(self):
        store = VectorStore()
        store.load_embeddings()
        self.vectors = store.vectors

    def query(self, text_embedding=None, top_k=5):
        """Returns top_k matches using cosine similarity.

        For now, generates a random embedding for the query (free mode).
        """
        if not self.vectors:
            raise ValueError("No embeddings loaded. Call load_embeddings() first.")

        # Free mode: generate dummy embedding
        query_vec = np.random.rand(len(self.vectors[0]["embedding"]))

        results = []
        for v in self.vectors:
            emb = np.array(v["embedding"])
            score = np.dot(query_vec, emb) / (np.linalg.norm(query_vec) * np.linalg.norm(emb))
            results.append({"score": score, **v})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]


# Quick test when running directly
if __name__ == "__main__":
    search = VectorSearch()
    search.load_embeddings()
    top_results = search.query(top_k=3)
    print("Top 3 results:")
    for r in top_results:
        print(f"Score: {r['score']:.4f}, Standard: {r['standard_code']}, Paragraph: {r['paragraph']}")
        print(f"Text: {r['text']}\n")