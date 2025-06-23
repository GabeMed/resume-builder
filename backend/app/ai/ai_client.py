from typing import Protocol
import textwrap
from app.config import Settings
import openai


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
        openai.api_key = settings.OPENAI_API_KEY

    def generate_feedback(self, resume_html: str, job_title: str) -> str:
        """
        Generate feedback and the revised html for a resume.
        """
        prompt = textwrap.dedent(
            f"""You are an expert recruiter and career coach. Below are the inputs:
                - [[{resume_html}]]: the candidate's current resume in raw HTML form.
                - [[{job_title}]]: the role the candidate is applying for.

                Generate exactly two sections in your output:

                1) **Analysis and Feedback**  
                - Critique the resume structure, content, and formatting relative to the target role.  
                - Identify strengths and areas for improvement (e.g., missing keywords, weak bullets, layout issues).  
                - Provide specific, actionable suggestions to optimize each section (summary, experience, skills, education) for the target role and ATS.

                2) **RevisedResumeHTML**  
                - Create a complete, professional HTML resume document that includes ALL the candidate's information from the original resume.
                - Improve the content, structure, and formatting to better match the target role requirements.
                - Include proper CSS styling in the <head> section for a clean, professional appearance.
                - Preserve all relevant information but enhance it for the target role.
                - Make sure the HTML is complete and functional - include all sections, content, and proper styling.
                - Do not include any explanations or comments outside the HTML structure.

                Output format (no extra text):

                1)
                <detailed analysis and feedback>

                2)
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Professional Resume</title>
                    <style>
                        /* Professional CSS styling for the resume */
                    </style>
                </head>
                <body>
                    <!-- Complete revised resume content with all sections -->
                </body>
                </html>
        """
        )
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
