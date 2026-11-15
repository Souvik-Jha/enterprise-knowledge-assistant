
from app.database.database import SessionLocal
from app.database.models import Company


def create_company(name: str):
    db = SessionLocal()

    try:
        # 1. Create a Python object
        company = Company(name=name)

        # 2. Add the object to the session
        db.add(company)

        # 3. Save the transaction in PostgreSQL
        db.commit()

        # 4. Refresh the object to get database-generated values
        db.refresh(company)

        return company

    except Exception:
        # Undo the transaction if something fails
        db.rollback()
        raise

    finally:
        # Always close the database session
        db.close()


def get_company(company_id):
    db = SessionLocal()

    try:
        company = db.get(Company, company_id)
        return company

    finally:
        db.close()


if __name__ == "__main__":
    # Create a company
    new_company = create_company("Acme Technologies")

    print("Company created successfully!")
    print("ID:", new_company.id)
    print("Name:", new_company.name)
    print("Created at:", new_company.created_at)

    # Retrieve the company
    existing_company = get_company(new_company.id)

    print("\nCompany retrieved successfully!")
    print("Name:", existing_company.name)
