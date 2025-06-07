from fastapi import Depends
from config import Settings
from ai.ai_client import IAIClient, OpenAIClient


def get_ai_client(settings: Settings = Depends()) -> IAIClient:
    return OpenAIClient(settings)
