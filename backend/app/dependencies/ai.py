from fastapi import Depends
from app.config import Settings
from app.ai.ai_client import IAIClient, OpenAIClient


def get_ai_client(settings: Settings = Depends()) -> IAIClient:
    return OpenAIClient(settings)
