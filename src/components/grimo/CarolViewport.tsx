"use client";

import { useEffect, useRef, useState } from "react";
import type { CarolRuntimeHandle } from "@/grimo/runtime/carol-runtime";

type QaWindow = Window & { __GRIMO_QA__?: { snapshot: CarolRuntimeHandle["snapshot"] } };

export function CarolViewport() {
  const hostRef = useRef<HTMLDivElement>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");

  useEffect(() => {
    const host = hostRef.current;
    if (!host) return;
    let cancelled = false;
    let runtime: CarolRuntimeHandle | null = null;

    import("@/grimo/runtime/carol-runtime")
      .then(({ mountCarolRuntime }) => mountCarolRuntime(host))
      .then((handle) => {
        if (cancelled) handle.destroy();
        else {
          runtime = handle;
          (window as QaWindow).__GRIMO_QA__ = { snapshot: handle.snapshot };
          setStatus("ready");
        }
      })
      .catch((error: unknown) => {
        console.error("Carol runtime failed to mount", error);
        if (!cancelled) setStatus("error");
      });

    return () => {
      cancelled = true;
      delete (window as QaWindow).__GRIMO_QA__;
      runtime?.destroy();
    };
  }, []);

  return (
    <div className="carol-viewport" aria-label="キャロルの表示エリア" aria-busy={status === "loading"}>
      <div ref={hostRef} className="carol-viewport__host" />
      {status === "loading" && <p className="carol-viewport__status">キャロルを呼んでいます…</p>}
      {status === "error" && <p className="carol-viewport__status is-error">キャロルを表示できませんでした。再読み込みしてください。</p>}
      <span className="sr-only" aria-live="polite">{status === "ready" ? "キャロルが表示されました" : ""}</span>
    </div>
  );
}
