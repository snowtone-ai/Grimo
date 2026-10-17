import { getDb } from "../db/grimo-db";
import type { Category, RewardEvent, Streak, Task, TaskCompletion } from "../db/types";
import { validAppointment, type CalendarImportTask } from "../../domain/calendar/calendar-import";
import { calcStreakCount } from "../../domain/task/streak";
import { doesTaskApplyToDate, localDateString, sortTasksByTime, taskForDisplayDate, todayDateString } from "../../domain/task/task-date";

type NewTask = Omit<Task, "id" | "createdAt" | "completed" | "completedAt" | "completionDates"> & { completed?: false; completedAt?: null };
type TaskChanges = Partial<Omit<NewTask, "completed" | "completedAt" | "importSourceKey">>;

function eventFor(taskId: string, occurrence: string | null, now: string): RewardEvent {
  const eventType = occurrence === null ? "TASK_CREATED" : "TASK_COMPLETED";
  return { rewardEventId: `${eventType}:${taskId}${occurrence === null ? "" : `:${occurrence}`}`,
    eventType, sourceId: taskId, occurrenceLocalDate: occurrence, occurredAt: now,
    state: "PENDING", processed: false, rewardResultId: null };
}

function validateTask(task: NewTask): void {
  if (!validAppointment(task) || !["job", "university", "life"].includes(task.category) ||
    !["none", "daily", "weekly", "monthly"].includes(task.recurrence) ||
    (task.recurrence === "weekly" && (!Number.isInteger(task.recurrenceDayOfWeek) || task.recurrenceDayOfWeek! < 0 || task.recurrenceDayOfWeek! > 6)) ||
    (task.recurrence === "monthly" && (!Number.isInteger(task.recurrenceDayOfMonth) || task.recurrenceDayOfMonth! < 1 || task.recurrenceDayOfMonth! > 31))) {
    throw new Error("Invalid task");
  }
}

function projectTasks(tasks: Task[], completions: TaskCompletion[]): Task[] {
  const dates = new Map<string, string[]>();
  for (const c of completions) {
    if (c.completed) { const list = dates.get(c.taskId) ?? []; list.push(c.completionLocalDate); dates.set(c.taskId, list); }
  }
  return tasks.map(task => ({ ...task, completionDates: dates.get(task.id) ?? [] }));
}

export async function getAllTasks(): Promise<Task[]> { return getDb().tasks.toArray(); }

export async function getTasksForDate(date: string): Promise<Task[]> {
  const db = getDb();
  return db.transaction("r", db.tasks, db.taskCompletions, async () => {
    const [dated, recurring] = await Promise.all([
      db.tasks.where("dueDate").equals(date).toArray(),
      db.tasks.where("recurrence").anyOf("daily", "weekly", "monthly").toArray(),
    ]);
    const tasks = [...new Map([...dated, ...recurring].filter(t => doesTaskApplyToDate(t, date)).map(t => [t.id, t])).values()];
    const completions = await db.taskCompletions.where("completionLocalDate").equals(date).toArray();
    return sortTasksByTime(projectTasks(tasks, completions).map(t => taskForDisplayDate(t, date)));
  });
}

export async function getTasksForMonth(year: number, month: number): Promise<Task[]> {
  const start = localDateString(new Date(year, month, 1));
  const end = localDateString(new Date(year, month + 1, 0));
  const db = getDb();
  return db.transaction("r", db.tasks, db.taskCompletions, async () => {
    const [dated, recurring, completions] = await Promise.all([
      db.tasks.where("dueDate").between(start, end, true, true).toArray(),
      db.tasks.where("recurrence").anyOf("daily", "weekly", "monthly").toArray(),
      db.taskCompletions.where("completionLocalDate").between(start, end, true, true).toArray(),
    ]);
    const completedTasks = await db.tasks.bulkGet([...new Set(completions.map(c => c.taskId))]);
    const tasks = [...new Map([...dated, ...recurring.filter(t => t.dueDate <= end), ...completedTasks.filter(t => t !== undefined)].map(t => [t.id, t])).values()];
    return projectTasks(tasks, completions);
  });
}

/** Reuse commandId when retrying the same registration; distinct registrations use distinct IDs. */
export async function createTask(task: NewTask, commandId = crypto.randomUUID()): Promise<Task> {
  validateTask(task);
  const db = getDb();
  return db.transaction("rw", db.tasks, db.rewardEvents, async () => {
    const existing = await db.tasks.get(commandId);
    if (existing) return existing;
    const next: Task = { ...task, id: commandId, completed: false, completedAt: null, createdAt: new Date().toISOString() };
    const event = eventFor(next.id, null, next.createdAt);
    if (await db.rewardEvents.get(event.rewardEventId)) throw new Error("Registration already deleted");
    await db.tasks.add(next);
    await db.rewardEvents.add(event);
    return next;
  });
}

export async function updateTask(id: string, changes: TaskChanges): Promise<void> {
  const db = getDb();
  await db.transaction("rw", db.tasks, async () => {
    const task = await db.tasks.get(id);
    if (!task) return;
    // Whitelist editable fields: status/identity must go through atomic commands.
    const { title, description, dueDate, dueTime, category, recurrence, recurrenceDayOfWeek, recurrenceDayOfMonth } = { ...task, ...changes };
    const editable = { title, description, dueDate, dueTime, category, recurrence, recurrenceDayOfWeek, recurrenceDayOfMonth };
    validateTask(editable);
    await db.tasks.update(id, editable);
  });
}
export async function deleteTask(id: string): Promise<void> { await getDb().tasks.delete(id); }

/** Explicit desired state makes overlapping clicks/tabs idempotent. */
export async function setTaskCompleted(id: string, completed: boolean, date = todayDateString()): Promise<void> {
  if (!validAppointment({ title: "date", dueDate: date, dueTime: null })) throw new Error("Invalid occurrence date");
  const db = getDb();
  await db.transaction("rw", db.tasks, db.taskCompletions, db.rewardEvents, async () => {
    const task = await db.tasks.get(id);
    if (!task) return;
    if (task.recurrence !== "none" && !doesTaskApplyToDate(task, date)) throw new Error("Ineligible occurrence date");
    const occurrence = task.recurrence === "none" ? "ONE_OFF" : date;
    const now = new Date().toISOString();
    const previous = await db.taskCompletions.get([id, occurrence]);
    if (previous?.completed === completed || (!previous && !completed)) return;
    await db.taskCompletions.put({ taskId: id, occurrenceLocalDate: occurrence, completed,
      completedAt: completed ? now : null, completionLocalDate: date });
    if (task.recurrence === "none") await db.tasks.update(id, { completed, completedAt: completed ? now : null });
    if (completed) {
      const event = eventFor(id, occurrence, now);
      if (!await db.rewardEvents.get(event.rewardEventId)) await db.rewardEvents.add(event);
    }
  });
}

export async function importCalendarTasks(tasks: CalendarImportTask[]): Promise<{ added: number; skipped: number }> {
  if (tasks.length > 30 || tasks.some(t => !validAppointment(t) || typeof t.importSourceKey !== "string" ||
    !t.importSourceKey.startsWith("google-calendar:") || t.importSourceKey.length > 3100 ||
    !["job", "university", "life"].includes(t.category) || t.recurrence !== "none")) throw new Error("Invalid calendar import");
  const db = getDb();
  return db.transaction("rw", db.tasks, db.rewardEvents, async () => {
    let added = 0, skipped = 0;
    for (const task of tasks) {
      const id = task.importSourceKey;
      const event = eventFor(id, null, new Date().toISOString());
      if (await db.rewardEvents.get(event.rewardEventId) || await db.tasks.where("importSourceKey").equals(id).first()) { skipped++; continue; }
      await db.tasks.add({ ...task, id, completed: false, completedAt: null, createdAt: event.occurredAt });
      await db.rewardEvents.add(event);
      added++;
    }
    return { added, skipped };
  });
}
export async function getTasksByCategory(category: Category): Promise<Task[]> { return getDb().tasks.where("category").equals(category).toArray(); }
export async function getAllStreaks(): Promise<Streak[]> { return getDb().streaks.orderBy("date").toArray(); }
export async function recordStreak(date: string, allCompleted: boolean): Promise<void> { await getDb().streaks.put({ date, allCompleted }); }
export async function getCurrentStreakCount(): Promise<number> { return calcStreakCount(await getDb().streaks.toArray(), todayDateString()); }
