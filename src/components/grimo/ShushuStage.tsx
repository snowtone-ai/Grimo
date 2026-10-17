"use client";

import { useEffect, useRef, useState } from "react";
import styles from "./ShushuStage.module.css";

export function ShushuStage() {
  const host = useRef<HTMLDivElement>(null);
  const [attempt, setAttempt] = useState(0);
  const [status, setStatus] = useState("シュシュを迎えています…");
  const [phase, setPhase] = useState("loading");
  useEffect(() => {
    let active = true;
    let dispose: (() => void) | undefined;
    import("@/3d/shushu-runtime").then(({ mountShushu }) => {
      if (!active || !host.current) return;
      dispose = mountShushu(host.current, text => { if (active) setStatus(text); },
        () => { if (active) setPhase("ready"); },
        () => { if (active) setPhase("error"); });
    }).catch(() => { if (active) setPhase("error"); });
    return () => { active = false; dispose?.(); };
  }, [attempt]);
  return <section className={styles.stage} aria-label="シュシュ" data-shushu-state={phase}>
    <div className={styles.halo} aria-hidden="true" />
    <div ref={host} className={styles.viewport} />
    <div className={styles.caption}><h1>シュシュ</h1><p>ここで、ひとやすみ。</p></div>
    {phase === "loading" && <p className={styles.notice} role="status">{status}</p>}
    {phase === "error" && <div className={styles.notice} role="alert">
      <p>シュシュを表示できませんでした。接続や端末の状態を確認して、もう一度お試しください。</p>
      <button onClick={() => { setPhase("loading"); setStatus("シュシュを迎えています…"); setAttempt(value => value + 1); }}>もう一度読み込む</button>
      <p>タスクとカレンダーは引き続き使えます。</p>
    </div>}
  </section>;
}
