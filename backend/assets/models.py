import uuid
from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    ASSET_TYPES = (
        ("pdf", "PDF"),
        ("docx", "DOCX"),
        ("txt", "TXT"),
        ("image", "IMAGE"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_name = models.CharField(max_length=255)
    storage_path = models.CharField(max_length=512)
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPES)
    mime_type = models.CharField(max_length=100)
    size_bytes = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
