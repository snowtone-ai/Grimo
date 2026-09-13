import type { Task } from "./types";
export function monthKeyLocal(now: Date): string { return `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,"0")}`; }
export function countMonthlyCompletedTasks(tasks: Task[], now: Date): number {
  const key = monthKeyLocal(now);
  return tasks.filter(t => t.completedAt?.slice(0,7) === key).length;
}
