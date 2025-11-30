from fastapi import APIRouter, HTTPException
from typing import List
from database import database
from schemas.authors import Authors
from crud.authors_crud import (
    get_authors, get_author, create_author,
    update_author, delete_author
)

router = APIRouter(prefix="/api/authors", tags=["Authors"])

# GET all authors
@router.get("/", response_model=List[Authors])
async def api_get_authors(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_authors(skip, limit)
        return [Authors(**dict(r)) for r in rows]

# GET one author by name
@router.get("/{author_name}", response_model=Authors)
async def api_get_author(author_name: str):
    async with database:
        author = await get_author(author_name)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return Authors(**author)

# POST: Create new author
@router.post("/", response_model=Authors)
async def api_create_author(author: Authors):
    async with database:
        try:
            await create_author(author.AuthorName, str(author.DOB), author.Nationality)
            return author
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

# PUT: Update existing author
@router.put("/", response_model=Authors)
async def api_update_author(author: Authors):
    async with database:
        try:
            await update_author(author.AuthorName, str(author.DOB), author.Nationality)
            return author
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

# DELETE: Delete a single author
@router.delete("/{author_name}")
async def api_delete_author(author_name: str):
    async with database:
        deleted = await delete_author(author_name)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Author not found")
        return {"detail": f"Author '{author_name}' deleted"}
    
# DELETE many: List of author names
@router.delete("/batch/")
async def api_delete_authors(author_names: List[str]):
    async with database:
        deleted_count = 0
        for author_name in author_names:
            deleted = await delete_author(author_name)
            if deleted:
                deleted_count += 1
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="No authors found to delete")
        return {"detail": f"Deleted {deleted_count} authors"}