import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

class EmbeddingService:
    def __init__(self, user_id):
        self.user_id = str(user_id)
        self.dim = 384
        
        # User-specific path
        self.index_path = BASE_DIR / "data" / "faiss" / f"user_{self.user_id}" / "index.bin"

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )

        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
        else:
            self.index = faiss.IndexFlatL2(self.dim)

    # --- CHANGED NAME HERE: from embed_texts to embed ---
    def embed(self, texts):
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        embeddings = np.asarray(embeddings, dtype="float32")

        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        return embeddings
    # ----------------------------------------------------

    def add(self, embeddings):
        start_id = self.index.ntotal
        self.index.add(embeddings)
        self._persist()
        return list(range(start_id, start_id + embeddings.shape[0]))

    def search(self, query_embedding, top_k=5):
        if self.index.ntotal == 0:
            return []

        _, indices = self.index.search(query_embedding, top_k)
        
        # Filter out invalid indices (-1)
        valid_indices = [i for i in indices[0].tolist() if i >= 0]
        return valid_indices

    def _persist(self):
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))