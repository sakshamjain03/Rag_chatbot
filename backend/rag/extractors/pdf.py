from pypdf import PdfReader
from io import BytesIO

def extract_pdf(content_bytes):
    reader = PdfReader(BytesIO(content_bytes))
    text = []
    for page in reader.pages:
        if page.extract_text():
            text.append(page.extract_text())
    return "\n".join(text)
