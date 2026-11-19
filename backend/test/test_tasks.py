from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.dependencies import get_current_user  # ADJUST name

client = TestClient(app)

def as_user(role="manager", company="company-a"):
    app.dependency_overrides[get_current_user] = lambda: {
        "id": "user-1", "company_id": company, "role": role}

def teardown_function():
    app.dependency_overrides.clear()

def test_create_task_invalid_payload_returns_422():
    as_user()
    assert client.post("/tasks", json={"title": ""}).status_code == 422

def test_employee_cannot_create_task():
    as_user(role="employee")
    r = client.post("/tasks", json={"title": "x", "assigned_to": "user-2"})
    assert r.status_code == 403

def test_update_missing_task_returns_404():
    as_user()
    r = client.patch("/tasks/00000000-0000-0000-0000-000000000000",
                     json={"status": "completed"})
    assert r.status_code == 404

def test_invalid_status_returns_422():
    as_user()
    r = client.patch("/tasks/1", json={"status": "banana"})
    assert r.status_code == 422