from django.urls import path
from .views import AssetUploadView, AssetListView, AssetDeleteView, AssetUpdateView

urlpatterns = [
    path("", AssetListView.as_view()),
    path("upload/", AssetUploadView.as_view()),
    path("<uuid:asset_id>/", AssetDeleteView.as_view()),
    path("<uuid:asset_id>/update/", AssetUpdateView.as_view()),
]
