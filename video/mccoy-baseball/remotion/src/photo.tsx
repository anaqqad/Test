// "Contact frame": how the channel shows a photograph.
// A vertical 35 mm strip is pulled up across a dark light table and stops on one frame. Grease-pencil
// crop corners draw around it (and optionally a circle around one detail); the photo slowly pushes in;
// frame number + caption are set beside it. The strip leaves upward, as if the film is advanced.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { C, HEAD, MONO } from "./theme";
import { roughEllipse, Stroke, useProg, wobble } from "./marks";

export type PhotoProps = {
  image: string; // file in public/stills
  aspect: number; // width / height of the picture area to show
  frameNo: string; // "07"
  title: string; // what we are looking at, 2-6 words
  caption: string; // who/where/when, one line
  source: string; // archive + call number
  focus?: [number, number]; // push-in origin, fractions of the photo
  circle?: [number, number, number, number]; // cx, cy, rx, ry as fractions of the photo
  crop?: [number, number, number, number]; // x, y, w, h fractions of the source image to show
  side?: "left" | "right"; // where the strip sits
};

const H = 1080;

export const PhotoCard: React.FC<PhotoProps> = ({ image, aspect, frameNo, title, caption, source, focus = [0.5, 0.5], circle, crop = [0, 0, 1, 1], side = "left" }) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  // picture area: fit inside 1000 x 820
  const ph = Math.min(820, 1000 / aspect), pw = ph * aspect;
  const stripW = pw + 2 * 92;
  const stripX = side === "left" ? 150 : 1920 - 150 - stripW;
  const capX = side === "left" ? stripX + stripW + 70 : 110;
  const capW = side === "left" ? 1920 - capX - 100 : stripX - 180;
  const frameY = (H - ph) / 2;
  const pitch = ph + 120; // distance between frames on the strip
  // strip motion: enters from below, settles (slight overshoot), exits upward
  const enter = interpolate(f, [0, 20], [pitch * 0.9, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(0.6)) });
  const exit = interpolate(f, [d - 14, d], [0, -pitch * 0.9], { extrapolateLeft: "clamp", easing: Easing.in(Easing.cubic) });
  const y = enter + exit;
  const tableOn = interpolate(f, [0, 8, d - 8, d], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const push = interpolate(f, [12, d], [1, 1.07], { extrapolateLeft: "clamp" });
  const corners = useProg(22, 14);
  const ring = useProg(40, 22);
  const cap = (k: number) => interpolate(f, [24 + k * 6, 36 + k * 6, d - 12, d - 4], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const capShift = (k: number) => interpolate(cap(k), [0, 1], [14, 0]);

  // sprocket holes along both edges of the strip
  const holes: React.ReactNode[] = [];
  for (let yy = -pitch * 2; yy < H + pitch * 2; yy += 56) {
    for (const x of [26, stripW - 26 - 22]) holes.push(<rect key={`${x}-${yy}`} x={x} y={yy} width={22} height={32} rx={5} fill={C.tableGlow} />);
  }
  const [cx, cy, cw, chh] = crop;
  const imgStyle: React.CSSProperties = {
    position: "absolute",
    width: `${100 / cw}%`, height: `${100 / chh}%`,
    left: `${(-cx / cw) * 100}%`, top: `${(-cy / chh) * 100}%`,
    objectFit: "fill", filter: "grayscale(1) contrast(1.05)",
  };
  const pad = 22, L = 70; // crop-corner geometry around the photo, in strip coords
  const bx = 92 - pad, by = frameY - pad, bw = pw + 2 * pad, bh = ph + 2 * pad;
  const cornerPath = [
    wobble([[bx, by + L], [bx, by], [bx + L, by]], 3),
    wobble([[bx + bw - L, by], [bx + bw, by], [bx + bw, by + L]], 5),
    wobble([[bx + bw, by + bh - L], [bx + bw, by + bh], [bx + bw - L, by + bh]], 7),
    wobble([[bx + L, by + bh], [bx, by + bh], [bx, by + bh - L]], 9),
  ];

  return (
    <AbsoluteFill style={{ opacity: tableOn, background: `radial-gradient(ellipse at ${side === "left" ? "40%" : "60%"} 50%, ${C.tableGlow} 0%, ${C.table} 70%)` }}>
      {/* the strip */}
      <div style={{ position: "absolute", left: stripX, top: 0, width: stripW, height: H, transform: `translateY(${y}px)` }}>
        <svg width={stripW} height={H} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
          <rect x={0} y={-pitch * 2} width={stripW} height={H + pitch * 4} fill={C.rebate} />
          {holes}
          {/* neighbouring frames, unexposed */}
          {[-1, 1].map((k) => (
            <rect key={k} x={92} y={frameY + k * pitch} width={pw} height={ph} fill="#1a1a1a" />
          ))}
          {/* edge print */}
          {[-1, 0, 1].map((k) => (
            <text key={k} x={64} y={frameY + k * pitch + ph - 10} fontFamily={MONO} fontSize={17} fill={C.edge} transform={`rotate(-90 ${64} ${frameY + k * pitch + ph - 10})`}>
              {`${String(Number(frameNo) + k).padStart(2, "0")}  ▸  ARCHIVE`}
            </text>
          ))}
        </svg>
        <div style={{ position: "absolute", left: 92, top: frameY, width: pw, height: ph, overflow: "hidden", background: "#000" }}>
          <div style={{ position: "absolute", inset: 0, transform: `scale(${push})`, transformOrigin: `${focus[0] * 100}% ${focus[1] * 100}%` }}>
            <Img src={staticFile(`stills/${image}`)} style={imgStyle} />
          </div>
        </div>
        <svg width={stripW} height={H} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
          {cornerPath.map((p, i) => <Stroke key={i} d={p} p={corners} w={7} />)}
          {circle ? <Stroke d={roughEllipse(92 + circle[0] * pw, frameY + circle[1] * ph, circle[2] * pw, circle[3] * ph, 11)} p={ring} w={6} /> : null}
        </svg>
      </div>
      {/* caption column */}
      <div style={{ position: "absolute", left: capX, width: capW, top: 0, height: H, display: "flex", flexDirection: "column", justifyContent: "center" }}>
        <div style={{ opacity: cap(0), transform: `translateY(${capShift(0)}px)`, fontFamily: HEAD, fontWeight: 700, fontSize: 40, letterSpacing: 2, color: C.grease }}>FR. {frameNo}</div>
        <div style={{ opacity: cap(1), transform: `translateY(${capShift(1)}px)`, fontFamily: HEAD, fontWeight: 700, fontSize: 74, lineHeight: 0.98, textTransform: "uppercase", color: C.light, marginTop: 10 }}>{title}</div>
        <div style={{ opacity: cap(2), transform: `translateY(${capShift(2)}px)`, fontFamily: MONO, fontSize: 25, lineHeight: 1.45, color: C.light, marginTop: 26 }}>{caption}</div>
        <div style={{ opacity: cap(3), transform: `translateY(${capShift(3)}px)`, fontFamily: MONO, fontSize: 19, lineHeight: 1.45, color: C.lightSoft, marginTop: 22, textTransform: "uppercase", letterSpacing: 1 }}>{source}</div>
      </div>
    </AbsoluteFill>
  );
};
