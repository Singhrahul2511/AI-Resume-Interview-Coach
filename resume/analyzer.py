import re

def extract_keywords(text):
    """
    Extracts unique, clean keywords from text using a simple split method.
    """
    # Remove punctuation, convert to lowercase, and split into words
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = set(text.split())
    # Remove common stopwords
    stopwords = {"i", "me", "my", "a", "an", "the", "and", "in", "is", "it"}
    return words - stopwords

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