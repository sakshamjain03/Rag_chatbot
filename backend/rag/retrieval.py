import numpy as np
from rag.embeddings import EmbeddingService
from rag.models import ChunkEmbedding

service = EmbeddingService()

def retrieve_chunks(user, query, top_k=5):
    query_embedding = service.embed_texts([query])
    indices = service.search(query_embedding, top_k=top_k)

    embeddings = ChunkEmbedding.objects.filter(
        user=user,
        vector_id__in=indices
    ).select_related("chunk", "chunk__asset")

    return embeddings