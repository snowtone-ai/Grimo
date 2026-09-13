import { getDb } from "@/data/db/grimo-db";
import type { Category, Streak, Task } from "@/data/db/types";
import { validAppointment, type CalendarImportTask } from "@/domain/calendar/calendar-import";
import { calcStreakCount } from "@/domain/task/streak";
import { doesTaskApplyToDate, sortTasksByTime, taskForDisplayDate, todayDateString } from "@/domain/task/task-date";

export async function getAllTasks():Promise<Task[]> { return getDb().tasks.toArray(); }
export async function getTasksForDate(date:string):Promise<Task[]> {
  const all=await getDb().tasks.toArray(); return sortTasksByTime(all.filter(t=>doesTaskApplyToDate(t,date)).map(t=>taskForDisplayDate(t,date)));
}
export async function createTask(task:Omit<Task,"id"|"createdAt">):Promise<Task>{
  const next={...task,id:crypto.randomUUID(),createdAt:new Date().toISOString()}; await getDb().tasks.add(next); return next;
}
export async function updateTask(id:string,changes:Partial<Omit<Task,"id"|"createdAt">>):Promise<void>{ await getDb().tasks.update(id,changes); }
export async function deleteTask(id:string):Promise<void>{ await getDb().tasks.delete(id); }
export async function toggleTaskComplete(id:string):Promise<void>{
  const db=getDb(); const task=await db.tasks.get(id); if(!task)return;
  if(task.recurrence!=="none") { const today=todayDateString(); const done=task.completedAt?.slice(0,10)===today; await db.tasks.update(id,{completed:!done,completedAt:done?null:new Date().toISOString()}); }
  else { const completed=!task.completed; await db.tasks.update(id,{completed,completedAt:completed?new Date().toISOString():null}); }
}
export async function importCalendarTasks(tasks:CalendarImportTask[]):Promise<{added:number;skipped:number}>{
  const db=getDb();
  if(tasks.length>30||tasks.some(t=>!validAppointment(t)||typeof t.importSourceKey!=="string"||!t.importSourceKey.startsWith("google-calendar:")||t.importSourceKey.length>3100||!["job","university","life"].includes(t.category)||t.recurrence!=="none")) throw new Error("Invalid calendar import");
  return db.transaction("rw",db.tasks,async()=>{let added=0,skipped=0;for(const task of tasks){const existing=await db.tasks.where("importSourceKey").equals(task.importSourceKey).first();if(existing){skipped++;continue;}await db.tasks.add({...task,id:task.importSourceKey,completed:false,completedAt:null,createdAt:new Date().toISOString()});added++;}return{added,skipped};});
}
export async function getTasksByCategory(category:Category):Promise<Task[]>{return getDb().tasks.where("category").equals(category).toArray();}
export async function getAllStreaks():Promise<Streak[]>{return getDb().streaks.orderBy("date").toArray();}
export async function recordStreak(date:string,allCompleted:boolean):Promise<void>{await getDb().streaks.put({date,allCompleted});}
export async function getCurrentStreakCount():Promise<number>{return calcStreakCount(await getDb().streaks.toArray(),todayDateString());}
