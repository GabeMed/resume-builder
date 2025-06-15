from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(ENV_PATH, override=False)


class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    UPLOAD_DIR: str
    AI_OUTPUT_DIR: str

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"
