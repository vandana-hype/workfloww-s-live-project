
export type TaskStatus = "pending" | "in_progress" | "completed";

export interface Task {
    id: string;
    title: string;
    description: string | null;
    status: TaskStatus;
    assigned_to: string;
    created_by: string;
    company_id: string;
    created_at: string;
}

// Filter tasks by status
export function filterTasks(tasks: Task[], status: TaskStatus): Task[] {
    return tasks.filter(task => task.status === status);
}

// Calculate completed task percentage
export function calculateCompletionPercentage(tasks: Task[]): number {
    if (tasks.length === 0) return 0;

    const completed = tasks.filter(
        task => task.status === "completed"
    ).length;

    return Math.round((completed / tasks.length) * 100);
}

// Fetch tasks from FastAPI
export async function fetchTasks(token: string): Promise<Task[]> {
    try {
        const response = await fetch("http://127.0.0.1:8000/tasks", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const data: unknown = await response.json();

        if (!Array.isArray(data)) {
            throw new Error("Invalid API response");
        }

        return data as Task[];

    } catch (error) {
        console.error("Unable to fetch tasks:", error);
        throw error;
    }
}
