from typing import Annotated
from app.config import Settings
from fastapi import Depends


def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
