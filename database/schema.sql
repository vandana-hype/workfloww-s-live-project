-- Tasks for a company
select * from tasks where company_id = :company_id order by created_at desc;

-- Completed vs pending counts
select
  count(*) filter (where status = 'completed') as completed,
  count(*) filter (where status <> 'completed') as pending
from tasks where company_id = :company_id;

-- Per-company summary
select c.name,
  count(*) filter (where t.status = 'completed') as completed,
  count(*) filter (where t.status <> 'completed') as pending
from companies c left join tasks t on t.company_id = c.id
group by c.name;