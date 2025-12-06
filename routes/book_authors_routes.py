from fastapi import APIRouter, HTTPException
from typing import List
from database import database
from schemas.book_authors import BookAuthor
from crud.book_authors_crud import (
    get_book_authors,
    get_authors_by_book,
    get_books_by_author,
    create_book_author,
    delete_book_author,
    delete_authors_by_book,
    delete_books_by_author
)

router = APIRouter(prefix="/api/book-authors", tags=["BookAuthors"])


# GET all book-author relationships
@router.get("/", response_model=List[BookAuthor])
async def api_get_book_authors(skip: int = 0, limit: int = 1000):
    async with database:
        rows = await get_book_authors(skip, limit)
        return [BookAuthor(**dict(r._mapping)) for r in rows]

# GET all authors for a specific book
@router.get("/book/{isbn}", response_model=List[BookAuthor])
async def api_get_authors_by_book(isbn: str):
    async with database:
        rows = await get_authors_by_book(isbn)
        return [BookAuthor(**r) for r in rows]
    
# GET all books for a specific author
@router.get("/author/{author_name}", response_model=List[BookAuthor])
async def api_get_books_by_author(author_name: str):
    async with database:
        rows = await get_books_by_author(author_name)
        return [BookAuthor(**r) for r in rows]

# POST: Create new book-author relationship
@router.post("/", response_model=BookAuthor)
async def api_create_book_author(rel: BookAuthor):
    async with database:
        try:
            return await create_book_author(rel.ISBN, rel.AuthorName)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        
# DELETE a single book-author relationship
@router.delete("/{isbn}/{author_name}")
async def api_delete_book_author(isbn: str, author_name: str):
    async with database:
        deleted = await delete_book_author(isbn, author_name)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Relationship not found")
        return {"detail": f"Deleted relationship ISBN={isbn}, Author={author_name}"}

# DELETE all authors for a book
@router.delete("/book/{isbn}")
async def api_delete_authors_by_book(isbn: str):
    async with database:
        deleted = await delete_authors_by_book(isbn)
        return {"detail": f"Deleted {deleted} author(s) for book {isbn}"}

# DELETE all books for an author
@router.delete("/author/{author_name}")
async def api_delete_books_by_author(author_name: str):
    async with database:
        deleted = await delete_books_by_author(author_name)
        return {"detail": f"Deleted {deleted} book(s) for author {author_name}"}