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

    def create_initial(self, original_filename: str, job_title: str) -> Resume:
        """
        Create an initial resume entry in the database.
        @param original_filename: The original filename of the resume
        @param job_title: The job title the user is applying for
        @return: The created resume
        """
        ...

    def parse_ai_response(self, ai_response: str) -> Dict[str, str]:
        """
        Parse the AI response into feedback text and revised HTML.
        @param ai_response: The raw AI response string
        @return: Dictionary containing feedback_text and revised_html
        """
        ...

    def make_pdf(self, revised_html: str, resume_id: int) -> str:
        """
        Generate a PDF from the revised HTML content.
        @param revised_html: The HTML content to convert to PDF
        @param resume_id: The ID of the resume
        @return: Path to the generated PDF file
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
        resume = self.create_initial(original_filename, job_title)
        resume_html = extract_html_from_file(file_path)
        ai_response = self.ai_client.generate_feedback(resume_html, job_title)
        ai_response_dict = self.parse_ai_response(ai_response)
        result_pdf_path = self.make_pdf(ai_response_dict["revised_html"], resume.id)
        resume_new = Resume(
            resume_html=resume_html,
            feedback_text=ai_response_dict["feedback_text"],
            revised_html=ai_response_dict["revised_html"],
            result_pdf_path=result_pdf_path,
        )
        self.resume_repository.update(resume_new, resume.id)
        return resume_new

    def get_resume(self, id: int) -> Optional[Resume]:
        return self.resume_repository.get_by_id(id)

    def create_initial(self, original_filename: str, job_title: str) -> Resume:
        resume = Resume(original_filename=original_filename, job_title=job_title)
        self.resume_repository.create(resume)
        return resume

    def parse_ai_response(self, ai_response: str) -> Dict[str, str]:
        parts = ai_response.split("1)")
        if len(parts) < 2:
            return {"feedback_text": ai_response.strip(), "revised_html": ""}
        after_1 = parts[1]
        feedback_parts = after_1.split("2)")
        if len(feedback_parts) < 2:
            return {"feedback_text": after_1.strip(), "revised_html": ""}
        feedback_text = feedback_parts[0].strip()
        revised_html = feedback_parts[1].strip()
        return {"feedback_text": feedback_text, "revised_html": revised_html}

    def make_pdf(self, revised_html: str, resume_id: int) -> str:
        os.makedirs(self.ai_output_dir, exist_ok=True)
        output_path = os.path.join(self.ai_output_dir, f"{resume_id}_revised.pdf")
        generate_pdf(revised_html, output_path)
        return output_path


class MockResumeService(IResumeService):
    """
    Mock implementation of the resume service.
    """

    def upload(self, job_title: str) -> Resume:
        return Resume(
            id=1,
            feedback_text="mock_feedback",
            revised_html="mock_html",
            job_title=job_title,
        )

    def get_resume(self, id: int) -> Optional[Resume]:
        return Resume(
            id=id,
            feedback_text="mock_feedback",
            revised_html="mock_html",
            job_title="mock_job_title",
        )
