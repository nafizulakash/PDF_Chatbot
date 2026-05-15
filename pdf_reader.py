import pypdf

def extract_text_from_pdf(pdf_file):
    """
    Extract text from PDF file
    
    Args:
        pdf_file: File object from Streamlit upload
    
    Returns:
        str: All text from the PDF
    """
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        # Go through each page and extract text
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            text += page_text + "\n"
        
        return text
    
    except Exception as e:
        return f"Error reading PDF: {str(e)}"