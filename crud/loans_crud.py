# crud/loans_crud.py
from typing import List, Optional
from datetime import date
from databases import Database
from schemas.loans import Loans
from database import database

TABLE_NAME = "Loans"

# Ensure database connection
async def ensure_connection():
    if not database.is_connected:
        await database.connect()


# Fetch all loans with optional pagination
async def get_loans(skip: int = 0, limit: int = 100) -> List[Loans]:
    await ensure_connection()
    query = f"""
        SELECT LoanID, ReturnDate, ISBN, MemberID, StaffID, CopyID
        FROM {TABLE_NAME}
        LIMIT :limit OFFSET :skip
    """
    rows = await database.fetch_all(query=query, values={"skip": skip, "limit": limit})
    loans = []
    for row in rows:
        loan_data = dict(row)
        if loan_data.get("ReturnDate"):
            loan_data["ReturnDate"] = loan_data["ReturnDate"].isoformat()
        loans.append(Loans(**loan_data))
    return loans


# Fetch a single loan by LoanID
async def get_loan(loan_id: int) -> Optional[Loans]:
    await ensure_connection()
    query = f"""
        SELECT LoanID, ReturnDate, ISBN, MemberID, StaffID, CopyID
        FROM {TABLE_NAME}
        WHERE LoanID = :loan_id
    """
    row = await database.fetch_one(query=query, values={"loan_id": loan_id})
    if row:
        loan_data = dict(row)
        if loan_data.get("ReturnDate"):
            loan_data["ReturnDate"] = loan_data["ReturnDate"].isoformat()
        return Loans(**loan_data)
    return None


# Create a new loan
async def create_loan(loan: Loans) -> Loans:
    await ensure_connection()
    query = f"""
        INSERT INTO {TABLE_NAME} (LoanID, ReturnDate, ISBN, MemberID, StaffID, CopyID)
        VALUES (:LoanID, :ReturnDate, :ISBN, :MemberID, :StaffID, :CopyID)
    """
    values = loan.dict()
    # Convert date to string if present
    if values.get("ReturnDate") and isinstance(values["ReturnDate"], date):
        values["ReturnDate"] = values["ReturnDate"].isoformat()
    await database.execute(query=query, values=values)
    return loan


# Update an existing loan
async def update_loan(loan: Loans) -> Loans:
    await ensure_connection()
    query = f"""
        UPDATE {TABLE_NAME}
        SET ReturnDate = :ReturnDate,
            ISBN = :ISBN,
            MemberID = :MemberID,
            StaffID = :StaffID,
            CopyID = :CopyID
        WHERE LoanID = :LoanID
    """
    values = loan.dict()
    if values.get("ReturnDate") and isinstance(values["ReturnDate"], date):
        values["ReturnDate"] = values["ReturnDate"].isoformat()
    await database.execute(query=query, values=values)
    return loan


# Delete a loan by LoanID
async def delete_loan(loan_id: int) -> None:
    await ensure_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE LoanID = :loan_id"
    await database.execute(query=query, values={"loan_id": loan_id})
