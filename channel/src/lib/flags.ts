// Flag sprites for unit markers, drawn in code (no image assets, no licensing questions) at 2x for crisp scaling.
// Simplified to read at ~18 px wide, like campaign-map counters.

export const FLAG_W = 36, FLAG_H = 24;
type Ctx = OffscreenCanvasRenderingContext2D;

function star(ctx: Ctx, cx: number, cy: number, r: number, rot = -Math.PI / 2) {
  ctx.beginPath();
  for (let i = 0; i < 10; i++) {
    const rr = i % 2 ? r * 0.42 : r;
    const a = rot + (i * Math.PI) / 5;
    ctx.lineTo(cx + rr * Math.cos(a), cy + rr * Math.sin(a));
  }
  ctx.closePath();
  ctx.fill();
}

const painters: Record<string, (ctx: Ctx, w: number, h: number) => void> = {
  // Democratic People's Republic of Korea
  dprk: (ctx, w, h) => {
    ctx.fillStyle = "#024fa2";
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, h * 0.17, w, h * 0.66);
    ctx.fillStyle = "#ed1c27";
    ctx.fillRect(0, h * 0.21, w, h * 0.58);
    ctx.fillStyle = "#fff";
    ctx.beginPath();
    ctx.arc(w * 0.36, h / 2, h * 0.24, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#ed1c27";
    star(ctx, w * 0.36, h / 2, h * 0.22);
  },
  // Republic of Korea: taegeuk and four trigrams
  rok: (ctx, w, h) => {
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, w, h);
    const cx = w / 2, cy = h / 2, r = h * 0.25;
    ctx.fillStyle = "#cd2e3a";
    ctx.beginPath();
    ctx.arc(cx, cy, r, Math.PI, 0);
    ctx.fill();
    ctx.fillStyle = "#0047a0";
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI);
    ctx.fill();
    ctx.fillStyle = "#cd2e3a";
    ctx.beginPath();
    ctx.arc(cx - r / 2, cy, r / 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#0047a0";
    ctx.beginPath();
    ctx.arc(cx + r / 2, cy, r / 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#111";
    for (const [x, y, a] of [[0.17, 0.22, 0.6], [0.83, 0.78, 0.6], [0.83, 0.22, -0.6], [0.17, 0.78, -0.6]]) {
      ctx.save();
      ctx.translate(w * x, h * y);
      ctx.rotate(a);
      for (let i = -1; i <= 1; i++) ctx.fillRect(-w * 0.07, i * h * 0.075 - h * 0.025, w * 0.14, h * 0.05);
      ctx.restore();
    }
  },
  // United States (48 stars in 1950; the stars are dots at this size)
  usa: (ctx, w, h) => {
    for (let i = 0; i < 13; i++) {
      ctx.fillStyle = i % 2 ? "#fff" : "#b22234";
      ctx.fillRect(0, (i * h) / 13, w, h / 13 + 0.5);
    }
    ctx.fillStyle = "#3c3b6e";
    ctx.fillRect(0, 0, w * 0.42, (h * 7) / 13);
    ctx.fillStyle = "#fff";
    for (let y = 0; y < 3; y++) for (let x = 0; x < 4; x++) ctx.fillRect(2 + x * 3.6, 2 + y * 3.8, 1.4, 1.4);
  },
  // People's Republic of China
  prc: (ctx, w, h) => {
    ctx.fillStyle = "#ee1c25";
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = "#ffde00";
    star(ctx, w * 0.17, h * 0.27, h * 0.17);
    for (const [x, y] of [[0.34, 0.1], [0.4, 0.2], [0.4, 0.34], [0.34, 0.44]]) star(ctx, w * x, h * y, h * 0.06);
  },
  // United Nations
  un: (ctx, w, h) => {
    ctx.fillStyle = "#5b92e5";
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(w / 2, h / 2, h * 0.3, 0, Math.PI * 2);
    ctx.stroke();
    ctx.fillStyle = "#fff";
    ctx.beginPath();
    ctx.arc(w / 2, h / 2, h * 0.12, 0, Math.PI * 2);
    ctx.fill();
  },
  // United Kingdom (Commonwealth contingents)
  uk: (ctx, w, h) => {
    ctx.fillStyle = "#012169";
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = h * 0.2;
    ctx.beginPath();
    ctx.moveTo(0, 0), ctx.lineTo(w, h), ctx.moveTo(w, 0), ctx.lineTo(0, h);
    ctx.stroke();
    ctx.strokeStyle = "#c8102e";
    ctx.lineWidth = h * 0.07;
    ctx.stroke();
    ctx.fillStyle = "#fff";
    ctx.fillRect(w * 0.4, 0, w * 0.2, h), ctx.fillRect(0, h * 0.35, w, h * 0.3);
    ctx.fillStyle = "#c8102e";
    ctx.fillRect(w * 0.44, 0, w * 0.12, h), ctx.fillRect(0, h * 0.4, w, h * 0.2);
  },
  // Wehrmacht Balkenkreuz (military insignia, used on campaign maps instead of the national flag)
  germany: (ctx, w, h) => {
    ctx.fillStyle = "#e9e6dc";
    ctx.fillRect(0, 0, w, h);
    const cx = w / 2, cy = h / 2, L = h * 0.42, T = h * 0.13;
    ctx.fillStyle = "#fff";
    ctx.fillRect(cx - L, cy - T - 2, 2 * L, 2 * T + 4);
    ctx.fillRect(cx - T - 2, cy - L, 2 * T + 4, 2 * L);
    ctx.fillStyle = "#111";
    ctx.fillRect(cx - L + 2, cy - T, 2 * L - 4, 2 * T);
    ctx.fillRect(cx - T, cy - L + 2, 2 * T, 2 * L - 4);
  },
  france: (ctx, w, h) => {
    ctx.fillStyle = "#0055a4";
    ctx.fillRect(0, 0, w / 3, h);
    ctx.fillStyle = "#fff";
    ctx.fillRect(w / 3, 0, w / 3, h);
    ctx.fillStyle = "#ef4135";
    ctx.fillRect((2 * w) / 3, 0, w / 3 + 1, h);
  },
  belgium: (ctx, w, h) => {
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, w / 3, h);
    ctx.fillStyle = "#fdda24";
    ctx.fillRect(w / 3, 0, w / 3, h);
    ctx.fillStyle = "#ef3340";
    ctx.fillRect((2 * w) / 3, 0, w / 3 + 1, h);
  },
  netherlands: (ctx, w, h) => {
    ctx.fillStyle = "#ae1c28";
    ctx.fillRect(0, 0, w, h / 3);
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, h / 3, w, h / 3);
    ctx.fillStyle = "#21468b";
    ctx.fillRect(0, (2 * h) / 3, w, h / 3 + 1);
  },
  poland: (ctx, w, h) => {
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, w, h / 2);
    ctx.fillStyle = "#dc143c";
    ctx.fillRect(0, h / 2, w, h / 2);
  },
  italy: (ctx, w, h) => {
    ctx.fillStyle = "#009246";
    ctx.fillRect(0, 0, w / 3, h);
    ctx.fillStyle = "#fff";
    ctx.fillRect(w / 3, 0, w / 3, h);
    ctx.fillStyle = "#ce2b37";
    ctx.fillRect((2 * w) / 3, 0, w / 3 + 1, h);
  },
  // Soviet Union: red field, gold star over a simplified hammer and sickle (centred so it survives the roundel crop)
  ussr: (ctx, w, h) => {
    ctx.fillStyle = "#cc0000";
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = "#ffd700";
    ctx.strokeStyle = "#ffd700";
    star(ctx, w * 0.5, h * 0.25, h * 0.1);
    ctx.lineWidth = 2.2;
    ctx.beginPath();
    ctx.arc(w * 0.5, h * 0.58, h * 0.2, Math.PI * 1.05, Math.PI * 0.35, false);
    ctx.stroke();
    ctx.lineWidth = 2.4;
    ctx.beginPath();
    ctx.moveTo(w * 0.4, h * 0.82), ctx.lineTo(w * 0.62, h * 0.45);
    ctx.stroke();
    ctx.fillRect(w * 0.55, h * 0.38, w * 0.12, h * 0.08);
  },
};

// A swallow-tailed army banner on a pole, in the faction's colour (for periods before national flags).
function banner(color: string): (ctx: Ctx, w: number, h: number) => void {
  return (ctx, w, h) => {
    ctx.fillStyle = "#2a2118";
    ctx.fillRect(w * 0.08, 0, w * 0.07, h);
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(w * 0.15, h * 0.05), ctx.lineTo(w * 0.95, h * 0.05), ctx.lineTo(w * 0.72, h * 0.38);
    ctx.lineTo(w * 0.95, h * 0.72), ctx.lineTo(w * 0.15, h * 0.72);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(w * 0.28, h * 0.22), ctx.lineTo(w * 0.28, h * 0.56), ctx.moveTo(w * 0.28, h * 0.39), ctx.lineTo(w * 0.5, h * 0.39);
    ctx.stroke();
  };
}

const cache = new Map<string, OffscreenCanvas>();

// Round badge: the flag cropped to a circle with a white ring, like campaign-map unit roundels.
function roundSprite(id: string): OffscreenCanvas {
  const D = 40;
  const c = new OffscreenCanvas(D, D);
  const ctx = c.getContext("2d")!;
  const flat = flagSprite(id, false);
  ctx.save();
  ctx.beginPath();
  ctx.arc(D / 2, D / 2, D / 2 - 3, 0, Math.PI * 2);
  ctx.clip();
  const h = D, w = (flat.width / flat.height) * h;
  ctx.drawImage(flat, 2, 2, flat.width - 4, flat.height - 4, (D - w) / 2, 0, w, h);
  ctx.restore();
  ctx.lineWidth = 3;
  ctx.strokeStyle = "#fff";
  ctx.beginPath();
  ctx.arc(D / 2, D / 2, D / 2 - 3, 0, Math.PI * 2);
  ctx.stroke();
  ctx.lineWidth = 1.2;
  ctx.strokeStyle = "rgba(10,12,14,0.9)";
  ctx.beginPath();
  ctx.arc(D / 2, D / 2, D / 2 - 0.8, 0, Math.PI * 2);
  ctx.stroke();
  return c;
}

export function flagSprite(id: string, round = false): OffscreenCanvas {
  if (round && !id.startsWith("banner:")) {
    let r = cache.get(`round:${id}`);
    if (!r) cache.set(`round:${id}`, (r = roundSprite(id)));
    return r;
  }
  let c = cache.get(id);
  if (!c) {
    c = new OffscreenCanvas(FLAG_W + 4, FLAG_H + 4);
    const ctx = c.getContext("2d")!;
    const paint = id.startsWith("banner:") ? banner(id.slice(7)) : painters[id];
    if (!paint) throw new Error(`Unknown flag "${id}" (known: ${Object.keys(painters).join(", ")}, banner:<colour>)`);
    ctx.translate(2, 2);
    ctx.save();
    ctx.beginPath();
    ctx.rect(0, 0, FLAG_W, FLAG_H);
    ctx.clip();
    paint(ctx, FLAG_W, FLAG_H);
    ctx.restore();
    if (!id.startsWith("banner:")) {
      ctx.strokeStyle = "rgba(29,25,20,0.9)";
      ctx.lineWidth = 2;
      ctx.strokeRect(0, 0, FLAG_W, FLAG_H);
    }
    cache.set(id, c);
  }
  return c;
}
