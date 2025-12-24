from rest_framework import serializers
from .models import Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = [
            "id",
            "original_name",
            "asset_type",
            "mime_type",
            "size_bytes",
            "uploaded_at",
        ]
