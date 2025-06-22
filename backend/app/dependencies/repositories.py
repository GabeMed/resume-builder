from typing import Annotated
from fastapi import Depends
from app.dependencies.database import SessionDep
from app.repositories.resume import IResumeRepository, ResumeRepository


def get_resume_repository(session: SessionDep) -> IResumeRepository:
    return ResumeRepository(db=session)


ResumeRepositoryDep = Annotated[IResumeRepository, Depends(get_resume_repository)]
