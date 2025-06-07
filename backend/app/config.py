from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    UPLOAD_DIR: str = "./TEMP_FILES"
    AI_OUTPUT_DIR: str = "./AI_OUTPUT"

    class Config:
        env_file = ".env"
