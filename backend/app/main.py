
from fastapi import FastAPI
from app.routes.tasks import router as task_router

app = FastAPI(
    title="Multi-Tenant Task Management API",
    description="A secure task management API for multiple companies",
    version="1.0.0"
)

app.include_router(task_router)


@app.get("/")
def home():
    return {"message": "Task Management API is running"}
