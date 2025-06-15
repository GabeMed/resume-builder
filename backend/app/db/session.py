from sqlmodel import create_engine, Session
from app.config import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
