from database import database
from typing import List, Optional


# READ: Get all authors
async def get_authors(skip: int = 0, limit: int = 10):
    query = """
        SELECT AuthorName, DOB, Nationality
        FROM Authors
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={"limit": limit, "skip": skip})


# READ: Get one author by name
async def get_author(author_name: str) -> Optional[dict]:
    query = """
        SELECT AuthorName, DOB, Nationality
        FROM Authors
        WHERE AuthorName = :author_name
    """
    row = await database.fetch_one(query=query, values={"author_name": author_name})
    return dict(row) if row else None


# CREATE: Insert new author
async def create_author(author_name: str, dob: str, nationality: str) -> str:
    query = """
        INSERT INTO Authors (AuthorName, DOB, Nationality)
        VALUES (:AuthorName, :DOB, :Nationality)
    """

    try:
        await database.execute(
            query=query,
            values={
                "AuthorName": author_name,
                "DOB": dob,
                "Nationality": nationality
            },
        )
        return author_name
    except Exception:
        raise ValueError(f"Author '{author_name}' already exists.")


# UPDATE: Update author info
async def update_author(author_name: str, dob: str, nationality: str) -> bool:
    query = """
        UPDATE Authors
        SET DOB = :DOB,
            Nationality = :Nationality
        WHERE AuthorName = :AuthorName
    """

    try:
        await database.execute(
            query=query,
            values={
                "AuthorName": author_name,
                "DOB": dob,
                "Nationality": nationality
            },
        )
        return True
    except Exception as err:
        raise ValueError(f"Error updating author '{author_name}': {err}")


# DELETE: Delete a single author
async def delete_author(author_name: str) -> int:
    query = "DELETE FROM Authors WHERE AuthorName = :author_name"
    return await database.execute(query=query, values={"author_name": author_name})


# DELETE many: List of names
async def delete_authors(author_names: List[str]) -> int:
    if not author_names:
        return 0

    placeholders = ",".join(f":name{i}" for i in range(len(author_names)))
    query = f"DELETE FROM Authors WHERE AuthorName IN ({placeholders})"
    values = {f"name{i}": name for i, name in enumerate(author_names)}

    return await database.execute(query=query, values=values)
