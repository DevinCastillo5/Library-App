from fastapi import APIRouter, HTTPException
from typing import List
from schemas.fines import Fines
from crud.fines_crud import get_fines, get_fine, create_fine, update_fine, delete_fine

router = APIRouter(prefix="/api/fines", tags=["fines"])

# GET all fines
@router.get("/", response_model=List[Fines])
async def api_get_fines(skip: int = 0, limit: int = 100):
    return await get_fines(skip, limit)

# GET single fine
@router.get("/{fine_id}", response_model=Fines)
async def api_get_fine(fine_id: int):
    fine = await get_fine(fine_id)
    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    return fine

# POST create fine
@router.post("/", response_model=Fines)
async def api_create_fine(fine: Fines):
    existing = await get_fine(fine.FineID)
    if existing:
        raise HTTPException(status_code=400, detail="Fine already exists")
    return await create_fine(fine)

# PUT update fine
@router.put("/", response_model=Fines)
async def api_update_fine(fine: Fines):
    existing = await get_fine(fine.FineID)
    if not existing:
        raise HTTPException(status_code=404, detail="Fine not found")
    return await update_fine(fine)

# DELETE fine
@router.delete("/{fine_id}")
async def api_delete_fine(fine_id: int):
    existing = await get_fine(fine_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Fine not found")
    await delete_fine(fine_id)
    return {"detail": "Fine deleted"}
