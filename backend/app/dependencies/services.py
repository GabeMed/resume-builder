from app.ai.ai_client import IAIClient
from app.db.session import get_session
from app.dependencies.ai import get_ai_client
from app.dependencies.repositories import get_resume_repository
from fastapi import Depends
from app.repositories.resume import IResumeRepository
from app.services.resume import IResumeService, ResumeService, MockResumeService
from sqlmodel import Session
from app.config import Settings


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


def get_mock_resume_service() -> IResumeService:
    return MockResumeService()
