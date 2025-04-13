import re
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Remove HTML tags, extra spaces, and unwanted characters from the summary.
    """
    soup = BeautifulSoup(text, "html.parser")
    cleaned = soup.get_text()
    cleaned = re.sub(r'\s+', ' ', cleaned)  # collapse multiple spaces
    cleaned = cleaned.strip()
    return cleaned

def extract_summary(entry):
    """
    Extract a meaningful summary from the RSS feed entry.
    """
    if hasattr(entry, 'summary') and entry.summary:
        return clean_text(entry.summary)
    elif hasattr(entry, 'description') and entry.description:
        return clean_text(entry.description)
    elif hasattr(entry, 'content') and entry.content:
        return clean_text(entry.content[0].value)
    else:
        return "No summary available."
