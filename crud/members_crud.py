from database import database


# READ all with pagination
async def get_members(skip: int = 0, limit: int = 10):
    query = """
        SELECT member_id, member_name, member_email, member_phone, member_address
        FROM Members
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={'limit': limit, 'skip': skip})


# READ one by member_id
async def get_member(member_id: int):
    query = """
        SELECT member_id, member_name, member_email, member_phone, member_address
        FROM Members 
        WHERE member_id = :member_id
    """
    row = await database.fetch_one(query=query, values={"member_id": member_id})
    return dict(row) if row else None

#I don't we need this one but I'll leave it here just in case

# READ with JOIN to get department name (for display purposes)
# async def get_course_with_department(course_code: int):
#    """
#    Fetch course with department name for better UI display.
#    JOIN: Combines rows from Course and Department tables based on matching department_code.
#    """
#    query = """
#        SELECT c.course_code, c.course_title, c.department_code, d.department_name
#        FROM Course c
#        LEFT JOIN Department d ON c.department_code = d.department_code
#        WHERE c.course_code = :course_code
#    """
#    row = await database.fetch_one(query=query, values={"course_code": course_code})
#    return dict(row) if row else None


# CREATE new course
async def create_member(member_id: int, member_name: str, member_email: str, member_phone: str, member_address: str) -> int:
    query = """
        INSERT INTO Members (member_id, member_name, member_email, member_phone, member_address)
        VALUES (:member_id, :member_name, :member_email, :member_phone, :member_address)
    """
    try:
        await database.execute(query=query, values={
            "member_id": member_id,
            "member_name": member_name,
            "member_email": member_email,
            "member_phone": member_phone,
            "member_address": member_address
        })
        return member_id
    except Exception:
        raise ValueError(f"Member with ID {member_id} already exists or invalid data.")

# UPDATE member
async def update_member(member_id: int, member_name: str, member_email: str, member_phone: str, member_address: str) -> bool:
    query = """
        UPDATE Members 
        SET member_name = :member_name, member_email = :member_email, member_phone = :member_phone, member_address = :member_address
        WHERE member_id = :member_id
    """
    try:
        await database.execute(query=query, values={
            "member_id": member_id,
            "member_name": member_name,
            "member_email": member_email,
            "member_phone": member_phone,
            "member_address": member_address
        })
        return True
    except Exception as err:
        raise ValueError(f"Error updating member {member_id}: {err}")

# DELETE one
async def delete_member(member_id: int) -> int:
    query = "DELETE FROM Members WHERE member_id = :member_id"
    return await database.execute(query=query, values={"member_id": member_id})


# DELETE many
async def delete_members(member_ids: list[int]) -> int:
    if not member_ids:
        return 0
    placeholders = ",".join(f":id{i}" for i in range(len(member_ids)))
    query = f"DELETE FROM Members WHERE member_id IN ({placeholders})"
    values = {f"id{i}": member_id for i, member_id in enumerate(member_ids)}
    return await database.execute(query=query, values=values)


# Helper: Get all departments for dropdown (NEW - for FK support)
#async def get_all_departments():
#   """
#    Fetch all departments to populate dropdown in admin UI.
#    Returns list of tuples: [(dept_code, dept_name), ...]
#    """
#    query = "SELECT department_code, department_name FROM Department ORDER BY department_name"
#    rows = await database.fetch_all(query=query)
#   return [(row["department_code"], row["department_name"]) for row in rows]
