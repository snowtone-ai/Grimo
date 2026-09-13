import test from "node:test";import assert from "node:assert/strict";import { doesTaskApplyToDate,taskForDisplayDate } from "../src/domain/task/task-date.ts";
const base={dueDate:"2026-09-01",dueTime:null,category:"life",completed:false,completedAt:null,recurrence:"none"};
test("one-off applies only to due date",()=>{assert.equal(doesTaskApplyToDate(base,"2026-09-01"),true);assert.equal(doesTaskApplyToDate(base,"2026-09-02"),false);});
test("daily recurrence starts on due date",()=>{const task={...base,recurrence:"daily"};assert.equal(doesTaskApplyToDate(task,"2026-08-31"),false);assert.equal(doesTaskApplyToDate(task,"2026-09-02"),true);});
test("recurring completion is projected per day",()=>{const task={...base,recurrence:"daily",completed:true,completedAt:"2026-09-13T01:00:00.000Z"};assert.equal(taskForDisplayDate(task,"2026-09-13").completed,true);assert.equal(taskForDisplayDate(task,"2026-09-12").completed,false);});
