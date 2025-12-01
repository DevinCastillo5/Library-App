from database import database
from typing import Optional, List
from datetime import date

# Get many loans
async def get_loans(skip: int = 0, limit: int = 10):
    query = """
        SELECT LoanID, ReturnDate, ISBN, MemberID, StaffID, CopyID
        FROM Loans
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={"limit": limit, "skip": skip})

# Get single loan by LoanID
async def get_loan(loan_id: int) -> Optional[dict]:
    query = """
        SELECT LoanID, ReturnDate, ISBN, MemberID, StaffID, CopyID
        FROM Loans
        WHERE LoanID = :loan_id
    """
    row = await database.fetch_one(query=query, values={"loan_id": loan_id})
    return dict(row) if row else None

# Create a new loan
async def create_loan(
    loan_id: int,
    return_date: Optional[date],
    isbn: Optional[str],
    member_id: Optional[int],
    staff_id: Optional[int],
    copy_id: Optional[int],
) -> int:
    query = """
        INSERT INTO Loans (LoanID, ReturnDate, ISBN, MemberID, StaffID, CopyID)
        VALUES (:LoanID, :ReturnDate, :ISBN, :MemberID, :StaffID, :CopyID)
    """

    try:
        await database.execute(
            query=query,
            values={
                "LoanID": loan_id,
                "ReturnDate": return_date,
                "ISBN": isbn,
                "MemberID": member_id,
                "StaffID": staff_id,
                "CopyID": copy_id,
            },
        )
        return loan_id
    except Exception as err:
        raise ValueError(f"Loan {loan_id} already exists or FK error: {err}")

# Update a loan
async def update_loan(
    loan_id: int,
    return_date: Optional[date],
    isbn: Optional[str],
    member_id: Optional[int],
    staff_id: Optional[int],
    copy_id: Optional[int],
) -> bool:
    query = """
        UPDATE Loans
        SET ReturnDate = :ReturnDate,
            ISBN = :ISBN,
            MemberID = :MemberID,
            StaffID = :StaffID,
            CopyID = :CopyID
        WHERE LoanID = :LoanID
    """

    try:
        await database.execute(
            query=query,
            values={
                "LoanID": loan_id,
                "ReturnDate": return_date,
                "ISBN": isbn,
                "MemberID": member_id,
                "StaffID": staff_id,
                "CopyID": copy_id,
            },
        )
        return True
    except Exception as err:
        raise ValueError(f"Error updating Loan {loan_id}: {err}")

# Delete one loan
async def delete_loan(loan_id: int) -> int:
    query = "DELETE FROM Loans WHERE LoanID = :loan_id"
    return await database.execute(query=query, values={"loan_id": loan_id})

# Delete many loans
async def delete_loans(loan_ids: List[int]) -> int:
    if not loan_ids:
        return 0

    placeholders = ",".join(f":id{i}" for i in range(len(loan_ids)))
    query = f"DELETE FROM Loans WHERE LoanID IN ({placeholders})"
    values = {f"id{i}": loan_id for i, loan_id in enumerate(loan_ids)}

    return await database.execute(query=query, values=values)