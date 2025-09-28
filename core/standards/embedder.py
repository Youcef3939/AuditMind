from pathlib import Path
import json
from sentence_transformers import SentenceTransformer
from .parser import load_all_standards

model = SentenceTransformer("all-MiniLM-L6-v2")  

def embed_text(text):
    """
    generate embedding vector for a given text using a free local model.
    returns list of floats.
    """
    return model.encode(text).tolist()

def embed_all_standards(output_file=None):
    """
    embed all loaded standards paragraphs
    returns:
        dict: {standard_code: [{paragraph, text, embedding}, ...]}
    """
    standards = load_all_standards()
    embedded_standards = {}

    for code, standard in standards.items():
        embedded_paragraphs = []
        for para in standard['paragraphs']:
            text = para['text']
            embedding = embed_text(text)
            embedded_paragraphs.append({
                "paragraph": para['paragraph'],
                "text": text,
                "embedding": embedding
            })
        embedded_standards[code] = embedded_paragraphs

    if output_file:
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(embedded_standards, f, ensure_ascii=False, indent=2)
        print(f"Embeddings saved to {output_path}")

    return embedded_standards

# test
if __name__ == "__main__":
    embedded = embed_all_standards("data/standards/embedded_standards.json")
    print("Embedding complete.")
    first_code = list(embedded.keys())[0]
    print(f"First paragraph embedding for {first_code}:")
    print(embedded[first_code][0])