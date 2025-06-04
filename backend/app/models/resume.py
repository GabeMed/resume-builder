import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Resume(SQLModel, table=True):
    """
    The entity representing a resume uploaded and its AI feedback.
    Violates the single responsibility principle, but it's fine for now.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    original_filename: str
    job_title: str
    resume_html_path: str
    feedback_text: Optional[str] = None
    revised_html_path: Optional[str] = None
