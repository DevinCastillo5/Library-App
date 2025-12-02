from fastapi import APIRouter, HTTPException
from database import database
from schemas.copies import Copies
from crud.copies_crud import get_copies, get_copy, create_copy, update_copy, delete_copy, delete_copies

router = APIRouter(prefix="/api/copies", tags=["Copies"])

@router.get("/", response_model=list[Copies])
async def api_get_copies(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_copies(skip=skip, limit=limit)
        return [Copies(**dict(r)) for r in rows]

@router.get("/{copy_id}", response_model=Copies)
async def api_get_copy(copy_id: int):
    async with database:
        copy = await get_copy(copy_id)
        if not copy:
            raise HTTPException(status_code=404, detail="Copy not found")
        return Copies(**copy)

@router.post("/", response_model=Copies)
async def api_create_copy(copy: Copies):
    async with database:
        try:
            await create_copy(copy.CopyID, copy.ISBN, copy.ShelfLocation, copy.ConditionDesc)
            return copy
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.put("/", response_model=Copies)
async def api_update_copy(copy: Copies):
    async with database:
        await update_copy(copy.CopyID, copy.ISBN, copy.ShelfLocation, copy.ConditionDesc)
        return copy

@router.delete("/{copy_id}")
async def api_delete_copy(copy_id: int):
    async with database:
        deleted = await delete_copy(copy_id)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Copy not found")
        return {"detail": "Copy deleted"}

@router.delete("/")
async def api_delete_copies(copy_ids: list[int]):
    async with database:
        if not copy_ids:
            raise HTTPException(status_code=400, detail="No copy IDs provided for deletion.")
        deleted_count = await delete_copies(copy_ids)
        return {"detail": f"Deleted {deleted_count} copies."}
