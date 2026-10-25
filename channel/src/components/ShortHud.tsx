// HUD for the vertical Short: everything stacked in the top third (date, counters + legend, caption) so the map
// owns the rest of the frame, as in the reference Shorts. Works for both styles.
import React from "react";
import { interpolate } from "remotion";
import type { Video } from "../schema";
import { dateParts, dayNumber, sampleSeries } from "../lib/time";
import { theme } from "../lib/theme";
import { flagSet } from "./MapView";
import { FlagBadge } from "./BattleHud";

const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const fmt = (n: number) => Math.round(n).toLocaleString("en-US");

type Props = { video: Video; day: number; startDay: number; endDay: number; frame: number; fps: number; eventFrames: number[]; areaKm2: number[] };

export const ShortHud: React.FC<Props> = ({ video, day, startDay, endDay, frame, fps, eventFrames, areaKm2 }) => {
  const panel: React.CSSProperties = {
    background: "rgba(12,15,18,0.82)",
    border: "1px solid rgba(255,255,255,0.09)",
    borderRadius: 14,
    color: theme.panelText,
    fontFamily: theme.number,
    padding: "14px 18px",
  };
  const { y, m, d } = dateParts(day);
  const yearly = video.timeline.clock === "year";
  const counter = yearly ? `YEAR ${y - dateParts(startDay).y + 1}` : `DAY ${Math.max(1, Math.floor(day) - startDay + 1)}`;
  const table = video.counters.find((c) => c.kind === "table");
  const area = video.counters.find((c) => c.kind === "area");
  const total = areaKm2.reduce((a, b) => a + b, 0) || 1;

  let idx = -1;
  video.events.forEach((e, i) => {
    if (eventFrames[i] <= frame && frame < eventFrames[i] + (e.captionSeconds + e.holdSeconds) * fps) idx = i;
  });
  const ev = idx >= 0 ? video.events[idx] : null;
  const age = idx >= 0 ? frame - eventFrames[idx] : 0;
  const life = ev ? (ev.captionSeconds + ev.holdSeconds) * fps : 1;
  const capOpacity = ev ? interpolate(age, [0, 5, life - 6, life], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const evDate = ev ? dateParts(dayNumber(ev.date)) : null;
  const p = (dd: number) => `${(100 * (dd - startDay)) / Math.max(1, endDay - startDay)}%`;

  return (
    <div style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 70, textAlign: "center", textShadow: "0 3px 18px rgba(0,0,0,0.8)" }}>
        <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 84, lineHeight: 1, color: "#fff" }}>
          {yearly ? y : `${d} ${MONTHS[m - 1].slice(0, 3)} `}
          {!yearly && <span style={{ color: theme.front }}>{y}</span>}
        </div>
        <div style={{ fontFamily: theme.number, fontWeight: 700, fontSize: 30, letterSpacing: 5, color: theme.front, marginTop: 10 }}>
          {counter} · {video.header.title.toUpperCase()}
        </div>
      </div>

      <div style={{ position: "absolute", left: 36, right: 36, top: 270, display: "flex", gap: 16, alignItems: "flex-start" }}>
        <div style={{ ...panel, flex: 1.25 }}>
          {table && table.kind === "table" ? (
            <div style={{ display: "grid", gridTemplateColumns: `34px repeat(${table.columns.length}, 1fr)`, columnGap: 10, rowGap: 6, alignItems: "center" }}>
              <div style={{ fontSize: 17, fontWeight: 700, letterSpacing: 2, color: theme.front }}>{table.label.toUpperCase()}</div>
              {table.columns.map((c) => (
                <div key={c} style={{ fontSize: 16, fontWeight: 700, letterSpacing: 1, color: theme.muted, textAlign: "right" }}>{c.toUpperCase()}</div>
              ))}
              {table.rows.map((r) => {
                const f = video.factions.find((q) => q.id === r.factionId);
                const id = r.flag ?? f?.flags[0]?.flag;
                return (
                  <React.Fragment key={r.factionId + (r.flag ?? "")}>
                    <div>{id ? <FlagBadge id={id} size={28} /> : null}</div>
                    {r.series.map((pts, i) => (
                      <div key={i} style={{ fontSize: 30, fontWeight: 700, textAlign: "right", fontVariantNumeric: "tabular-nums" }}>
                        {pts ? fmt(sampleSeries(pts.map(([dd, v]) => [dayNumber(dd), v]), day)) : "—"}
                      </div>
                    ))}
                  </React.Fragment>
                );
              })}
            </div>
          ) : area && area.kind === "area" && area.mode === "total" ? (
            <>
              <div style={{ fontSize: 17, fontWeight: 700, letterSpacing: 2, color: theme.front }}>{area.label.toUpperCase()}</div>
              <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 52 }}>{(total / 1e6).toFixed(1)}M km²</div>
            </>
          ) : (
            <>
              <div style={{ fontSize: 17, fontWeight: 700, letterSpacing: 2, color: theme.front, marginBottom: 10 }}>{(area?.label ?? "Territory").toUpperCase()}</div>
              <div style={{ display: "flex", height: 16, borderRadius: 3, overflow: "hidden", background: "#3a332a" }}>
                {video.factions.map((f, i) => (
                  <div key={f.id} style={{ width: `${(100 * areaKm2[i]) / total}%`, background: f.color }} />
                ))}
              </div>
              {video.factions.map((f, i) => (
                <div key={f.id} style={{ display: "flex", justifyContent: "space-between", fontSize: 28, marginTop: 8, fontWeight: 700 }}>
                  <span style={{ color: f.color }}>■</span>
                  <span style={{ fontVariantNumeric: "tabular-nums" }}>{Math.round((100 * areaKm2[i]) / total)}%</span>
                </div>
              ))}
            </>
          )}
        </div>
        <div style={{ ...panel, flex: 1 }}>
          {video.factions.map((f) => {
            const set = flagSet(f, day);
            const shown = set.length ? set.slice(0, 3) : null;
            if (!shown && video.factions.length > 2 && !areaKm2[video.factions.indexOf(f)]) return null;
            return (
              <div key={f.id} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                {shown ? (
                  <div style={{ display: "flex", gap: 3 }}>{shown.map((x) => <FlagBadge key={x.id} id={x.id} size={26} round={!x.id.startsWith("banner:")} />)}</div>
                ) : (
                  <div style={{ width: 22, height: 22, borderRadius: 4, background: f.color }} />
                )}
                <div style={{ fontSize: 24, fontWeight: 700, lineHeight: 1.05 }}>{f.name.toUpperCase()}</div>
              </div>
            );
          })}
          {video.header.watermark && (
            <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 15, letterSpacing: 5, color: theme.muted, marginTop: 4 }}>{video.header.watermark.toUpperCase()}</div>
          )}
        </div>
      </div>

      {ev && evDate && (
        <div style={{ position: "absolute", left: 36, right: 36, top: 560, opacity: capOpacity }}>
          <div style={{ ...panel, fontSize: 34, lineHeight: 1.25, textAlign: "center", padding: "16px 22px" }}>
            <span style={{ color: theme.front, fontWeight: 700 }}>{yearly ? evDate.y : `${evDate.d} ${MONTHS[evDate.m - 1]}`}.</span>{" "}
            <span style={{ fontWeight: 700 }}>{ev.title}.</span> {ev.text && <span style={{ fontWeight: 500 }}>{ev.text}</span>}
          </div>
        </div>
      )}

      <div style={{ position: "absolute", left: 36, right: 36, bottom: 120, height: 6, background: "rgba(255,255,255,0.18)", borderRadius: 3 }}>
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: p(day), background: theme.accent, borderRadius: 3 }} />
      </div>
    </div>
  );
};
