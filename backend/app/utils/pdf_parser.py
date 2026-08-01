from pypdf import PdfReader
from io import BytesIO

def extract_text(file_bytes):
    f = BytesIO(file_bytes)
    reader = PdfReader(f)
    texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            texts.append(text)
    return "\n".join(texts)