# resume/extractor.py

import fitz  # PyMuPDF
from docx import Document
import io

def load_pdf_text(file_stream):
    """Extracts text from a PDF file stream."""
    try:
        doc = fitz.open(stream=file_stream.read(), filetype="pdf")
        text_data = ""
        for page in doc:
            text_data += page.get_text()
        return text_data
    except Exception as e:
        return f"Error reading PDF: {e}"

def load_docx_text(file_stream):
    """Extracts text from a DOCX file stream."""
    try:
        doc = Document(file_stream)
        text_data = []
        for para in doc.paragraphs:
            text_data.append(para.text)
        return "\n".join(text_data)
    except Exception as e:
        return f"Error reading DOCX: {e}"