def clean_text(text: str) -> str:
    return text.replace("\n", " ").replace("\r", " ").strip()