import PyPDF2
from io import BytesIO

def extract_text(file):
    """Extract text from PDF or TXT file"""
    if file.type == "application/pdf":
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            return " ".join(page.extract_text() for page in pdf_reader.pages)
        except Exception as e:
            print(f"PDF Error: {e}")
            return ""
    elif file.type == "text/plain":
        return str(file.read(), "utf-8")
    return ""

def detect_topics(text, max_topics=5):
    """Topic detection using subheadings"""
    lines = text.split('\n')
    topics = []
    for line in lines:
        if line.strip().endswith(":") or (line.strip() and line.strip()[0].isupper()):
            topics.append(line.strip())
            if len(topics) >= max_topics:
                break
    return topics