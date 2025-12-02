from fastapi import APIRouter, HTTPException
from typing import List
from schemas.books import Books
from crud.books_crud import get_books, get_book, create_book, update_book, delete_book

router = APIRouter(prefix="/api/books", tags=["books"])

# GET all books
@router.get("/", response_model=List[Books])
async def api_get_books(skip: int = 0, limit: int = 100):
    return await get_books(skip, limit)

# GET single book
@router.get("/{isbn}", response_model=Books)
async def api_get_book(isbn: str):
    book = await get_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# POST create book
@router.post("/", response_model=Books)
async def api_create_book(book: Books):
    existing = await get_book(book.ISBN)
    if existing:
        raise HTTPException(status_code=400, detail="Book already exists")
    return await create_book(book)

# PUT update book
@router.put("/", response_model=Books)
async def api_update_book(book: Books):
    existing = await get_book(book.ISBN)
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")
    return await update_book(book)

# DELETE book
@router.delete("/{isbn}")
async def api_delete_book(isbn: str):
    existing = await get_book(isbn)
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")
    await delete_book(isbn)
    return {"detail": "Book deleted"}
