"use client";

import { type FormEvent, useCallback, useEffect, useState } from "react";
import { AppShell } from "@/components/app-shell/AppShell";
import type { Task } from "@/data/db/types";
import {
  createTask,
  getTasksForDate,
  toggleTaskComplete,
} from "@/data/repositories/task-repository";
import { todayDateString } from "@/domain/task/task-date";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const nextTasks = await getTasksForDate(todayDateString());
      setTasks(nextTasks);
      setError(null);
    } catch {
      setError("タスクを読み込めませんでした");
    }
  }, []);

  useEffect(() => {
    let active = true;

    void getTasksForDate(todayDateString()).then(
      (nextTasks) => {
        if (!active) return;
        setTasks(nextTasks);
        setError(null);
      },
      () => {
        if (!active) return;
        setError("タスクを読み込めませんでした");
      },
    );

    return () => {
      active = false;
    };
  }, []);

  async function add(event: FormEvent) {
    event.preventDefault();
    const clean = title.trim();
    if (!clean) return;

    await createTask({
      title: clean,
      dueDate: todayDateString(),
      dueTime: null,
      category: "life",
      completed: false,
      completedAt: null,
      recurrence: "none",
    });
    setTitle("");
    await refresh();
  }

  return (
    <AppShell title="タスク">
      <section className="hero">
        <p className="eyebrow">TODAY</p>
        <h1>今日やること</h1>
        <p>
          タスク管理のbackend互換を確認するためのFoundation
          UIです。正式デザインは次工程で作り込みます。
        </p>
      </section>

      <form className="quick-add" onSubmit={add}>
        <input
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="タスクを追加"
          aria-label="タスク名"
        />
        <button type="submit">追加</button>
      </form>

      {error && (
        <p role="alert" className="error">
          {error}
        </p>
      )}

      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id}>
            <button
              className="check"
              aria-label={`${task.title}を${task.completed ? "未完了" : "完了"}にする`}
              onClick={async () => {
                await toggleTaskComplete(task.id);
                await refresh();
              }}
            >
              {task.completed ? "✓" : ""}
            </button>
            <div>
              <span className={task.completed ? "done" : ""}>{task.title}</span>
              {task.dueTime && <small>{task.dueTime}</small>}
            </div>
          </li>
        ))}
      </ul>

      {!tasks.length && !error && (
        <div className="empty">今日のタスクはまだありません。</div>
      )}
    </AppShell>
  );
}
