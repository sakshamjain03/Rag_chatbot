from .embeddings import EmbeddingService
from .models import DocumentChunk, ChunkEmbedding


def retrieve_chunks(user, query, top_k=5):
    results = []

    # We search text + image separately
    for modality in ("text", "image"):
        service = EmbeddingService(user_id=user.id, modality=modality)

        query_embedding = service.embed_texts([query])
        if query_embedding is None:
            continue

        indices = service.search(query_embedding, top_k=top_k)

        if not indices:
            continue

        # Map FAISS indices back to DB chunks
        embeddings = (
            ChunkEmbedding.objects
            .filter(user=user, vector_id__in=indices, chunk__modality=modality)
            .select_related("chunk", "chunk__asset")
        )

        for emb in embeddings:
            results.append({
                "asset": emb.chunk.asset.original_name,
                "snippet": emb.chunk.content[:300],
            })

    return results