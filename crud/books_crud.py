from database import database

async def get_books(skip: int = 0, limit: int = 10):
    query="""
        SELECT ISBN, Title
        FROM Books
        LIMIT :limit OFFSET :skip
        """
    return await database.fetch_all(query=query, values={'limit': limit, 'skip': skip})

# READ one: Get single book by ISBN
async def get_book(ISBN: str):
    query = """
    SELECT ISBN, Title
    FROM Books WHERE ISBN = :ISBN
    """
    row = await database.fetch_one(query=query, values={"ISBN": ISBN})
    return dict(row) if row else None  # Convert Row → dict for Pydantic

# CREATE: Insert a new book. Returns the ISBN (PK).
# :param tells type checkers what each argument is — improves code clarity and IDE help.
async def create_book(ISBN: str, Title: str) -> str:
    query = """
    INSERT INTO Books (ISBN, Title)
    VALUES (:ISBN, :Title)
    """
    try:
        # Execute the insert using named parameters (:name) — safe from SQL injection
        await database.execute(query=query, values={
            "ISBN": ISBN,
            "Title": Title
        })
        return ISBN  # Return PK so API can confirm creation
    except Exception:
        # Raise clear error if ISBN already exists (duplicate primary key)
        raise ValueError(f"Book with ISBN {ISBN} already exists.")
    
# UPDATE
async def update_book(ISBN: str, Title: str) -> bool:
    query = """
    UPDATE Books SET Title = :Title
    WHERE ISBN = :ISBN
    """
    try:
        await database.execute(query=query, values={
            "ISBN": ISBN,
            "Title": Title
        })
        return True
    except Exception as err:
        raise ValueError(f"Error updating book {ISBN}: {err}")
    
# DELETE one
async def delete_book(ISBN: str) -> str:
    query = "DELETE FROM Books WHERE ISBN = :ISBN"
    return await database.execute(query=query, values={"ISBN": ISBN})

# DELETE many
async def delete_books(ISBNs: list[str]) -> int:
    if not ISBNs:
        return 0  # No books to delete
    placeholders = ', '.join(f":isbn_{i}" for i in range(len(ISBNs)))
    query = f"DELETE FROM Books WHERE ISBN IN ({placeholders})"
    values = {f"isbn_{i}": ISBNs[i] for i in range(len(ISBNs))}
    return await database.execute(query=query, values=values)