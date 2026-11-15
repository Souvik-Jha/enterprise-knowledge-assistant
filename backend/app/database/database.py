
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load environment variables from the project root .env file.
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# Read the database connection string.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured.")

# Create the database engine.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Create a factory for database sessions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Base class for our future SQLAlchemy models.
class Base(DeclarativeBase):
    pass


# Dependency for FastAPI endpoints.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
