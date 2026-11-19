# Multi-Tenant Task Management API

A task management backend for a multi-company environment. Managers assign tasks to employees, employees update task status, and every user can only access data from their own company.

**Stack:** Python, FastAPI, Pydantic, Supabase (PostgreSQL + Auth), TypeScript

## Project Structure
```
backend/app/routes/      API routes (HTTP layer only)
backend/app/services/    Business logic
backend/app/schemas.py   Pydantic request/response models
backend/app/dependencies.py   Authentication / current user
backend/tests/           Backend tests (pytest)
database/schema.sql      Tables and foreign keys
database/rls.sql         Row Level Security policies
database/queries.sql     Task queries and completed/pending counts
frontend/task.ts         TypeScript types and utility functions
frontend/task.test.ts    TypeScript tests
get_token.py             Helper script to log in and print an access token
```

## Prerequisites
- Python 3.11+
- A Supabase project
- Node.js 18+ (only for the TypeScript tests)

## Setup

1. Create and activate a virtual environment (from the project root):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r backend/requirements.txt
   ```
3. Create the environment file:
   ```
   copy .env.example .env
   ```
   Then set `SUPABASE_URL` and `SUPABASE_KEY` (anon key) in `.env`.
4. Set up the database: in the Supabase SQL Editor, run `database/schema.sql`, then `database/rls.sql`.

## Run
```
uvicorn backend.app.main:app --reload
```
Interactive API docs: http://127.0.0.1:8000/docs

## Authentication
Run `python get_token.py`, log in with a user's email and password, and copy the printed access token. Send it as:
```
Authorization: Bearer <token>
```
In the `/docs` page, use the **Authorize** button.

## Endpoints

| Method | Path | Description | Access | Status codes |
|---|---|---|---|---|
| POST | /tasks | Create a task | Manager | 201, 403, 422 |
| GET | /tasks | List tasks for the user's company | Authenticated | 200, 401 |
| PATCH | /tasks/{id} | Update task status | Manager, or the assigned employee | 200, 403, 404, 422 |

## Tests
Backend (from the project root):
```
pip install pytest httpx
pytest
```
TypeScript:
```
cd frontend
npm install -D vitest
npx vitest run
```

## Security: how cross-company access is prevented

1. **Tenant identity comes from the verified JWT, never from the request.** `company_id` is not accepted in the body or query parameters, so changing request parameters has no effect.
2. **Row Level Security is enforced in PostgreSQL on all tables**, using `current_company_id()` derived from `auth.uid()`. Even if the API layer has a bug, or someone queries the database directly, other companies' rows are invisible.
3. **INSERT/UPDATE use `WITH CHECK`**, so a user cannot create or move a task into another company, or assign a task to a user from another company.
4. **A trigger restricts employees to updating task status only.**
5. **The service role key is never exposed to clients.** Only the anon key is used, so RLS always applies.

## Assumptions
- Roles: `manager` and `employee`
- Statuses: `pending`, `in_progress`, `completed`
- Each user belongs to exactly one company
- Authentication is handled by Supabase Auth

## Status

**Completed:**
- FastAPI endpoints with Pydantic validation and a separate service layer
- Database schema, RLS policies and queries
- TypeScript types and utility functions
- Basic backend and TypeScript tests

**Not completed / with more time I would:**
- <add only what is actually missing, for example integration tests against a real Supabase instance>
- <for example, pagination on GET /tasks>
