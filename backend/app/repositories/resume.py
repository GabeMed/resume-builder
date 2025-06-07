from typing import Dict, Protocol, Optional
from sqlmodel import Session, select
from models.resume import Resume


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

    def update(self, resume_in: Resume, resume_id: int) -> Optional[Resume]:
        """
        Update the fields of a resume.
        @param resume_in: The resume with the updated fields.
        @param resume_id: The id of the resume to update.
        @return: The updated resume or None if the resume was not found.
        """
        ...


class ResumeRepository(IResumeRepository):
    """
    Concrete implementation of IResumeRepository using SQLModel / SQLAlchemy.
    @attribute db: The SQLModel session.
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

    def update(self, resume_in: Resume, resume_id: int) -> Optional[Resume]:
        resume = self.db.get(Resume, resume_id)
        if not resume:
            return None
        update_data = resume_in.model_dump(exclude_unset=True)
        update_data.pop("id", None)
        update_data.pop("created_at", None)
        for field, value in update_data.items():
            setattr(resume, field, value)
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume
