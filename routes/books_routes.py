from fastapi import APIRouter, HTTPException
from database import database
from schemas.books import Books
from crud.books_crud import (get_books, get_book, create_book,
                              delete_book, update_book, delete_books)

router = APIRouter(prefix="/api/books", tags=["Books"])

@router.get("/", response_model=list[Books])
async def api_get_books(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_books(skip, limit)
        return [Books(**dict(r)) for r in rows] 
    
@router.get("/{isbn}", response_model=Books)
async def api_get_book(isbn: str):
    async with database:
        b = await get_book(isbn)
        if not b:
            raise HTTPException(404, "Book not found")
        return Books(**b)   
    

@router.post("/", response_model=Books)
async def api_create_book(book: Books):
    async with database:
        try:
            code = await create_book(book.ISBN, book.Title, book.Categories, book.PublishYear, book.PublishName)
            return Books(**book.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        
@router.put("/", response_model=Books)
async def api_update_book(book: Books):
    async with database:
        try:
            await update_book(book.ISBN, book.Title, book.Categories, book.PublishYear, book.PublishName)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        finally:
            return Books(**book.dict())
        
@router.delete("/{isbn}")
async def api_delete_book(isbn: str):
    async with database:
        deleted = await delete_book(isbn)
        if deleted == 0:
            raise HTTPException(404, "Book not found")
        return {"detail": "Book deleted"}
    

@router.delete("/")
async def api_delete_books(isbn_list: list[str]):
    async with database:
        if not isbn_list:
            raise HTTPException(status_code=400, detail="No ISBNs provided for deletion.")
        deleted_count = await delete_books(isbn_list)
        return {"detail": f"Deleted {deleted_count} books."}
    if not ISBNs:
        return 0  # Nothing to delete
    placeholders = ', '.join([f":isbn{i}" for i in range(len(ISBNs))])
    query = f"DELETE FROM Books WHERE ISBN IN ({placeholders})"
    return await database.execute(query=query, values={f"isbn{i}": ISBNs[i] for i in range(len(ISBNs))})