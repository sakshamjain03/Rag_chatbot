from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .models import Asset
from .serializers import AssetSerializer
from .storage import S3Storage

ALLOWED_TYPES = {
    "application/pdf": "pdf",
    "text/plain": "txt",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "image/png": "image",
    "image/jpeg": "image",
}

class AssetUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=400)

        if file.content_type not in ALLOWED_TYPES:
            return Response({"error": "Unsupported file type"}, status=400)

        storage = S3Storage()
        key = storage.upload(request.user.id, file, file.name)

        asset = Asset.objects.create(
            user=request.user,
            original_name=file.name,
            storage_path=key,
            asset_type=ALLOWED_TYPES[file.content_type],
            mime_type=file.content_type,
            size_bytes=file.size,
        )

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
