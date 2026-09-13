import test from "node:test";import assert from "node:assert/strict";import { calcStreakCount } from "../src/domain/task/streak.ts";
test("unfinished today does not break streak",()=>{assert.equal(calcStreakCount([{date:"2026-09-12",allCompleted:true},{date:"2026-09-11",allCompleted:true}],"2026-09-13"),2);});
test("one historical miss is insured",()=>{assert.equal(calcStreakCount([{date:"2026-09-12",allCompleted:true},{date:"2026-09-10",allCompleted:true}],"2026-09-13"),2);});
