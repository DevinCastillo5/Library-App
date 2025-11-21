from database import database
from schemas.department import Department
from crud.department_crud import (get_departments, get_department, create_department,
                                  delete_department, update_department)
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/departments", tags=["Departments"])

    # DB Term   Web Term
    # INSERT    POST
    # UPDATE    PUT
    # DELETE    DELETE
    # SELECT    GET

@router.get("/", response_model=list[Department])
async def api_get_departments(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_departments(skip, limit)
        return [Department(**dict(r)) for r in rows]

# GET one: By department_code in URL path
@router.get("/{department_code}", response_model=Department)
async def api_get_department(department_code: int):
    async with database:
        d = await get_department(department_code)
        if not d:
            # HTTPException: Standard way to return error codes (404 = Not Found)
            raise HTTPException(404, "Department not found")
        return Department(**d)  # **d unpacks dict into model fields

# POST: Create new
@router.post("/", response_model=Department)
async def api_create_department(dept: Department):
    async with database:
        try:
            code = await create_department(dept.department_code, dept.department_name)
            # Return full model (includes code user sent)
            return Department(**dept.dict())
        except ValueError as err:
            # status_code=400 → client error (bad request, e.g. duplicate)
            raise HTTPException(status_code=400, detail=str(err))

# PUT → update
@router.put("/", response_model=Department)
async def api_update_department(dept: Department):
    async with database:
        try:
            await update_department(dept.department_code, dept.department_name)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        finally:
            return Department(**dept.dict())

# DELETE → one
@router.delete("/{department_code}")
async def api_delete_department(department_code: int):
    async with database:
        deleted = await delete_department(department_code)
        if deleted == 0:
            raise HTTPException(404, "Department not found")
        return {"detail": "Department deleted"}
