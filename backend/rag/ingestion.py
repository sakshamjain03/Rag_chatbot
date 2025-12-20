from assets.storage import S3Storage
from .models import DocumentChunk
from .chunking import chunk_text
from .extractors.pdf import extract_pdf
from .extractors.docx import extract_docx
from .extractors.txt import extract_txt
from .extractors.image import extract_image_text

def ingest_asset(asset):
    storage = S3Storage()
    content = storage.download(asset.storage_path)

    if asset.asset_type == "pdf":
        text = extract_pdf(content)
    elif asset.asset_type == "docx":
        text = extract_docx(content)
    elif asset.asset_type == "txt":
        text = extract_txt(content)
    elif asset.asset_type == "image":
        text = extract_image_text(content)
    else:
        raise ValueError("Unsupported asset type")

    chunks = chunk_text(text)

    DocumentChunk.objects.filter(asset=asset).delete()

    for idx, chunk in enumerate(chunks):
        DocumentChunk.objects.create(
            user=asset.user,
            asset=asset,
            chunk_index=idx,
            content=chunk,
        )
