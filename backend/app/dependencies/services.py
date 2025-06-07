from ai.ai_client import IAIClient
from db.session import get_session
from dependencies.ai import get_ai_client
from dependencies.repositories import get_resume_repository
from fastapi import Depends
from repositories.resume import IResumeRepository
from services.resume import IResumeService, ResumeService
from sqlmodel import Session
from config import Settings


def get_resume_service(
    repo: IResumeRepository = Depends(get_resume_repository),
    session: Session = Depends(get_session),
    ai: IAIClient = Depends(get_ai_client),
    settings: Settings = Depends(),
) -> IResumeService:
    return ResumeService(
        repo,
        session,
        ai,
        settings.UPLOAD_DIR,
        settings.AI_OUTPUT_DIR,
    )
