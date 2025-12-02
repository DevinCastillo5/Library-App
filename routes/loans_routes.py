# routes/loans_routes.py
from fastapi import APIRouter, HTTPException
from typing import List
from schemas.loans import Loans
from crud.loans_crud import (
    get_loans,
    get_loan,
    create_loan,
    update_loan,
    delete_loan,
)

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
async def api_create_loan(loan: Loans):
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
