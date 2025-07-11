# utils.py

import fitz  # PyMuPDF

def extract_text_from_pdf(file) -> str:
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"⚠️ Failed to extract PDF text: {str(e)}"
