from fastapi import APIRouter, HTTPException
from database import database
from schemas.course import Course
from crud.course_crud import (get_courses, get_course, create_course,
                              delete_course, update_course)

router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.get("/", response_model=list[Course])
async def api_get_courses(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_courses(skip, limit)
        return [Course(**dict(r)) for r in rows]


@router.get("/{course_code}", response_model=Course)
async def api_get_course(course_code: int):
    async with database:
        c = await get_course(course_code)
        if not c:
            raise HTTPException(404, "Course not found")
        return Course(**c)


@router.post("/", response_model=Course)
async def api_create_course(course: Course):
    async with database:
        try:
            code = await create_course(course.course_code, course.course_title, course.department_code)
            return Course(**course.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))


@router.put("/", response_model=Course)
async def api_update_course(course: Course):
    async with database:
        try:
            await update_course(course.course_code, course.course_title, course.department_code)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        finally:
            return Course(**course.dict())


@router.delete("/{course_code}")
async def api_delete_course(course_code: int):
    async with database:
        deleted = await delete_course(course_code)
        if deleted == 0:
            raise HTTPException(404, "Course not found")
        return {"detail": "Course deleted"}
