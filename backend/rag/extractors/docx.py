from docx import Document
from io import BytesIO

def extract_docx(content_bytes):
    doc = Document(BytesIO(content_bytes))
    return "\n".join(p.text for p in doc.paragraphs)
