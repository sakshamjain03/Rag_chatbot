from PIL import Image
import pytesseract
import io

def extract_image_text(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, lang="eng")
    return text.strip()
