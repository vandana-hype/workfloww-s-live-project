-- Fetch tasks for a company
SELECT *
FROM public.tasks
WHERE company_id = 'YOUR_COMPANY_UUID';

-- Count completed tasks
SELECT COUNT(*) AS completed_count
FROM public.tasks
WHERE company_id = 'YOUR_COMPANY_UUID'
AND status = 'completed';

-- Count pending tasks
SELECT COUNT(*) AS pending_count
FROM public.tasks
WHERE company_id = 'YOUR_COMPANY_UUID'
AND status = 'pending';