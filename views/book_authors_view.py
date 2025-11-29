import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import StringField
from crud.book_authors_crud import *
from database import database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BookAuthorsView(BaseModelView):
    # ===================================================================
    # BASIC CONFIGURATION
    # ===================================================================
    identity = "book_authors"
    name = "BookAuthor"
    label = "Book Authors"
    icon = "fa fa-user-edit"
    pk_attr = "ISBN"  # composite PK, serialize PK in delete

    form_include_pk = True
    searchable_fields = ["ISBN", "AuthorName"]
    sortable_fields = ["ISBN", "AuthorName"]

    # ===================================================================
    # FIELD DEFINITIONS
    # ===================================================================
    fields = [
        StringField(name="ISBN", label="Book ISBN", required=True),
        StringField(name="AuthorName", label="Author Name", required=True),
    ]

    # ===================================================================
    # EXTRACT PRIMARY KEY VALUE (composite PK)
    # ===================================================================
    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        # composite PK as tuple
        return (obj["ISBN"], obj["AuthorName"]) if isinstance(obj, dict) else (getattr(obj, "ISBN"), getattr(obj, "AuthorName"))

    # ===================================================================
    # SERIALIZE
    # ===================================================================
    async def serialize(self, *args, **kwargs) -> dict:
        obj = args[0] if args else kwargs.get("obj") or kwargs.get("instance")
        if obj is None:
            return {}

        if not isinstance(obj, dict):
            obj = dict(obj._mapping) if hasattr(obj, "_mapping") else obj.__dict__

        # Optional: Fetch Book title and Author details for display
        async with database:
            book_title = None
            author_dob = None
            author_nationality = None

            if obj.get("ISBN"):
                book = await database.fetch_one("SELECT Title FROM Books WHERE ISBN = :isbn", values={"isbn": obj["ISBN"]})
                book_title = book["Title"] if book else None

            if obj.get("AuthorName"):
                author = await database.fetch_one("SELECT DOB, Nationality FROM Authors WHERE AuthorName = :name", values={"name": obj["AuthorName"]})
                if author:
                    author_dob = author["DOB"]
                    author_nationality = author["Nationality"]

        return {
            "ISBN": obj.get("ISBN"),
            "BookTitle": book_title,
            "AuthorName": obj.get("AuthorName"),
            "AuthorDOB": author_dob,
            "AuthorNationality": author_nationality,
            "_meta": {"pk": (obj.get("ISBN"), obj.get("AuthorName"))},
        }

    # ===================================================================
    # VALIDATE FORM INPUT
    # ===================================================================
    async def validate(self, request: Request, data: dict) -> None:
        errors = {}
        if not data.get("ISBN"):
            errors["ISBN"] = "Required"
        if not data.get("AuthorName"):
            errors["AuthorName"] = "Required"

        # Check foreign keys exist
        async with database:
            if data.get("ISBN"):
                exists = await database.fetch_val("SELECT COUNT(*) FROM Books WHERE ISBN = :isbn", values={"isbn": data["ISBN"]})
                if exists == 0:
                    errors["ISBN"] = f"Book ISBN {data['ISBN']} does not exist"

            if data.get("AuthorName"):
                exists = await database.fetch_val("SELECT COUNT(*) FROM Authors WHERE AuthorName = :name", values={"name": data["AuthorName"]})
                if exists == 0:
                    errors["AuthorName"] = f"Author {data['AuthorName']} does not exist"

        if errors:
            raise FormValidationError(errors)

    # ===================================================================
    # LIST VIEW
    # ===================================================================
    async def find_all(self, request: Request, skip: int = 0, limit: int = 100, where: Optional[Any] = None, order_by: Optional[List[Any]] = None) -> List[Any]:
        async with database:
            rows = await get_book_authors(skip, limit)
            return [dict(row) for row in rows]

    # ===================================================================
    # COUNT TOTAL RECORDS
    # ===================================================================
    async def count(self, request: Request, where: Optional[Any] = None) -> int:
        async with database:
            return await database.fetch_val("SELECT COUNT(*) FROM BookAuthors")

    # ===================================================================
    # FIND BY PRIMARY KEY
    # ===================================================================
    async def find_by_pk(self, request: Request, pk: Any) -> Optional[Any]:
        isbn, author_name = pk
        async with database:
            rows = await get_authors_by_book(isbn)
            for r in rows:
                if r["AuthorName"] == author_name:
                    return r
            return None

    # ===================================================================
    # CREATE NEW RELATIONSHIP
    # ===================================================================
    async def create(self, request: Request, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            await create_book_author(data["ISBN"], data["AuthorName"])
            return {"ISBN": data["ISBN"], "AuthorName": data["AuthorName"]}

    # ===================================================================
    # DELETE ONE OR MANY RELATIONSHIPS
    # ===================================================================
    async def delete(self, request: Request, pks: List[Any]) -> int:
        async with database:
            count = 0
            for isbn, author_name in pks:
                count += await delete_book_author(isbn, author_name)
            return count
