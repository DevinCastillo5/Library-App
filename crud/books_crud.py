# crud/books_crud.py
from typing import List, Optional
from databases import Database
from fastapi import HTTPException
from schemas.books import Books
from database import database  # your Database instance

TABLE_NAME = "Books"

# Ensure database connection
async def ensure_connection():
    if not database.is_connected:
        await database.connect()


# Fetch all books with optional pagination
async def get_books(skip: int = 0, limit: int = 100) -> List[Books]:
    await ensure_connection()
    query = f"""
        SELECT ISBN, Title, Categories, PublishYear, PublishName
        FROM {TABLE_NAME}
        LIMIT :limit OFFSET :skip
    """
    rows = await database.fetch_all(query=query, values={"skip": skip, "limit": limit})
    return [Books(**dict(row)) for row in rows]


# Fetch a single book by ISBN
async def get_book(isbn: str) -> Optional[Books]:
    await ensure_connection()
    query = f"""
        SELECT ISBN, Title, Categories, PublishYear, PublishName
        FROM {TABLE_NAME}
        WHERE ISBN = :isbn
    """
    row = await database.fetch_one(query=query, values={"isbn": isbn})
    if row:
        return Books(**dict(row))
    return None


# Create a new book
async def create_book(book: Books) -> Books:
    await ensure_connection()
    query = f"""
        INSERT INTO {TABLE_NAME} (ISBN, Title, Categories, PublishYear, PublishName)
        VALUES (:ISBN, :Title, :Categories, :PublishYear, :PublishName)
    """
    await database.execute(query=query, values=book.dict())
    return book


# Update an existing book
async def update_book(book: Books) -> Optional[Books]:
    await ensure_connection()
    query = f"""
        UPDATE {TABLE_NAME}
        SET Title = :Title,
            Categories = :Categories,
            PublishYear = :PublishYear,
            PublishName = :PublishName
        WHERE ISBN = :ISBN
    """
    await database.execute(query=query, values=book.dict())
    return book


# Delete a book by ISBN
async def delete_book(isbn: str) -> None:
    await ensure_connection()
    query = f"DELETE FROM {TABLE_NAME} WHERE ISBN = :isbn"
    await database.execute(query=query, values={"isbn": isbn})
