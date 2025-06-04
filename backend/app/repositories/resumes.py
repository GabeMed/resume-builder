from typing import Protocol, Optional
from sqlmodel import Session, select
from app.models.resume import Resume


class IResumeRepository(Protocol):
    """
    Interface for the resume repository.
    """

    def create(self, resume: Resume) -> Resume:
        """
        Persist a new resume in the database and return the saved instace.
        @param resume: The resume to save.
        @return: The saved resume.
        """
        ...

    def get_by_id(self, resume_id: int) -> Optional[Resume]:
        """
        Retrieve a resume by its id.
        @param resume_id: The id of the resume to get.
        @return: The resume with the given id, or None if not found.
        """
        ...

    def update_feedback(
        self, resume_id: int, feedback_text: str, revised_html_path: str
    ) -> Optional[Resume]:
        """
        Update the feedback of a resume.
        @param resume_id: The id of the resume to update.
        @param feedback_text: The feedback text to update.
        @param revised_html_path: The path of the revised html file to update.
        @return: The updated resume or None if the resume was not found.
        """
        ...


class ResumeRepository(IResumeRepository):
    """
    Concrete implementation of IResumeRepository using SQLModel / SQLAlchemy.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, resume: Resume) -> Resume:
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get_by_id(self, resume_id: int) -> Optional[Resume]:
        return self.db.get(Resume, resume_id)

    def update_feedback(
        self, resume_id: int, feedback_text: str, revised_html_path: str
    ) -> Optional[Resume]:
        resume = self.db.get(Resume, resume_id)
        if not resume:
            return None
        resume.feedback_text = feedback_text
        resume.revised_html_path = revised_html_path
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume
