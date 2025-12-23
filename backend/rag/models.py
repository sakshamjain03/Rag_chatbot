import uuid
from django.db import models
from django.contrib.auth.models import User
from assets.models import Asset

class DocumentChunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="chunks")
    chunk_index = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modality = models.CharField(
        max_length=10,
        choices=[("text", "text"), ("image", "image")],
        default="text",
    )

    class Meta:
        unique_together = ("asset", "chunk_index")

class ChunkEmbedding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chunk_embeddings",
    )
    chunk = models.OneToOneField(
        "DocumentChunk",
        on_delete=models.CASCADE,
        related_name="embedding",
    )
    vector_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Embedding(chunk={self.chunk.id}, vector_id={self.vector_id})"