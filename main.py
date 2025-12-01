import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine

from database import database, DATABASE_URL

# Import your views
from views.authors_view import AuthorsView
from views.loans_view import LoansView
from views.book_authors_view import BookAuthorsView

# Import Admin from Starlette Admin
from starlette_admin.contrib.sqla import Admin


# ================================
# LIFESPAN: Connect/Disconnect DB
# ================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Database connection established")
    yield
    await database.disconnect()
    print("Database disconnection established")


# ================================
# CREATE APP
# ================================
app = FastAPI(lifespan=lifespan)

# ================================
# CORS (optional, for frontend dev)
# ================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# CREATE SQLAlchemy ENGINE
# ================================
engine = create_async_engine(DATABASE_URL)

# ================================
# CREATE ADMIN PANEL
# ================================
admin = Admin(
    engine=engine,
    title="Library Admin Panel",
    base_url="/admin"
)

# Add views
admin.add_view(AuthorsView)
admin.add_view(LoansView)
admin.add_view(BookAuthorsView)

# Mount admin to FastAPI app
admin.mount_to(app)

# ================================
# ROOT ROUTE
# ================================
@app.get("/")
async def root():
    return {
        "message": "Welcome to Library Admin Panel",
        "admin_url": "/admin",
        "api_docs": "/docs"
    }


# ================================
# RUN SERVER
# ================================
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8007, reload=True)
