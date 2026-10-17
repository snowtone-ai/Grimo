import Dexie, { type Table } from "dexie";
import type { RewardEvent, Streak, Task, TaskCompletion } from "./types";

export class GrimoDB extends Dexie {
  tasks!: Table<Task, string>;
  taskCompletions!: Table<TaskCompletion, [string, string]>;
  rewardEvents!: Table<RewardEvent, string>;
  streaks!: Table<Streak, string>;

  constructor() {
    super("GrimoLocalV1");
    this.version(1).stores({
      tasks: "id, dueDate, category, recurrence, &importSourceKey",
      taskCompletions: "[taskId+occurrenceLocalDate], completionLocalDate",
      rewardEvents: "rewardEventId, state",
      streaks: "date",
    });
  }
}
let instance: GrimoDB | null = null;
export function getDb(): GrimoDB {
  if (typeof window === "undefined") throw new Error("getDb() called outside browser");
  if (!instance) instance = new GrimoDB();
  return instance;
}
