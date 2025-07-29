import re
import spacy
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Load models and data only once at module load
nlp = spacy.load("en_core_web_sm")
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("punkt_tab", quiet=True)

stop_words = set(stopwords.words("english"))

# Extend your skills database here or load dynamically from a file
skills_db = {
    "python", "sql", "django", "flask", "machine learning", "deep learning",
    "docker", "java", "html", "aws", "langchain", "nlp", "c++", "javascript",
    "react", "git", "linux", "tensorflow", "pytorch"
}

# Regex patterns centralized for reusability
EMAIL_PATTERN = re.compile(r'\b[\w.-]+?@\w+?\.\w+?\b')
PHONE_PATTERN = re.compile(r'\+?\d[\d\s\-]{8,}\d')

def extract_names(text):
    """
    Extract the first detected person name entity using spaCy's NER.
    """
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":  # spaCy entity labels are uppercase
            return ent.text
    return None

def extract_email(text):
    """
    Extract the first email found in the text.
    """
    match = EMAIL_PATTERN.findall(text)
    return match[0] if match else None

def extract_phone(text):
    """
    Extract the first phone number found in the text.
    """
    match = PHONE_PATTERN.findall(text)
    return match[0] if match else None

def extract_skills(text):
    tokens = nltk.word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token.isalpha() and token not in stop_words]

    token_counts = Counter(filtered_tokens)  # Count occurrences of each token

    found_skills = {skill: token_counts[skill.lower()] for skill in skills_db if skill.lower() in token_counts}
    # Sort by frequency descending
    sorted_skills = sorted(found_skills.items(), key=lambda x: x[1], reverse=True)

    return sorted_skills  # returns list of tuples (skill, count)

def resume_score(parsed_data):
    """
    A simple scoring system to rate the resume based on presence of key fields.
    For demonstration, score is weighted sum of found fields.
    """
    score = 0
    max_score = 100

    # Weights for each component
    weights = {
        "name": 20,
        "email": 20,
        "phone": 15,
        "skills": 45,
    }

    # Add score if field present
    if parsed_data.get("name"):
        score += weights["name"]
    if parsed_data.get("email"):
        score += weights["email"]
    if parsed_data.get("phone"):
        score += weights["phone"]

    # Score for skills is proportional to how many are found (capped at max)
    num_skills_found = len(parsed_data.get("skills", []))
    max_skills_considered = 10  # For example, max 10 skills counted

    skills_score = (min(num_skills_found, max_skills_considered) / max_skills_considered) * weights["skills"]
    score += skills_score

    # Normalize score to 0-100 scale (just in case)
    return round(min(score, max_score), 2)

def parse_resume(text):
    """
    Extract resume data and calculate a score.

    Returns:
        dict: {
            'name': str or None,
            'email': str or None,
            'phone': str or None,
            'skills': list of str,
            'score': float
        }
    """
    parsed = {
        "name": extract_names(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }
    parsed["score"] = resume_score(parsed)
    return parsed

