"""Text preprocessing utilities."""

import re


def clean_text(text: str) -> str:
    """Remove extra whitespace and non-ASCII characters."""
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def truncate_text(text: str, max_chars: int = 2000) -> str:
    """Truncate text for embedding model input."""
    return text[:max_chars]
