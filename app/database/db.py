"""SQLAlchemy database setup."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

def initialize() -> None:
    from app.models.scholarship import Scholarship, Evidence, ChangeEvent, CrawlRun, SourceSnapshot  # noqa: F401
    Base.metadata.create_all(engine)
