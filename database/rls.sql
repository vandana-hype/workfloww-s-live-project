create or replace function public.current_company_id() returns uuid
language sql stable security definer set search_path = public as $$
  select company_id from public.users where id = auth.uid()
$$;

create or replace function public.current_user_role() returns text
language sql stable security definer set search_path = public as $$
  select role from public.users where id = auth.uid()
$$;

alter table companies enable row level security;
alter table users     enable row level security;
alter table tasks     enable row level security;

create policy companies_select on companies for select
  using (id = current_company_id());

create policy users_select on users for select
  using (company_id = current_company_id());

-- Managers see all company tasks; employees see only their own
create policy tasks_select on tasks for select
  using (company_id = current_company_id()
         and (current_user_role() = 'manager' or assigned_to = auth.uid()));

-- Only managers create tasks, only in their company, only for colleagues
create policy tasks_insert on tasks for insert
  with check (
    company_id = current_company_id()
    and current_user_role() = 'manager'
    and exists (select 1 from users u
                where u.id = assigned_to and u.company_id = current_company_id())
  );

-- Employees update their own tasks; managers any in their company
create policy tasks_update on tasks for update
  using (company_id = current_company_id()
         and (current_user_role() = 'manager' or assigned_to = auth.uid()))
  with check (company_id = current_company_id());

-- Employees may change status only
create or replace function enforce_employee_status_only() returns trigger
language plpgsql as $$
begin
  if current_user_role() = 'employee' and (
       new.title is distinct from old.title or
       new.company_id is distinct from old.company_id or
       new.assigned_to is distinct from old.assigned_to) then
    raise exception 'Employees can only update task status';
  end if;
  return new;
end $$;

create trigger trg_employee_status_only before update on tasks
  for each row execute function enforce_employee_status_only();