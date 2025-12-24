from .embeddings import EmbeddingService
from .models import ChunkEmbedding

def retrieve_chunks(user, query, top_k=5):
    service = EmbeddingService(user.id)
    q = service.embed([query])

    ids = service.search(q, top_k)

    return ChunkEmbedding.objects.filter(
        user=user,
        vector_id__in=ids
    ).select_related("chunk", "chunk__asset")
