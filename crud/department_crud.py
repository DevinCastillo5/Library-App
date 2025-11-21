from database import database


async def get_departments(skip: int = 0, limit: int = 10):
    query="""
        SELECT department_code, department_name
        FROM department
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={'limit': limit, 'skip': skip})

# READ one: Get single department by code
async def get_department(department_code: int):
    query = """
    SELECT department_code, department_name
    FROM Department WHERE department_code = :department_code
    """
    row = await database.fetch_one(query=query, values={"department_code": department_code})
    return dict(row) if row else None  # Convert Row → dict for Pydantic

# CREATE: Insert a new department. Returns the code (PK).
# :param tells type checkers what each argument is — improves code clarity and IDE help.
async def create_department(department_code: int, department_name: str) -> int:
    query = """
    INSERT INTO Department (department_code, department_name)
    VALUES (:department_code, :department_name)
    """
    try:
        # Execute the insert using named parameters (:name) — safe from SQL injection
        await database.execute(query=query, values={
            "department_code": department_code,
            "department_name": department_name
        })
        return department_code  # Return PK so API can confirm creation
    except Exception:
        # Raise clear error if code already exists (duplicate primary key)
        raise ValueError(f"Department with code {department_code} already exists.")

# UPDATE
async def update_department(department_code: int, department_name: str) -> bool:
    query = """
    UPDATE Department SET department_name = :department_name
    WHERE department_code = :department_code
    """
    try:
        await database.execute(query=query, values={
            "department_code": department_code,
            "department_name": department_name
        })
        return True
    except Exception as err:
        raise ValueError(f"Error updating department {department_code}: {err}")

# DELETE one
async def delete_department(department_code: int) -> int:
    query = "DELETE FROM Department WHERE department_code = :department_code"
    return await database.execute(query=query, values={"department_code": department_code})

# DELETE many
async def delete_departments(department_codes: list[int]) -> int:
    if not department_codes:
        return 0
    placeholders = ",".join(f":id{i}" for i in range(len(department_codes)))
    query = f"DELETE FROM Department WHERE department_code IN ({placeholders})"
    values = {f"id{i}": code for i, code in enumerate(department_codes)}
    return await database.execute(query=query, values=values)
