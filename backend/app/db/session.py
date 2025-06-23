from sqlmodel import create_engine
from app.dependencies.settings import SettingsDep

settings = SettingsDep()
engine = create_engine(settings.DATABASE_URL, echo=True)
