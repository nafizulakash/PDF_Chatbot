import pypdf

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = pypdf.PdfReader(pdf_file)   # use pypdf, not PyPDF2
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text if text else "No text found in PDF (might be scanned images)."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"