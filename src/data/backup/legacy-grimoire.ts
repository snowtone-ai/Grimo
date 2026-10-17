import type { DropRecord, PlantState, Streak, Task } from "@/data/db/types";
export interface LegacyBackupPayload { app:"grimoire"; version:number; exportedAt:string; tasks:Task[]; streaks:Streak[]; plantState:PlantState[]; drops:DropRecord[] }
export function parseLegacyBackup(_text: string): LegacyBackupPayload {
  void _text;
  throw new Error("旧Grimoireバックアップの読込は無効です");
}
export async function importLegacyBackup(_payload: LegacyBackupPayload): Promise<never> {
  void _payload;
  throw new Error("旧Grimoireバックアップの移行は無効です");
}
