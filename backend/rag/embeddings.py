# import faiss
import numpy as np
from pathlib import Path
# from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
FAISS_PATH = BASE_DIR / "data" / "faiss" / "index.bin"


class EmbeddingService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.dim = 384

        # Load model ONCE
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cuda"
        )

        # Load or create FAISS index
        if FAISS_PATH.exists():
            self.index = faiss.read_index(str(FAISS_PATH))
        else:
            self.index = faiss.IndexFlatL2(self.dim)

    def embed_texts(self, texts):
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        embeddings = np.asarray(embeddings, dtype="float32")

        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        return embeddings

    def add(self, embeddings):
        start_id = self.index.ntotal
        self.index.add(embeddings)
        self._persist()
        return list(range(start_id, start_id + embeddings.shape[0]))

    def search(self, query_embedding, top_k=5):
        if self.index.ntotal == 0:
            return []

        _, indices = self.index.search(query_embedding, top_k)
        return indices[0].tolist()

    def _persist(self):
        FAISS_PATH.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(FAISS_PATH))
