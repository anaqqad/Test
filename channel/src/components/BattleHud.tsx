// HUD for the full-frame battle layout: date and losses (top left), legend and scale (top right), caption bar
// and progress (bottom). Everything is data-driven from the video JSON.
import React, { useLayoutEffect, useRef } from "react";
import { interpolate } from "remotion";
import type { Video } from "../schema";
import { flagSprite } from "../lib/flags";
import { dateParts, dayNumber, sampleSeries } from "../lib/time";
import { theme } from "../lib/theme";
import { flagSet } from "./MapView";

const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const fmt = (n: number) => Math.round(n).toLocaleString("en-US");

const panel: React.CSSProperties = {
  background: "rgba(12,15,18,0.80)",
  border: "1px solid rgba(255,255,255,0.09)",
  borderRadius: 12,
  boxShadow: "0 10px 30px rgba(0,0,0,0.35)",
  color: theme.panelText,
  fontFamily: theme.number,
};

export const FlagBadge: React.FC<{ id: string; size: number; round?: boolean }> = ({ id, size, round = true }) => {
  const ref = useRef<HTMLCanvasElement>(null);
  const sprite = flagSprite(id, round);
  const w = round ? size : (size * sprite.width) / sprite.height;
  useLayoutEffect(() => {
    const ctx = ref.current!.getContext("2d")!;
    ctx.clearRect(0, 0, ref.current!.width, ref.current!.height);
    ctx.drawImage(sprite, 0, 0, ref.current!.width, ref.current!.height);
  }, [sprite]);
  return <canvas ref={ref} width={Math.round(w * 2)} height={size * 2} style={{ width: w, height: size, display: "block" }} />;
};

type Props = {
  video: Video;
  day: number;
  startDay: number;
  endDay: number;
  frame: number;
  fps: number;
  eventFrames: number[];
  kmPerScreenPx: number;
};

export const BattleHud: React.FC<Props> = ({ video, day, startDay, endDay, frame, fps, eventFrames, kmPerScreenPx }) => {
  const { y, m, d } = dateParts(day);
  const dayN = Math.max(1, Math.floor(day) - startDay + 1);
  const tables = video.counters.filter((c) => c.kind === "table");

  // Scale bar: the round length closest to ~150 px.
  const km = [5, 10, 20, 25, 50, 100, 200, 250, 500, 1000].reduce((best, v) => (Math.abs(v / kmPerScreenPx - 150) < Math.abs(best / kmPerScreenPx - 150) ? v : best));
  const barPx = km / kmPerScreenPx;

  // Caption: the latest event still within its caption time.
  let idx = -1;
  video.events.forEach((e, i) => {
    if (eventFrames[i] <= frame && frame < eventFrames[i] + (e.captionSeconds + e.holdSeconds) * fps) idx = i;
  });
  const ev = idx >= 0 ? video.events[idx] : null;
  const age = idx >= 0 ? frame - eventFrames[idx] : 0;
  const life = ev ? (ev.captionSeconds + ev.holdSeconds) * fps : 1;
  const capOpacity = ev ? interpolate(age, [0, 6, life - 8, life], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const evDate = ev ? dateParts(dayNumber(ev.date)) : null;

  const p = (dd: number) => `${(100 * (dd - startDay)) / Math.max(1, endDay - startDay)}%`;

  return (
    <div style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
      {/* Date and losses */}
      <div style={{ position: "absolute", left: 40, top: 34 }}>
        <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 62, lineHeight: 1, color: "#fff", textShadow: "0 3px 18px rgba(0,0,0,0.75)" }}>
          {d} {MONTHS[m - 1]} <span style={{ color: theme.front }}>{y}</span>
        </div>
        <div style={{ fontFamily: theme.number, fontWeight: 700, fontSize: 22, letterSpacing: 4, color: theme.front, marginTop: 8, textShadow: "0 2px 10px rgba(0,0,0,0.8)" }}>
          DAY {dayN} · {video.header.title.toUpperCase()}
        </div>
        {tables.map((t, ti) =>
          t.kind !== "table" ? null : (
            <div key={ti} style={{ ...panel, marginTop: 16, padding: "12px 16px", minWidth: 380 }}>
              <div style={{ display: "grid", gridTemplateColumns: `32px repeat(${t.columns.length}, 1fr)`, columnGap: 14, rowGap: 6, alignItems: "center" }}>
                <div style={{ fontSize: 15, fontWeight: 700, letterSpacing: 2, color: theme.front }}>{t.label.toUpperCase()}</div>
                {t.columns.map((c) => (
                  <div key={c} style={{ fontSize: 14, fontWeight: 700, letterSpacing: 2, color: theme.muted, textAlign: "right" }}>{c.toUpperCase()}</div>
                ))}
                {t.rows.map((r) => {
                  const f = video.factions.find((q) => q.id === r.factionId);
                  const id = r.flag ?? f?.flags[0]?.flag;
                  return (
                    <React.Fragment key={r.factionId + (r.flag ?? "")}>
                      <div>{id ? <FlagBadge id={id} size={26} /> : <div style={{ width: 26, height: 26, borderRadius: 13, background: f?.color }} />}</div>
                      {r.series.map((pts, i) => (
                        <div key={i} style={{ fontSize: 28, fontWeight: 700, textAlign: "right", fontVariantNumeric: "tabular-nums" }}>
                          {fmt(sampleSeries(pts.map(([dd, v]) => [dayNumber(dd), v]), day))}
                        </div>
                      ))}
                    </React.Fragment>
                  );
                })}
              </div>
            </div>
          ),
        )}
      </div>

      {/* Legend and scale */}
      <div style={{ position: "absolute", right: 40, top: 34, ...panel, padding: "14px 18px", minWidth: 260 }}>
        {video.factions.map((f) => {
          const set = flagSet(f, day);
          if (!set.length) return null;
          return (
            <div key={f.id} style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
              <div style={{ display: "flex", gap: 3 }}>
                {set.map((x) => (
                  <FlagBadge key={x.id} id={x.id} size={24} />
                ))}
              </div>
              <div style={{ fontSize: 22, fontWeight: 700, letterSpacing: 1 }}>{f.name.toUpperCase()}</div>
            </div>
          );
        })}
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 6 }}>
          <div style={{ width: barPx, height: 6, borderLeft: "2px solid #fff", borderRight: "2px solid #fff", borderBottom: "2px solid #fff" }} />
          <div style={{ fontSize: 18, fontWeight: 700 }}>{km} km</div>
        </div>
        {video.header.watermark && (
          <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 14, letterSpacing: 5, color: theme.muted, marginTop: 10 }}>{video.header.watermark.toUpperCase()}</div>
        )}
      </div>

      {/* Caption bar */}
      {ev && evDate && (
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 58, display: "flex", justifyContent: "center", opacity: capOpacity }}>
          <div style={{ ...panel, padding: "14px 28px", maxWidth: 1400, fontSize: 32, lineHeight: 1.25, textAlign: "center", transform: `translateY(${interpolate(age, [0, 8], [12, 0], { extrapolateRight: "clamp" })}px)` }}>
            <span style={{ color: theme.front, fontWeight: 700 }}>{evDate.d} {MONTHS[evDate.m - 1]}.</span>{" "}
            <span style={{ fontWeight: 700 }}>{ev.title}.</span> {ev.text && <span style={{ fontWeight: 500 }}>{ev.text}</span>}
          </div>
        </div>
      )}

      {/* Progress */}
      <div style={{ position: "absolute", left: 40, right: 40, bottom: 26, height: 5, background: "rgba(255,255,255,0.15)", borderRadius: 3 }}>
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: p(day), background: theme.accent, borderRadius: 3 }} />
        {video.events.map((e, i) => {
          const dd = dayNumber(e.date);
          return <div key={i} style={{ position: "absolute", left: p(dd), top: -4, width: 3, height: 13, marginLeft: -1.5, background: dd <= day ? theme.front : "rgba(255,255,255,0.4)" }} />;
        })}
      </div>
    </div>
  );
};
