from database import database
from typing import List, Optional


# FOR THE UPDATE FUNCTION:
# In many to many relationship, you have you just delete the row and
# then insert a new row to replace it, so for this file there is NO update function.

# READ many: Get multiple book authors
async def get_book_authors(skip: int = 0, limit: int = 10):
    query = """
        SELECT ISBN, AuthorName
        FROM BookAuthors
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={"limit": limit, "skip": skip})

# READ one: Get single book author by ISBN and AuthorName
async def get_authors_by_book(isbn: str):
    query = """
        SELECT ISBN, AuthorName
        FROM BookAuthors
        WHERE ISBN = :isbn
    """
    rows = await database.fetch_all(query=query, values={"isbn": isbn})
    return [dict(r) for r in rows]

# READ: all books for one author
async def get_books_by_author(author_name: str):
    query = """
        SELECT ISBN, AuthorName
        FROM BookAuthors
        WHERE AuthorName = :author_name
    """
    rows = await database.fetch_all(query=query, values={"author_name": author_name})
    return [dict(r) for r in rows]

# CREATE: Insert a new book-author relationship
async def create_book_author(isbn: str, author_name: str):
    query = """
        INSERT INTO BookAuthors (ISBN, AuthorName)
        VALUES (:ISBN, :AuthorName)
    """

    try:
        await database.execute(
            query=query,
            values={"ISBN": isbn, "AuthorName": author_name},
        )
        return {"ISBN": isbn, "AuthorName": author_name}
    except Exception as err:
        raise ValueError(
            f"Relationship (ISBN={isbn}, Author={author_name}) already exists or FK error: {err}"
        )

# NO UPDATE FUNCTION

# DELETE: a relationship (just one pair)
async def delete_book_author(isbn: str, author_name: str) -> int:
    query = """
        DELETE FROM BookAuthors
        WHERE ISBN = :ISBN AND AuthorName = :AuthorName
    """
    return await database.execute(
        query=query,
        values={"ISBN": isbn, "AuthorName": author_name},
    )

# DELETE: all authors for a book
async def delete_authors_by_book(isbn: str) -> int:
    query = "DELETE FROM BookAuthors WHERE ISBN = :ISBN"
    return await database.execute(query=query, values={"ISBN": isbn})

# DELETE: all books for an author
async def delete_books_by_author(author_name: str) -> int:
    query = "DELETE FROM BookAuthors WHERE AuthorName = :AuthorName"
    return await database.execute(query=query, values={"AuthorName": author_name})