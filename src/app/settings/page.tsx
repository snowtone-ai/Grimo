"use client";

import Link from "next/link";
import { useSyncExternalStore } from "react";
import {
  getStartPageServerSnapshot,
  getStartPageSnapshot,
  subscribeStartPage,
  type StartPage,
  writeStartPage,
} from "@/domain/preferences/start-page";

export default function SettingsPage() {
  const value = useSyncExternalStore(
    subscribeStartPage,
    getStartPageSnapshot,
    getStartPageServerSnapshot,
  );

  function choose(next: StartPage) {
    writeStartPage(next);
  }

  return (
    <main className="settings-screen">
      <header className="top-bar">
        <strong>設定</strong>
        <Link
          href={value === "grimo" ? "/grimo" : "/tasks"}
          className="subtle-link"
        >
          戻る
        </Link>
      </header>

      <section className="settings-section">
        <h1>起動時に開く画面</h1>
        <p>次回以降、PWAを開いたときに最初に表示する場所を選びます。</p>
        <div
          className="choice-row"
          role="radiogroup"
          aria-label="起動ページ"
        >
          <button
            role="radio"
            aria-checked={value === "tasks"}
            className={value === "tasks" ? "choice is-selected" : "choice"}
            onClick={() => choose("tasks")}
          >
            タスク
          </button>
          <button
            role="radio"
            aria-checked={value === "grimo"}
            className={value === "grimo" ? "choice is-selected" : "choice"}
            onClick={() => choose("grimo")}
          >
            グリモ
          </button>
        </div>
      </section>

      <section className="settings-section">
        <h2>連携</h2>
        <p>
          Google / Geminiの接続UIはTask
          UI刷新フェーズで接続します。Foundationではsecret/API境界だけを先に固定しています。
        </p>
      </section>
    </main>
  );
}
