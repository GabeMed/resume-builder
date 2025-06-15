from fastapi import Depends
from sqlmodel import Session
from app.repositories.resume import IResumeRepository, ResumeRepository


def get_resume_repository(session: Session = Depends()) -> IResumeRepository:
    return ResumeRepository(db=session)
