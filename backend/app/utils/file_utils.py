import os
import shutil
import uuid
from fastapi import UploadFile
from app.config import Settings


def store_temp_file(upload: UploadFile, settings: Settings) -> str:
    """Store an uploaded file in a temporary location.

    Args:
        upload: The uploaded file
        settings: Application settings

    Returns:
        str: Path to the stored temporary file
    """
    ext = os.path.splitext(upload.filename)[1]
    dest = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(dest, "wb") as fdst:
        shutil.copyfileobj(upload.file, fdst)
    return dest
