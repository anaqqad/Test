import { useEffect, useState } from "react";
import { cancelRender, continueRender, delayRender } from "remotion";
import type { Video } from "../schema";
import { loadFonts } from "./fonts";
import { loadEngine, type MapEngine } from "./map";

// Loads fonts, map data and the territory engine once per video; blocks rendering until ready.
export function useEngine(video: Video): MapEngine | null {
  const [engine, setEngine] = useState<MapEngine | null>(null);
  const [handle] = useState(() => delayRender(`map engine ${video.id}`, { timeoutInMilliseconds: 120_000 }));
  useEffect(() => {
    let alive = true;
    Promise.all([loadFonts(), loadEngine(video)])
      .then(([, e]) => {
        if (alive) setEngine(e);
        continueRender(handle);
      })
      .catch((err) => cancelRender(err));
    return () => {
      alive = false;
    };
  }, [video, handle]);
  return engine;
}
