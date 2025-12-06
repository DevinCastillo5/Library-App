from fastapi import APIRouter, HTTPException
from typing import List
from schemas.loans import Loans, LoanCreate, LoanRequest
from database import database
from crud.loans_crud import get_loans, get_loan, create_loan, update_loan, delete_loan

router = APIRouter(prefix="/api/loans", tags=["Loans"])

@router.get("/", response_model=List[Loans])
async def api_get_loans(skip: int = 0, limit: int = 100):
    return await get_loans(skip=skip, limit=limit)

@router.get("/{loan_id}", response_model=Loans)
async def api_get_loan(loan_id: int):
    loan = await get_loan(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@router.post("/", response_model=Loans)
async def api_create_loan(req: LoanRequest):
    # Find an available copy for this ISBN
    query = """
        SELECT c.CopyID
        FROM Copies c
        WHERE c.ISBN = :isbn
          AND c.CopyID NOT IN (SELECT CopyID FROM Loans WHERE ReturnDate IS NULL)
        LIMIT 1
    """
    row = await database.fetch_one(query=query, values={"isbn": req.ISBN})
    if not row:
        raise HTTPException(status_code=404, detail="No available copy to loan")

    copy_id = row["CopyID"]

    # StaffID is supplied internally (e.g. from session, or hardcoded for now)
    staff_id = 1  # replace with actual staff context

    loan = LoanCreate(
        ISBN=req.ISBN,
        MemberID=req.MemberID,
        StaffID=staff_id,
        CopyID=copy_id,
        ReturnDate=None,
    )

    return await create_loan(loan)

@router.put("/", response_model=Loans)
async def api_update_loan(loan: Loans):
    existing = await get_loan(loan.LoanID)
    if not existing:
        raise HTTPException(status_code=404, detail="Loan not found")
    return await update_loan(loan)

@router.delete("/{loan_id}")
async def api_delete_loan(loan_id: int):
    existing = await get_loan(loan_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Loan not found")
    await delete_loan(loan_id)
    return {"detail": "Loan deleted"}
