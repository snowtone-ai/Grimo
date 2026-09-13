import type { Category, Recurrence } from "../../domain/task/task-date";
export type { Category, Recurrence };
export interface Task {
  id: string; title: string; description?: string; dueDate: string; dueTime: string | null;
  category: Category; completed: boolean; completedAt: string | null; recurrence: Recurrence;
  recurrenceDayOfWeek?: number; recurrenceDayOfMonth?: number; createdAt: string; importSourceKey?: string;
}
export interface Streak { date: string; allCompleted: boolean }
export interface PlantState { id?: number; monthlyCompleted: number; monthKey: string; lifetimeCompleted: number; lastUpdated: string }
export interface DropRecord { id?: number; taskId: string; dateKey: string; dropId: string; rarity: number; at: string }
