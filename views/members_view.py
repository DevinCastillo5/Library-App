import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView  # ✅ No RequestAction import needed
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import IntegerField, StringField
from crud.members_crud import *
from database import database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CourseView(BaseModelView):
    # ===================================================================
    # BASIC CONFIGURATION
    # ===================================================================
    identity = "members"
    name = "Member"
    label = "Members"
    icon = "fa fa-user"
    pk_attr = "member_id"
    form_include_pk = True

    searchable_fields = ["member_name"]
    sortable_fields = ["member_id", "member_name", "member_email"]

    # ===================================================================
    # FIELD DEFINITIONS (simplified - no dynamic loading)
    # ===================================================================
    fields = [
        IntegerField(
            name="member_id",
            label="Member ID",
            required=True,
        ),
        StringField(name="member_name", label="Member Name", required=True),
        StringField(name="member_email", label="Member Email", required=True),
        StringField(name="member_phone", label="Member Phone", required=True),
        StringField(name="member_address", label="Member Address", required=True),
    ]


    # ===================================================================
    # EXTRACT PRIMARY KEY VALUE
    # ===================================================================
    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        return obj["member_id"] if isinstance(obj, dict) else getattr(obj, self.pk_attr)

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
        if not data.get("member_id"):
            errors["member_id"] = "Required"
        if not data.get("member_name"):
            errors["member_name"] = "Required"
        if not data.get("member_email"):
            errors["member_email"] = "Required"
        if not data.get("member_phone"):
            errors["member_phone"] = "Required"
        if not data.get("member_address"):
            errors["member_address"] = "Required"

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

        #Fetch members names using JOIN.

        async with database:
            if where and isinstance(where, (str, int)) and str(where).strip():
                search_term = str(where).strip()
                query = """
                    SELECT m.member_id, m.member_name, m.member_email, m.member_phone, m.member_address
                    FROM Member m
                    WHERE m.member_name LIKE :search 
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query=query,
                    values={"search": f"%{search_term}%", "limit": limit, "skip": skip}
                )

            return [dict(row) for row in rows]

    # ===================================================================
    # COUNT TOTAL RECORDS OF MEMBERS
    # ===================================================================
    async def count(self, request: Request, where: Optional[Any] = None) -> int:
        async with database:
            if where and isinstance(where, (str, int)) and str(where).strip():
                search_term = str(where).strip()
                query = "SELECT COUNT(*) FROM Member WHERE member_name LIKE :search"
                return await database.fetch_val(query, values={"search": f"%{search_term}%"})
            else:
                return await database.fetch_val("SELECT COUNT(*) FROM Member")

    # ===================================================================
    # FIND BY PRIMARY KEY
    # ===================================================================
    async def find_by_pk(self, request: Request, pk: Any) -> Optional[Any]:
        async with database:
            return await get_member(pk)

    # ===================================================================
    # CREATE NEW COURSE
    # ===================================================================
    async def create(self, request: Request, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            code = await create_member(
                data["member_id"],
                data["member_name"],
                data["member_email"],
                data["member_phone"],
                data["member_address"]
                
            )
            return await get_member(code)

    # ===================================================================
    # UPDATE EXISTING MEMBER
    # ===================================================================
    async def edit(self, request: Request, pk: Any, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            updated = await update_member(
                pk,
                data["member_name"],
                data["member_email"],
                data["member_phone"],
                data["member_address"]
            )
            if not updated:
                raise FormValidationError({"_schema": "Update failed"})
            return await get_member(pk)
    # ===================================================================
    # DELETE ONE OR MANY
    # ===================================================================
    async def delete(self, request: Request, pks: List[Any]) -> int:
        async with database:
            return await delete_members(pks)
