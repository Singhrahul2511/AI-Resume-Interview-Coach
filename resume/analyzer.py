# resume/analyzer.py

import spacy

# Load the spaCy model once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Handle case where model is not downloaded
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def extract_keywords(text):
    """
    Extracts unique, clean keywords from text using spaCy for lemmatization.
    """
    doc = nlp(text.lower())
    keywords = set()
    for token in doc:
        # Filter out stopwords, punctuation, and spaces
        if not token.is_stop and not token.is_punct and not token.is_space:
            # Lemmatize the token (e.g., 'running' -> 'run')
            keywords.add(token.lemma_)
    return keywords

# ... (the rest of your analyzer.py file)

def compare_resume(resume_text, job_description):
    """Compares the resume and job description to find matched and missing keywords."""
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    matched_keywords = resume_keywords.intersection(job_keywords)
    missing_keywords = job_keywords.difference(resume_keywords)

    return matched_keywords, missing_keywords, job_keywords

def calculate_ats_score(matched_keywords, total_job_keywords):
    """Calculates the ATS score as a percentage."""
    if not total_job_keywords:
        return 0
    return (len(matched_keywords) / len(total_job_keywords)) * 100