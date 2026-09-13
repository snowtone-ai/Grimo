import { getDb } from "@/data/db/grimo-db";
import type { DropRecord, PlantState, Streak, Task } from "@/data/db/types";
export interface LegacyBackupPayload { app:"grimoire"; version:number; exportedAt:string; tasks:Task[]; streaks:Streak[]; plantState:PlantState[]; drops:DropRecord[] }
export function parseLegacyBackup(text:string):LegacyBackupPayload {
  const data:unknown=JSON.parse(text); if(!data||typeof data!=="object")throw new Error("バックアップ形式ではありません"); const r=data as Record<string,unknown>;
  if(r.app!=="grimoire")throw new Error("旧Grimoireのバックアップではありません"); if(typeof r.version!=="number"||r.version>4)throw new Error("対応していないバックアップバージョンです");
  if(!Array.isArray(r.tasks)||!Array.isArray(r.streaks)||!Array.isArray(r.plantState)||!Array.isArray(r.drops))throw new Error("バックアップの中身が壊れています");
  if(!r.tasks.every(x=>typeof (x as Task)?.id==="string"))throw new Error("タスクデータのIDが不正です");
  return r as unknown as LegacyBackupPayload;
}
export async function importLegacyBackup(payload:LegacyBackupPayload):Promise<void>{
  const db=getDb(); await db.transaction("rw",[db.tasks,db.streaks,db.plantState,db.drops],async()=>{
    await db.tasks.bulkPut(payload.tasks); await db.streaks.bulkPut(payload.streaks); await db.plantState.bulkPut(payload.plantState);
    for(const drop of payload.drops){const existing=await db.drops.where("[taskId+dateKey]").equals([drop.taskId,drop.dateKey]).first();if(!existing){const copy={...drop};delete copy.id;await db.drops.add(copy);}}
  });
}
