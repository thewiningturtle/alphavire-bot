import re
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Clean the given text by removing HTML tags, URLs, and extra spaces.
    """
    soup = BeautifulSoup(text, "html.parser")
    cleaned = soup.get_text()
    cleaned = re.sub(r"http\S+", "", cleaned)  # remove URLs
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def extract_summary(entry):
    """
    Extract and clean summary text from RSS feed entry.
    """
    if hasattr(entry, "summary"):
        return clean_text(entry.summary)
    elif hasattr(entry, "description"):
        return clean_text(entry.description)
    else:
        return ""
