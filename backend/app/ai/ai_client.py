from typing import Protocol
import openai, textwrap
from app.config import Settings


class IAIClient(Protocol):
    """
    Interface for AI clients.
    """

    def generate_feedback(self, resume_html: str, job_title: str) -> str:
        """
        Generate feedback for a resume.
        @param resume_html: The HTML extracted from the resume uploaded by the user.
        @param job_title: The job title the user is applying for.
        @return: The generated feedback formatted as:\n
                            1) <detailed analysis and feedback>. \n
                            2) <Revised resume HTML>.
        """
        ...


class OpenAIClient(IAIClient):
    """
    Concrete implementation of IAIClient using OpenAI.
    """

    def __init__(self, settings: Settings):
        self.api_key = settings.OPENAI_API_KEY

    def generate_feedback(self, resume_html: str, job_title: str) -> str:
        """
        Generate feedback for a resume.
        """
        prompt = textwrap.dedent(
            f"""You are an expert recruiter and career coach. Bellow deliminated by [[ ]] are the inputs:
                - [[{resume_html}]]: the candidate's current resume in raw HTML form.
                - [[{job_title}]]: the role the candidate is applying for.

                Generate exactly two sections in your output:

                1) **Analysis and Feedback**  
                - Critique the resume structure, content, and formatting relative to role.  
                - Identify strengths and areas for improvement (e.g., missing keywords, weak bullets, layout issues).  
                - Provide specific, actionable suggestions to optimize each section (summary, experience, skills, education) for the target role and ATS.

                2) **RevisedResumeHTML**  
                - Produce a complete HTML document (including `<head>` and CSS) that preserves the original content hierarchy but restyles everything to improve the resume for the target role, keep it simple basic and functional.  
                - Do not include any explanation only the updated HTML.  

                Output format (no extra text):

                1)
                <detailed analysis and feedback>

                2)
                <!DOCTYPE html> <html> <head> <!-- CSS to improve the resume for the target role --> </head> <body> <!-- Restyled resume content --> </body> </html> 
        """
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
