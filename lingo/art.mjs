// Procedural flat-vector art: characters (busts) and landscape backgrounds, as SVG strings.
// Everything is original and resolution-independent, so frames are crisp at 1080p/4K.

// ---------- helpers ----------
export function rng(seed) {
  let s = typeof seed === "string" ? [...seed].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7) : seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}
const hex = (c) => c.replace("#", "").match(/../g).map((h) => parseInt(h, 16));
const toHex = (a) => "#" + a.map((v) => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("");
export const mix = (a, b, t) => toHex(hex(a).map((v, i) => v + (hex(b)[i] - v) * t));
export const shade = (c, t) => (t < 0 ? mix(c, "#000000", -t) : mix(c, "#ffffff", t));

// ---------- characters ----------
// viewBox 0 0 800 1000; head centred at x=400.
const SKIN = { pale: "#f6dcc8", light: "#eec4a2", tan: "#d9a27a", olive: "#c89064", brown: "#a0673f", dark: "#6e4127", deep: "#4f2d1b" };
const HAIR = { black: "#1f1a1c", brown: "#5a3825", auburn: "#8a3b1d", blonde: "#e2bb6c", grey: "#b9b6b2", white: "#ecebe7", red: "#b5462a" };

function hairBack(h, c, line) {
  const d = {
    long: "M232 330 C214 120 586 120 568 330 C585 470 610 600 640 760 C520 800 280 800 160 760 C190 600 215 470 232 330Z",
    braids: "M236 330 C220 140 580 140 564 330 C570 420 575 480 572 540 L228 540 C225 480 230 420 236 330Z",
    ponytail: "M236 330 C220 140 580 140 564 330 C600 260 690 330 660 520 C640 600 600 620 580 560 C600 470 590 400 564 330Z",
    curly: "",
    bob: "M228 330 C210 130 590 130 572 330 C585 420 590 500 580 560 C540 580 260 580 220 560 C210 500 215 420 228 330Z",
  }[h];
  if (h === "curly") {
    let s = "";
    for (let i = 0; i < 16; i++) {
      const a = Math.PI * (0.95 + (i / 15) * 1.1), r = 190;
      s += `<circle cx="${400 + Math.cos(a) * r}" cy="${350 + Math.sin(a) * r * 0.95}" r="62" fill="${c}" stroke="${line}" stroke-width="6"/>`;
    }
    for (const [x, y] of [[225, 450], [575, 450], [235, 520], [565, 520]]) s += `<circle cx="${x}" cy="${y}" r="50" fill="${c}" stroke="${line}" stroke-width="6"/>`;
    return s;
  }
  return d ? `<path d="${d}" fill="${c}" stroke="${line}" stroke-width="7" stroke-linejoin="round"/>` : "";
}

function hairFront(h, c, line) {
  const hl = shade(c, 0.18);
  if (h === "bald") return `<path d="M300 205 C340 185 380 182 410 186" stroke="${shade(c, 0.5)}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".35"/>`;
  if (h === "curly") {
    let s = "";
    for (let i = 0; i < 9; i++) s += `<circle cx="${262 + i * 34.5}" cy="${232 - Math.sin((i / 8) * Math.PI) * 52}" r="44" fill="${c}" stroke="${line}" stroke-width="6"/>`;
    return s;
  }
  const fringe = {
    short: "M240 360 C222 150 578 150 560 360 C548 290 520 250 470 238 C430 268 330 262 300 246 C262 270 246 310 240 360Z",
    long: "M236 380 C218 140 582 140 564 380 C552 300 520 248 450 232 C420 270 340 300 260 300 C250 320 240 350 236 380Z",
    braids: "M238 360 C222 150 578 150 562 360 C550 280 500 236 400 232 C300 236 250 280 238 360Z",
    ponytail: "M238 360 C222 150 578 150 562 360 C550 280 500 236 400 232 C300 236 250 280 238 360Z",
    bob: "M232 380 C214 140 586 140 568 380 C560 300 540 270 520 262 C470 280 330 280 280 262 C260 270 240 300 232 380Z",
    bun: "M238 360 C222 150 578 150 562 360 C550 280 500 236 400 232 C300 236 250 280 238 360Z",
    spiky: "M238 360 C230 250 250 200 270 190 L285 130 L320 180 L350 115 L380 170 L415 108 L440 168 L475 118 L492 178 L530 140 L535 200 C560 220 570 290 562 360 C548 290 520 250 470 240 C430 262 330 262 300 246 C262 270 246 310 238 360Z",
  }[h] || "";
  let s = `<path d="${fringe}" fill="${c}" stroke="${line}" stroke-width="7" stroke-linejoin="round"/>`;
  s += `<path d="M300 200 C340 180 400 176 440 184" stroke="${hl}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".7"/>`;
  if (h === "bun") s = `<circle cx="400" cy="150" r="70" fill="${c}" stroke="${line}" stroke-width="7"/>` + s;
  if (h === "braids") for (const x of [250, 550]) {
    let b = "";
    for (let i = 0; i < 7; i++) b += `<ellipse cx="${x + (x < 400 ? -18 : 18)}" cy="${470 + i * 52}" rx="34" ry="32" fill="${c}" stroke="${line}" stroke-width="6"/>`;
    s += b + `<rect x="${x + (x < 400 ? -40 : -4)}" y="${818}" width="44" height="22" rx="8" fill="#c0392b"/>`;
  }
  return s;
}

const PATTERNS = {
  stripes: (a, b) => `<pattern id="P" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="${a}"/><rect width="60" height="20" fill="${b}"/></pattern>`,
  vstripes: (a, b) => `<pattern id="P" width="70" height="70" patternUnits="userSpaceOnUse"><rect width="70" height="70" fill="${a}"/><rect width="22" height="70" fill="${b}"/></pattern>`,
  zigzag: (a, b) => `<pattern id="P" width="80" height="60" patternUnits="userSpaceOnUse"><rect width="80" height="60" fill="${a}"/><path d="M0 40 L20 20 L40 40 L60 20 L80 40" stroke="${b}" stroke-width="10" fill="none"/></pattern>`,
  dots: (a, b) => `<pattern id="P" width="50" height="50" patternUnits="userSpaceOnUse"><rect width="50" height="50" fill="${a}"/><circle cx="25" cy="25" r="8" fill="${b}"/></pattern>`,
  check: (a, b) => `<pattern id="P" width="80" height="80" patternUnits="userSpaceOnUse"><rect width="80" height="80" fill="${a}"/><rect width="40" height="40" fill="${b}" opacity=".8"/><rect x="40" y="40" width="40" height="40" fill="${b}" opacity=".8"/></pattern>`,
  diamonds: (a, b) => `<pattern id="P" width="70" height="70" patternUnits="userSpaceOnUse"><rect width="70" height="70" fill="${a}"/><path d="M35 8 L62 35 L35 62 L8 35Z" fill="none" stroke="${b}" stroke-width="8"/></pattern>`,
};

function outfit(o, skin, uid) {
  const c = o.color || "#3d5a80", c2 = o.color2 || shade(c, 0.35), line = shade(c, -0.45), trim = o.trim || "#e9c46a";
  const body = "M110 1000 C118 840 210 735 330 705 L470 705 C590 735 682 840 690 1000Z";
  const fill = o.pattern ? `url(#P${uid})` : c;
  let defs = o.pattern ? PATTERNS[o.pattern](c, c2).replace('id="P"', `id="P${uid}"`) : "";
  let s = `<path d="${body}" fill="${fill}" stroke="${line}" stroke-width="8" stroke-linejoin="round"/>`;
  s += `<path d="M170 1000 C180 880 230 800 300 760" stroke="${shade(c, 0.25)}" stroke-width="14" fill="none" opacity=".45" stroke-linecap="round"/>`;
  const t = o.type || "tunic";
  if (t === "tunic") s += `<path d="M340 705 L400 790 L460 705Z" fill="${skin}" stroke="${shade(skin, -0.3)}" stroke-width="6"/><path d="M330 705 L400 800 L470 705" stroke="${trim}" stroke-width="16" fill="none" stroke-linejoin="round"/>`;
  if (t === "robe") s += `<path d="M335 705 L470 1000" stroke="${trim}" stroke-width="40"/><path d="M465 705 L330 1000" stroke="${shade(trim, -0.15)}" stroke-width="40"/><path d="M345 705 L400 770 L455 705Z" fill="${skin}"/>`;
  if (t === "shirt") s += `<path d="M345 705 L400 780 L455 705Z" fill="#ffffff" stroke="${line}" stroke-width="5"/><path d="M335 700 L300 790 L395 780Z M465 700 L500 790 L405 780Z" fill="#f4f4f4" stroke="${line}" stroke-width="6" stroke-linejoin="round"/>` + (o.vest ? `<path d="M210 1000 C220 860 260 770 330 730 L390 900 L390 1000Z M590 1000 C580 860 540 770 470 730 L410 900 L410 1000Z" fill="${o.vest}" stroke="${shade(o.vest, -0.4)}" stroke-width="6"/>` : "") + (o.tie ? `<path d="M390 785 L410 785 L425 900 L400 930 L375 900Z" fill="${o.tie}"/>` : "");
  if (t === "dress") s += `<path d="M300 715 C330 790 470 790 500 715Z" fill="${skin}" stroke="${shade(skin, -0.3)}" stroke-width="5"/><path d="M285 712 C320 815 480 815 515 712" stroke="${trim}" stroke-width="26" fill="none"/><path d="M285 712 C320 815 480 815 515 712" stroke="${c2}" stroke-width="8" stroke-dasharray="4 18" fill="none" stroke-linecap="round"/>`;
  if (t === "coat") s += `<path d="M345 705 L400 790 L455 705Z" fill="${o.inner || "#f1ece2"}"/><path d="M330 705 L400 830 L355 1000 L270 1000 L290 800Z M470 705 L400 830 L445 1000 L530 1000 L510 800Z" fill="${shade(c, -0.12)}" stroke="${line}" stroke-width="6" stroke-linejoin="round"/>`;
  if (t === "parka") s += `<path d="M260 760 C290 690 510 690 540 760 C500 800 300 800 260 760Z" fill="${o.fur || "#efe6d6"}" stroke="${shade(o.fur || "#efe6d6", -0.3)}" stroke-width="6"/><path d="M400 800 L400 1000" stroke="${trim}" stroke-width="22"/><path d="M140 930 L660 930" stroke="${trim}" stroke-width="26" opacity=".9"/>`;
  if (t === "wrap") s += `<path d="M120 1000 C140 880 250 760 400 740 C550 760 660 880 680 1000Z" fill="${c2}" stroke="${shade(c2, -0.4)}" stroke-width="6" opacity=".95"/><path d="M330 705 L470 705 L400 760Z" fill="${skin}"/><path d="M160 930 C300 860 500 860 640 930" stroke="${trim}" stroke-width="14" fill="none"/>`;
  if (t === "bare") s += `<path d="M300 705 C330 760 470 760 500 705 L520 715 C480 790 320 790 280 715Z" fill="${skin}"/>`;
  if (o.necklace) s += `<path d="M320 720 C340 800 460 800 480 720" stroke="${o.necklace}" stroke-width="12" fill="none" stroke-dasharray="1 24" stroke-linecap="round"/>`;
  if (o.sash) s += `<path d="M200 820 L640 1000 L590 1000 L180 860Z" fill="${o.sash}" opacity=".95"/>`;
  return { defs, s };
}

function hat(h, uid) {
  if (!h) return { back: "", front: "" };
  const c = h.color || "#7b2d26", c2 = h.color2 || "#e9c46a", line = shade(c, -0.45);
  const L = `stroke="${line}" stroke-width="7" stroke-linejoin="round"`;
  switch (h.type) {
    case "flatcap": return { back: "", front: `<path d="M228 300 C220 150 580 150 572 300 C520 270 280 270 228 300Z" fill="${c}" ${L}/><path d="M232 298 C300 330 520 320 590 300 C600 330 520 350 400 350 C290 350 240 330 232 298Z" fill="${shade(c, -0.15)}" ${L}/>` };
    case "beanie": return { back: "", front: `<path d="M235 300 C220 110 580 110 565 300Z" fill="${c}" ${L}/><rect x="222" y="270" width="356" height="62" rx="26" fill="${c2}" ${L}/><circle cx="400" cy="112" r="34" fill="${c2}" ${L}/>` };
    case "fez": return { back: "", front: `<path d="M300 270 L320 140 L480 140 L500 270Z" fill="${c}" ${L}/><path d="M480 150 C520 170 530 230 515 270" stroke="${c2}" stroke-width="10" fill="none"/><circle cx="515" cy="276" r="12" fill="${c2}"/>` };
    case "turban": return { back: "", front: `<path d="M222 320 C190 120 610 120 578 320 C520 290 280 290 222 320Z" fill="${c}" ${L}/><path d="M240 290 C320 200 480 180 570 250 M232 250 C330 160 470 150 560 200 M300 150 C380 230 470 260 560 300" stroke="${shade(c, -0.2)}" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M380 230 C390 200 420 200 425 230 C420 260 390 260 380 230Z" fill="${c2}" ${L}/>` };
    case "conical": return { back: "", front: `<path d="M60 330 L400 40 L740 330 C600 360 200 360 60 330Z" fill="${c}" ${L}/><path d="M160 300 L400 70 M640 300 L400 70 M260 320 L400 60 M540 320 L400 60" stroke="${shade(c, -0.2)}" stroke-width="5" opacity=".6"/>` };
    case "feathers": {
      let f = "";
      const cols = h.cols || ["#d62828", "#f77f00", "#fcbf49", "#2a9d8f", "#264653"];
      for (let i = 0; i < 13; i++) {
        const a = Math.PI * (1.05 + (i / 12) * 0.9), x = 400 + Math.cos(a) * 185, y = 290 + Math.sin(a) * 120;
        const tx = 400 + Math.cos(a) * 360, ty = 290 + Math.sin(a) * 300, col = cols[i % cols.length];
        f += `<path d="M${x} ${y} Q${(x + tx) / 2 + 30} ${(y + ty) / 2} ${tx} ${ty} Q${(x + tx) / 2 - 30} ${(y + ty) / 2} ${x} ${y}Z" fill="${col}" stroke="${shade(col, -0.5)}" stroke-width="5"/>`;
      }
      return { back: f, front: `<path d="M226 300 C300 260 500 260 574 300 L570 340 C500 305 300 305 230 340Z" fill="${c2}" ${L}/><path d="M250 318 L550 318" stroke="${c}" stroke-width="10" stroke-dasharray="20 14"/>` };
    }
    case "headband": return { back: "", front: `<path d="M232 285 C300 255 500 255 568 285 L566 325 C500 295 300 295 234 325Z" fill="${c}" ${L}/><path d="M250 300 L550 300" stroke="${c2}" stroke-width="10" stroke-dasharray="14 12"/>` };
    case "headscarf": return {
      back: `<path d="M200 330 C180 90 620 90 600 330 C620 520 640 650 680 780 C520 820 280 820 120 780 C160 650 180 520 200 330Z" fill="${c}" ${L}/>`,
      front: `<path d="M236 400 C210 140 590 140 564 400 C550 300 500 250 400 248 C300 250 250 300 236 400Z" fill="${c}" ${L}/><path d="M250 330 C320 250 480 250 550 330" stroke="${c2}" stroke-width="12" fill="none" stroke-dasharray="10 14"/>`,
    };
    case "kokoshnik": return { back: `<path d="M210 320 C190 60 610 60 590 320Z" fill="${c}" ${L}/><path d="M250 300 C240 120 560 120 550 300" stroke="${c2}" stroke-width="14" fill="none"/><circle cx="400" cy="120" r="22" fill="${c2}"/>`, front: "" };
    case "beret": return { back: "", front: `<ellipse cx="390" cy="210" rx="210" ry="80" fill="${c}" ${L}/><path d="M240 250 C320 280 470 280 560 250" stroke="${shade(c, -0.25)}" stroke-width="12" fill="none"/><path d="M390 130 L398 105" stroke="${line}" stroke-width="9"/>` };
    case "widehat": return { back: "", front: `<ellipse cx="400" cy="270" rx="330" ry="62" fill="${c}" ${L}/><path d="M270 268 C270 120 530 120 530 268Z" fill="${c}" ${L}/><path d="M272 240 L528 240" stroke="${c2}" stroke-width="20"/>` };
    case "furhat": return { back: "", front: `<path d="M210 330 C180 90 620 90 590 330 C560 300 240 300 210 330Z" fill="${h.fur || "#8d6e53"}" ${L}/><path d="M250 280 C320 230 480 230 550 280" stroke="${shade(h.fur || "#8d6e53", 0.25)}" stroke-width="16" fill="none" stroke-linecap="round" opacity=".7"/><path d="M215 320 C190 420 210 470 240 500 L262 380Z M585 320 C610 420 590 470 560 500 L538 380Z" fill="${h.fur || "#8d6e53"}" ${L}/>` };
    case "tophat": return { back: "", front: `<ellipse cx="400" cy="250" rx="220" ry="40" fill="${c}" ${L}/><rect x="290" y="70" width="220" height="185" rx="12" fill="${c}" ${L}/><rect x="290" y="200" width="220" height="30" fill="${c2}"/>` };
    case "bonnet": return { back: `<path d="M200 380 C170 100 630 100 600 380 C560 320 240 320 200 380Z" fill="${c}" ${L}/>`, front: `<path d="M250 300 C320 230 480 230 550 300" stroke="${c2}" stroke-width="14" fill="none"/>` };
    case "flower": return { back: "", front: [0, 72, 144, 216, 288].map((a) => `<ellipse cx="${540 + Math.cos((a * Math.PI) / 180) * 26}" cy="${240 + Math.sin((a * Math.PI) / 180) * 26}" rx="24" ry="16" transform="rotate(${a} ${540 + Math.cos((a * Math.PI) / 180) * 26} ${240 + Math.sin((a * Math.PI) / 180) * 26})" fill="${c}" stroke="${shade(c, -0.4)}" stroke-width="4"/>`).join("") + `<circle cx="540" cy="240" r="14" fill="${c2}"/>` };
    case "crown": return { back: "", front: `<path d="M260 270 L250 170 L310 220 L350 150 L400 210 L450 150 L490 220 L550 170 L540 270Z" fill="${c2}" ${L}/><circle cx="400" cy="240" r="16" fill="${c}"/>` };
    default: return { back: "", front: "" };
  }
}

// Make the avatar match the speaker's voice, keeping the outfit's colours and style.
export function withGender(spec, g) {
  const fem = !!spec.fem;
  if (!g || (g === "f") === fem) return spec;
  const s = JSON.parse(JSON.stringify(spec));
  if (g === "m") {
    s.fem = false;
    if (["long", "braids", "bun", "bob", "ponytail"].includes(s.hair)) s.hair = "short";
    delete s.earrings;
    if (s.hat && ["flower", "kokoshnik", "bonnet", "headscarf"].includes(s.hat.type)) s.hat = s.hat.type === "headscarf" ? { type: "flatcap", color: shade(s.hat.color, -0.3) } : undefined;
    if (s.outfit && s.outfit.type === "dress") s.outfit = { ...s.outfit, type: "tunic" };
    if (s.expression === "grin") s.expression = "smile";
  } else {
    s.fem = true;
    delete s.beard; delete s.mustache;
    if (["short", "spiky", "bald"].includes(s.hair)) s.hair = "long";
    if (s.hat && ["flatcap", "tophat", "fez", "beret"].includes(s.hat.type)) delete s.hat;
    if (s.outfit && s.outfit.tie) s.outfit = { ...s.outfit, tie: undefined };
    if (s.outfit && s.outfit.type === "shirt") s.outfit = { ...s.outfit, type: "dress", color2: s.outfit.vest || s.outfit.color, trim: s.outfit.vest || "#c0392b" };
  }
  return s;
}

export function character(spec, uid = "c") {
  const skin = SKIN[spec.skin] || spec.skin || SKIN.light;
  const sl = shade(skin, -0.38);
  const hc = HAIR[spec.hairColor] || spec.hairColor || HAIR.brown, hl = shade(hc, -0.5);
  const hairStyle = spec.hair || "short";
  const H = hat(spec.hat, uid);
  const O = outfit(spec.outfit || {}, skin, uid);
  const eye = spec.eyeColor || "#3b2a20";
  const ex = spec.expression || "smile";
  const fem = !!spec.fem;
  let s = `<defs>${O.defs}<radialGradient id="cheek${uid}"><stop offset="0" stop-color="#ff7b7b" stop-opacity=".55"/><stop offset="1" stop-color="#ff7b7b" stop-opacity="0"/></radialGradient></defs>`;
  const HY = 62; // head sits lower than the drawing grid so the neck is short
  s += `<g transform="translate(0 ${HY})">` + H.back;
  if (!spec.hat || spec.hat.type !== "headscarf") s += hairBack(hairStyle, hc, hl);
  s += `</g>`;
  // neck + body
  s += `<path d="M348 560 L348 720 C370 745 430 745 452 720 L452 560Z" fill="${skin}" stroke="${sl}" stroke-width="7"/>`;
  s += `<path d="M348 610 C370 660 430 660 452 610 L452 650 C420 690 380 690 348 650Z" fill="${shade(skin, -0.18)}"/>`;
  s += O.s;
  s += `<g transform="translate(0 ${HY})">`;
  // ears
  for (const x of [252, 548]) s += `<ellipse cx="${x}" cy="400" rx="30" ry="44" fill="${skin}" stroke="${sl}" stroke-width="7"/>`;
  if (spec.earrings) for (const x of [250, 550]) s += `<circle cx="${x}" cy="456" r="13" fill="${spec.earrings}" stroke="${shade(spec.earrings, -0.4)}" stroke-width="4"/>`;
  // face
  const face = fem ? "M252 330 C252 175 548 175 548 330 C548 455 480 548 400 556 C320 548 252 455 252 330Z" : "M250 330 C250 170 550 170 550 330 C550 470 485 560 400 566 C315 560 250 470 250 330Z";
  s += `<path d="${face}" fill="${skin}" stroke="${sl}" stroke-width="8"/>`;
  s += `<path d="M270 300 C268 220 320 190 370 186" stroke="${shade(skin, 0.3)}" stroke-width="16" fill="none" stroke-linecap="round" opacity=".5"/>`;
  if (spec.facepaint) s += spec.facepaint === "lines" ? `<path d="M290 430 L350 440 M290 455 L350 462 M510 430 L450 440 M510 455 L450 462" stroke="${spec.paintColor || "#ffffff"}" stroke-width="9" stroke-linecap="round"/>` : `<path d="M300 420 C330 400 360 410 370 440" stroke="${spec.paintColor || "#c0392b"}" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M500 420 C470 400 440 410 430 440" stroke="${spec.paintColor || "#c0392b"}" stroke-width="12" fill="none" stroke-linecap="round"/>`;
  if (spec.tattoo) s += `<path d="M370 520 L370 560 M400 525 L400 568 M430 520 L430 560" stroke="#2c3e50" stroke-width="7" stroke-linecap="round"/>`;
  // eyes
  const eyeY = 385;
  for (const [x, dir] of [[335, -1], [465, 1]]) {
    const ry = ex === "sleepy" ? 11 : 21;
    s += `<ellipse cx="${x}" cy="${eyeY}" rx="31" ry="${ry}" fill="#fff" stroke="${shade(skin, -0.55)}" stroke-width="5"/>`;
    s += `<circle cx="${x + 2}" cy="${eyeY + 1}" r="${Math.min(16, ry)}" fill="${eye}"/><circle cx="${x + 2}" cy="${eyeY + 1}" r="${Math.min(8, ry - 3)}" fill="#111"/><circle cx="${x + 8}" cy="${eyeY - 6}" r="5" fill="#fff"/>`;
    s += `<path d="M${x - 36} ${eyeY - 4} C${x - 20} ${eyeY - 28} ${x + 20} ${eyeY - 28} ${x + 36} ${eyeY - 4}" stroke="#2a1d17" stroke-width="${fem ? 8 : 6}" fill="none" stroke-linecap="round"/>`;
    if (fem) s += `<path d="M${x + dir * 34} ${eyeY - 8} l${dir * 14} -10 M${x + dir * 30} ${eyeY - 14} l${dir * 10} -12" stroke="#2a1d17" stroke-width="5" stroke-linecap="round"/>`;
    const by = eyeY - 50, tilt = ex === "sad" ? dir * 10 : ex === "angry" ? -dir * 12 : ex === "smug" && dir > 0 ? -8 : 0;
    s += `<path d="M${x - 34} ${by + (dir < 0 ? -tilt : tilt) * 0.5 + 4} C${x - 10} ${by - 10} ${x + 10} ${by - 10} ${x + 34} ${by + (dir < 0 ? tilt : -tilt) * 0.5 + 4}" stroke="${spec.hair === "bald" ? shade(skin, -0.5) : shade(hc, -0.2)}" stroke-width="${fem ? 9 : 14}" fill="none" stroke-linecap="round"/>`;
  }
  if (spec.glasses) s += `<circle cx="335" cy="${eyeY}" r="46" fill="#bfe3ff" fill-opacity=".18" stroke="#1d1d1d" stroke-width="8"/><circle cx="465" cy="${eyeY}" r="46" fill="#bfe3ff" fill-opacity=".18" stroke="#1d1d1d" stroke-width="8"/><path d="M381 ${eyeY - 4} C392 ${eyeY - 14} 408 ${eyeY - 14} 419 ${eyeY - 4} M289 ${eyeY - 8} L255 ${eyeY - 14} M511 ${eyeY - 8} L545 ${eyeY - 14}" stroke="#1d1d1d" stroke-width="7" fill="none"/>`;
  // nose
  s += `<path d="M402 410 C392 440 380 455 392 466 C402 472 414 470 420 464" stroke="${shade(skin, -0.42)}" stroke-width="7" fill="none" stroke-linecap="round"/>`;
  // cheeks
  s += `<ellipse cx="305" cy="455" rx="42" ry="26" fill="url(#cheek${uid})"/><ellipse cx="495" cy="455" rx="42" ry="26" fill="url(#cheek${uid})"/>`;
  // beard (under mouth)
  if (spec.beard) s += `<path d="M258 410 C262 540 330 615 400 620 C470 615 538 540 542 410 C520 470 480 505 400 505 C320 505 280 470 258 410Z" fill="${spec.beardColor ? HAIR[spec.beardColor] || spec.beardColor : hc}" stroke="${hl}" stroke-width="6"/>`;
  // mouth
  const lip = fem ? "#c2575a" : shade(skin, -0.5);
  const my = 500;
  const mouths = {
    smile: `<path d="M352 ${my - 6} C375 ${my + 24} 425 ${my + 24} 448 ${my - 6}" stroke="${lip}" stroke-width="${fem ? 10 : 8}" fill="none" stroke-linecap="round"/>`,
    grin: `<path d="M345 ${my - 10} C370 ${my + 40} 430 ${my + 40} 455 ${my - 10}Z" fill="#7a2e2e" stroke="${shade(skin, -0.5)}" stroke-width="6"/><path d="M352 ${my - 6} L448 ${my - 6} L440 ${my + 6} L360 ${my + 6}Z" fill="#fff"/>`,
    neutral: `<path d="M362 ${my + 4} L438 ${my + 4}" stroke="${lip}" stroke-width="${fem ? 10 : 8}" stroke-linecap="round"/>`,
    sad: `<path d="M360 ${my + 14} C380 ${my - 4} 420 ${my - 4} 440 ${my + 14}" stroke="${lip}" stroke-width="8" fill="none" stroke-linecap="round"/>`,
    smug: `<path d="M360 ${my + 6} C390 ${my + 14} 420 ${my + 10} 448 ${my - 10}" stroke="${lip}" stroke-width="8" fill="none" stroke-linecap="round"/>`,
    sleepy: `<path d="M370 ${my + 2} C390 ${my + 12} 410 ${my + 12} 430 ${my + 2}" stroke="${lip}" stroke-width="7" fill="none" stroke-linecap="round"/>`,
    open: `<ellipse cx="400" cy="${my + 8}" rx="26" ry="20" fill="#7a2e2e" stroke="${shade(skin, -0.5)}" stroke-width="6"/>`,
  };
  s += mouths[ex] || mouths.smile;
  if (spec.mustache) s += `<path d="M330 ${my - 8} C350 ${my - 40} 390 ${my - 34} 400 ${my - 22} C410 ${my - 34} 450 ${my - 40} 470 ${my - 8} C440 ${my - 18} 420 ${my - 14} 400 ${my - 10} C380 ${my - 14} 360 ${my - 18} 330 ${my - 8}Z" fill="${spec.beardColor ? HAIR[spec.beardColor] || spec.beardColor : hc}" stroke="${hl}" stroke-width="5"/>`;
  // hair front + hat
  if (!spec.hat || !["headscarf", "turban", "furhat", "beanie"].includes(spec.hat.type)) s += hairFront(hairStyle, hc, hl);
  s += H.front;
  if (spec.tear) s += `<path d="M470 420 C460 445 462 460 472 462 C482 460 484 445 470 420Z" fill="#8fd3ff" stroke="#3a8fc4" stroke-width="3"/>`;
  s += `</g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="60 60 680 940">${s}</svg>`;
}

// ---------- landscapes (1920x1080) ----------
const W = 1920, H = 1080;
function ridge(r, y0, amp, rough, n = 14) {
  const pts = [];
  let y = y0;
  for (let i = 0; i <= n; i++) {
    const x = (i / n) * W;
    y = y0 - amp * (0.35 + 0.65 * r()) * (rough ? (i % 2 ? 1 : 0.55) : 1);
    pts.push([x, y]);
  }
  let d = `M0 ${H} L0 ${pts[0][1]}`;
  for (let i = 1; i < pts.length; i++) {
    const [x0, yy0] = pts[i - 1], [x1, yy1] = pts[i];
    d += rough ? ` L${x1} ${yy1}` : ` C${x0 + (x1 - x0) / 2} ${yy0} ${x0 + (x1 - x0) / 2} ${yy1} ${x1} ${yy1}`;
  }
  return { d: d + ` L${W} ${H}Z`, pts };
}

const SKIES = {
  day: ["#4a90d9", "#a9d6f5", "#e8f6ff"],
  morning: ["#7fb2e5", "#cfe6f7", "#fff1d6"],
  sunset: ["#3b3b7a", "#e0607e", "#ffc27a"],
  dusk: ["#1b2a52", "#5b4a8a", "#e9967a"],
  night: ["#060b1f", "#14244a", "#2d4a73"],
  overcast: ["#8f9aa6", "#c3cad1", "#e3e6e9"],
  arctic: ["#5c7fa8", "#b9d3ea", "#f1f6fb"],
  tropical: ["#1e88e5", "#64c4f5", "#d6f3ff"],
  desert: ["#5aa0d8", "#bfe0f2", "#fbe8c8"],
};

function tree(kind, x, y, s, col, r) {
  const trunk = "#5b3a24";
  if (kind === "pine") return `<path d="M${x} ${y - 150 * s} L${x + 46 * s} ${y - 40 * s} L${x + 22 * s} ${y - 40 * s} L${x + 58 * s} ${y + 10 * s} L${x - 58 * s} ${y + 10 * s} L${x - 22 * s} ${y - 40 * s} L${x - 46 * s} ${y - 40 * s}Z" fill="${col}"/><rect x="${x - 7 * s}" y="${y + 8 * s}" width="${14 * s}" height="${22 * s}" fill="${trunk}"/>`;
  if (kind === "snowpine") return tree("pine", x, y, s, col, r) + `<path d="M${x} ${y - 150 * s} L${x + 20 * s} ${y - 100 * s} L${x - 20 * s} ${y - 100 * s}Z M${x + 22 * s} ${y - 40 * s} L${x + 40 * s} ${y - 30 * s} L${x - 40 * s} ${y - 30 * s} L${x - 22 * s} ${y - 40 * s}Z" fill="#fff" opacity=".9"/>`;
  if (kind === "round") return `<rect x="${x - 8 * s}" y="${y - 40 * s}" width="${16 * s}" height="${70 * s}" fill="${trunk}"/><circle cx="${x}" cy="${y - 70 * s}" r="${55 * s}" fill="${col}"/><circle cx="${x - 30 * s}" cy="${y - 45 * s}" r="${38 * s}" fill="${shade(col, -0.1)}"/><circle cx="${x + 32 * s}" cy="${y - 48 * s}" r="${40 * s}" fill="${shade(col, 0.08)}"/>`;
  if (kind === "acacia") return `<path d="M${x} ${y + 20 * s} L${x - 4 * s} ${y - 60 * s} L${x - 40 * s} ${y - 110 * s} M${x - 4 * s} ${y - 60 * s} L${x + 36 * s} ${y - 115 * s}" stroke="${trunk}" stroke-width="${10 * s}" fill="none" stroke-linecap="round"/><ellipse cx="${x}" cy="${y - 122 * s}" rx="${110 * s}" ry="${26 * s}" fill="${col}"/><ellipse cx="${x - 20 * s}" cy="${y - 132 * s}" rx="${70 * s}" ry="${18 * s}" fill="${shade(col, 0.1)}"/>`;
  if (kind === "palm") {
    let f = `<path d="M${x} ${y + 20 * s} Q${x + 30 * s} ${y - 80 * s} ${x + 10 * s} ${y - 190 * s}" stroke="#7a5534" stroke-width="${14 * s}" fill="none" stroke-linecap="round"/>`;
    for (const a of [-160, -125, -90, -55, -20, 15, -200]) {
      const rad = (a * Math.PI) / 180, tx = x + 10 * s + Math.cos(rad) * 120 * s, ty = y - 190 * s + Math.sin(rad) * 60 * s + 50 * s;
      f += `<path d="M${x + 10 * s} ${y - 190 * s} Q${(x + 10 * s + tx) / 2} ${y - 250 * s} ${tx} ${ty}" stroke="${col}" stroke-width="${18 * s}" fill="none" stroke-linecap="round"/>`;
    }
    return f;
  }
  if (kind === "cypress") return `<ellipse cx="${x}" cy="${y - 80 * s}" rx="${18 * s}" ry="${95 * s}" fill="${col}"/>`;
  return "";
}

function hut(x, y, s, wall, roof) {
  return `<rect x="${x - 60 * s}" y="${y - 70 * s}" width="${120 * s}" height="${70 * s}" fill="${wall}"/><path d="M${x - 85 * s} ${y - 62 * s} L${x} ${y - 165 * s} L${x + 85 * s} ${y - 62 * s}Z" fill="${roof}"/><path d="M${x - 70 * s} ${y - 80 * s} L${x + 70 * s} ${y - 80 * s} M${x - 50 * s} ${y - 105 * s} L${x + 50 * s} ${y - 105 * s}" stroke="${shade(roof, -0.25)}" stroke-width="${5 * s}"/><rect x="${x - 15 * s}" y="${y - 45 * s}" width="${30 * s}" height="${45 * s}" fill="${shade(wall, -0.45)}"/>`;
}
function house(x, y, s, wall, roof) {
  return `<rect x="${x - 50 * s}" y="${y - 90 * s}" width="${100 * s}" height="${90 * s}" fill="${wall}"/><path d="M${x - 62 * s} ${y - 88 * s} L${x} ${y - 150 * s} L${x + 62 * s} ${y - 88 * s}Z" fill="${roof}"/><rect x="${x - 30 * s}" y="${y - 70 * s}" width="${20 * s}" height="${22 * s}" fill="#ffe8a3"/><rect x="${x + 10 * s}" y="${y - 70 * s}" width="${20 * s}" height="${22 * s}" fill="#ffe8a3"/><rect x="${x - 10 * s}" y="${y - 35 * s}" width="${20 * s}" height="${35 * s}" fill="${shade(wall, -0.5)}"/>`;
}

// preset scenes; opts: {sky, sun, seed, ...}
export function scene(name, seed = name) {
  const r = rng(seed);
  const P = PRESETS[name] || PRESETS.hills;
  const sky = SKIES[P.sky] || SKIES.day;
  let s = `<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${sky[0]}"/><stop offset=".6" stop-color="${sky[1]}"/><stop offset="1" stop-color="${sky[2]}"/></linearGradient>
  <radialGradient id="sun"><stop offset="0" stop-color="#fffbe6"/><stop offset=".35" stop-color="#fff0b3" stop-opacity=".9"/><stop offset="1" stop-color="#fff0b3" stop-opacity="0"/></radialGradient>
  <linearGradient id="haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${sky[2]}" stop-opacity="0"/><stop offset="1" stop-color="${sky[2]}" stop-opacity=".55"/></linearGradient>
  <linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${P.water || "#3a86c8"}"/><stop offset="1" stop-color="${shade(P.water || "#3a86c8", -0.35)}"/></linearGradient>
  <linearGradient id="vig" x1="0" y1="0" x2="0" y2="1"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient></defs>`;
  s += `<rect width="${W}" height="${H}" fill="url(#sky)"/>`;
  if (["night", "dusk"].includes(P.sky)) for (let i = 0; i < 160; i++) s += `<circle cx="${r() * W}" cy="${r() * H * 0.55}" r="${r() * 2.2 + 0.4}" fill="#fff" opacity="${0.3 + r() * 0.7}"/>`;
  if (P.aurora) s += `<path d="M-50 260 C300 120 600 330 900 200 C1200 70 1500 260 1980 140 L1980 300 C1500 420 1200 230 900 360 C600 480 300 280 -50 420Z" fill="#3cf2a0" opacity=".28"/><path d="M-50 200 C400 90 700 260 1000 150 C1300 40 1600 190 1980 90 L1980 170 C1600 270 1300 120 1000 230 C700 340 400 170 -50 290Z" fill="#7cf7d4" opacity=".22"/>`;
  const sunX = P.sunX ?? 1500, sunY = P.sunY ?? 230;
  if (P.sun !== false) s += P.sky === "night" ? `<circle cx="${sunX}" cy="${sunY}" r="60" fill="#f4f1e1"/><circle cx="${sunX + 22}" cy="${sunY - 10}" r="54" fill="${sky[0]}" opacity=".0"/>` : `<circle cx="${sunX}" cy="${sunY}" r="260" fill="url(#sun)"/><circle cx="${sunX}" cy="${sunY}" r="70" fill="#fffdf2"/>`;
  // clouds
  for (let i = 0; i < (P.clouds ?? 5); i++) {
    const cx = r() * W, cy = 90 + r() * 260, k = 0.6 + r() * 0.9, op = P.sky === "overcast" ? 0.85 : 0.8;
    const col = P.sky === "sunset" ? "#ffd6c4" : P.sky === "dusk" ? "#b28cb8" : "#ffffff";
    s += `<g opacity="${op}" fill="${col}"><ellipse cx="${cx}" cy="${cy}" rx="${130 * k}" ry="${34 * k}"/><ellipse cx="${cx - 50 * k}" cy="${cy - 20 * k}" rx="${60 * k}" ry="${40 * k}"/><ellipse cx="${cx + 30 * k}" cy="${cy - 32 * k}" rx="${70 * k}" ry="${48 * k}"/></g>`;
  }
  for (const L of P.layers) s += layer(L, r, sky);
  s += `<rect width="${W}" height="${H}" fill="url(#vig)"/>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice">${s}</svg>`;
}

function layer(L, r, sky) {
  const [type, a = {}] = L;
  const fade = (c, t) => mix(c, sky[2], t);
  let s = "";
  switch (type) {
    case "mountains": {
      const { d, pts } = ridge(r, a.y ?? 640, a.h ?? 380, true, a.n ?? 9);
      const col = fade(a.color || "#6b7f99", a.far ?? 0.35);
      s += `<path d="${d}" fill="${col}"/>`;
      if (a.snow) for (let i = 1; i < pts.length - 1; i++) {
        const [x, y] = pts[i];
        if (y < (a.y ?? 640) - (a.h ?? 380) * 0.55) s += `<path d="M${x} ${y} L${x + 60} ${y + 70} L${x + 30} ${y + 60} L${x} ${y + 82} L${x - 28} ${y + 58} L${x - 60} ${y + 70}Z" fill="${fade("#ffffff", a.far ?? 0.2)}"/>`;
      }
      s += `<path d="${d}" fill="url(#haze)"/>`;
      break;
    }
    case "hills": { const { d } = ridge(r, a.y ?? 760, a.h ?? 140, false, a.n ?? 6); s += `<path d="${d}" fill="${fade(a.color || "#6fa85a", a.far ?? 0)}"/>`; break; }
    case "mesa": {
      const y = a.y ?? 700, col = a.color || "#c46a3b";
      for (const [x, w, h] of [[160, 380, 230], [820, 260, 300], [1380, 470, 210]]) s += `<path d="M${x} ${y} L${x + 40} ${y - h} L${x + w - 40} ${y - h} L${x + w} ${y}Z" fill="${fade(col, a.far ?? 0.15)}"/><path d="M${x + 40} ${y - h} L${x + w - 40} ${y - h} L${x + w - 30} ${y - h + 28} L${x + 30} ${y - h + 28}Z" fill="${shade(col, 0.15)}"/><path d="M${x + 20} ${y - h * 0.45} L${x + w - 20} ${y - h * 0.45}" stroke="${shade(col, -0.18)}" stroke-width="10"/>`;
      s += `<rect y="${y}" width="${W}" height="${H - y}" fill="${a.ground || "#e2a66b"}"/>`;
      break;
    }
    case "dunes": { for (let k = 0; k < 3; k++) { const { d } = ridge(r, (a.y ?? 760) + k * 90, 90, false, 5); s += `<path d="${d}" fill="${shade(a.color || "#e7b97a", -k * 0.08)}"/>`; } break; }
    case "sea": {
      const y = a.y ?? 690;
      s += `<rect y="${y}" width="${W}" height="${H - y}" fill="url(#water)"/>`;
      for (let i = 0; i < 40; i++) { const yy = y + 12 + r() * (H - y); s += `<path d="M${r() * W} ${yy} l${40 + r() * 80} 0" stroke="#ffffff" stroke-opacity="${0.15 + r() * 0.25}" stroke-width="4" stroke-linecap="round"/>`; }
      break;
    }
    case "beach": s += `<path d="M0 ${a.y ?? 900} C500 ${(a.y ?? 900) - 60} 1300 ${(a.y ?? 900) - 20} 1920 ${(a.y ?? 900) - 90} L1920 1080 L0 1080Z" fill="${a.color || "#f1d9a6"}"/><path d="M0 ${(a.y ?? 900) - 6} C500 ${(a.y ?? 900) - 66} 1300 ${(a.y ?? 900) - 26} 1920 ${(a.y ?? 900) - 96}" stroke="#fff" stroke-width="10" opacity=".7" fill="none"/>`; break;
    case "ground": s += `<rect y="${a.y ?? 860}" width="${W}" height="${H}" fill="${a.color || "#7cae5b"}"/>`; break;
    case "ice": for (let i = 0; i < 6; i++) { const x = r() * W, y = (a.y ?? 720) + r() * 40, w = 80 + r() * 160; s += `<path d="M${x} ${y} L${x + w * 0.2} ${y - 50 - r() * 60} L${x + w * 0.7} ${y - 40 - r() * 50} L${x + w} ${y}Z" fill="#eaf6ff" stroke="#b9dcf2" stroke-width="4"/>`; } break;
    case "trees": {
      const n = a.n ?? 12;
      const items = [];
      for (let i = 0; i < n; i++) items.push([r() * W, (a.y ?? 860) + r() * (a.spread ?? 60), (a.s ?? 1) * (0.7 + r() * 0.6)]);
      items.sort((p, q) => p[1] - q[1]);
      for (const [x, y, k] of items) s += tree(a.kind || "pine", x, y, k, fade(a.color || "#2f6b3a", a.far ?? 0), r);
      break;
    }
    case "huts": for (let i = 0; i < (a.n ?? 4); i++) s += hut(200 + i * (1600 / (a.n ?? 4)) + r() * 120, (a.y ?? 860) + r() * 30, (a.s ?? 1.2) * (0.8 + r() * 0.4), a.wall || "#b5835a", a.roof || "#d8b56a"); break;
    case "houses": {
      const cols = a.cols || ["#f4e1c1", "#e8b4a0", "#f7d488", "#cfe1e8", "#f2f2f2"];
      for (let i = 0; i < (a.n ?? 9); i++) s += house(120 + i * (1700 / (a.n ?? 9)) + r() * 60, (a.y ?? 860) + r() * 20, (a.s ?? 1.1) * (0.85 + r() * 0.3), cols[i % cols.length], a.roof || "#b5452f");
      break;
    }
    case "skyline": {
      const y = a.y ?? 820;
      for (let x = 0; x < W; ) { const w = 60 + r() * 110, h = 120 + r() * 340; s += `<rect x="${x}" y="${y - h}" width="${w}" height="${h + 300}" fill="${fade(a.color || "#5b6b82", a.far ?? 0.2)}"/>`; for (let wy = y - h + 20; wy < y; wy += 34) for (let wx = x + 12; wx < x + w - 14; wx += 26) if (r() > 0.45) s += `<rect x="${wx}" y="${wy}" width="12" height="16" fill="#ffe9a8" opacity=".55"/>`; x += w + 6; }
      break;
    }
    case "church": { const x = a.x ?? 1250, y = a.y ?? 800; s += `<rect x="${x}" y="${y - 260}" width="70" height="260" fill="${a.color || "#e9dcc4"}"/><path d="M${x - 8} ${y - 258} L${x + 35} ${y - 380} L${x + 78} ${y - 258}Z" fill="${a.roof || "#8a4a32"}"/>`; break; }
    case "tipis": for (let i = 0; i < (a.n ?? 4); i++) { const x = 300 + i * 400 + r() * 100, y = (a.y ?? 860), k = 0.9 + r() * 0.4; s += `<path d="M${x} ${y - 220 * k} L${x + 110 * k} ${y} L${x - 110 * k} ${y}Z" fill="#e6d3b1" stroke="#9c7b50" stroke-width="5"/><path d="M${x - 20 * k} ${y - 260 * k} L${x + 20 * k} ${y - 180 * k} M${x + 20 * k} ${y - 260 * k} L${x - 20 * k} ${y - 180 * k}" stroke="#6b4a2b" stroke-width="7"/><path d="M${x - 30 * k} ${y} L${x} ${y - 70 * k} L${x + 30 * k} ${y}Z" fill="#6b4a2b"/><path d="M${x - 70 * k} ${y - 80 * k} L${x + 70 * k} ${y - 80 * k}" stroke="#b5452f" stroke-width="10"/>`; } break;
    case "river": s += `<path d="M700 ${a.y ?? 760} C800 850 600 950 900 1080 L1300 1080 C1000 950 1100 850 820 ${a.y ?? 760}Z" fill="url(#water)" opacity=".95"/>`; break;
    case "boat": { const x = a.x ?? 1300, y = a.y ?? 760; s += `<path d="M${x - 90} ${y} L${x + 90} ${y} L${x + 60} ${y + 30} L${x - 60} ${y + 30}Z" fill="#7a4a2a"/><path d="M${x} ${y - 140} L${x} ${y} M${x} ${y - 135} L${x + 70} ${y - 20} L${x} ${y - 20}" stroke="#4a3020" stroke-width="5" fill="#f4efe2"/>`; break; }
    case "grass": for (let i = 0; i < (a.n ?? 120); i++) { const x = r() * W, y = (a.y ?? 900) + r() * (H - (a.y ?? 900)); s += `<path d="M${x} ${y} l-6 -28 M${x} ${y} l2 -34 M${x} ${y} l9 -26" stroke="${shade(a.color || "#5c9a45", r() * 0.3 - 0.15)}" stroke-width="4" stroke-linecap="round"/>`; } break;
    case "flowers": for (let i = 0; i < (a.n ?? 70); i++) { const x = r() * W, y = (a.y ?? 920) + r() * (H - (a.y ?? 920)); s += `<circle cx="${x}" cy="${y}" r="${5 + r() * 4}" fill="${(a.cols || ["#f25f5c", "#ffe066", "#ffffff", "#c77dff"])[i % 4]}"/>`; } break;
    case "fence": { const y = a.y ?? 900; s += `<path d="M0 ${y} L1920 ${y - 20} M0 ${y + 30} L1920 ${y + 10}" stroke="#8a6a4a" stroke-width="8"/>`; for (let x = 20; x < W; x += 110) s += `<rect x="${x}" y="${y - 40 - (x / W) * 20}" width="12" height="90" fill="#7a5a3a"/>`; break; }
    case "stonewall": { const y = a.y ?? 880; for (let x = -20; x < W; x += 52) for (let k = 0; k < 2; k++) s += `<ellipse cx="${x + (k ? 26 : 0)}" cy="${y - k * 26 - (x / W) * 30}" rx="30" ry="16" fill="${shade("#9a9a92", r() * 0.3 - 0.15)}" stroke="#6b6b65" stroke-width="3"/>`; break; }
    case "temple": { const x = a.x ?? 1450, y = a.y ?? 820; for (let k = 0; k < 3; k++) s += `<path d="M${x - 150 + k * 30} ${y - k * 90} L${x + 150 - k * 30} ${y - k * 90} L${x + 110 - k * 30} ${y - k * 90 - 30} L${x - 110 + k * 30} ${y - k * 90 - 30}Z" fill="#7a2d26"/><rect x="${x - 100 + k * 30}" y="${y - k * 90 - 2}" width="${200 - k * 60}" height="10" fill="#3a2a22"/>`; s += `<rect x="${x - 90}" y="${y}" width="180" height="60" fill="#b5452f"/>`; break; }
  }
  return s;
}

export const PRESETS = {
  hills: { sky: "day", layers: [["mountains", { y: 640, h: 240, color: "#7f9bb5", far: 0.45 }], ["hills", { y: 760, h: 150, color: "#86b86a" }], ["hills", { y: 880, h: 120, color: "#5f9a4a" }], ["trees", { kind: "round", n: 10, y: 850, color: "#3f7d3a" }], ["grass", { y: 930 }]] },
  baltic: { sky: "morning", water: "#4f7fa8", layers: [["sea", { y: 700 }], ["dunes", { y: 860, color: "#e9d7b0" }], ["trees", { kind: "pine", n: 18, y: 860, s: 1.1, color: "#2e5a3c", spread: 40 }], ["grass", { y: 960, color: "#9cae6a", n: 80 }]] },
  fuego: { sky: "overcast", water: "#3f6f8f", clouds: 7, layers: [["mountains", { y: 700, h: 360, color: "#5d6f80", snow: true, far: 0.3 }], ["sea", { y: 760 }], ["hills", { y: 930, h: 80, color: "#5b7a4a" }], ["trees", { kind: "round", n: 8, y: 930, color: "#3d5f38", s: 0.8 }], ["boat", { x: 1250, y: 800 }]] },
  alaska: { sky: "arctic", water: "#4d7ea6", layers: [["mountains", { y: 680, h: 420, color: "#6c819a", snow: true, far: 0.25 }], ["sea", { y: 760 }], ["ice", { y: 790 }], ["hills", { y: 940, h: 70, color: "#6d7f55" }], ["trees", { kind: "snowpine", n: 10, y: 960, color: "#2e4d3a" }]] },
  adriatic: { sky: "day", water: "#2f8fbf", layers: [["hills", { y: 650, h: 160, color: "#93a37a", far: 0.35 }], ["sea", { y: 700 }], ["houses", { y: 960, n: 9, cols: ["#f2e3c6", "#f0d0b0", "#e9c9a0", "#f7efe0"], roof: "#c0563a" }], ["church", { x: 1500, y: 960 }], ["trees", { kind: "cypress", n: 5, y: 980, color: "#2f5a35" }]] },
  andaman: { sky: "tropical", water: "#1fa3b8", sunX: 400, layers: [["hills", { y: 700, h: 120, color: "#3e8a4a", far: 0.3 }], ["sea", { y: 720 }], ["beach", { y: 960 }], ["trees", { kind: "palm", n: 6, y: 950, color: "#2f7d3a", s: 1.3 }]] },
  kola: { sky: "night", aurora: true, sunX: 1650, sunY: 170, layers: [["mountains", { y: 720, h: 200, color: "#2f3d55", far: 0.15 }], ["ground", { y: 860, color: "#dfe8f1" }], ["trees", { kind: "snowpine", n: 14, y: 870, color: "#1f3a33", spread: 50 }]] },
  himalaya: { sky: "day", layers: [["mountains", { y: 620, h: 460, color: "#7d8fa8", snow: true, far: 0.3, n: 8 }], ["hills", { y: 820, h: 180, color: "#5e8f4c" }], ["trees", { kind: "pine", n: 14, y: 880, color: "#2d5b36" }], ["grass", { y: 950, color: "#6a9b4c" }]] },
  grassland: { sky: "morning", layers: [["mountains", { y: 700, h: 160, color: "#8aa2b5", far: 0.5 }], ["hills", { y: 820, h: 100, color: "#9bbf6a" }], ["trees", { kind: "round", n: 7, y: 860, color: "#4a7d3a" }], ["grass", { y: 900, color: "#7aa64e", n: 160 }], ["flowers", { y: 940 }]] },
  oklahoma: { sky: "sunset", sunX: 1450, sunY: 560, layers: [["hills", { y: 800, h: 60, color: "#7a6a4a", far: 0.2 }], ["ground", { y: 840, color: "#a88f5a" }], ["trees", { kind: "round", n: 6, y: 850, color: "#4c5e35", s: 0.7 }], ["grass", { y: 900, color: "#b39a5c", n: 140 }]] },
  sierra: { sky: "day", layers: [["mountains", { y: 640, h: 380, color: "#8a9ab0", snow: true, far: 0.35 }], ["hills", { y: 800, h: 160, color: "#b5a66a" }], ["trees", { kind: "round", n: 9, y: 860, color: "#5c7a3a", s: 0.9 }], ["grass", { y: 920, color: "#c2a860", n: 120 }]] },
  patagonia: { sky: "overcast", clouds: 8, layers: [["mountains", { y: 640, h: 300, color: "#7a8696", snow: true, far: 0.4 }], ["hills", { y: 800, h: 80, color: "#b9a77a" }], ["ground", { y: 860, color: "#c7b583" }], ["grass", { y: 880, color: "#a69561", n: 200 }]] },
  alps: { sky: "day", layers: [["mountains", { y: 620, h: 480, color: "#7d8ea6", snow: true, far: 0.25, n: 8 }], ["hills", { y: 820, h: 160, color: "#6fae55" }], ["houses", { y: 900, n: 5, cols: ["#f4efe2", "#e6d2b5"], roof: "#6b4a32", s: 1 }], ["trees", { kind: "pine", n: 10, y: 920, color: "#2f6235" }], ["flowers", { y: 960, n: 40 }]] },
  faroe: { sky: "overcast", water: "#3f6a85", clouds: 9, layers: [["mountains", { y: 700, h: 300, color: "#5f7a5c", far: 0.25, n: 6 }], ["sea", { y: 720 }], ["hills", { y: 900, h: 120, color: "#4f8a45" }], ["houses", { y: 940, n: 4, cols: ["#c0392b", "#f2f2f2", "#2c3e50", "#f1c40f"], roof: "#2f3d2a", s: 0.9 }], ["grass", { y: 960, color: "#4c8a40" }]] },
  forest: { sky: "morning", layers: [["hills", { y: 700, h: 120, color: "#5e8a6a", far: 0.45 }], ["trees", { kind: "pine", n: 30, y: 760, s: 0.8, color: "#3a6b48", far: 0.25, spread: 40 }], ["hills", { y: 880, h: 60, color: "#5a8f45" }], ["houses", { y: 930, n: 4, cols: ["#f4efe2", "#e9d8b5"], roof: "#8a3d2a" }], ["trees", { kind: "round", n: 6, y: 980, color: "#3f7a38" }]] },
  istanbul: { sky: "sunset", water: "#5a6fa0", sunX: 500, sunY: 520, layers: [["skyline", { y: 720, color: "#6a5a7a", far: 0.3 }], ["sea", { y: 720 }], ["boat", { x: 1400, y: 820 }]] },
  dalarna: { sky: "morning", water: "#4a7aa0", layers: [["hills", { y: 640, h: 140, color: "#3e6b4c", far: 0.4 }], ["trees", { kind: "pine", n: 26, y: 690, s: 0.7, color: "#2f5a3c", far: 0.2, spread: 30 }], ["sea", { y: 720 }], ["ground", { y: 900, color: "#6f9a4a" }], ["houses", { y: 930, n: 4, cols: ["#9b2d20"], roof: "#3a3a3a", s: 1.1 }]] },
  village: { sky: "day", layers: [["hills", { y: 700, h: 140, color: "#8fae7a", far: 0.4 }], ["hills", { y: 820, h: 80, color: "#7aa65a" }], ["houses", { y: 900, n: 7, cols: ["#f4efe2", "#f2d8b8", "#e8e2d0"], roof: "#a8442f" }], ["church", { x: 1100, y: 900, color: "#f0e8d8" }], ["fence", { y: 960 }]] },
  moorland: { sky: "overcast", clouds: 8, layers: [["hills", { y: 720, h: 140, color: "#7a8a5a", far: 0.35 }], ["hills", { y: 860, h: 100, color: "#6a7f45" }], ["stonewall", { y: 960 }], ["grass", { y: 960, color: "#7b8a4a" }]] },
  steppe: { sky: "day", layers: [["hills", { y: 760, h: 80, color: "#a7b06a", far: 0.3 }], ["ground", { y: 820, color: "#b9b56e" }], ["houses", { y: 860, n: 5, cols: ["#f4efe2", "#cfe1e8"], roof: "#4a6fa5", s: 0.9 }], ["grass", { y: 880, color: "#9aa458", n: 160 }]] },
  greenland: { sky: "arctic", water: "#2f6f9a", layers: [["mountains", { y: 680, h: 300, color: "#7a8ea6", snow: true, far: 0.2 }], ["sea", { y: 720 }], ["ice", { y: 760 }], ["houses", { y: 940, n: 5, cols: ["#c0392b", "#2980b9", "#f1c40f", "#27ae60"], roof: "#2c2c2c", s: 0.9 }]] },
  jersey: { sky: "day", water: "#2c8fb5", layers: [["sea", { y: 660 }], ["hills", { y: 820, h: 180, color: "#7aa65a" }], ["houses", { y: 880, n: 4, cols: ["#e9dcc4", "#d8c6a3"], roof: "#5a5a5a" }], ["flowers", { y: 940, n: 60, cols: ["#ffe066", "#ffffff", "#f25f5c", "#ffe066"] }]] },
  abstract: { sky: "dusk", sun: false, layers: [["hills", { y: 820, h: 160, color: "#3a3a6a", far: 0.2 }], ["hills", { y: 930, h: 100, color: "#2a2a50" }]] },
  savanna: { sky: "desert", sunX: 1500, layers: [["mountains", { y: 720, h: 140, color: "#9a8a7a", far: 0.5 }], ["ground", { y: 800, color: "#d5b16a" }], ["trees", { kind: "acacia", n: 5, y: 830, color: "#6a8a3a", s: 1.1, spread: 80 }], ["huts", { y: 960, n: 3, wall: "#b98a5a", roof: "#d8b56a" }], ["grass", { y: 900, color: "#c9a24f", n: 140 }]] },
  kalahari: { sky: "desert", sunX: 400, layers: [["dunes", { y: 760, color: "#d9a066" }], ["trees", { kind: "acacia", n: 3, y: 860, color: "#6d7f3a", s: 1.2 }], ["grass", { y: 940, color: "#b8934a", n: 60 }]] },
  canary: { sky: "day", water: "#2a7fb8", layers: [["mountains", { y: 640, h: 360, color: "#6f8a5a", far: 0.2, n: 7 }], ["sea", { y: 760 }], ["hills", { y: 900, h: 160, color: "#7d6a4a" }], ["houses", { y: 960, n: 4, cols: ["#ffffff", "#f4efe2"], roof: "#b5452f", s: 0.8 }]] },
  caucasus: { sky: "day", layers: [["mountains", { y: 650, h: 460, color: "#6f7f99", snow: true, far: 0.25, n: 7 }], ["hills", { y: 820, h: 150, color: "#5f8f4a" }], ["trees", { kind: "pine", n: 12, y: 880, color: "#2f5a35" }], ["houses", { y: 950, n: 3, cols: ["#d8c6a3", "#c9b28a"], roof: "#6a4a3a" }]] },
  bougainville: { sky: "tropical", water: "#1d8fb0", layers: [["mountains", { y: 680, h: 300, color: "#2f6a45", far: 0.3, n: 6 }], ["sea", { y: 760 }], ["beach", { y: 940 }], ["trees", { kind: "palm", n: 5, y: 960, color: "#2a7a3a", s: 1.4 }]] },
  amazon: { sky: "tropical", water: "#7a6a3a", sunX: 1600, layers: [["trees", { kind: "round", n: 30, y: 700, s: 1.0, color: "#2f6a3a", far: 0.3, spread: 30 }], ["river", { y: 720 }], ["trees", { kind: "round", n: 14, y: 980, s: 1.5, color: "#245a30", spread: 60 }], ["huts", { y: 940, n: 2, wall: "#8a6a3a", roof: "#c9a85a", s: 1 }]] },
  hongkong: { sky: "dusk", water: "#2a3a6a", sunX: 1550, sunY: 420, layers: [["mountains", { y: 640, h: 180, color: "#3a3a5a", far: 0.3 }], ["skyline", { y: 760, color: "#40476a", far: 0.1 }], ["sea", { y: 760 }], ["boat", { x: 600, y: 860 }]] },
  tbilisi: { sky: "sunset", sunX: 300, sunY: 500, layers: [["mountains", { y: 640, h: 260, color: "#6a5a7a", far: 0.35 }], ["hills", { y: 820, h: 140, color: "#6a7a4a" }], ["houses", { y: 920, n: 8, cols: ["#f2d8b8", "#e8b4a0", "#d9c6a0", "#f7efe0"], roof: "#9a3a2a" }], ["church", { x: 1350, y: 860, color: "#d8c6a0", roof: "#7a5a3a" }]] },
  prague: { sky: "morning", water: "#4a6f8f", layers: [["houses", { y: 720, n: 12, cols: ["#f2e3c6", "#f0d0b0", "#e9c9a0", "#f7efe0", "#d6e2e8"], roof: "#b5452f", s: 1.2 }], ["church", { x: 700, y: 720, color: "#7a7a7a", roof: "#3a5a4a" }], ["church", { x: 1250, y: 720, color: "#7a7a7a", roof: "#3a5a4a" }], ["sea", { y: 740 }], ["stonewall", { y: 940 }]] },
  copenhagen: { sky: "day", water: "#2f6f9a", layers: [["houses", { y: 720, n: 11, cols: ["#e74c3c", "#f1c40f", "#3498db", "#e67e22", "#2ecc71", "#f5f5f5"], roof: "#4a3a32", s: 1.3 }], ["sea", { y: 740 }], ["boat", { x: 900, y: 830 }], ["boat", { x: 1500, y: 860 }]] },
  bella: { sky: "overcast", water: "#3a6a7a", clouds: 6, layers: [["mountains", { y: 660, h: 420, color: "#4f6a6a", far: 0.2, snow: true, n: 7 }], ["trees", { kind: "pine", n: 30, y: 760, s: 0.8, color: "#2a4a3a", far: 0.15, spread: 30 }], ["sea", { y: 780 }], ["trees", { kind: "pine", n: 6, y: 1000, s: 1.5, color: "#1f3a2c" }]] },
  wales: { sky: "overcast", clouds: 7, layers: [["mountains", { y: 680, h: 260, color: "#6a7a6a", far: 0.3, n: 6 }], ["hills", { y: 830, h: 120, color: "#5a9a4a" }], ["stonewall", { y: 930 }], ["grass", { y: 950, color: "#4f8f3a" }]] },
  hawaii: { sky: "tropical", water: "#1a9ec0", sunX: 1550, layers: [["mountains", { y: 680, h: 320, color: "#3a7a4a", far: 0.25, n: 6 }], ["sea", { y: 740 }], ["beach", { y: 950 }], ["trees", { kind: "palm", n: 4, y: 960, color: "#2a8a3a", s: 1.5 }]] },
  arabia: { sky: "desert", sunX: 1550, layers: [["dunes", { y: 740, color: "#e3b26e" }], ["houses", { y: 880, n: 4, cols: ["#e9d4a8", "#dcc394"], roof: "#c9a874", s: 1 }], ["trees", { kind: "palm", n: 4, y: 920, color: "#3a7a3a", s: 1.1 }]] },
  zagros: { sky: "day", layers: [["mountains", { y: 640, h: 420, color: "#9a7d62", far: 0.3, n: 8 }], ["hills", { y: 820, h: 140, color: "#b39a6a" }], ["ground", { y: 900, color: "#a8925f" }], ["tipis", { y: 960, n: 2 }], ["grass", { y: 920, color: "#9a8a4a", n: 90 }]] },
  caspian: { sky: "overcast", water: "#4a7a8a", clouds: 7, layers: [["mountains", { y: 640, h: 300, color: "#4f7a5a", far: 0.3, n: 7 }], ["trees", { kind: "round", n: 26, y: 720, s: 0.8, color: "#3a6b3f", far: 0.15, spread: 30 }], ["sea", { y: 760 }], ["beach", { y: 960, color: "#d9cba6" }]] },
  tuscany: { sky: "morning", layers: [["hills", { y: 700, h: 160, color: "#a7b77a", far: 0.35 }], ["hills", { y: 820, h: 120, color: "#8fae5a" }], ["trees", { kind: "cypress", n: 12, y: 860, color: "#2f5a35", s: 1.1, spread: 60 }], ["church", { x: 1450, y: 870, color: "#e9dcc4", roof: "#b5452f" }], ["grass", { y: 950, color: "#7a9a4a" }]] },
  // ranking backdrop is a CSS gradient, not a scene
};

// ---------- meme ("wojak-like") style ----------
// Thin black ink lines, flat colours, small tired eyes with bags, minimal mouth: the look of
// "X languages be like" channels, drawn from scratch (no copied artwork).
const INK = "#1b1b1b";
export function memeCharacter(spec, uid = "m") {
  const skin = SKIN[spec.skin] || spec.skin || SKIN.light;
  const hc = HAIR[spec.hairColor] || spec.hairColor || HAIR.brown;
  const fem = !!spec.fem;
  const H = hat(spec.hat, uid);
  const O = outfit(spec.outfit || {}, skin, uid);
  const ink = (s) => s.replace(/stroke="#[0-9a-fA-F]{6}"/g, `stroke="${INK}"`).replace(/stroke-width="(\d+(\.\d+)?)"/g, (m, w) => `stroke-width="${Math.min(+w, 5)}"`);
  let s = `<defs>${O.defs}</defs>`;
  const HY = 62;
  s += `<g transform="translate(0 ${HY})">` + ink(H.back);
  if (!spec.hat || spec.hat.type !== "headscarf") s += ink(hairBack(spec.hair || "short", hc, INK));
  s += `</g>`;
  s += `<path d="M352 560 L350 720 C372 742 428 742 450 720 L448 560Z" fill="${skin}" stroke="${INK}" stroke-width="4"/>`;
  s += ink(O.s).replace(/opacity="\.45"/g, 'opacity="0"');
  s += `<g transform="translate(0 ${HY})">`;
  // ear + head: slightly lopsided wojak skull, long jaw
  s += `<path d="M262 380 C236 372 232 430 262 444" fill="${skin}" stroke="${INK}" stroke-width="4"/><path d="M270 405 C258 405 258 425 268 428" stroke="${INK}" stroke-width="3" fill="none"/>`;
  const head = fem
    ? "M268 330 C262 205 360 168 420 172 C500 178 548 240 544 330 C542 420 520 500 470 540 C440 562 380 566 350 548 C300 520 274 440 268 330Z"
    : "M262 320 C252 200 360 160 425 166 C510 174 552 240 548 330 C546 430 520 510 468 548 C436 570 372 574 342 556 C292 528 268 440 262 320Z";
  s += `<path d="${head}" fill="${skin}" stroke="${INK}" stroke-width="4.5"/>`;
  if (spec.facepaint === "lines") s += `<path d="M300 440 L345 446 M300 462 L345 467 M500 440 L455 446 M500 462 L455 467" stroke="${spec.paintColor || "#fff"}" stroke-width="7" stroke-linecap="round"/>`;
  // eyes: small, half-lidded, with bags
  const ex = spec.expression || "neutral";
  for (const [x, d] of [[352, -1], [462, 1]]) {
    s += `<path d="M${x - 26} ${386} C${x - 12} ${374} ${x + 12} ${374} ${x + 26} ${386} C${x + 12} ${394} ${x - 12} ${394} ${x - 26} ${386}Z" fill="#fff" stroke="${INK}" stroke-width="3"/>`;
    s += `<circle cx="${x + 3}" cy="${385}" r="6.5" fill="${INK}"/>`;
    s += `<path d="M${x - 30} ${381} C${x - 12} ${368} ${x + 14} ${368} ${x + 30} ${381}" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round"/>`;
    s += `<path d="M${x - 18} ${404} C${x - 6} ${410} ${x + 8} ${410} ${x + 18} ${403}" stroke="${INK}" stroke-width="2" fill="none" opacity=".55"/>`;
    if (fem) s += `<path d="M${x + d * 26} ${379} l${d * 10} -7" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>`;
    const tilt = ex === "sad" ? d * 8 : ex === "angry" ? -d * 8 : 0;
    s += `<path d="M${x - 28} ${352 - (d < 0 ? -tilt : tilt)} C${x - 8} ${344} ${x + 8} ${344} ${x + 28} ${352 + (d < 0 ? -tilt : tilt)}" stroke="${spec.hair === "bald" ? INK : shade(hc, -0.3)}" stroke-width="${fem ? 4 : 7}" fill="none" stroke-linecap="round"/>`;
  }
  // nose: one angular wojak stroke
  s += `<path d="M410 398 L398 452 L420 458" stroke="${INK}" stroke-width="3.5" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`;
  if (spec.beard) s += `<path d="M300 450 C306 540 360 590 410 590 C470 588 520 530 528 450 C506 500 470 516 412 516 C356 516 318 498 300 450Z" fill="${HAIR[spec.beardColor] || spec.beardColor || hc}" stroke="${INK}" stroke-width="3"/>`;
  if (spec.mustache) s += `<path d="M366 486 C384 470 410 474 414 482 C420 474 446 470 462 486 C442 484 426 488 414 492 C402 488 386 484 366 486Z" fill="${HAIR[spec.beardColor] || spec.beardColor || hc}" stroke="${INK}" stroke-width="2.5"/>`;
  const my = 505;
  s += ex === "grin" || ex === "smile"
    ? `<path d="M380 ${my} C398 ${my + 10} 430 ${my + 10} 446 ${my - 2}" stroke="${fem ? "#a0454a" : INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>`
    : ex === "sad" ? `<path d="M382 ${my + 6} C400 ${my - 2} 428 ${my - 2} 444 ${my + 6}" stroke="${INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>`
    : `<path d="M384 ${my + 2} L442 ${my}" stroke="${fem ? "#a0454a" : INK}" stroke-width="3.5" stroke-linecap="round"/>`;
  if (spec.earrings) s += `<circle cx="258" cy="452" r="9" fill="${spec.earrings}" stroke="${INK}" stroke-width="2"/>`;
  if (spec.glasses) s += `<circle cx="352" cy="386" r="40" fill="none" stroke="${INK}" stroke-width="5"/><circle cx="462" cy="386" r="40" fill="none" stroke="${INK}" stroke-width="5"/><path d="M392 384 L422 384" stroke="${INK}" stroke-width="5"/>`;
  if (!spec.hat || !["headscarf", "turban", "furhat", "beanie"].includes(spec.hat.type)) s += ink(hairFront(spec.hair || "short", hc, INK)).replace(/stroke="[^"]*" stroke-width="12" fill="none" stroke-linecap="round" opacity="\.7"/g, 'stroke="none"');
  s += ink(H.front);
  s += `</g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="60 60 680 940">${s}</svg>`;
}
