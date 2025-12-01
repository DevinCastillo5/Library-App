from database import database

async def get_publishers(skip: int = 0, limit: int = 10):
    query="""
        SELECT PublishName, ContactInfo
        FROM Publishers
        LIMIT :limit OFFSET :skip
        """
    return await database.fetch_all(query=query, values={'limit': limit, 'skip': skip})

# READ one: Get single publisher by PublishName
async def get_publisher(PublishName: str):
    query = """
    SELECT PublishName, ContactInfo
    FROM Publishers WHERE PublishName = :PublishName
    """
    row = await database.fetch_one(query=query, values={"PublishName": PublishName})
    return dict(row) if row else None  # Convert Row → dict for Pydantic

# CREATE: Insert a new publisher. Returns the PublishName (PK).
# :param tells type checkers what each argument is — improves code clarity and IDE help.
async def create_publisher(PublishName: str, ContactInfo: str) -> str:
    query = """
    INSERT INTO Publishers (PublishName, ContactInfo)
    VALUES (:PublishName, :ContactInfo)
    """
    try:
        # Execute the insert using named parameters (:name) — safe from SQL injection
        await database.execute(query=query, values={
            "PublishName": PublishName,
            "ContactInfo": ContactInfo
        })
        return PublishName  # Return PK so API can confirm creation
    except Exception:
        # Raise clear error if PublishName already exists (duplicate primary key)
        raise ValueError(f"Publisher with name {PublishName} already exists.")
    
# UPDATE
async def update_publisher(PublishName: str, ContactInfo: str) -> bool:
    query = """
    UPDATE Publishers SET ContactInfo = :ContactInfo
    WHERE PublishName = :PublishName
    """
    try:
        await database.execute(query=query, values={
            "PublishName": PublishName,
            "ContactInfo": ContactInfo
        })
        return True
    except Exception as err:
        raise ValueError(f"Error updating publisher {PublishName}: {err}")
    
# DELETE one
async def delete_publisher(PublishName: str) -> str:
    query = "DELETE FROM Publishers WHERE PublishName = :PublishName"
    return await database.execute(query=query, values={"PublishName": PublishName})

# DELETE many
async def delete_publishers(PublishNames: list[str]) -> int:
    if not PublishNames:
        return 0  # Nothing to delete
    placeholders = ', '.join(f":name{i}" for i in range(len(PublishNames)))
    query = f"DELETE FROM Publishers WHERE PublishName IN ({placeholders})"
    values = {f"name{i}": name for i, name in enumerate(PublishNames)}
    return await database.execute(query=query, values=values)