import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import database, DATABASE_URL

# ------------------------
# IMPORT ALL API ROUTERS
# ------------------------
from routes.authors_routes import router as authors_router
from routes.books_routes import router as books_router
from routes.members_routes import router as members_router
from routes.loans_routes import router as loans_router
from routes.publishers_routes import router as publishers_router
from routes.reservations_routes import router as reservations_router
from routes.staff_routes import router as staff_router
from routes.copies_routes import router as copies_router
from routes.fines_routes import router as fines_router
from routes.book_authors_routes import router as book_authors_router

# (Admin still imported but we won’t rely on it now)
from views.authors_view import AuthorsView
from views.book_authors_view import BookAuthorsView
from views.books_view import BooksView
from views.copies_view import CopiesView
from views.fines_view import FinesView
from views.loans_view import LoansView
from views.members_view import MemberView
from views.publishers_view import PublishersView
from views.reservations_view import ReservationsView
from views.staff_views import StaffView

from starlette_admin.contrib.sqla import Admin


# ================================
# LIFESPAN: DB Connect/Disconnect
# ================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Database connected")
    yield
    await database.disconnect()
    print("Database disconnected")


# ================================
# CREATE APP
# ================================
app = FastAPI(lifespan=lifespan)


# ================================
# CORS (for frontend dev)
# ================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# STATIC FILES + HTML TEMPLATES
# ================================
templates = Jinja2Templates(directory="templates")


# ================================
# ROOT = index.html
# ================================
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/authors", response_class=HTMLResponse)
async def read_authors(request: Request):
    return templates.TemplateResponse("authors.html", {"request": request})


# ================================
# REGISTER API ROUTERS
# ================================
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(members_router)
app.include_router(loans_router)
app.include_router(publishers_router)
app.include_router(reservations_router)
app.include_router(staff_router)
app.include_router(copies_router)
app.include_router(fines_router)
app.include_router(book_authors_router)


# ================================
# ADMIN (still mounted but optional)
# ================================
engine = create_async_engine(DATABASE_URL)

admin = Admin(engine=engine, title="Library Admin Panel", base_url="/admin")
admin.add_view(AuthorsView)
admin.add_view(BookAuthorsView)
admin.add_view(BooksView)
admin.add_view(CopiesView)
admin.add_view(FinesView)
admin.add_view(LoansView)
admin.add_view(MemberView)
admin.add_view(PublishersView)
admin.add_view(ReservationsView)
admin.add_view(StaffView)
admin.mount_to(app)


# ================================
# RUN SERVER
# ================================
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8008, reload=True)
