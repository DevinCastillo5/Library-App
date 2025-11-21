from database import database


# READ all with pagination
async def get_courses(skip: int = 0, limit: int = 10):
    query = """
        SELECT course_code, course_title, department_code
        FROM Course
        LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={'limit': limit, 'skip': skip})


# READ one by course_code
async def get_course(course_code: int):
    query = """
        SELECT course_code, course_title, department_code
        FROM Course 
        WHERE course_code = :course_code
    """
    row = await database.fetch_one(query=query, values={"course_code": course_code})
    return dict(row) if row else None


# READ with JOIN to get department name (for display purposes)
async def get_course_with_department(course_code: int):
    """
    Fetch course with department name for better UI display.
    JOIN: Combines rows from Course and Department tables based on matching department_code.
    """
    query = """
        SELECT c.course_code, c.course_title, c.department_code, d.department_name
        FROM Course c
        LEFT JOIN Department d ON c.department_code = d.department_code
        WHERE c.course_code = :course_code
    """
    row = await database.fetch_one(query=query, values={"course_code": course_code})
    return dict(row) if row else None


# CREATE new course
async def create_course(course_code: int, course_title: str, department_code: int) -> int:
    query = """
        INSERT INTO Course (course_code, course_title, department_code)
        VALUES (:course_code, :course_title, :department_code)
    """
    try:
        await database.execute(query=query, values={
            "course_code": course_code,
            "course_title": course_title,
            "department_code": department_code
        })
        return course_code
    except Exception:
        raise ValueError(f"Course with code {course_code} already exists or invalid department.")


# UPDATE course
async def update_course(course_code: int, course_title: str, department_code: int) -> bool:
    query = """
        UPDATE Course 
        SET course_title = :course_title, department_code = :department_code
        WHERE course_code = :course_code
    """
    try:
        await database.execute(query=query, values={
            "course_code": course_code,
            "course_title": course_title,
            "department_code": department_code
        })
        return True
    except Exception as err:
        raise ValueError(f"Error updating course {course_code}: {err}")


# DELETE one
async def delete_course(course_code: int) -> int:
    query = "DELETE FROM Course WHERE course_code = :course_code"
    return await database.execute(query=query, values={"course_code": course_code})


# DELETE many
async def delete_courses(course_codes: list[int]) -> int:
    if not course_codes:
        return 0
    placeholders = ",".join(f":id{i}" for i in range(len(course_codes)))
    query = f"DELETE FROM Course WHERE course_code IN ({placeholders})"
    values = {f"id{i}": code for i, code in enumerate(course_codes)}
    return await database.execute(query=query, values=values)


# Helper: Get all departments for dropdown (NEW - for FK support)
async def get_all_departments():
    """
    Fetch all departments to populate dropdown in admin UI.
    Returns list of tuples: [(dept_code, dept_name), ...]
    """
    query = "SELECT department_code, department_name FROM Department ORDER BY department_name"
    rows = await database.fetch_all(query=query)
    return [(row["department_code"], row["department_name"]) for row in rows]
