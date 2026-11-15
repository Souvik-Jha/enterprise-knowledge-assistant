import uuid
from app.database.database import SessionLocal
from app.database.models import Document


def create_document(filename: str,company_id: uuid.UUID, status: str):
    db = SessionLocal()

    try:
        # 1. Create a Python object
        document = Document(filename=filename, company_id=company_id, status=status)

        # 2. Add the object to the session
        db.add(document)

        # 3. Save the transaction in PostgreSQL
        db.commit()

        # 4. Refresh the object to get database-generated values
        db.refresh(document)

        return document

    except Exception:
        # Undo the transaction if something fails
        db.rollback()
        raise

    finally:
        # Always close the database session
        db.close()


def get_document(document_id):
    db = SessionLocal()

    try:
        document = db.get(Document, document_id)
        return document

    finally:
        db.close()


if __name__ == "__main__":
    
    new_document = create_document("Company Document", "18926f10-c2ef-4fa4-bdc6-48a2d087d091", "Active")

    print("Document created successfully!")
    print("ID:", new_document.id)
    print("filename:", new_document.filename)
    print("Created at:", new_document.created_at)

   
    existing_document = get_document(new_document.id)

    print("\nDocument retrieved successfully!")
    print("filename:", existing_document.filename)
