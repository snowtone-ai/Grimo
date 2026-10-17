"use client";
import { useEffect,useState } from "react";
import { liveQuery } from "dexie";
import { AppShell } from "@/components/app-shell/AppShell";
import type { Task } from "@/data/db/types";
import { getTasksForMonth } from "@/data/repositories/task-repository";
import { buildCalendarSummary,toDateStr } from "@/domain/task/task-date";
export default function CalendarPage(){
  const now=new Date(); const year=now.getFullYear(), month=now.getMonth();
  const [tasks,setTasks]=useState<Task[]>([]);
  const [error,setError]=useState(false);
  useEffect(()=>{
    const subscription=liveQuery(()=>getTasksForMonth(year,month)).subscribe({
      next: tasks=>{setTasks(tasks);setError(false);}, error:()=>setError(true),
    });
    return ()=>subscription.unsubscribe();
  },[year,month]);
  const summary=buildCalendarSummary(tasks,year,month);
  const days=new Date(year,month+1,0).getDate();
  return <AppShell title="カレンダー"><section className="hero"><p className="eyebrow">CALENDAR</p><h1>{month+1}月</h1><p>既存のtask date/recurrence semanticsを使うFoundation表示です。</p></section>{error&&<p role="alert" className="error">カレンダーを読み込めませんでした</p>}<div className="calendar-grid" aria-label="月間カレンダー">{Array.from({length:days},(_,i)=>{const key=toDateStr(year,month,i+1);const day=summary[key];return <div className="calendar-cell" key={key}><span>{i+1}</span>{day&&<small>{day.completed?`✓${day.completed}`:""}{day.pending?` · ${day.pending}`:""}</small>}</div>})}</div></AppShell>;
}
