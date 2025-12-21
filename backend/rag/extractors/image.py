from PIL import Image
import pytesseract
from io import BytesIO

def extract_image_text(content_bytes):
    image = Image.open(BytesIO(content_bytes))
    return pytesseract.image_to_string(image)
