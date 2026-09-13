"use client";

import { useEffect, useState } from "react";

export function HumanGateFullscreenButton() {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isUnavailable, setIsUnavailable] = useState(false);

  useEffect(() => {
    const sync = () => setIsFullscreen(Boolean(document.fullscreenElement));
    document.addEventListener("fullscreenchange", sync);
    sync();
    return () => document.removeEventListener("fullscreenchange", sync);
  }, []);

  const toggleFullscreen = async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await document.documentElement.requestFullscreen();
      setIsUnavailable(false);
    } catch {
      setIsUnavailable(true);
    }
  };

  return (
    <button
      type="button"
      className="human-gate__fullscreen"
      aria-pressed={isFullscreen}
      onClick={() => void toggleFullscreen()}
    >
      {isFullscreen ? "全画面を終了" : isUnavailable ? "F11で全画面にしてください" : "全画面で確認"}
    </button>
  );
}
