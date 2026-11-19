# Multi-Tenant Task Management API

## Setup
Backend:  cd backend && python -m venv venv && venv\Scripts\activate
          pip install -r requirements.txt
          copy .env.example .env  (set SUPABASE_URL, SUPABASE_KEY, JWT_SECRET)
          uvicorn backend.app.main:app --reload
Database: run database/schema.sql, then database/rls.sql in the Supabase SQL editor
Tests:    pytest  |  cd frontend && npx vitest run

## Endpoints
POST /tasks (201, manager only) | GET /tasks (200) | PATCH /tasks/{id} (200/404/403/422)

## Security: how cross-company access is prevented
1. Tenant identity comes from the verified JWT, never from the request. company_id
   is not accepted in body or query params, so changing parameters has no effect.
2. Row Level Security is enforced in PostgreSQL on all tables, using
   current_company_id() derived from auth.uid(). Even if the API layer has a bug,
   or someone calls the database directly, other companies' rows are invisible.
3. INSERT/UPDATE use WITH CHECK, so a user cannot create or move a task into
   another company, or assign a task to a user from another company.
4. A trigger restricts employees to updating task status only.
5. The service role key is never exposed to clients.

## Assumptions
Roles: manager/employee. Statuses: pending, in_progress, completed.
One company per user. Auth handled by Supabase Auth.