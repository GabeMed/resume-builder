from typing import Annotated
from fastapi import Depends
from app.ai.ai_client import IAIClient, OpenAIClient
from app.dependencies.settings import SettingsDep


def get_ai_client(settings: SettingsDep) -> IAIClient:
    return OpenAIClient(settings)


AIClientDep = Annotated[IAIClient, Depends(get_ai_client)]
