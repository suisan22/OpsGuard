import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Automatically prefix Postgres URLs with +psycopg2 for SQLAlchemy compatibility
db_url = settings.DATABASE_URL
if db_url and db_url.startswith(("postgres://", "postgresql://")):
    db_url = re.sub(r"^postgres(ql)?://", "postgresql+psycopg2://", db_url)

engine = create_engine(db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()