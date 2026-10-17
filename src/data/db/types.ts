import type { Category, Recurrence } from "../../domain/task/task-date";
export type { Category, Recurrence };
export interface Task {
  id: string; title: string; description?: string; dueDate: string; dueTime: string | null;
  category: Category; completed: boolean; completedAt: string | null; recurrence: Recurrence;
  recurrenceDayOfWeek?: number; recurrenceDayOfMonth?: number; createdAt: string; importSourceKey?: string;
  /** Query projection only; never persisted on tasks. */
  completionDates?: string[];
}
export interface Streak { date: string; allCompleted: boolean }
export interface TaskCompletion {
  taskId: string;
  /** Local occurrence date, or ONE_OFF for a lifetime grant across due-date edits. */
  occurrenceLocalDate: string;
  completed: boolean;
  completedAt: string | null;
  completionLocalDate: string;
}
export interface RewardEvent {
  rewardEventId: string;
  eventType: "TASK_CREATED" | "TASK_COMPLETED";
  sourceId: string;
  occurrenceLocalDate: string | null;
  occurredAt: string;
  state: "PENDING";
  processed: false;
  rewardResultId: null;
}
export interface PlantState { id?: number; monthlyCompleted: number; monthKey: string; lifetimeCompleted: number; lastUpdated: string }
export interface DropRecord { id?: number; taskId: string; dateKey: string; dropId: string; rarity: number; at: string }
