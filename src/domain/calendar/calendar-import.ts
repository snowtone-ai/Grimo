import type { Task } from "../../data/db/types";
export interface Appointment { title:string; dueDate:string; dueTime:string|null }
export type CalendarImportTask = Omit<Task,"id"|"createdAt"> & { importSourceKey:string };
export interface ComparisonPair { id:number; left:Appointment; right:Appointment }
export interface DuplicateHint { title:string; dueDate:string; dueTime:string|null; kind:"existing"|"candidate" }
export const MAX_COMPARISON_PAIRS=100;
export function validAppointment(value:unknown): value is Appointment {
  if (!value || typeof value!=="object") return false; const a=value as Appointment;
  if (typeof a.title!=="string" || !a.title.trim() || a.title.length>500) return false;
  if (typeof a.dueDate!=="string" || !/^\d{4}-\d{2}-\d{2}$/.test(a.dueDate)) return false;
  const d=new Date(`${a.dueDate}T00:00:00Z`); if (!Number.isFinite(d.getTime()) || d.toISOString().slice(0,10)!==a.dueDate) return false;
  return a.dueTime===null || (typeof a.dueTime==="string" && /^([01]\d|2[0-3]):[0-5]\d$/.test(a.dueTime));
}
function normalizedTitle(title:string):string { return title.normalize("NFKC").replace(/\s+/g," ").trim().toLocaleLowerCase("ja"); }
export function sameAppointmentText(a:Appointment,b:Appointment):boolean { return a.dueDate===b.dueDate && a.dueTime===b.dueTime && normalizedTitle(a.title)===normalizedTitle(b.title); }
export function plausiblePair(a:Appointment,b:Appointment):boolean {
  if (a.dueDate!==b.dueDate) return false; if (a.dueTime===null || b.dueTime===null) return true;
  const m=(t:string)=>Number(t.slice(0,2))*60+Number(t.slice(3)); return Math.abs(m(a.dueTime)-m(b.dueTime))<=60;
}
function appointment(a:Appointment):Appointment { return {title:a.title.slice(0,120),dueDate:a.dueDate,dueTime:a.dueTime}; }
export function planCalendarComparisons(incoming:CalendarImportTask[],stored:Task[]) {
  if (incoming.length>30) throw new Error("Too many calendar events");
  const existingKeys=new Set(stored.map(t=>t.importSourceKey).filter(Boolean));
  const hardDuplicates=incoming.map(t=>existingKeys.has(t.importSourceKey)); const hints:(DuplicateHint|null)[]=incoming.map(()=>null);
  const pairs:ComparisonPair[]=[]; const targets:{candidate:number;hint:DuplicateHint}[]=[]; let omittedPairs=0;
  const compare=(a:CalendarImportTask,b:Appointment,candidate:number,kind:DuplicateHint["kind"])=>{
    if(!validAppointment(b)||!plausiblePair(a,b))return; const hint={...appointment(b),kind};
    if(sameAppointmentText(a,b)) hints[candidate]??=hint; else if(pairs.length<MAX_COMPARISON_PAIRS){pairs.push({id:pairs.length,left:appointment(a),right:appointment(b)});targets.push({candidate,hint});} else omittedPairs++;
  };
  incoming.forEach((a,i)=>{if(hardDuplicates[i])return;stored.forEach(b=>compare(a,b,i,"existing"));incoming.slice(0,i).forEach(b=>compare(a,b,i,"candidate"));});
  return {hardDuplicates,hints,pairs,targets,omittedPairs};
}
export function parseComparisonPairs(value:unknown):ComparisonPair[]|null {
  if(!Array.isArray(value)||!value.length||value.length>MAX_COMPARISON_PAIRS)return null; const ids=new Set<number>(); const out:ComparisonPair[]=[];
  for(const item of value){ if(!item||typeof item!=="object")return null; const x=item as ComparisonPair; if(!Number.isInteger(x.id)||x.id<0||x.id>=MAX_COMPARISON_PAIRS||ids.has(x.id))return null; if(!validAppointment(x.left)||!validAppointment(x.right)||!plausiblePair(x.left,x.right))return null; ids.add(x.id); out.push({id:x.id,left:appointment(x.left),right:appointment(x.right)}); }
  return out;
}
export function parseDuplicateMatches(value:unknown,pairs:ComparisonPair[]):number[]{
  if(!value||typeof value!=="object"||!("matches" in value)||!Array.isArray((value as {matches:unknown}).matches))throw new Error("Invalid duplicate result");
  const matches=(value as {matches:unknown[]}).matches; const allowed=new Set(pairs.map(p=>p.id));
  if(matches.length>pairs.length||matches.some(id=>!Number.isInteger(id)||!allowed.has(id as number))||new Set(matches).size!==matches.length)throw new Error("Invalid duplicate pair ID");
  return matches as number[];
}
