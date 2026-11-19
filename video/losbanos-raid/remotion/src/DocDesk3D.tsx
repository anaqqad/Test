// 3D document on a desk (learned from Hoog, "The Hardest NASA Mission in History" 5:38-5:50 and 11:04-12:15):
// a real scanned page lies flat on a dark walnut desk; a 3D camera pushes / glides / tilts over it with a shallow
// depth of field (one sharp band, the near and far page soft), warm key light from the top-right, dark lower-left,
// heavy vignette, and a small grey source credit bottom-left. The narrator reads the exact line the camera is on.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";

export type Cam = {
  tilt: number;   // rotateX in degrees: 0 = straight down on the page, 60-75 = grazing low angle
  rz: number;     // rotateZ in degrees (page turned on the desk)
  zoom: number;   // 1 = page width 1000 px at the focus point
  fx: number; fy: number; // focus point on the page, 0-1 (what sits at screen centre)
};
export type Shot = {
  from: Cam; to: Cam;
  focus?: { y: number; band: number; blur: number }; // sharp band centre/height as fraction of frame height, max blur px
};
export const SHOTS = {
  // A: overhead wide, slow push + slight turn (Hoog 5:39-5:48)
  wide: (fx = 0.5, fy = 0.5): Shot => ({ from: { tilt: 26, rz: -6, zoom: 0.62, fx, fy }, to: { tilt: 30, rz: -2, zoom: 0.72, fx, fy }, focus: { y: 0.5, band: 0.7, blur: 2.5 } }),
  // C: macro glide along a line of text, narrow focus band (Hoog 11:16-11:41)
  glide: (fy: number, x0 = 0.25, x1 = 0.7): Shot => ({ from: { tilt: 34, rz: -2, zoom: 2.5, fx: x0, fy }, to: { tilt: 36, rz: -1, zoom: 2.6, fx: x1, fy }, focus: { y: 0.5, band: 0.22, blur: 8 } }),
  // D: grazing angle that rises and pulls back (Hoog 11:44-11:53)
  grazing: (fy = 0.35): Shot => ({ from: { tilt: 68, rz: 7, zoom: 1.45, fx: 0.5, fy }, to: { tilt: 54, rz: 3, zoom: 1.08, fx: 0.5, fy: fy + 0.05 } , focus: { y: 0.52, band: 0.34, blur: 6 } }),
  // B: low-angle macro on a heading, page receding into blur (Hoog 5:49, 12:11)
  heading: (fx: number, fy: number): Shot => ({ from: { tilt: 70, rz: -22, zoom: 2.3, fx, fy }, to: { tilt: 70, rz: -19, zoom: 2.45, fx: fx + 0.03, fy }, focus: { y: 0.55, band: 0.2, blur: 9 } }),
};

const lerp = (a: Cam, b: Cam, t: number): Cam => ({
  tilt: a.tilt + (b.tilt - a.tilt) * t, rz: a.rz + (b.rz - a.rz) * t, zoom: a.zoom + (b.zoom - a.zoom) * t,
  fx: a.fx + (b.fx - a.fx) * t, fy: a.fy + (b.fy - a.fy) * t,
});

const Scene: React.FC<{ page: string; aspect: number; desk: string; cam: Cam; blur?: number }> = ({ page, aspect, desk, cam, blur = 0 }) => {
  const PW = 1000, PH = PW * aspect;
  const fx = (cam.fx - 0.5) * PW, fy = (cam.fy - 0.5) * PH;
  return (
    <AbsoluteFill style={{ filter: blur ? `blur(${blur}px)` : undefined }}>
    <AbsoluteFill style={{ perspective: 1500, perspectiveOrigin: "50% 42%" }}>
      <div style={{ position: "absolute", left: 960, top: 540, width: 0, height: 0, transformStyle: "preserve-3d",
        transform: `rotateX(${cam.tilt}deg) rotateZ(${cam.rz}deg) scale(${cam.zoom}) translate(${-fx}px, ${-fy}px)` }}>
        <Img src={staticFile(desk)} style={{ position: "absolute", left: -2400, top: -1500, width: 4800, height: 3000, objectFit: "cover" }} />
        {/* contact shadow */}
        <div style={{ position: "absolute", left: -PW / 2 + 10, top: -PH / 2 + 14, width: PW, height: PH, background: "rgba(0,0,0,0.6)", filter: "blur(14px)" }} />
        <div style={{ position: "absolute", left: -PW / 2, top: -PH / 2, width: PW, height: PH }}>
          <Img src={staticFile(page)} style={{ width: "100%", height: "100%" }} />
          {/* key light: warm from the top-right, falling off to the lower-left */}
          <div style={{ position: "absolute", inset: 0, background: "linear-gradient(225deg, rgba(255,214,160,0.10) 0%, rgba(0,0,0,0) 40%, rgba(20,12,6,0.30) 100%)" }} />
        </div>
      </div>
    </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const DocDesk3D: React.FC<{
  page: string; aspect: number; desk?: string; shot: Shot; dur: number; credit?: string;
}> = ({ page, aspect, desk = "doctest/desk.jpg", shot, dur, credit }) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.sin) });
  const cam = lerp(shot.from, shot.to, t);
  const fo = shot.focus ?? { y: 0.5, band: 0.5, blur: 4 };
  const top = (fo.y - fo.band / 2) * 100, bot = (fo.y + fo.band / 2) * 100;
  const mask = `linear-gradient(to bottom, transparent ${Math.max(0, top - 14)}%, black ${top}%, black ${bot}%, transparent ${Math.min(100, bot + 14)}%)`;
  return (
    <AbsoluteFill style={{ background: "#0b0705", overflow: "hidden" }}>
      <Scene page={page} aspect={aspect} desk={desk} cam={cam} blur={fo.blur} />
      <AbsoluteFill style={{ WebkitMaskImage: mask, maskImage: mask }}>
        <Scene page={page} aspect={aspect} desk={desk} cam={cam} />
      </AbsoluteFill>
      {/* warm top-right light, darker lower-left, vignette */}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 70% 60% at 78% 18%, rgba(255,205,150,0.12), transparent 70%)" }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 85% 80% at 55% 45%, transparent 45%, rgba(0,0,0,0.72) 100%)" }} />
      {credit && <div style={{ position: "absolute", left: 22, bottom: 16, fontFamily: "Arial, sans-serif", fontSize: 17, color: "rgba(225,225,225,0.75)", textShadow: "0 0 4px rgba(0,0,0,0.9)" }}>{credit}</div>}
    </AbsoluteFill>
  );
};
