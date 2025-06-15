import os
from app.config import Settings
from app.dependencies.services import get_resume_service
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from app.services.resume import IResumeService
from app.utils.file_utils import store_temp_file

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("", response_model=int)
async def upload_resume(
    file: UploadFile = File(...),
    job_title: str = Form(...),
    service: IResumeService = Depends(get_resume_service),
    settings: Settings = Depends(),
):
    temp = store_temp_file(file, settings)
    try:
        resume = service.upload(temp, file.filename, job_title)
        return resume.id
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        if os.path.exists(temp):
            os.remove(temp)


@router.get("/{resume_id}")
def get_resume(resume_id: int, service: IResumeService = Depends(get_resume_service)):
    resume = service.get_resume(resume_id)
    if not resume:
        raise HTTPException(404, "Resume not found")
    return {
        "id": resume.id,
        "feedback_text": resume.feedback_text,
        "download_url": f"/resumes/{resume.id}/download",
    }


@router.get("/{resume_id}/download")
def download(resume_id: int, service: IResumeService = Depends(get_resume_service)):
    resume = service.get_resume(resume_id)
    if not resume or not resume.revised_html:
        raise HTTPException(404)
    return {"html": resume.revised_html}
