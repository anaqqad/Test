import React from "react";
import { Img, staticFile } from "remotion";
import type { Video } from "../schema";
import { dateParts, dayNumber, formatDate, sampleSeries } from "../lib/time";
import { theme } from "../lib/theme";

const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const fmt = (n: number) => Math.round(n).toLocaleString("en-US");
const WORLD_LAND_KM2 = 134.9e6; // land area excluding Antarctica

type Props = {
  video: Video;
  day: number;
  startDay: number;
  frame: number;
  eventFrames: number[];
  areaKm2: number[];
};

const Section: React.FC<{ label: string; children: React.ReactNode }> = ({ label, children }) => (
  <div style={{ marginTop: 26 }}>
    <div style={{ fontFamily: theme.number, fontWeight: 700, fontSize: 17, letterSpacing: 4, color: theme.muted, marginBottom: 10 }}>
      {label.toUpperCase()}
    </div>
    {children}
  </div>
);

export const Sidebar: React.FC<Props> = ({ video, day, startDay, frame, eventFrames, areaKm2 }) => {
  const { y, m, d } = dateParts(day);
  const yearly = video.timeline.clock === "year";
  const counter = yearly ? `YEAR ${fmt(y - dateParts(startDay).y + 1)}` : `DAY ${fmt(Math.max(1, Math.floor(day) - startDay + 1))}`;
  const total = areaKm2.reduce((a, b) => a + b, 0) || 1;
  const leaders = video.leaders.filter(
    (l) => (!l.from || dayNumber(l.from) <= day) && (!l.to || day < dayNumber(l.to)),
  );
  const past = video.events.map((e, i) => ({ e, f: eventFrames[i] })).filter((x) => x.f <= frame).slice(-3).reverse();

  return (
    <div
      style={{
        position: "absolute", left: 1440, top: 0, width: 480, height: 1080, boxSizing: "border-box",
        padding: "44px 40px", background: theme.panel, color: theme.panelText,
        borderLeft: `3px solid ${theme.front}`, fontFamily: theme.number,
      }}
    >
      {/* The clock: the element the viewer's eye returns to every few seconds. */}
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
        <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 92, lineHeight: 1, fontVariantNumeric: "tabular-nums" }}>{y}</div>
        <div style={{ fontSize: 24, fontWeight: 700, color: theme.front, letterSpacing: 2 }}>{counter}</div>
      </div>
      {!yearly && (
        <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 40, marginTop: 6 }}>
          {d} {MONTHS[m - 1]}
        </div>
      )}

      <div style={{ height: 2, background: theme.muted, opacity: 0.35, margin: "26px 0 20px" }} />
      <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 30, lineHeight: 1.15 }}>{video.header.title}</div>
      <div style={{ fontSize: 22, color: theme.muted, marginTop: 6 }}>{video.header.subtitle}</div>

      {video.counters.map((c, ci) =>
        c.kind === "area" && c.mode === "total" ? (
          <Section key={ci} label={c.label}>
            <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 46, fontVariantNumeric: "tabular-nums" }}>
              {(total / 1e6).toFixed(1)}M km²
            </div>
            <div style={{ fontSize: 22, color: theme.muted }}>
              {((100 * total) / WORLD_LAND_KM2).toFixed(1)}% of all land outside Antarctica
            </div>
            {video.factions.filter((_, i) => areaKm2[i] > 0).length > 1 &&
              video.factions.map((f, i) =>
                areaKm2[i] > 0 ? (
                  <div key={f.id} style={{ display: "flex", justifyContent: "space-between", fontSize: 22, marginTop: 6 }}>
                    <span><span style={{ color: f.color }}>■</span> {f.name}</span>
                    <span style={{ fontVariantNumeric: "tabular-nums" }}>{(areaKm2[i] / 1e6).toFixed(1)}M km²</span>
                  </div>
                ) : null,
              )}
          </Section>
        ) : c.kind === "area" ? (
          <Section key={ci} label={c.label}>
            <div style={{ display: "flex", height: 16, borderRadius: 3, overflow: "hidden", background: "#3a332a" }}>
              {video.factions.map((f, i) => (
                <div key={f.id} style={{ width: `${(100 * areaKm2[i]) / total}%`, background: f.color }} />
              ))}
            </div>
            {video.factions.map((f, i) => (
              <div key={f.id} style={{ display: "flex", justifyContent: "space-between", fontSize: 24, marginTop: 8 }}>
                <span><span style={{ color: f.color }}>■</span> {f.name}</span>
                <span style={{ fontVariantNumeric: "tabular-nums" }}>
                  {fmt(areaKm2[i])} km² <span style={{ color: theme.muted }}>{Math.round((100 * areaKm2[i]) / total)}%</span>
                </span>
              </div>
            ))}
          </Section>
        ) : (
          <Section key={ci} label={c.label}>
            {c.rows.map((r) => {
              const f = video.factions.find((x) => x.id === r.factionId);
              const v = sampleSeries(r.points.map(([dd, val]) => [dayNumber(dd), val]), day);
              return (
                <div key={r.factionId} style={{ display: "flex", justifyContent: "space-between", fontSize: 26, marginTop: 6 }}>
                  <span><span style={{ color: f?.color }}>■</span> {f?.name}</span>
                  <span style={{ fontWeight: 700, fontVariantNumeric: "tabular-nums" }}>{fmt(v)}</span>
                </div>
              );
            })}
          </Section>
        ),
      )}

      {leaders.length > 0 && (
        <Section label="Leaders">
          {leaders.map((l) => {
            const f = video.factions.find((x) => x.id === l.factionId);
            return (
              <div key={l.name} style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 10 }}>
                {l.image ? (
                  <Img src={staticFile(l.image)} style={{ width: 52, height: 52, borderRadius: 4, objectFit: "cover", filter: "sepia(0.4)", border: `2px solid ${f?.color}` }} />
                ) : (
                  <div style={{ width: 52, height: 52, borderRadius: 4, background: f?.color, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: theme.display, fontWeight: 700, fontSize: 20, color: theme.panel }}>
                    {(l.name[0] + (l.name.split(" ").pop() ?? "")[0]).toUpperCase()}
                  </div>
                )}
                <div>
                  <div style={{ fontSize: 24, fontWeight: 700, lineHeight: 1.1 }}>{l.name}</div>
                  <div style={{ fontSize: 19, color: theme.muted }}>{l.role}</div>
                </div>
              </div>
            );
          })}
        </Section>
      )}

      {past.length > 0 && (
        <Section label="Chronicle">
          {past.map(({ e, f }, i) => (
            <div key={f + e.title} style={{ display: "flex", gap: 12, fontSize: 21, marginTop: 6, opacity: i === 0 ? 1 : 0.55 }}>
              <span style={{ color: theme.front, minWidth: 100, fontVariantNumeric: "tabular-nums" }}>{formatDate(dayNumber(e.date), "short")}</span>
              <span>{e.title}</span>
            </div>
          ))}
        </Section>
      )}

      {video.header.footnote && (
        <div style={{ position: "absolute", bottom: 64, left: 40, right: 40, fontSize: 17, color: theme.muted, opacity: 0.8 }}>{video.header.footnote}</div>
      )}
      {video.header.watermark && (
        <div style={{ position: "absolute", bottom: 30, left: 40, right: 40, fontFamily: theme.display, fontWeight: 700, fontSize: 18, letterSpacing: 6, color: theme.muted, opacity: 0.7 }}>
          {video.header.watermark.toUpperCase()}
        </div>
      )}
    </div>
  );
};
