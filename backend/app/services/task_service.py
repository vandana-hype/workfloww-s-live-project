
from fastapi import HTTPException


def create_task(supabase, user, task_data):
    if user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can create tasks"
        )

    # Verify that the employee belongs to this manager's company.
    employee = (
        supabase.table("users")
        .select("id")
        .eq("id", str(task_data.assigned_to))
        .eq("company_id", user["company_id"])
        .eq("role", "employee")
        .execute()
    )

    if not employee.data:
        raise HTTPException(
            status_code=400,
            detail="Employee does not belong to your company"
        )

    new_task = {
        "title": task_data.title,
        "description": task_data.description,
        "assigned_to": str(task_data.assigned_to),
        "created_by": user["id"],
        "company_id": user["company_id"]
    }

    response = (
        supabase.table("tasks")
        .insert(new_task)
        .execute()
    )

    return response.data[0]


def get_tasks(supabase):
    response = (
        supabase.table("tasks")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    # RLS automatically restricts the result to the user's company.
    return response.data


def update_task(supabase, user, task_id, task_data):
    # First, find the task within the user's company.
    task = (
        supabase.table("tasks")
        .select("*")
        .eq("id", str(task_id))
        .execute()
    )

    if not task.data:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    existing_task = task.data[0]

    if user["role"] == "employee":
        if existing_task["assigned_to"] != user["id"]:
            raise HTTPException(
                status_code=403,
                detail="You can update only your assigned tasks"
            )
    elif user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Access denied")

    response = (
        supabase.table("tasks")
        .update({"status": task_data.status})
        .eq("id", str(task_id))
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Task not found")

    return response.data[0]
