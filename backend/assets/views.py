from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .models import Asset
from .serializers import AssetSerializer
from .storage import S3Storage
import os

ALLOWED_EXTENSIONS = {
    "pdf": "pdf",
    "txt": "txt",
    "docx": "docx",
    "png": "image",
    "jpg": "image",
    "jpeg": "image",
}

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/png",
    "image/jpeg",
    "application/octet-stream",  # fallback for curl
}

class AssetUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=400)

        ext = os.path.splitext(file.name)[1].lower().replace(".", "")

        if ext not in ALLOWED_EXTENSIONS:
            return Response({"error": "Unsupported file extension"}, status=400)

        if file.content_type not in ALLOWED_MIME_TYPES:
            return Response({"error": "Unsupported MIME type"}, status=400)

        storage = S3Storage()
        key = storage.upload(request.user.id, file, file.name)

        asset = Asset.objects.create(
            user=request.user,
            original_name=file.name,
            storage_path=key,
            asset_type=ALLOWED_EXTENSIONS[ext],  
            mime_type=file.content_type,
            size_bytes=file.size,
        )

        try:
            from rag.ingestion import ingest_asset
            ingest_asset(asset)
        except Exception as e:
            # Log but DO NOT fail upload
            import logging
            logger = logging.getLogger(__name__)
            logger.exception("Ingestion failed for asset %s", asset.id)            
            
        try:
            from rag.ingestion import ingest_asset
            from rag.indexing import index_asset

            ingest_asset(asset)
            index_asset(asset)

        except Exception:
            logger.exception("Post-upload processing failed for asset %s", asset.id)

        return Response(AssetSerializer(asset).data, status=201)

class AssetListView(APIView):
    def get(self, request):
        assets = Asset.objects.filter(user=request.user)
        return Response(AssetSerializer(assets, many=True).data)


class AssetDeleteView(APIView):
    def delete(self, request, asset_id):
        asset = Asset.objects.filter(id=asset_id, user=request.user).first()
        if not asset:
            return Response(status=404)

        storage = S3Storage()
        storage.delete(asset.storage_path)
        asset.delete()
        return Response(status=204)
