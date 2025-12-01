import logging
from typing import Any, List, Optional
from starlette.requests import Request
from starlette_admin import BaseModelView  # ✅ No RequestAction import needed
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import IntegerField, StringField
from crud.books_crud import *
from database import database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BooksView(BaseModelView):
    # ===================================================================
    # BASIC CONFIGURATION
    # ===================================================================
    identity = "books"
    name = "Book"
    label = "Books"
    icon = "fa fa-book"
    pk_attr = "isbn"
    form_include_pk = True

    searchable_fields = ["title", "categories"]
    sortable_fields = ["isbn", "title", "publishyear", "publishname"]

    # ===================================================================
    # FIELD DEFINITIONS
    # ===================================================================
    fields = [
        StringField(name="isbn", label="ISBN", required=True),
        StringField(name="title", label="Title", required=True),
        StringField(name="categories", label="Categories"),
        IntegerField(name="publishyear", label="Publish Year"),
        StringField(name="publishname", label="Publisher", required=False),
    ]

    # ===================================================================
    # EXTRACT PRIMARY KEY VALUE
    # ===================================================================
    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        return obj["isbn"] if isinstance(obj, dict) else getattr(obj, self.pk_attr)

    # ===================================================================
    # SERIALIZE A BOOK FOR DISPLAY
    # ===================================================================
    async def serialize(self, *args, **kwargs) -> dict:
        obj = args[0] if args else kwargs.get("obj") or kwargs.get("instance")
        if obj is None:
            return {}

        if not isinstance(obj, dict):
            obj = dict(obj._mapping) if hasattr(obj, "_mapping") else obj.__dict__

        # Resolve publisher name if missing
        publisher = obj.get("publishname")
        if not publisher:
            async with database:
                row = await database.fetch_one(
                    "SELECT PublishName FROM Publishers WHERE PublishName = :p",
                    values={"p": obj.get("publishname")}
                )
                publisher = row["PublishName"] if row else "Unknown"

        return {
            "isbn": obj.get("isbn"),
            "title": obj.get("title"),
            "categories": obj.get("categories"),
            "publishyear": obj.get("publishyear"),
            "publishname": publisher,
            "_meta": {"pk": obj.get("isbn")},
        }

    # ===================================================================
    # VALIDATE FORM INPUT
    # ===================================================================
    async def validate(self, request: Request, data: dict) -> None:
        errors = {}

        if not data.get("isbn"):
            errors["isbn"] = "Required"
        if not data.get("title"):
            errors["title"] = "Required"

        # Foreign key check: publisher must exist
        if data.get("publishname"):
            async with database:
                exists = await database.fetch_val(
                    "SELECT COUNT(*) FROM Publishers WHERE PublishName = :p",
                    values={"p": data["publishname"]}
                )
                if exists == 0:
                    errors["publishname"] = f"Publisher '{data['publishname']}' does not exist"

        if errors:
            raise FormValidationError(errors)

    # ===================================================================
    # LIST VIEW + SEARCH
    # ===================================================================
    async def find_all(
        self,
        request: Request,
        skip: int = 0,
        limit: int = 100,
        where: Optional[Any] = None,
        order_by: Optional[List[Any]] = None,
    ) -> List[Any]:

        async with database:
            if where and isinstance(where, (str, int)) and str(where).strip():
                term = f"%{str(where).strip()}%"
                query = """
                    SELECT ISBN, Title, Categories, PublishYear, PublishName
                    FROM Books
                    WHERE Title LIKE :search OR Categories LIKE :search
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query=query,
                    values={"search": term, "limit": limit, "skip": skip}
                )
            else:
                query = """
                    SELECT ISBN, Title, Categories, PublishYear, PublishName
                    FROM Books
                    LIMIT :limit OFFSET :skip
                """
                rows = await database.fetch_all(
                    query=query,
                    values={"limit": limit, "skip": skip}
                )

        return [dict(r) for r in rows]

    # ===================================================================
    # COUNT RECORDS
    # ===================================================================
    async def count(self, request: Request, where: Optional[Any] = None) -> int:
        async with database:
            if where and isinstance(where, (str, int)) and str(where).strip():
                term = f"%{str(where).strip()}%"
                return await database.fetch_val(
                    "SELECT COUNT(*) FROM Books WHERE Title LIKE :search OR Categories LIKE :search",
                    values={"search": term},
                )
            return await database.fetch_val("SELECT COUNT(*) FROM Books")

    # ===================================================================
    # FIND BY PK
    # ===================================================================
    async def find_by_pk(self, request: Request, pk: Any) -> Optional[Any]:
        async with database:
            return await get_book(pk)

    # ===================================================================
    # CREATE BOOK
    # ===================================================================
    async def create(self, request: Request, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            isbn = await create_book(
                data["isbn"],
                data["title"],
                data.get("categories"),
                data.get("publishyear"),
                data.get("publishname"),
            )
            return await get_book(isbn)

    # ===================================================================
    # UPDATE BOOK
    # ===================================================================
    async def edit(self, request: Request, pk: Any, data: dict) -> Any:
        await self.validate(request, data)
        async with database:
            updated = await update_book(
                pk,
                data["title"],
                data.get("categories"),
                data.get("publishyear"),
                data.get("publishname"),
            )
            if not updated:
                raise FormValidationError({"_schema": "Update failed"})
            return await get_book(pk)

    # ===================================================================
    # DELETE
    # ===================================================================
    async def delete(self, request: Request, pks: List[Any]) -> int:
        async with database:
            return await delete_books(pks)