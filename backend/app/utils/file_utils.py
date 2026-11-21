"""
File Utilities
==============
Helpers for saving uploaded resume files to disk.
"""

import uuid
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def save_upload(file_content: bytes, filename: str) -> str:
    """
    Save uploaded file bytes to the uploads directory with a unique name.

    Returns the absolute file path as a string.
    """
    ext = Path(filename).suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / unique_name
    file_path.write_bytes(file_content)
    return str(file_path)


def allowed_file(filename: str) -> bool:
    """Return True if the file extension is supported."""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS
