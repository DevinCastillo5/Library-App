import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

from database import database, DATABASE_URL
from z_tobedeleted.department_routes import router as department_router
from starlette_admin.contrib.sqla import Admin
from views.department_view import DepartmentView
from sqlalchemy.ext.asyncio import create_async_engine

from routes.course_routes import router as course_router
from views.course_view import CourseView


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Database connection established")
    yield
    await database.disconnect()
    print("Database disconnection established")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(department_router)
app.include_router(course_router)

# Create SQLAlchemy engine for admin
engine = create_async_engine(DATABASE_URL)

# Create admin instance without SQLAlchemy engine (for custom raw SQL views)
admin = Admin(
    engine=engine,
    title="Database Admin Panel",
    base_url="/admin"
)

admin.add_view(DepartmentView)
#admin.add_view(CourseView)

admin.mount_to(app)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Database Course Project 2",
        "dashboard_url": "/dashboard",
        "admin_url": "/admin",
        "api_docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8007, reload=True)