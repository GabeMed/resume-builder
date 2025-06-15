import os, shutil, uuid
from config import Settings
from dependencies.services import get_resume_service
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from services.resume import IResumeService

router = APIRouter(prefix="/resumes", tags=["resumes"])


##Todo move this util outside of the routers
def _store_temp(upload: UploadFile, settings: Settings) -> str:
    ext = os.path.splitext(upload.filename)[1]
    dest = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(dest, "wb") as fdst:
        shutil.copyfileobj(upload.file, fdst)
    return dest


##Todo return the resume object (Need to create the response objects)
@router.post("", response_model=int)
async def upload_resume(  ## Uploads the resume to a tempfile, create an object with the temp file information, and then deletes the temp
    file: UploadFile,
    job_title: str,
    service: IResumeService = Depends(get_resume_service),
    settings: Settings = Depends(),
):
    temp = _store_temp(file, settings)
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
