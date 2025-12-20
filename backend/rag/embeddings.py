from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cuda"
        )
        self.dim = 384
        self.index = faiss.IndexFlatL2(self.dim)

    def embed_texts(self, texts):
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return np.array(embeddings).astype("float32")

    def add(self, embeddings):
        start_id = self.index.ntotal
        self.index.add(embeddings)
        return list(range(start_id, start_id + len(embeddings)))

    def search(self, query_embedding, top_k=5):
        distances, indices = self.index.search(query_embedding, top_k)
        return indices[0]