
import os
from pypdf import PdfReader
import docx

def extract_text_from_pdf(path):
    """
    Extract text content from a PDF file using pypdf.
    
    Args:
        path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text from the PDF.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF file not found: {path}")

    text = ""
    reader = PdfReader(path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


def extract_text_from_docx(path):
    """
    Extract text content from a DOCX file.
    
    Args:
        path (str): Path to the DOCX file.
    
    Returns:
        str: Extracted text from the DOCX.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"DOCX file not found: {path}")

    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])
