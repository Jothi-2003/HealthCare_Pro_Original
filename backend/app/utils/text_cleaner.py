# utils/text_cleaner.py
import re

def clean_text(text: str) -> str:
    text = re.sub(r"\W+", " ", text)
    return text.strip().lower()