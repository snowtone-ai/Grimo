import Dexie, { type Table } from "dexie";
import { countMonthlyCompletedTasks, monthKeyLocal } from "./legacy-plant";
import type { DropRecord, PlantState, Streak, Task } from "./types";

export class GrimoDB extends Dexie {
  tasks!: Table<Task,string>; streaks!: Table<Streak,string>; plantState!: Table<PlantState,number>; drops!: Table<DropRecord,number>;
  constructor() {
    super("TaskManagerDB");
    this.version(1).stores({ tasks:"id, dueDate, category, completed, recurrence", streaks:"date" });
    this.version(2).stores({ tasks:"id, dueDate, category, completed, recurrence", streaks:"date", plantState:"++id" });
    this.version(3).stores({
      tasks:"id, dueDate, category, completed, recurrence", streaks:"date", plantState:"++id",
      drops:"++id, taskId, dateKey, rarity, &[taskId+dateKey]",
    }).upgrade(async tx => {
      const now=new Date(); const tasks=(await tx.table("tasks").toArray()) as Task[];
      const monthlyCompleted=countMonthlyCompletedTasks(tasks,now);
      await tx.table("plantState").toCollection().modify((state: Record<string,unknown>) => {
        state.monthlyCompleted=monthlyCompleted; state.monthKey=monthKeyLocal(now); delete state.weeklyCompleted; delete state.weekStartDate;
      });
    });
    this.version(4).stores({
      tasks:"id, dueDate, category, completed, recurrence, &importSourceKey", streaks:"date", plantState:"++id",
      drops:"++id, taskId, dateKey, rarity, &[taskId+dateKey]",
    });
  }
}
let instance: GrimoDB | null = null;
export function getDb(): GrimoDB {
  if (typeof window === "undefined") throw new Error("getDb() called outside browser");
  if (!instance) instance = new GrimoDB();
  return instance;
}
