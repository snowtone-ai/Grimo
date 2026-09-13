export interface StreakRecord { date: string; allCompleted: boolean }
const MAX_LOOKBACK_DAYS = 400;
function shiftDate(dateKey: string, days: number): string {
  const date = new Date(`${dateKey}T00:00:00`); date.setDate(date.getDate()+days);
  return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,"0")}-${String(date.getDate()).padStart(2,"0")}`;
}
export function calcStreakCount(records: StreakRecord[], today: string, freezes=1): number {
  const byDate = new Map(records.map(r => [r.date,r.allCompleted]));
  let count=0, freezesLeft=freezes;
  for (let i=0;i<MAX_LOOKBACK_DAYS;i++) {
    const done = byDate.get(shiftDate(today,-i)) === true;
    if (done) { count++; continue; }
    if (i===0) continue;
    if (freezesLeft>0) { freezesLeft--; continue; }
    break;
  }
  return count;
}
