import PyPDF2
import os

def load_pdf(file_path: str) -> str:
    """
    Loads a PDF file and returns all extracted text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found: {file_path}")

    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                print(f"[PDF Loader] Page {page_num + 1} contains no readable text")

    print(f"[PDF Loader] Loaded {len(reader.pages)} pages from PDF.")
    return text.strip()
