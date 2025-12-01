from fastapi import APIRouter, HTTPException
from typing import List, Optional
from database import database
from schemas.loans import Loans
from crud.loans_crud import (
    get_loans, get_loan, create_loan,
    update_loan, delete_loan
)

router = APIRouter(prefix="/api/loans", tags=["Loans"])

# GET all loans
@router.get("/", response_model=List[Loans])
async def api_get_loans(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_loans(skip, limit)
        return [Loans(**dict(r)) for r in rows]

# GET one loan by LoanID
@router.get("/{loan_id}", response_model=Loans)
async def api_get_loan(loan_id: int):
    async with database:
        loan = await get_loan(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        return Loans(**loan)

# POST: Create new loan
@router.post("/", response_model=Loans)
async def api_create_loan(loan: Loans):
    async with database:
        try:
            await create_loan(
                loan.LoanID,
                loan.ReturnDate,
                loan.ISBN,
                loan.MemberID,
                loan.StaffID,
                loan.CopyID
            )
            return loan
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

# PUT: Update existing loan
@router.put("/", response_model=Loans)
async def api_update_loan(loan: Loans):
    async with database:
        try:
            await update_loan(
                loan.LoanID,
                loan.ReturnDate,
                loan.ISBN,
                loan.MemberID,
                loan.StaffID,
                loan.CopyID
            )
            return loan
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

# DELETE: Delete one loan
@router.delete("/{loan_id}")
async def api_delete_loan(loan_id: int):
    async with database:
        deleted = await delete_loan(loan_id)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Loan not found")
        return {"detail": f"Loan {loan_id} deleted"}
