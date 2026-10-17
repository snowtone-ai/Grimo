import "fake-indexeddb/auto";
import { registerHooks } from "node:module";
import { existsSync } from "node:fs";
import test from "node:test";
import assert from "node:assert/strict";

// The app uses bundler extension resolution; exercise the same sources in Node.
registerHooks({ resolve(specifier, context, next) {
  if (specifier.startsWith(".") && context.parentURL?.includes("/src/") && existsSync(new URL(`${specifier}.ts`, context.parentURL))) {
    return next(`${specifier}.ts`, context);
  }
  return next(specifier, context);
} });
globalThis.window = {};
const { getDb, GrimoDB } = await import("../src/data/db/grimo-db.ts");
const repo = await import("../src/data/repositories/task-repository.ts");
const { buildCalendarSummary, localDateString } = await import("../src/domain/task/task-date.ts");
const db = getDb();
const base = { title: "task", dueDate: "2026-10-17", dueTime: null, category: "life", recurrence: "none" };
const create = (id, changes = {}) => repo.createTask({ ...base, ...changes }, id);

test.beforeEach(async () => {
  await db.open();
  await db.transaction("rw", db.tables, () => Promise.all(db.tables.map(t => t.clear())));
});
test.after(() => db.close());

test("clean isolated v1 install, atomic registration retries, and close/reopen durability", async () => {
  assert.equal(db.name, "GrimoLocalV1");
  assert.equal(db.verno, 1);
  await Promise.all(Array.from({ length: 8 }, () => create("register")));
  assert.equal(await db.tasks.count(), 1);
  assert.equal(await db.rewardEvents.count(), 1);
  db.close();
  await db.open();
  assert.equal((await db.tasks.get("register")).title, "task");
  const event = await db.rewardEvents.get("TASK_CREATED:register");
  assert.equal(event.state, "PENDING");
  assert.equal(event.processed, false);
  assert.equal(event.rewardResultId, null);
  const names = (await indexedDB.databases()).map(x => x.name);
  assert.deepEqual(names, ["GrimoLocalV1"]); // Never even open the legacy database.
});

test("one-off complete/undo/recomplete and due-date edit keep one lifetime grant", async () => {
  await create("once");
  await Promise.all(Array.from({ length: 8 }, () => repo.setTaskCompleted("once", true, "2026-10-17")));
  await repo.setTaskCompleted("once", false, "2026-10-17");
  const first = await db.rewardEvents.get("TASK_COMPLETED:once:ONE_OFF");
  await repo.updateTask("once", { dueDate: "2026-10-18", title: "edited" });
  await repo.setTaskCompleted("once", true, "2026-10-18");
  assert.deepEqual(await db.rewardEvents.get(first.rewardEventId), first);
  assert.equal(await db.rewardEvents.count(), 2);
  assert.equal(await db.taskCompletions.count(), 1);
  assert.equal((await repo.getTasksForDate("2026-10-18"))[0].completed, true);
  await repo.deleteTask("once");
  await assert.rejects(create("once"), /already deleted/);
  assert.equal(await db.tasks.count(), 0);
});

test("daily history remains independent on non-monotonic dates and calendar projection", async () => {
  await create("daily", { recurrence: "daily" });
  for (const date of ["2026-10-18", "2026-10-17"]) await repo.setTaskCompleted("daily", true, date);
  await repo.setTaskCompleted("daily", false, "2026-10-18");
  assert.equal((await repo.getTasksForDate("2026-10-17"))[0].completed, true);
  assert.equal((await repo.getTasksForDate("2026-10-18"))[0].completed, false);
  const summary = buildCalendarSummary(await repo.getTasksForMonth(2026, 9), 2026, 9);
  assert.deepEqual(summary["2026-10-17"], { completed: 1, pending: 0 });
  assert.deepEqual(summary["2026-10-18"], { completed: 0, pending: 1 });
  await repo.setTaskCompleted("daily", true, "2026-10-18");
  assert.equal(await db.rewardEvents.count(), 3);
  await assert.rejects(repo.setTaskCompleted("daily", true, "2026-10-16"), /Ineligible/);
  await assert.rejects(repo.setTaskCompleted("daily", true, "2026-02-30"), /Invalid/);
});

test("weekly/monthly occurrences grant only eligible local dates", async () => {
  await create("weekly", { recurrence: "weekly", recurrenceDayOfWeek: 6 });
  await create("monthly", { dueDate: "2026-01-31", recurrence: "monthly", recurrenceDayOfMonth: 31 });
  for (const date of ["2026-10-17", "2026-10-24"]) await repo.setTaskCompleted("weekly", true, date);
  await assert.rejects(repo.setTaskCompleted("weekly", true, "2026-10-18"), /Ineligible/);
  for (const date of ["2026-01-31", "2026-03-31"]) await repo.setTaskCompleted("monthly", true, date);
  await assert.rejects(repo.setTaskCompleted("monthly", true, "2026-02-28"), /Ineligible/);
  assert.equal(await db.taskCompletions.count(), 4);
});

test("calendar import replay/concurrency/deletion preserves stable event identity", async () => {
  const tasks = [{ ...base, completed: false, completedAt: null, importSourceKey: "google-calendar:calendar:event" }];
  const results = await Promise.all([repo.importCalendarTasks(tasks), repo.importCalendarTasks(tasks)]);
  assert.equal(results.reduce((n, x) => n + x.added, 0), 1);
  assert.equal(await db.rewardEvents.count(), 1);
  await repo.deleteTask(tasks[0].importSourceKey);
  assert.deepEqual(await repo.importCalendarTasks(tasks), { added: 0, skipped: 1 });
});

test("event write quota failure rolls back registration, import batch and completion", async () => {
  const fail = () => { throw new DOMException("quota failure", "QuotaExceededError"); };
  db.rewardEvents.hook("creating", fail);
  try {
    await assert.rejects(create("failed"), /quota failure/);
    assert.equal(await db.tasks.count(), 0);
  } finally { db.rewardEvents.hook("creating").unsubscribe(fail); }
  const failSecond = (_key, event) => { if (event.sourceId === "google-calendar:second") fail(); };
  db.rewardEvents.hook("creating", failSecond);
  try {
    await assert.rejects(repo.importCalendarTasks(["first", "second"].map(key => ({ ...base,
      completed: false, completedAt: null, importSourceKey: `google-calendar:${key}` }))), /quota failure/);
    assert.equal(await db.tasks.count(), 0);
    assert.equal(await db.rewardEvents.count(), 0);
  } finally { db.rewardEvents.hook("creating").unsubscribe(failSecond); }
  await create("complete-fail");
  db.rewardEvents.hook("creating", fail);
  try {
    await assert.rejects(repo.setTaskCompleted("complete-fail", true, "2026-10-17"), /quota failure/);
    assert.equal((await db.tasks.get("complete-fail")).completed, false);
    assert.equal(await db.taskCompletions.count(), 0);
  } finally { db.rewardEvents.hook("creating").unsubscribe(fail); }
  await repo.setTaskCompleted("complete-fail", true, "2026-10-17");
  assert.equal(await db.rewardEvents.count(), 2);
});

test("unique constraints are shared by separate database connections", async () => {
  const otherTab = new GrimoDB();
  try {
    await otherTab.open();
    await create("tabs");
    const event = await db.rewardEvents.get("TASK_CREATED:tabs");
    const results = await Promise.allSettled([db.rewardEvents.add(event), otherTab.rewardEvents.add(event)]);
    assert.ok(results.every(x => x.status === "rejected" && x.reason.name === "ConstraintError"));
    assert.equal(await otherTab.rewardEvents.count(), 1);
  } finally { otherTab.close(); }
});

test("legacy backup entry points fail closed before any write", async () => {
  const legacy = await import("../src/data/backup/legacy-grimoire.ts");
  assert.throws(() => legacy.parseLegacyBackup('{"app":"grimoire"}'), /無効/);
  await assert.rejects(legacy.importLegacyBackup({}), /無効/);
  assert.equal(await db.tasks.count(), 0);
});

test("local date contract crosses midnight, DST and timezone changes deliberately", () => {
  const original = process.env.TZ;
  try {
    process.env.TZ = "Asia/Tokyo";
    assert.equal(localDateString(new Date("2026-10-17T14:59:59Z")), "2026-10-17");
    assert.equal(localDateString(new Date("2026-10-17T15:00:00Z")), "2026-10-18");
    process.env.TZ = "America/New_York";
    assert.equal(localDateString(new Date("2026-11-01T05:30:00Z")), "2026-11-01");
    assert.equal(localDateString(new Date("2026-11-01T06:30:00Z")), "2026-11-01");
    assert.equal(localDateString(new Date("2026-10-17T15:00:00Z")), "2026-10-17");
  } finally { if (original === undefined) delete process.env.TZ; else process.env.TZ = original; }
});
