# pdfplumber example
import pdfplumber

def extract_text_pdfplumber(filepath):
    with pdfplumber.open(filepath) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# PyPDF2 example
from PyPDF2 import PdfReader

def extract_text_pypdf2(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
