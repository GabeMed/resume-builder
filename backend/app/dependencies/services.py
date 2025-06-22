from typing import Annotated
from app.dependencies.database import SessionDep
from app.dependencies.ai import AIClientDep
from app.dependencies.repositories import ResumeRepositoryDep
from fastapi import Depends
from app.services.resume import IResumeService, ResumeService, MockResumeService
from app.dependencies.settings import SettingsDep


def get_resume_service(
    repo: ResumeRepositoryDep,
    session: SessionDep,
    ai: AIClientDep,
    settings: SettingsDep,
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


ResumeServiceDep = Annotated[IResumeService, Depends(get_resume_service)]
