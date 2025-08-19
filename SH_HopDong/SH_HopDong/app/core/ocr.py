import os
from typing import Optional
from io import BytesIO

import fitz  # PyMuPDF
from PIL import Image
import pytesseract

from app.core.config import settings


if settings.tesseract_path and os.path.exists(settings.tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path


def extract_text_from_image(image_path: str, lang: Optional[str] = None) -> str:
    lang = lang or settings.default_lang
    image = Image.open(image_path)
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")
    text = pytesseract.image_to_string(image, lang=lang)
    return text.strip()


def extract_text_from_pdf(pdf_path: str, lang: Optional[str] = None) -> str:
    lang = lang or settings.default_lang
    doc = fitz.open(pdf_path)
    parts = []
    for page in doc:
        text = page.get_text().strip()
        if text:
            parts.append(text)
            continue
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        image = Image.open(BytesIO(img_bytes))
        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB")
        parts.append(pytesseract.image_to_string(image, lang=lang))
    doc.close()
    return "\n\n".join(p.strip() for p in parts if p and p.strip()) 