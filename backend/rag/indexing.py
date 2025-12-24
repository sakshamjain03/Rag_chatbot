from .models import DocumentChunk, ChunkEmbedding
from .embeddings import EmbeddingService

service = EmbeddingService()

def index_asset(asset):
    chunks = DocumentChunk.objects.filter(asset=asset)
    texts = [c.content for c in chunks]

    embeddings = service.embed_texts(texts)
    vector_ids = service.add(embeddings)

    for chunk, vid in zip(chunks, vector_ids):
        ChunkEmbedding.objects.create(
            user=chunk.user,
            chunk=chunk,
            vector_id=vid
        )