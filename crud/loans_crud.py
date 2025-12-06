from typing import List, Optional
from databases import Database
from schemas.loans import Loans, LoanCreate
from database import database

TABLE_NAME = "Loans"

async def ensure_connection():
    if not database.is_connected:
        await database.connect()

async def get_loans(skip: int = 0, limit: int = 100) -> List[Loans]:
    await ensure_connection()
    query = f"""
        SELECT LoanID, ISBN, MemberID, StaffID, CopyID, ReturnDate
        FROM {TABLE_NAME}
        LIMIT :limit OFFSET :skip
    """
    rows = await database.fetch_all(query=query, values={"skip": skip, "limit": limit})
    return [Loans(**dict(row)) for row in rows]

async def get_loan(loan_id: int) -> Optional[Loans]:
    await ensure_connection()
    query = f"""
        SELECT LoanID, ISBN, MemberID, StaffID, CopyID, ReturnDate
        FROM {TABLE_NAME}
        WHERE LoanID = :loan_id
    """
    row = await database.fetch_one(query=query, values={"loan_id": loan_id})
    if row:
        return Loans(**dict(row))
    return None

async def create_loan(loan: LoanCreate) -> Loans:
    await ensure_connection()
    query = """
        INSERT INTO Loans (ISBN, MemberID, StaffID, CopyID, ReturnDate)
        VALUES (:ISBN, :MemberID, :StaffID, :CopyID, :ReturnDate)
    """
    values = loan.dict()
    await database.execute(query=query, values=values)

    row = await database.fetch_one(
        "SELECT LoanID, ISBN, MemberID, StaffID, CopyID, ReturnDate FROM Loans ORDER BY LoanID DESC LIMIT 1"
    )
    return Loans(**dict(row))

async def update_loan(loan: Loans) -> Loans:
    await ensure_connection()
    query = f"""
        UPDATE {TABLE_NAME}
        SET ISBN = :ISBN,
            MemberID = :MemberID,
            StaffID = :StaffID,
            CopyID = :CopyID,
            ReturnDate = :ReturnDate
        WHERE LoanID = :LoanID
    """
    values = loan.dict()
    await database.execute(query=query, values=values)
    return loan

async def delete_loan(loan_id: int) -> None:
    await ensure_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE LoanID = :loan_id"
    await database.execute(query=query, values={"loan_id": loan_id})
