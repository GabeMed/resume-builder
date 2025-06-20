import os
from typing import Dict, Optional, Protocol
from app.ai.ai_client import IAIClient
from app.extractors.docling_extractor import extract_html_from_file
from app.generators.pdf_weasy_generator import generate_pdf
from app.models.resume import Resume
from app.repositories.resume import IResumeRepository
from sqlmodel import Session


class IResumeService(Protocol):
    """
    Interface for business-level operations on resumes.
    """

    def upload(self, file_path: str, original_filename: str, job_title: str) -> Resume:
        """
        Upload a new resume.
        @param file_path: The path to where the resume file will be saved.
        @param original_filename: The original filename of the resume.
        @param job_title: The job title the user is applying for.
        @return: The uploaded resume.
        """
        ...

    def get_resume(self, id: int) -> Resume:
        """
        Get a resume by id.
        @param id: The id of the resume.
        @return: The resume or None if not found.
        """
        ...


class ResumeService(IResumeService):
    """
    Concrete implementation of the resume service.
    @attribute resume_repository: An instance of the resume repository.
    @attribute session: An instance of the SQLModel session.
    @attribute ai_client: An instance of the AI client.
    @attribute upload_dir: The directory to upload the resumes.
    @attribute ai_output_dir: The directory to save the AI output.
    """

    def __init__(
        self,
        resume_repository: IResumeRepository,
        session: Session,
        ai_client: IAIClient,
        upload_dir: str,
        ai_output_dir: str,
    ):
        self.resume_repository = resume_repository
        self.session = session
        self.ai_client = ai_client
        self.upload_dir = upload_dir
        self.ai_output_dir = ai_output_dir

    def upload(self, file_path: str, original_filename: str, job_title: str) -> Resume:
        resume = self.__create_initial(original_filename, job_title)
        resume_html = extract_html_from_file(file_path)
        ai_response = self.ai_client.generate_feedback(resume_html, job_title)
        ai_response_dict = self.__parse_ai_response(ai_response)
        result_pdf_path = self._make_pdf(ai_response_dict["revised_html"], resume.id)
        resume_new = Resume(
            resume_html=resume_html,
            feedback_text=ai_response_dict["feedback_text"],
            revised_html=ai_response_dict["revised_html"],
            result_pdf_path=result_pdf_path,
        )
        self.resume_repository.update(resume_new, resume.id)
        return resume_new

    def get_resume(self, id: int) -> Optional[Resume]:
        self.resume_repository.get_by_id(id)

    def __create_initial(self, original_filename: str, job_title: str) -> Resume:
        resume = Resume(original_filename=original_filename, job_title=job_title)
        self.resume_repository.create(resume)
        return resume

    def __parse_ai_response(self, ai_response: str) -> Dict[str, str]:
        feedback_text = (
            ai_response.split("1)")[0].strip()
            if "1)" in ai_response
            else ai_response.strip()
        )
        revised_html = ai_response.split("2)")[1].strip() if "2)" in ai_response else ""
        return {"feedback_text": feedback_text, "revised_html": revised_html}

    def _make_pdf(self, revised_html: str, resume_id: int) -> str:
        os.makedirs(self.ai_output_dir, exist_ok=True)
        output_path = os.path.join(self.ai_output_dir, f"{resume_id}_revised.pdf")
        generate_pdf(revised_html, output_path)
        return output_path
