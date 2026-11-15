
from sqlalchemy import select

from app.database.database import SessionLocal
from app.database.models import Company, Document, DocumentChunk


def test_models():
    db = SessionLocal()

    try:
        # Check whether SQLAlchemy can query the companies table.
        statement = select(Company)
        companies = db.scalars(statement).all()

        print("Companies:", companies)

        print("Company model:", Company.__tablename__)
        print("Document model:", Document.__tablename__)
        print("Chunk model:", DocumentChunk.__tablename__)

        print("ORM models loaded successfully!")

    except Exception as error:
        print("ORM test failed:", error)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    test_models()
