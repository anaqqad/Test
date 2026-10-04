// Interior / everyday settings for the comedy skits (1920x1080 SVG). Same flat style as art.mjs.
import { scene, shade, rng } from "./art.mjs";

const W = 1920, H = 1080;
const wrap = (s) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice">${s}</svg>`;

function room(wall, floor, floorY = 800, pattern = "") {
  let s = `<rect width="${W}" height="${floorY}" fill="${wall}"/>${pattern}`;
  s += `<rect y="${floorY}" width="${W}" height="${H - floorY}" fill="${floor}"/>`;
  for (let x = -400; x < W + 400; x += 160) s += `<path d="M${960 + (x - 960) * 0.55} ${floorY} L${x} ${H}" stroke="${shade(floor, -0.08)}" stroke-width="3"/>`;
  s += `<rect y="${floorY - 14}" width="${W}" height="14" fill="${shade(wall, -0.25)}"/>`;
  s += `<rect width="${W}" height="${H}" fill="url(#vig)"/>`;
  return `<defs><radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient></defs>` + s;
}
const sign = (x, y, w, h, bg, fg, text, size = 44) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="${bg}" stroke="${shade(bg, -0.35)}" stroke-width="6"/><text x="${x + w / 2}" y="${y + h / 2 + size * 0.36}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="${size}" fill="${fg}">${text}</text>`;

const SETTINGS = {
  airport() {
    let s = room("#dfe6ec", "#b9c3cc", 790);
    for (let i = 0; i < 4; i++) s += `<rect x="${120 + i * 440}" y="80" width="400" height="430" rx="8" fill="#9fd0f5" stroke="#8a97a3" stroke-width="10"/><path d="M${120 + i * 440} 420 L${520 + i * 440} 420" stroke="#8a97a3" stroke-width="6"/>`;
    s += `<path d="M640 220 l140 -20 l60 -40 l20 0 l-30 50 l120 -10 l30 -30 l16 0 l-16 46 l-300 30Z" fill="#f4f6f8" opacity=".9"/>`;
    s += sign(700, 560, 520, 90, "#1f3a5f", "#ffcf5c", "✈ ARRIVALS", 50);
    return s;
  },
  airportFront() {
    return `<path d="M1000 820 L1920 820 L1920 1080 L1000 1080Z" fill="#8a97a3"/><rect x="1000" y="800" width="920" height="40" fill="#5e6b78"/>` + sign(1250, 880, 440, 80, "#1f3a5f", "#fff", "IMMIGRATION", 40);
  },
  coffee() {
    let brick = `<defs><pattern id="brick" width="120" height="60" patternUnits="userSpaceOnUse"><rect width="120" height="60" fill="#b5653f"/><path d="M0 30 H120 M60 0 V30 M0 30 V60 M120 30 V60" stroke="#8c4a2c" stroke-width="5"/></pattern></defs>`;
    let s = room("url(#brick)", "#6b4a32", 790, "");
    s = brick + s;
    s += `<rect x="1080" y="90" width="700" height="380" rx="16" fill="#2b2b2b" stroke="#6b4a32" stroke-width="16"/>`;
    const items = [["Latte", "4.95"], ["Cold Brew", "5.45"], ["Oat Vanilla Iced", "7.25"], ["Caramel Frappé", "6.95"], ["Pumpkin Spice ???", "8.50"]];
    items.forEach(([n, p], i) => (s += `<text x="1130" y="${170 + i * 62}" font-family="Montserrat" font-weight="700" font-size="38" fill="#f4f1e8">${n}</text><text x="1730" y="${170 + i * 62}" text-anchor="end" font-family="Montserrat" font-weight="700" font-size="38" fill="#ffcf5c">${p}</text>`));
    for (const x of [300, 700]) s += `<path d="M${x} 0 V120" stroke="#2b2b2b" stroke-width="5"/><path d="M${x - 50} 170 Q${x} 100 ${x + 50} 170Z" fill="#2b2b2b"/><circle cx="${x}" cy="176" r="18" fill="#ffe8a3"/>`;
    return s;
  },
  coffeeFront() {
    let s = `<rect x="980" y="810" width="940" height="270" fill="#4a3324"/><rect x="980" y="790" width="940" height="34" fill="#2b1d14"/>`;
    s += `<rect x="1600" y="640" width="200" height="160" rx="16" fill="#c9ccd1" stroke="#7a7f86" stroke-width="6"/><rect x="1640" y="690" width="40" height="70" fill="#4a4f56"/><rect x="1720" y="690" width="40" height="70" fill="#4a4f56"/>`;
    for (const [x, c] of [[1100, "#f4f1e8"], [1180, "#2e6b4f"]]) s += `<path d="M${x} 790 L${x + 10} 720 L${x + 60} 720 L${x + 70} 790Z" fill="${c}" stroke="#2b1d14" stroke-width="4"/>`;
    return s;
  },
  barber() {
    let stripes = `<defs><pattern id="str" width="80" height="80" patternUnits="userSpaceOnUse"><rect width="80" height="80" fill="#2a7f86"/><rect width="40" height="80" fill="#2f8e96"/></pattern></defs>`;
    let s = stripes + room("url(#str)", "#e6e1d6", 800);
    s += `<rect x="760" y="120" width="560" height="480" rx="20" fill="#cfe9f2" stroke="#c9a84a" stroke-width="18"/><path d="M820 160 L960 160 L860 300Z" fill="#fff" opacity=".5"/>`;
    s += `<rect x="1420" y="60" width="70" height="420" rx="35" fill="#fff" stroke="#8a8a8a" stroke-width="6"/>`;
    for (let y = 70; y < 470; y += 60) s += `<path d="M1424 ${y} L1486 ${y + 40} L1486 ${y + 60} L1424 ${y + 20}Z" fill="#c0392b"/><path d="M1424 ${y + 30} L1486 ${y + 70} L1486 ${y + 80} L1424 ${y + 40}Z" fill="#1f4e8c"/>`;
    s += `<rect x="760" y="610" width="560" height="22" fill="#c9a84a"/>`;
    for (let i = 0; i < 7; i++) s += `<rect x="${790 + i * 72}" y="${560 - (i % 3) * 18}" width="34" height="${50 + (i % 3) * 18}" rx="8" fill="${["#e74c3c", "#3498db", "#f1c40f", "#2ecc71"][i % 4]}"/>`;
    s += sign(120, 90, 460, 110, "#1d1d1d", "#ffcf5c", "✂ BARBER", 64);
    return s;
  },
  store() {
    let s = room("#eef0f2", "#cfd5da", 800);
    for (let row = 0; row < 3; row++) {
      const y = 170 + row * 200;
      s += `<rect x="60" y="${y + 150}" width="1000" height="18" fill="#9aa3ab"/>`;
      const r = rng("store" + row);
      for (let x = 80; x < 1040; x += 58) { const h = 80 + r() * 60; s += `<rect x="${x}" y="${y + 150 - h}" width="48" height="${h}" rx="6" fill="${["#e74c3c", "#f39c12", "#27ae60", "#2980b9", "#8e44ad", "#f1c40f"][Math.floor(r() * 6)]}"/>`; }
    }
    for (let x = 200; x < W; x += 500) s += `<rect x="${x}" y="30" width="300" height="18" rx="9" fill="#fffbe6"/>`;
    s += sign(1180, 90, 640, 100, "#27ae60", "#fff", "SELF CHECKOUT", 54);
    return s;
  },
  street() {
    return scene("village", "a2street").replace(/^<svg[^>]*>/, "").replace(/<\/svg>$/, "");
  },
  apartment() {
    let s = room("#f2e3c6", "#a0785a", 800);
    s += `<rect x="1180" y="120" width="560" height="420" rx="10" fill="#9fd0f5" stroke="#f4f1e8" stroke-width="22"/><path d="M1460 120 V540 M1180 330 H1740" stroke="#f4f1e8" stroke-width="14"/>`;
    s += `<path d="M150 620 Q150 560 220 560 H620 Q690 560 690 620 V800 H150Z" fill="#7a8fa6"/><rect x="130" y="640" width="580" height="100" rx="30" fill="#8aa0b8"/>`;
    s += `<rect x="900" y="660" width="80" height="140" fill="#b5653f"/><circle cx="940" cy="600" r="80" fill="#3f7d3a"/>`;
    return s;
  },
  doctor() {
    let s = room("#e3f1f7", "#c4d4dc", 800);
    s += `<rect x="1300" y="120" width="300" height="400" fill="#fff" stroke="#9fb3bf" stroke-width="8"/>`;
    ["E", "F P", "T O Z", "L P E D", "P E C F D"].forEach((t, i) => (s += `<text x="1450" y="${200 + i * 70}" text-anchor="middle" font-family="DejaVu Sans" font-weight="700" font-size="${64 - i * 10}" fill="#1d1d1d">${t}</text>`));
    s += `<rect x="200" y="140" width="160" height="160" rx="16" fill="#fff"/><path d="M260 165 h40 v50 h50 v40 h-50 v50 h-40 v-50 h-50 v-40 h50Z" fill="#e74c3c"/>`;
    s += `<rect x="700" y="660" width="560" height="60" rx="20" fill="#7fb2e5"/><rect x="720" y="720" width="20" height="80" fill="#9aa3ab"/><rect x="1220" y="720" width="20" height="80" fill="#9aa3ab"/>`;
    return s;
  },
  party() {
    let s = `<rect width="${W}" height="${H}" fill="#1b1036"/>`;
    const cols = ["#ff4fd8", "#4fd1ff", "#ffe14f", "#7cff4f"];
    cols.forEach((c, i) => (s += `<path d="M960 120 L${200 + i * 500} 1080 L${420 + i * 500} 1080Z" fill="${c}" opacity=".16"/>`));
    s += `<circle cx="960" cy="120" r="70" fill="#c9ccd1"/>`;
    for (let i = 0; i < 40; i++) s += `<rect x="${910 + (i % 8) * 13}" y="${70 + Math.floor(i / 8) * 20}" width="10" height="16" fill="${i % 3 ? "#f4f6f8" : "#9aa3ab"}"/>`;
    for (let x = 0; x < W; x += 60) s += `<circle cx="${x + 30}" cy="${40 + Math.sin(x / 120) * 25}" r="9" fill="${cols[(x / 60) % 4]}"/>`;
    s += `<rect y="860" width="${W}" height="220" fill="#2a1a4e"/>`;
    return s;
  },
};

export function setting(name) { return wrap(SETTINGS[name]()); }
export function foreground(name) { return SETTINGS[name + "Front"] ? wrap(SETTINGS[name + "Front"]()) : ""; }

// Stand-ins for "characters" that are machines
export function kiosk() {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 900"><rect x="120" y="120" width="360" height="780" rx="30" fill="#5e6b78"/><rect x="150" y="150" width="300" height="230" rx="16" fill="#0b1220"/>
  <rect id="scr" x="165" y="165" width="270" height="200" rx="10" fill="#f39c12"/><text x="300" y="250" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#1d1d1d">⚠ UNEXPECTED</text><text x="300" y="295" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#1d1d1d">ITEM</text>
  <rect x="80" y="470" width="440" height="40" rx="8" fill="#9aa3ab"/><rect x="170" y="420" width="260" height="50" rx="6" fill="#e74c3c" opacity=".85"/><rect x="200" y="560" width="200" height="40" rx="10" fill="#2b2b2b"/></svg>`;
}
export function phoneUI() {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 900"><rect x="130" y="60" width="340" height="700" rx="46" fill="#1d1d1d"/><rect x="150" y="90" width="300" height="640" rx="30" fill="#24324a"/>
  <circle cx="300" cy="250" r="70" fill="#3a4d6e"/><text x="300" y="272" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="60" fill="#fff">🏦</text>
  <text x="300" y="380" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff">BANK</text>
  <text id="hold" x="300" y="430" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="28" fill="#9fd0f5">On hold 47:00</text>
  <circle cx="300" cy="640" r="44" fill="#e74c3c"/><path d="M276 640 q24 -20 48 0" stroke="#fff" stroke-width="8" fill="none"/></svg>`;
}
