"""SQLAlchemy database setup."""
from sqlalchemy import create_engine, inspect
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
    # create_all does not add columns to tables that already exist. Keep the
    # small SQLite deployment schema upgrade explicit and safe to repeat.
    if engine.dialect.name == "sqlite":
        columns = {column["name"] for column in inspect(engine).get_columns("change_events")}
        with engine.begin() as connection:
            if "is_demonstration" not in columns:
                connection.exec_driver_sql(
                    "ALTER TABLE change_events ADD COLUMN is_demonstration BOOLEAN NOT NULL DEFAULT 0"
                )
            if "scenario_id" not in columns:
                connection.exec_driver_sql("ALTER TABLE change_events ADD COLUMN scenario_id VARCHAR(100)")
        # Create indexes after the columns exist, including for legacy databases.
        with engine.begin() as connection:
            connection.exec_driver_sql(
                "CREATE INDEX IF NOT EXISTS ix_change_events_is_demonstration ON change_events (is_demonstration)"
            )
            connection.exec_driver_sql(
                "CREATE INDEX IF NOT EXISTS ix_change_events_scenario_id ON change_events (scenario_id)"
            )
