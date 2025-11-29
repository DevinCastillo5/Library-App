import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView  # ✅ No RequestAction import needed
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import IntegerField, StringField
from crud.course_crud import *
from database import database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CourseView(BaseModelView):
    # ===================================================================
    # BASIC CONFIGURATION
    # ===================================================================
    identity = "courses"
    name = "Course"
    label = "Courses"
    icon = "fa fa-book"
    pk_attr = "course_code"

    form_include_pk = True

    searchable_fields = ["course_title"]
    sortable_fields = ["course_code", "course_title", "department_code"]

    # ===================================================================
    # FIELD DEFINITIONS (simplified - no dynamic loading)
    # ===================================================================
    fields = [
        IntegerField(
            name="course_code",
            label="Course Code",
            required=True,
        ),
        StringField(name="course_title", label="Course Title", required=True),
        IntegerField(
            name="department_code",
            label="Department Code",
            required=True,
            # Note: User enters department_code as integer
            # We'll display department_name in list view via serialize
        ),
    ]

    # ===================================================================
    # EXTRACT PRIMARY KEY VALUE
    # ===================================================================
    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        return obj["course_code"] if isinstance(obj, dict) else getattr(obj, self.pk_attr)

    # ===================================================================
    # SERIALIZE WITH DEPARTMENT NAME
    # ===================================================================
    async def serialize(self, *args, **kwargs) -> dict:

        # Convert database row to dict, fetching department name for display.

        obj = args[0] if args else kwargs.get('obj') or kwargs.get('instance')

        if obj is None:
            return {}

        if not isinstance(obj, dict):
            obj = dict(obj._mapping) if hasattr(obj, '_mapping') else obj.__dict__

        # Fetch department name for display in list view
        department_name = obj.get("department_name")
        if not department_name and obj.get("department_code"):
            async with database:
                dept_query = "SELECT department_name FROM Department WHERE department_code = :code"
                dept = await database.fetch_one(dept_query, values={"code": obj.get("department_code")})
                department_name = dept["department_name"] if dept else "Unknown"

        return {
            "course_code": obj.get("course_code"),
            "course_title": obj.get("course_title"),
            "department_code": obj.get("department_code"),
            "department_name": department_name,  # For display purposes
            "_meta": {"pk": obj.get("course_code")}
        }

    # ===================================================================
    # VALIDATE FORM INPUT
    # ===================================================================
    async def validate(self, request: Request, data: dict) -> None:

        #Check all required fields and validate FK exists.

        #Without FK validation: Could create courses with non-existent departments

        errors = {}
        if not data.get("course_code"):
            errors["course_code"] = "Required"
        if not data.get("course_title"):
            errors["course_title"] = "Required"
        if not data.get("department_code"):
            errors["department_code"] = "Required"

        # Validate foreign key exists in parent table
        if data.get("department_code"):
            async with database:
                dept_exists = await database.fetch_val(
                    "SELECT COUNT(*) FROM Department WHERE department_code = :code",
                    values={"code": data.get("department_code")}
                )
                if dept_exists == 0:
                    errors["department_code"] = f"Department code {data.get('department_code')} does not exist"

        if errors:
            raise FormValidationError(errors)

    # ===================================================================
    # LIST VIEW WITH SEARCH
    # ===================================================================
    async def find_all(
            self,
            request: Request,
            skip: int = 0,
            limit: int = 100,
            where: Optional[Any] = None,
            order_by: Optional[List[Any]] = None,
    ) -> List[Any]:

        #Fetch courses with department names using JOIN.

        #LEFT JOIN: Includes courses even if department is missing (shows NULL)

        async with database:
            if where and isinstance(where, (str, int)) and str(where).strip():
                search_term = str(where).strip()
                query = """
                    SELECT c.course_code, c.course_title, c.department_code, d.department_name
                    FROM Course c
                    LEFT JOIN Department d ON c.department_code = d.department_code
                    WHERE c.course_title LIKE :search 
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query=query,
                    values={"search": f"%{search_term}%", "limit": limit, "skip": skip}
                )
            else:
                query = """
                    SELECT c.course_code, c.course_title, c.department_code, d.department_name
                    FROM Course c
                    LEFT JOIN Department d ON c.department_code = d.department_code
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query=query,
                    values={"limit": limit, "skip": skip}
                )

            return [dict(row) for row in rows]

    # ===================================================================
    # COUNT TOTAL RECORDS
    # ===================================================================
    async def count(self, request: Request, where: Optional[Any] = None) -> int:
        async with database:
            if where and isinstance(where, (str, int)) and str(where).strip():
                search_term = str(where).strip()
                query = "SELECT COUNT(*) FROM Course WHERE course_title LIKE :search"
                return await database.fetch_val(query, values={"search": f"%{search_term}%"})
            else:
                return await database.fetch_val("SELECT COUNT(*) FROM Course")

    # ===================================================================
    # FIND BY PRIMARY KEY
    # ===================================================================
    async def find_by_pk(self, request: Request, pk: Any) -> Optional[Any]:
        async with database:
            return await get_course_with_department(pk)

    # ===================================================================
    # CREATE NEW COURSE
    # ===================================================================
    async def create(self, request: Request, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            code = await create_course(
                data["course_code"],
                data["course_title"],
                data["department_code"]
            )
            return await get_course_with_department(code)

    # ===================================================================
    # UPDATE EXISTING COURSE
    # ===================================================================
    async def edit(self, request: Request, pk: Any, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            updated = await update_course(
                pk,
                data["course_title"],
                data["department_code"]
            )
            if not updated:
                raise FormValidationError({"_schema": "Update failed"})
            return await get_course_with_department(pk)

    # ===================================================================
    # DELETE ONE OR MANY
    # ===================================================================
    async def delete(self, request: Request, pks: List[Any]) -> int:
        async with database:
            return await delete_courses(pks)
