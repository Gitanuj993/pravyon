from fastapi import APIRouter, HTTPException

from app.db.supabase import supabase
from app.schemas.project import ProjectCreate

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"]
)

@router.post("/")
def create_project(project: ProjectCreate):

    project_data = project.model_dump(
        mode="json",
        exclude_none=True
    )

    response = (
        supabase
        .table("projects")
        .insert(project_data)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=400,
            detail="Failed to create project"
        )

    return {
        "message": "Project created successfully",
        "data": response.data[0]
    }

@router.get("/")
def get_projects():

    response = (
        supabase
        .table("projects")
        .select("*")
        .execute()
    )

    return {
        "count": len(response.data),
        "data": response.data
    }

