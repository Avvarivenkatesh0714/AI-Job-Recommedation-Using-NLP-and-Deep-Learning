import spacy
import PyPDF2

nlp = spacy.load("en_core_web_sm")

def extract_skills_from_resume(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    doc = nlp(text)
    skills = [token.text.lower() for token in doc if token.is_alpha]
    return list(set(skills))
