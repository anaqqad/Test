// Long-form documentary renderer, v4 (Malta v4: shot-based edit). v3 stays on longform3.mjs, v2 on longform.mjs.
// v4 adds: every line is cut into `shots` (no shot may run longer than 5 s; checked and written to shots_<tag>.json),
// a 3D Mediterranean table (one shared scene, objects placed on it), an investigation board (cards pinned as evidence
// arrives, red string only between evidence and what it supports, claims that rewrite themselves), a document desk
// (port of the WWII Frontlines DocDesk3D: page on a desk, focus band, highlighter), typography driven by the real
// recording's loudness envelope, pillarboxed vertical footage, STAND-IN tags, and a sound bed per location with pre-laps.
// node longform4.mjs <key> [--voice am_fenrir] [--opening A|B] [--until 25] [--still id@sec,...] [--workers 3] [--out name]
//   episode:   longform/<key>/episode.mjs   (openings + lines; see longform/malta3/episode.mjs for every field)
//   narration: cache/longform/<key>/vo_<voice>/<id>.wav   (python3 longform_tts.py <key> --voice <voice>)
//   output:    out/<out>.mp4 + cache/longform/<key>/stems_<tag>/{vo,words,amb,sfx,score}.wav + project_<tag>.json
// New in v3 (each is a reusable technique, documented in .claude/skills/lingodude-video-method/techniques/):
//   video   real footage, frame-accurate, its own location sound as ambience       (Footage With Its Own Air)
//   lock    two spoken words, consonants slide into shared columns                 (The Consonants Lock In)
//   twin    two places at one scale under one shared year, pausing for evidence   (Two Islands, One Clock)
//   photo.path / sweep / attrib   track across a document, highlight, pull back   (Read the Ink)
//   claim   a claim visibly struck through and revised when evidence lands        (The Claim Revises Itself)
//   sfx with negative `at`        the next place is heard before it is seen       (The Cut Starts in the Soundtrack)
import fs from "node:fs";
import path from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import * as d3 from "d3-geo";
import * as topo from "topojson-client";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const W = 1920, H = 1080, FPS = 30;
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i < 0 ? d : args[i + 1] ?? true; };
const key = args[0]; // the episode folder comes first: node longform3.mjs malta3 ...
const EP = (await import(pathToFileURL(path.join(HERE, "longform", key, "episode.mjs")).href)).default;
const VOICE = opt("voice", "am_fenrir"), OPEN = opt("opening", EP.defaultOpening || "A"), UNTIL = +opt("until", 0);
const TAG = opt("out", `longform_${key}_${OPEN}${UNTIL ? "_" + UNTIL + "s" : ""}`);
const CACHE = path.join(HERE, "cache", "longform", key);
const INC = path.join(HERE, "incoming", EP.assets || key);
for (const d of ["hear", "vid", "amb"]) fs.mkdirSync(path.join(CACHE, d), { recursive: true });
const nm = (p) => path.join(HERE, "node_modules", p);
const furl = (p) => pathToFileURL(p).href;
const r1 = (n) => Math.round(n * 10) / 10;
const run = (cmd, a) => { const r = spawnSync(cmd, a, { encoding: "utf8" }); if (r.status) throw new Error(cmd + " failed: " + r.stderr); return r.stdout; };
const dur = (f) => parseFloat(run("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]));
const C = EP.palette;

// ───────── sounds ─────────
const slug = (s) => s.replace(/[^\p{L}\p{N}]+/gu, "_");
function soundFile(name) { // a word/phrase: EP.sounds[name] (path under incoming) or a Lingua Libre Maltese word
  const src = EP.sounds?.[name] ? path.join(INC, EP.sounds[name].file) : path.join(INC, `LL-Q9166 (mlt)-GħawdxiVeru-${name}.wav`);
  const s = EP.sounds?.[name] || {};
  const out = path.join(CACHE, "hear", slug(name) + (s.start ? "_" + s.start : "") + ".wav");
  if (!fs.existsSync(out)) {
    if (!fs.existsSync(src)) throw new Error("missing recording " + src);
    const a = ["-v", "error", "-y"]; if (s.start != null) a.push("-ss", String(s.start), "-t", String(s.end - s.start));
    run("ffmpeg", [...a, "-i", src, "-vn", "-ac", "1", "-ar", "48000", "-af",
      (s.start != null ? "afade=t=in:d=0.08,areverse,afade=t=in:d=0.3,areverse," : "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,afade=t=in:d=0.02,")
      + "loudnorm=I=-17:TP=-2", out]);
  }
  return out;
}
function sfxFile(name) {
  const s = EP.sfx[name]; const out = path.join(CACHE, "hear", "sfx_" + name + ".wav");
  if (!fs.existsSync(out)) {
    const a = ["-v", "error", "-y"]; if (s.start != null) a.push("-ss", String(s.start), "-t", String(s.end - s.start));
    run("ffmpeg", [...a, "-i", path.join(INC, s.file), "-vn", "-ac", "1", "-ar", "48000", "-af", "afade=t=in:d=0.03,areverse,afade=t=in:d=0.15,areverse", out]);
  }
  return out;
}

// ───────── timeline ─────────
const LINES = [...(EP.openings?.[OPEN] || []), ...EP.lines];
const VO = path.join(CACHE, "vo_" + VOICE);
let t = 0.3; const T = []; let estimated = 0;
for (const L of LINES) {
  const row = { ...L, t0: t, clips: [] };
  t += L.lead ?? 0;
  const clips = (L.hear || []).map((w) => ({ word: w, file: soundFile(w) }));
  const placeClips = () => { if (!clips.length) return; t += L.hearPad ?? 0.25; for (const c of clips) { const d = dur(c.file); row.clips.push({ ...c, t, d }); t += d + (L.hearGap ?? 0.55); } };
  if (L.hearFirst) placeClips();
  const vo = path.join(VO, L.id + ".wav");
  if (L.say) {
    let d; if (fs.existsSync(vo)) d = dur(vo); else { d = L.say.split(/\s+/).length / 2.75 + 0.2; estimated++; }
    row.say0 = t; row.sayDur = d; row.vo = fs.existsSync(vo) ? vo : null; t += d;
  }
  if (!L.hearFirst) placeClips();
  if (L.dur) t = Math.max(t, row.t0 + L.dur);
  if ((L.show || []).some((s) => s.type === "title")) { row.titleAt = t + 0.1; t += 3.0; }
  t += L.gap ?? 0.4;
  row.t1 = t;
  T.push(row);
}
let TOTAL = t + (EP.tail ?? 2.5);
const END = UNTIL ? Math.min(UNTIL, TOTAL) : TOTAL;
if (estimated) console.log(`  ${estimated}/${T.length} lines have no narration yet: timing estimated at 165 wpm`);
console.log(`  opening ${OPEN}: total ${TOTAL.toFixed(1)} s (${(TOTAL / 60).toFixed(2)} min)${UNTIL ? `, rendering 0–${END}s` : ""}`);
const byId = (id) => { const r = T.find((x) => x.id === id); if (!r) throw new Error("no line " + id); return r; };
fs.writeFileSync(path.join(CACHE, `chapters_${TAG}.json`), JSON.stringify([{ t: 0, title: "Intro" }, ...T.filter((r) => r.kicker).map((r) => ({ t: r.t0, title: r.kicker }))], null, 1));
fs.writeFileSync(path.join(CACHE, `midrolls_${TAG}.json`), JSON.stringify(T.filter((r) => r.midroll).map((r) => ({ id: r.id, t: +(r.t1 - (r.gap ?? 0.4) + 0.5).toFixed(1) }))));

// ───────── shots (v4) ─────────
// A line's `shots` share its time (fixed `d` seconds, or weights `w`); a line without shots extends the previous shot.
// No shot may run longer than 5 s: the list is checked here and written to shots_<tag>.json.
const SHOTS = [];
const shotKind = (s) => ["map", "video", "photo", "table", "board", "desk", "lock", "words", "plate"].find((k) => k in s) || "?";
for (const r of T) {
  if (!r.shots) { if (SHOTS.length) SHOTS[SHOTS.length - 1].t1 = r.t1; continue; }
  const list = r.shots, D = r.t1 - r.t0, fixed = list.reduce((a, x) => a + (x.d || 0), 0), wsum = list.reduce((a, x) => a + (x.d ? 0 : (x.w ?? 1)), 0);
  let tt = r.t0;
  list.forEach((x, k) => { const d = x.d ?? (D - fixed) * (x.w ?? 1) / wsum; const sh = { ...x, kind: shotKind(x), line: r.id, t0: tt, t1: k === list.length - 1 ? r.t1 : tt + d }; tt = sh.t1; SHOTS.push(sh); });
}
if (SHOTS.length) SHOTS[SHOTS.length - 1].t1 = Math.max(SHOTS[SHOTS.length - 1].t1, TOTAL);
if (SHOTS.length) SHOTS[0].t0 = 0; // the first shot covers the lead-in (v5: the map showed for 0.3 s before it)
{
  const rows = SHOTS.map((x, i) => ({ n: i + 1, t0: +x.t0.toFixed(2), t1: +x.t1.toFixed(2), d: +(x.t1 - x.t0).toFixed(2), kind: x.kind, line: x.line, what: x.what || String(x[x.kind] && typeof x[x.kind] !== "object" ? x[x.kind] : x.kind) }));
  fs.writeFileSync(path.join(CACHE, `shots_${TAG}.json`), JSON.stringify(rows, null, 0).replace(/},{/g, "},\n{"));
  const long = rows.filter((x) => x.d > 5.0 && x.t0 < END);
  if (SHOTS.length) console.log(`  ${rows.length} shots, longest ${Math.max(...rows.map((x) => x.d)).toFixed(2)} s, average ${(rows.reduce((a, x) => a + x.d, 0) / rows.length).toFixed(2)} s`);
  if (long.length) console.log("  WARNING shots over 5 s: " + long.map((x) => `#${x.n} ${x.line}/${x.kind} ${x.d}s`).join("; "));
}

// ───────── map geometry ─────────
const world = JSON.parse(fs.readFileSync(nm("world-atlas/countries-10m.json")));
const feats = topo.feature(world, world.objects.countries).features;
const S = 20000, proj = d3.geoMercator().scale(S).translate([0, 0]);
const [bx0, by0] = proj([-30, 63]), [bx1, by1] = proj([55, 18]);
proj.clipExtent([[bx0, by0], [bx1, by1]]);
const gp = d3.geoPath(proj).digits(1), gp50 = d3.geoPath(proj).digits(0);
const pxPerDeg = S * Math.PI / 180;
const P = (k) => { const ll = Array.isArray(k) ? k : EP.places[k]; if (!ll) throw new Error("no place " + k); return proj(ll); };
const inBox = (f) => { const [[a, b], [c, d]] = d3.geoBounds(f); return c > -32 && a < 57 && d > 16 && b < 65; };
const boxA = (bx1 - bx0) * (by1 - by0), sane = (f) => gp.area(f) < boxA * 0.5;
const w50 = JSON.parse(fs.readFileSync(nm("world-atlas/countries-50m.json")));
const f50 = topo.feature(w50, w50.objects.countries).features;
const detail = new Set(EP.landDetail || []);
const landD = f50.filter(inBox).filter(sane).filter((f) => !detail.has(f.id)).map((f) => gp50(f) || "").join("") + feats.filter((f) => detail.has(f.id)).map((f) => gp(f) || "").join("");
function regGeo(spec) {
  const f = feats.find((x) => x.id === spec.id); if (!f) throw new Error("no country " + spec.id);
  if (!spec.near) return f;
  const polys = f.geometry.type === "MultiPolygon" ? f.geometry.coordinates : [f.geometry.coordinates];
  return { type: "MultiPolygon", coordinates: polys.filter((c) => d3.geoDistance(d3.geoCentroid({ type: "Polygon", coordinates: c }), spec.near) * 180 / Math.PI < spec.r) };
}
const REG = Object.fromEntries(Object.entries(EP.regions).sort((x, y) => !!x[1].near - !!y[1].near).map(([k, v]) => [k, gp(regGeo(v))]));
const regBox = (k) => d3.geoPath(proj).bounds(regGeo(EP.regions[k]));

// camera
const camK = [];
for (const r of T) {
  if (r.route) {
    const a = P(r.route.from), b = P(r.route.to), dx = Math.abs(b[0] - a[0]) + 1, dy = Math.abs(b[1] - a[1]) + 1;
    const z = Math.min(W * 0.6 / dx, H * 0.52 / dy, W / (1.2 * pxPerDeg));
    camK.push({ t: r.t0 - 0.2, x: (a[0] + b[0]) / 2, y: (a[1] + b[1]) / 2 + H * 0.03 / z, z, tilt: r.cam?.tilt ?? 0, rot: r.cam?.rot ?? 0 });
  } else if (r.cam) { const [x, y] = proj(r.cam.c); camK.push({ t: r.t0 - 0.2, x, y, z: W / (r.cam.span * pxPerDeg), tilt: r.cam.tilt ?? 0, rot: r.cam.rot ?? 0, cut: !!r.cam.cut }); }
}
for (const x of SHOTS) if (x.kind === "map") { const m = x.map; const [px, py] = proj(m.c); camK.push({ t: x.t0, x: px, y: py, z: W / (m.span * pxPerDeg), tilt: m.tilt ?? 0, rot: m.rot ?? 0, cut: true }); }
camK.sort((a, b) => a.t - b.t);
if (!camK.length) { const [x, y] = proj([14.3, 36.6]); camK.push({ t: 0, x, y, z: W / (12 * pxPerDeg), tilt: 0, rot: 0 }); }
camK.forEach((k, i) => { k.dir = i % 2 ? 1 : -1; });
const fillK = {}; for (const k of Object.keys(REG)) fillK[k] = [];
const setFill = (tt, obj) => { for (const [k, v] of Object.entries(obj)) { if (!fillK[k]) throw new Error("no region " + k); fillK[k].push({ t: tt, c: v }); } };
for (const r of T) { if (r.fill) setFill(r.t0, r.fill); if (r.then) setFill((r.say0 ?? r.t0) + (r.sayDur ?? 1) * r.then.at, r.then.fill); }
for (const x of SHOTS) if (x.fill) setFill(x.t0 + (x.fillAt ?? 0), x.fill);
for (const k of Object.keys(fillK)) fillK[k].sort((a, b) => a.t - b.t);
const labelK = [];
T.forEach((r) => { if (r.labels) labelK.push({ t: r.t0, items: r.labels.map(([txt, at]) => ({ txt, p: P(at) })) }); else if (r.cam && labelK.length && labelK[labelK.length - 1].items.length) labelK.push({ t: r.t0, items: [] }); });
for (const x of SHOTS) if (x.labels) labelK.push({ t: x.t0, items: x.labels.map(([txt, at]) => ({ txt, p: P(at) })) }); else if (x.kind === "map") labelK.push({ t: x.t0, items: [] });
labelK.sort((a, b) => a.t - b.t);
const routes = T.filter((r) => r.route).map((r) => {
  const idx = T.indexOf(r), a = P(r.route.from), b = P(r.route.to), mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1], k = 0.18;
  const lab = (q, l) => l ?? (typeof q === "string" ? q.toUpperCase() : "");
  return { t: r.t0 + 0.2, tOut: (T[idx + (r.route.hold ?? 2)] || T[T.length - 1]).t1, color: r.route.color, a, b, la: lab(r.route.from, r.route.fromLabel), lb: lab(r.route.to, r.route.toLabel), d: `M${r1(a[0])},${r1(a[1])} Q${r1(mx - dy * k)},${r1(my + dx * k)} ${r1(b[0])},${r1(b[1])}` };
});
const yearK = T.filter((r) => "year" in r).map((r) => ({ t: r.t0, v: r.year }));
const kickK = T.filter((r) => r.kicker).map((r) => ({ t: r.t0, v: r.kicker }));

// ───────── photos & footage ─────────
const PH = EP.photos || {};
const phInfo = {};
function photo(k) {
  if (phInfo[k]) return phInfo[k];
  const f = path.join(INC, "photos", k + ".jpg"); if (!fs.existsSync(f) || !PH[k]) throw new Error("missing photo " + k);
  const [w, h] = run("identify", ["-format", "%w %h", f + "[0]"]).trim().split(" ").map(Number);
  return (phInfo[k] = { url: furl(f), w, h, credit: `${PH[k][2]} · ${PH[k][1]} · Wikimedia Commons` });
}
const VID = EP.videos || {};
const ambItems = [];
function footage(o) { // extract the frames this overlay needs (graded towards the palette)
  const v = VID[o.src]; if (!v) throw new Error("missing video " + o.src);
  const need = o.tOut - o.tIn + 0.6, from = o.from ?? v.from ?? 0, rate = o.rate ?? 1;
  const dir = path.join(CACHE, "vid", `${o.src}_${from}_${rate}_${Math.ceil(need)}${o.pillar ? "_p" : ""}`);
  if (!fs.existsSync(path.join(dir, "done"))) {
    fs.mkdirSync(dir, { recursive: true });
    run("ffmpeg", ["-v", "error", "-y", "-ss", String(from), "-i", path.join(INC, v.file), "-t", String(need * rate + 0.5), "-vf",
      `setpts=PTS/${rate},fps=${FPS},${o.pillar ? `scale=-2:${H}` : `scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H}`},eq=saturation=0.92:contrast=1.04,colorbalance=rs=.03:gs=.01:bs=-.03`, "-q:v", "4", path.join(dir, "%05d.jpg")]);
    fs.writeFileSync(path.join(dir, "done"), "");
  }
  o.dir = furl(dir) + "/"; o.n = fs.readdirSync(dir).filter((f) => f.endsWith(".jpg")).length;
  o.credit = `${v.lic} · ${v.by} · Wikimedia Commons`;
  const av = v.ambFrom ? VID[v.ambFrom] : v; // silent footage borrows real Malta location sound from a nearby clip (ambFrom)
  if (o.amb !== false && v.amb !== false) ambItems.push({ f: path.join(INC, av.file), from: v.ambFrom ? (v.ambAt ?? 0) + (o.from ?? 0) % 20 : from, t: o.tIn, d: o.tOut - o.tIn + 0.3, gain: o.ambGain ?? v.ambGain ?? -6, rate });
}

// ───────── overlays ─────────
const OV = [];
const clipsAll = T.flatMap((x) => x.clips);
T.forEach((r, i) => {
  const until = (T[i + (r.hold || 0)] || r).t1 - 0.12;
  for (const s of r.show || []) {
    const o = { ...s, tIn: r.t0 + (s.delay ?? 0.08), tOut: until };
    if (s.until) o.tOut = byId(s.until).t1 - 0.12;
    if (s.type === "title") { o.tIn = r.titleAt; o.tOut = r.titleAt + 2.9; }
    if (s.from && typeof s.from === "string" && s.type === "dist") { o.a = P(s.from); o.b = P(s.to); }
    if (typeof s.at === "string") o.p = P(s.at);
    if (s.src && (s.type === "photo" || s.type === "frame")) Object.assign(o, (({ url, w, h, credit }) => ({ url, iw: w, ih: h, credit }))(photo(s.src)));
    if (s.type === "video") footage(o);
    if (s.type === "words") prep(o, r);
    if (s.type === "lock") { // rows appear when their word is heard
      o.rows = s.rows.map((rw) => { const c = T.flatMap((x) => x.clips).find((c) => c.word === rw.hear && c.t >= r.t0 - 0.01); return { ...rw, at: c ? c.t : r.t0 + 0.5, d: c ? c.d : 0.8 }; });
      const last = o.rows[o.rows.length - 1]; o.lockAt = last.at + last.d + 0.15;
    }
    if (s.type === "twin") {
      o.steps = s.steps.map((st) => ({ ...st, t: byId(st.at).t0 + (st.delay ?? 0.15) }));
      const z = Math.min(780 / (regBox("sicily")[1][0] - regBox("sicily")[0][0]), 600 / (regBox("sicily")[1][1] - regBox("sicily")[0][1]));
      o.panels = ["sicily", "malta"].map((k) => { const b = regBox(k); return { k, d: REG[k], cx: (b[0][0] + b[1][0]) / 2, cy: (b[0][1] + b[1][1]) / 2, z }; });
    }
    OV.push(o);
  }
  for (const c of r.clips) OV.push({ type: "hear", word: c.word, label: EP.sounds?.[c.word]?.label, tIn: c.t - 0.12, tOut: c.t + c.d + 0.25, d: c.d, quiet: r.quietHear });
});
// ───────── shots → layers (v4) ─────────
function prep(o, r) {
  if (o.from && typeof o.from === "string" && o.type === "dist") { o.a = P(o.from); o.b = P(o.to); }
  if (typeof o.at === "string" && !["table", "board", "desk", "claim"].includes(o.type)) o.p = P(o.at);
  if (o.src && (o.type === "photo" || o.type === "frame")) Object.assign(o, (({ url, w, h, credit }) => ({ url, iw: w, ih: h, credit }))(photo(o.src)));
  if (o.type === "video") footage(o);
  const firstClip = (w) => { const cs = clipsAll.filter((c) => c.word === w); return cs.filter((c) => c.t <= o.tOut + 0.05).pop() || cs[0]; }; // the recording heard most recently by the end of the shot
  if (o.type === "plate" && o.src) Object.assign(o, (({ url, w, h }) => ({ url, iw: w, ih: h }))(photo(o.src)));
  if (o.type === "lock") { o.rows = o.rows.map((rw) => { const c = firstClip(rw.hear); return { ...rw, at: c ? c.t : o.tIn + 0.5, d: c ? c.d : 0.8 }; }); const last = o.rows[o.rows.length - 1]; o.lockAt = o.lockAt != null ? o.tIn + o.lockAt : Math.max(o.tIn + 0.4, last.at + last.d + 0.15); if (o.reveal != null) o.revealT = o.tIn + o.reveal; }
  if (o.type === "words") o.items = o.items.map((it) => { const c = it.hear ? firstClip(it.hear) : null; return { ...it, ci: c ? clipsAll.indexOf(c) : -1, labelT: it.labelAt == null ? null : typeof it.labelAt === "string" ? byId(it.labelAt).t0 + (it.labelOff ?? 0) : o.tIn + it.labelAt }; });
  return o;
}
for (const x of SHOTS) {
  const r = byId(x.line);
  if (x.kind !== "map") {
    const spec = x[x.kind]; let o;
    if (x.kind === "video" || x.kind === "photo") o = { ...x, type: x.kind, src: spec };
    else if (x.kind === "lock" || x.kind === "words") o = { ...spec, type: x.kind, base: true };
    else if (x.kind === "plate") o = { type: "plate", src: typeof spec === "string" ? spec : null, ...(typeof spec === "object" ? spec : {}) };
    else o = { ...x, type: x.kind, spec: typeof spec === "string" ? { view: spec, doc: spec } : spec };
    delete o.over; o.tIn = x.t0; o.tOut = x.t1; o.shot = true;
    OV.push(prep(o, r));
  }
  for (const s2 of x.over || []) OV.push(prep({ ...s2, tIn: x.t0 + (s2.delay ?? 0.05), tOut: s2.until ? byId(s2.until).t1 - 0.12 : x.t1 }, r));
  if (x.tag) OV.push({ type: "tagline", text: x.tag, tIn: x.t0, tOut: x.t1 });
}
// Full-screen layers (photo, video, twin): between two of them it is always a hard cut and the map never shows through;
// fades/wipes are used only between the map and a photo or video (owner, 2026-11-20).
{
  const FULLS = OV.filter((o) => o.shot || ["photo", "video", "twin"].includes(o.type)).sort((a, b) => a.tIn - b.tIn);
  for (const o of FULLS) {
    const nxt = FULLS.find((n) => n !== o && n.tIn > o.tIn && n.tIn >= o.tOut - 0.05 && n.tIn <= o.tOut + 0.8);
    if (nxt) { o.tOut = nxt.tIn; o.cutOut = true; nxt.cutIn = true; }
    if (FULLS.some((q) => q !== o && q.tIn <= o.tIn && q.tOut > o.tIn + 0.05)) o.cutIn = true;          // starts over another full layer
    if (FULLS.some((q) => q !== o && q.tIn <= o.tIn && q.tOut > o.tOut + 0.2)) o.cutOut = true;         // returns to it
  }
  // a layer that ends where a map shot begins cuts to it: a fade would show the map at its previous framing for a few frames (v4 flash at 6:27)
  const mapStarts = SHOTS.filter((x) => x.kind === "map").map((x) => x.t0);
  for (const o of FULLS) if (mapStarts.some((m) => Math.abs(m - o.tOut) < 0.1)) o.cutOut = true;
  // cards and lock graphics that end just before a hard cut stay up and cut with it (no fade back to the layer below)
  const cutTimes = FULLS.filter((o) => o.cutOut).map((o) => o.tOut);
  for (const o of OV) if (!o.shot && !["photo", "video", "twin", "hear", "fadeout", "title"].includes(o.type)) {
    const c = cutTimes.find((T) => T >= o.tOut - 0.05 && T - o.tOut < 0.6); if (c != null) { o.tOut = c; o.cutOut = true; }
  }
  const covered = (t0, t1) => FULLS.some((q) => q.tIn <= t0 + 0.02 && q.tOut >= t1 - 0.02);
  const flash = FULLS.flatMap((o) => FULLS.filter((n) => n.tIn > o.tOut && n.tIn - o.tOut < 0.8 && !covered(o.tOut, n.tIn)).map((n) => `${o.src || o.type}@${o.tOut.toFixed(2)} -> ${n.src || n.type}@${n.tIn.toFixed(2)}`));
  if (flash.length) console.log("  WARNING map flashes between full-screen layers: " + flash.join("; "));
  fs.writeFileSync(path.join(CACHE, `cuts_${TAG}.json`), JSON.stringify(FULLS.map((o) => ({ type: o.type, src: o.src, tIn: +o.tIn.toFixed(2), tOut: +o.tOut.toFixed(2), cutIn: !!o.cutIn, cutOut: !!o.cutOut }))));
}
OV.push({ type: "fadeout", tIn: TOTAL - 1.6, tOut: TOTAL + 2 });
OV.sort((a, b) => ((b.shot || ["photo", "video"].includes(b.type)) ? 1 : 0) - ((a.shot || ["photo", "video"].includes(a.type)) ? 1 : 0));
// small copies of photos for table prints and board cards (full-size scans inside 3D layers crash the renderer)
function thumb(k, mw = 800) {
  const ph = photo(k), d = path.join(CACHE, "thumbs"); fs.mkdirSync(d, { recursive: true });
  const out = path.join(d, `${k}_${mw}.jpg`);
  if (!fs.existsSync(out)) run("convert", [path.join(INC, "photos", k + ".jpg") + "[0]", "-resize", `${mw}x${mw}>`, "-quality", "88", out]);
  return { url: furl(out), w: ph.w, h: ph.h };
}
// ───────── 3D Mediterranean table (v4) ─────────
let TABLE = null;
if (EP.table) {
  const tb = EP.table, SW = tb.w || 2600, box = tb.box;
  const m0 = d3.geoMercator().scale(1).translate([0, 0]), a = m0([box[0][0], box[1][1]]), b = m0([box[1][0], box[0][1]]);
  const sc = SW / (b[0] - a[0]), SH = Math.round((b[1] - a[1]) * sc);
  const tp = d3.geoMercator().scale(sc).translate([-a[0] * sc, -a[1] * sc]).clipExtent([[0, 0], [SW, SH]]), tg = d3.geoPath(tp).digits(1);
  const near = feats.filter((f) => { const [[x0, y0], [x1, y1]] = d3.geoBounds(f); return x1 - x0 < 60 && x1 > box[0][0] - 1 && x0 < box[1][0] + 1 && y1 > box[0][1] - 1 && y0 < box[1][1] + 1; });
  const objs = Object.entries(tb.objects || {}).map(([id, ob]) => {
    const [x, y] = tp(Array.isArray(ob.at) ? ob.at : EP.places[ob.at]); const o2 = { id, ...ob, x: x + (ob.dx || 0), y: y + (ob.dy || 0), t: 1e9 };
    if (ob.src) { const ph = thumb(ob.src, ob.kind === "coin" ? 1200 : 700); o2.url = ph.url; o2.iw = ph.w; o2.ih = ph.h; }
    o2.h = ob.kind === "coin" ? ob.w : ob.kind === "print" ? Math.round(ob.w * (o2.ih / o2.iw) + 58) : (ob.h || 220);
    return o2;
  });
  const at = (k) => { if (Array.isArray(k)) return tp(k); const ob = objs.find((q) => q.id === k); if (ob) return [ob.x, ob.y]; return tp(EP.places[k]); };
  const pxDeg = tp([15, 36.5])[0] - tp([14, 36.5])[0];
  TABLE = { w: SW, h: SH, tex: furl(path.join(INC, tb.tex)), paper: furl(path.join(HERE, "cache", "longform", "paper.png")),
    land: near.map((f) => tg(f) || "").join(""), regs: Object.fromEntries((tb.regions || Object.keys(EP.regions)).map((k) => [k, tg(regGeo(EP.regions[k])) || ""])),
    labels: (tb.labels || []).map(([txt, k, size, dx, dy]) => { const [x, y] = at(k); return { txt, x: x + (dx || 0), y: y + (dy || 0), size: size || 44 }; }),
    grat: [...Array(12)].map((_, i) => { const lon = Math.floor(box[0][0]) + i; return tg({ type: "LineString", coordinates: [[lon, box[0][1] - 1], [lon, box[1][1] + 1]] }); }).concat([...Array(8)].map((_, i) => { const lat = Math.floor(box[0][1]) + i; return tg({ type: "LineString", coordinates: [[box[0][0] - 1, lat], [box[1][0] + 1, lat]] }); })).filter(Boolean),
    km100: pxDeg * 100 / (111.32 * Math.cos(36.5 * Math.PI / 180)), objs,
    arrows: (tb.arrows || []).map((ar) => { const [x0, y0] = at(ar.from), [x1, y1] = at(ar.to); const mx = (x0 + x1) / 2, my = (y0 + y1) / 2, dx = x1 - x0, dy = y1 - y0; const bend = ar.dash ? 0 : 0.15; return { ...ar, d: `M${r1(x0)},${r1(y0)} Q${r1(mx - dy * bend)},${r1(my + dx * bend)} ${r1(x1)},${r1(y1)}`, lx: mx + (ar.ldx || 0), ly: my + (ar.ldy || 0), t: byId(ar.at).t0 + (ar.off ?? 0.5) }; }),
    title: tb.title ? { ...tb.title, xy: at(tb.title.at), t0: byId(tb.title.from).t0 + (tb.title.off ?? 0), t1: byId(tb.title.to).t1 } : null };
  SHOTS.forEach((x, i) => (x.place || []).forEach((id, k) => { const ob = objs.find((q) => q.id === id); if (!ob) throw new Error("no table object " + id);
    const cutIn = true, at = (x.placeAt ?? 0.45) + k * 0.6; // every table shot starts on a cut: an object due in the first 0.5 s is already falling on the first frame
    if (ob.t > 1e8) ob.t = cutIn && at < 0.5 ? x.t0 - 0.05 : x.t0 + at; }));
  const camOf = (c) => { const [x, y] = at(c.at); return { tilt: c.tilt ?? 0, rz: c.rz ?? 0, zoom: c.zoom ?? 0.6, x: x - SW / 2 + (c.dx || 0), y: y - SH / 2 + (c.dy || 0) }; };
  for (const o of OV) if (o.type === "table") { const sp = o.spec; o.c0 = camOf(sp.from || sp); o.c1 = camOf(sp.to || { ...(sp.from || sp), zoom: (sp.from || sp).zoom * 1.06 }); o.focus = sp.focus || null; }
}
// ───────── investigation board (v4, v5) ─────────
// v5: a laid-out board (heads, divider lines), labelled strings (records / shows / suggests / challenges / open),
// [[highlighted]] phrases inside cards, `lit` = cards kept bright while the rest dims, `cap` = a caption strip carried
// across consecutive board shots, and a camera that glides from the previous board shot's framing to the next one.
let BOARD = null;
if (EP.board) {
  const bd = EP.board, mk = (s) => (s == null ? s : String(s).replace(/\[\[(.+?)\]\]/g, '<span class="hl">$1</span>'));
  const LSTYLE = { records: "solid", shows: "solid", supports: "solid", suggests: "dash", challenges: "blue", raises: "honey", open: "open", tests: "blue" };
  BOARD = { w: bd.w, h: bd.h, lines: bd.lines || [], links: [], rewrites: [],
    cards: Object.entries(bd.cards).map(([id, c]) => ({ id, ...c, text: mk(c.text), sub: mk(c.sub), cite: mk(c.cite), ...(c.src ? (({ url, w, h }) => ({ url, iw: w, ih: h }))(thumb(c.src, 800)) : {}), t: c.kind === "head" ? 0 : 1e9, fixed: c.kind === "head", hlT: 1e9 })) };
  const card = (id) => { const i = BOARD.cards.findIndex((q) => q.id === id); if (i < 0) throw new Error("no board card " + id); return i; };
  const LK = Object.fromEntries(Object.entries(bd.links || {}).map(([id, L]) => { const [a, b, label, style, opt] = Array.isArray(L) ? L : [L.a, L.b, L.label, L.style, L]; return [id, { id, a: card(a), b: card(b), label: label || "", style: style || LSTYLE[label] || "solid", ax: opt?.ax || 0, bx: opt?.bx || 0, route: opt?.route || null, at: opt?.at ?? 0.5, sag: opt?.sag ?? 130 }]; }));
  let bid = 0, prev = null;
  for (const x of SHOTS) if (x.kind === "board") {
    const cutIn = !(prev && Math.abs(prev.t1 - x.t0) < 0.06); // cutting in from another layer: a card due in the first 0.5 s is already landing on the cut (no empty board)
    (x.add || []).forEach((id, k) => { const c = BOARD.cards[card(id)]; if (c.t > 1e8) c.t = cutIn && (x.addAt ?? 0.35) + k * 0.6 < 0.5 ? x.t0 - 0.1 : x.t0 + (x.addAt ?? 0.35) + k * 0.6; });
    (x.link || []).forEach((L, k) => { const t = x.t0 + (x.linkAt ?? 0.9) + k * 0.7;
      if (Array.isArray(L)) BOARD.links.push({ id: L.join("-"), a: card(L[0]), b: card(L[1]), label: L[2] || "", style: L[3] || LSTYLE[L[2]] || "solid", t });
      else { if (!LK[L]) throw new Error("no board link " + L); if (!BOARD.links.includes(LK[L])) BOARD.links.push(Object.assign(LK[L], { t })); } });
    (x.hl || []).forEach((id) => { const c = BOARD.cards[card(id)]; c.hlT = Math.min(c.hlT, x.t0 + (x.hlAt ?? 0.6)); });
    if (x.rewrite) BOARD.rewrites.push({ ...x.rewrite, i: card(x.rewrite.card), t: x.t0 + (x.rewrite.at ?? 0.6) });
    x.bid = bid++; x.pbid = prev && Math.abs(prev.t1 - x.t0) < 0.06 ? prev.bid : null; prev = x;
  }
  for (const x of SHOTS) if (x.kind === "board" && x.lit) x.lit.forEach((id) => card(id));
  for (const o of OV) if (o.type === "board") { const x = SHOTS.find((q) => q.kind === "board" && Math.abs(q.t0 - o.tIn) < 1e-6); o.bid = x.bid; o.pbid = x.pbid; }
  const unused = Object.keys(LK).filter((k) => !BOARD.links.includes(LK[k])); if (unused.length) console.log("  board links never shown: " + unused.join(", "));
}
// ───────── desk documents (v4) ─────────
const DOCS = Object.fromEntries(Object.entries(EP.docs || {}).map(([k, src]) => { const ph0 = photo(src), ph = { ...thumb(src, 2400), credit: ph0.credit }; return [k, { url: ph.url, iw: ph.w, ih: ph.h, credit: ph.credit, tex: furl(path.join(INC, EP.deskTex || EP.table?.tex)) }]; }));
// ───────── loudness envelopes of every heard recording (typography follows the real voice) ─────────
const CLIPS = clipsAll.map((c) => {
  const raw = spawnSync("ffmpeg", ["-v", "error", "-i", c.file, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], { maxBuffer: 1 << 28 }).stdout;
  const a = new Float32Array(raw.buffer.slice(raw.byteOffset, raw.byteOffset + raw.length)), hop = Math.round(16000 / FPS), e = [];
  for (let i = 0; i < a.length; i += hop) { let s2 = 0, n = 0; for (let j = i; j < Math.min(a.length, i + hop); j++) { s2 += a[j] * a[j]; n++; } e.push(Math.sqrt(s2 / Math.max(1, n))); }
  const mx = Math.max(...e, 1e-6), en = e.map((v) => +(v / mx).toFixed(3)), tot = en.reduce((p, v) => p + v, 0) || 1; let cum = 0;
  return { word: c.word, t: c.t, d: c.d, e: en, cu: en.map((v) => +((cum += v) / tot).toFixed(3)) };
});
const DATA = { W, H, TOTAL, camK, fillK, labelK, routes, yearK, kickK, OV, title: EP.cardTitle, C, table: TABLE, board: BOARD, docs: DOCS, clips: CLIPS };

// ───────── page ─────────
const TEX = path.join(HERE, "cache", "longform", "paper.png");
const fontCss = [...["700", "800", "900", "700-italic", "800-italic", "900-italic"].map((w) => nm(`@fontsource/fraunces/${w}.css`)), ...["500", "700", "800"].map((w) => nm(`@fontsource/inter/${w}.css`)), nm("@fontsource/noto-naskh-arabic/700.css")]
  .map((f) => `<link rel="stylesheet" href="${furl(f)}">`).join("");
for (const o of OV) if (o.img) o.img = fs.existsSync(path.join(HERE, o.img)) ? furl(path.join(HERE, o.img)) : null;
const html = `<!doctype html><html><head><meta charset="utf-8">${fontCss}<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--paper:${C.paper};--ink:${C.ink};--red:${C.red};--honey:${C.honey};--sea:${C.sea};--sea2:${C.sea2};--soft:${C.soft}}
body{width:${W}px;height:${H}px;overflow:hidden;background:var(--sea2);font-family:Inter,sans-serif}
#world{position:absolute;inset:0;transform-origin:50% 62%}
#sea{position:absolute;inset:-70%;background:radial-gradient(ellipse at 50% 45%,var(--sea) 0%,var(--sea) 25%,var(--sea2) 62%)}
svg{position:absolute;inset:0}
#map{filter:drop-shadow(0 3px 0 rgba(70,50,20,.28)) drop-shadow(0 10px 16px rgba(0,0,0,.28))}
#hi{filter:drop-shadow(2px 6px 0 rgba(40,20,10,.42)) drop-shadow(4px 14px 16px rgba(0,0,0,.4))}
#tex{position:absolute;inset:0;background:url(${furl(TEX)});background-size:1024px;mix-blend-mode:multiply;opacity:.34;pointer-events:none}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0) 55%,rgba(3,16,26,.5) 100%)}
.lab{position:absolute;transform:translate(-50%,-50%);font:800 24px Inter;letter-spacing:.18em;color:#33281c;text-shadow:0 0 6px rgba(243,230,204,.95),0 0 2px rgba(243,230,204,1);white-space:nowrap}
#year{position:absolute;right:56px;top:44px;background:var(--paper);border-radius:8px;padding:6px 20px 8px;font:900 52px Fraunces;color:var(--ink);box-shadow:0 6px 16px rgba(0,0,0,.35);z-index:5}
#kick{position:absolute;left:56px;top:50px;background:var(--paper);border-radius:8px;padding:10px 20px;font:800 24px Inter;letter-spacing:.16em;color:var(--ink);box-shadow:0 6px 16px rgba(0,0,0,.3);z-index:5}
#kick b{display:inline-block;width:11px;height:11px;border-radius:50%;background:var(--red);margin-right:12px;vertical-align:2px}
.card{position:absolute;background:var(--paper);border-radius:10px;box-shadow:0 10px 26px rgba(0,0,0,.38);color:var(--ink)}
.k{font:800 19px Inter;letter-spacing:.16em;color:var(--red);text-transform:uppercase}
.big{font:900 112px/1 Fraunces;color:var(--red)}
.pill{display:inline-block;font:800 16px Inter;letter-spacing:.14em;color:#fff;background:var(--red);border-radius:5px;padding:4px 9px}
.word{font:italic 800 60px/1.1 Fraunces}
.gloss{font:500 26px Inter;color:var(--soft)}
.ar{font:700 48px "Noto Naskh Arabic";direction:rtl}
.cap{position:absolute;left:50%;bottom:64px;transform:translateX(-50%);background:var(--paper);border-radius:10px;padding:16px 30px;font:800 40px Inter;color:var(--ink);box-shadow:0 8px 20px rgba(0,0,0,.35);white-space:nowrap}
.stamp{position:absolute;left:50%;top:44%;white-space:nowrap;width:max-content;line-height:1.1;font:900 96px Inter;letter-spacing:.06em;color:var(--red);border:9px solid var(--red);border-radius:14px;padding:6px 30px;background:rgba(243,230,204,.9)}
.dot{display:inline-block;width:14px;height:14px;border-radius:50%;margin:0 4px 4px 0}
.on{outline:6px solid var(--red);outline-offset:4px}
.tag{position:absolute;left:56px;top:52px;font:500 22px "Inter";letter-spacing:.08em;color:#f3ece0;background:rgba(10,10,10,.72);padding:8px 14px;border-radius:4px;z-index:6}
.tag i{display:inline-block;width:10px;height:10px;background:var(--red);border-radius:50%;margin-right:10px}
</style></head><body>
<div id="world"><div id="sea"></div>
<svg id="map" viewBox="0 0 ${W} ${H}"><g id="cam"><path id="land" d="${landD}" fill="${C.land}" stroke="${C.border}" stroke-width="1.2" vector-effect="non-scaling-stroke" stroke-linejoin="round"/></g></svg>
<svg id="hi" viewBox="0 0 ${W} ${H}"><g id="cam2">${Object.entries(REG).map(([k, d]) => `<path id="r_${k}" d="${d}" fill="transparent" stroke="rgba(60,30,20,.35)" stroke-width="1" vector-effect="non-scaling-stroke"/>`).join("")}</g></svg>
<svg id="rt" viewBox="0 0 ${W} ${H}"><g id="cam3"></g></svg>
<div id="labs"></div><div id="pins"></div></div>
<div id="tex"></div><div id="vig"></div>
<div id="ov"></div>
<div id="kick" style="opacity:0"></div><div id="year" style="opacity:0"></div>
<script>
const D=${JSON.stringify(DATA)};
const $=(s)=>document.querySelector(s);
const cl=(v,lo,hi)=>Math.max(lo,Math.min(hi,v));
const ease=(x)=>x<0?0:x>1?1:x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const eo=(x)=>x<0?0:x>1?1:1-Math.pow(1-x,3);
const back=(x)=>{x=cl(x,0,1);const c=1.6;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const hex=(c)=>c?[parseInt(c.slice(1,3),16),parseInt(c.slice(3,5),16),parseInt(c.slice(5,7),16),1]:[233,220,191,0];
const mix=(a,b,k)=>a.map((v,i)=>v+(b[i]-v)*k);
function held(k,t){const u=Math.max(0,t-k.t-1.6);const q=1-Math.exp(-u/9);return {x:k.x+k.dir*q*${W}*0.05/k.z,y:k.y-q*${H}*0.02/k.z,z:k.z*(1+0.12*q),tilt:k.tilt,rot:k.rot+k.dir*q*1.0}}
function cam(t){const K=D.camK;let i=K.findIndex(k=>k.t>t);if(i<0)i=K.length;if(i<=1)return held(K[0],t);const b=K[i-1],a=held(K[i-2],b.t);const bb=held(b,t);
  const k=b.cut?1:ease((t-b.t)/1.6);return {x:a.x+(bb.x-a.x)*k,y:a.y+(bb.y-a.y)*k,z:Math.exp(Math.log(a.z)+(Math.log(bb.z)-Math.log(a.z))*k),tilt:a.tilt+(bb.tilt-a.tilt)*k,rot:a.rot+(bb.rot-a.rot)*k}}
const R=$("#cam3");D.routes.forEach((r,i)=>{R.insertAdjacentHTML("beforeend",'<path id="rt'+i+'" d="'+r.d+'" fill="none" stroke="'+r.color+'" stroke-width="6" stroke-linecap="round" vector-effect="non-scaling-stroke" stroke-dasharray="1 14" /><circle id="rh'+i+'" r="9" fill="'+r.color+'" stroke="#f3e6cc" stroke-width="3" vector-effect="non-scaling-stroke"/>');const el=document.getElementById("rt"+i),len=el.getTotalLength();r.pts=Array.from({length:61},(_,j)=>{const q=el.getPointAtLength(len*j/60);return [q.x,q.y]})});
const ov=$("#ov");const pins=$("#pins");
D.routes.forEach((r,i)=>{pins.insertAdjacentHTML("beforeend",[["a",r.la],["b",r.lb]].map(([e,l])=>'<div id="pin'+i+e+'" style="position:absolute;opacity:0;transform:translate(-50%,-100%)"><div class="card" style="position:relative;padding:6px 14px;font:800 24px Inter;letter-spacing:.12em;white-space:nowrap;margin-bottom:8px">'+l+'</div><div style="width:20px;height:20px;margin:0 auto -10px;border-radius:50%;background:'+r.color+';border:4px solid #f3e6cc;box-shadow:0 3px 8px rgba(0,0,0,.4)"></div></div>').join(""))});
function chipHTML(it,lang,col){const [w,g,src]=it;return '<div class="card chip" data-w="'+w+'" style="position:relative;display:inline-block;padding:16px 26px;margin:0 10px;text-align:center">'+(lang?'<div class="pill" style="background:'+(col||D.C.red)+'">'+lang+'</div>':'')+'<div class="word" style="font-size:'+(g?50:46)+'px;margin-top:4px">'+w+'</div>'+(g?'<div class="gloss">“'+g+'”</div>':'')+(src?'<div class="gloss" style="font-size:22px;color:'+D.C.red+';margin-top:2px">← '+src+'</div>':'')+'</div>'}
const BUILD={
 number:o=>'<div class="card" style="left:50%;top:70px;padding:16px 38px 18px;text-align:center"><div class="big"><span class="n"></span></div><div class="k" style="margin-top:6px;color:#3a2c1e">'+o.caption+'</div></div>',
 chip:o=>'<div style="position:absolute;'+(o.pos==="right"?"right:120px;top:360px":o.pos==="center"?"left:50%;top:330px;transform:translateX(-50%)":"left:120px;top:360px")+'">'+chipHTML([o.word,o.gloss,o.src],o.lang).replace('margin:0 10px','margin:0')+'</div>',
 pair:o=>'<div style="position:absolute;left:50%;bottom:'+(o.bottom||90)+'px;transform:translateX(-50%) scale('+(o.zoom||1)+');transform-origin:50% 100%;display:flex;align-items:center;gap:28px">'+chipHTML([o.a.word,o.a.gloss],o.a.lang).replace('margin:0 10px','margin:0')+'<div style="font:900 70px Fraunces;color:#f3e6cc;text-shadow:0 3px 8px rgba(0,0,0,.5)">≈</div><div class="card chip" data-w="'+(o.b.hear||o.b.word)+'" style="position:relative;padding:16px 28px;text-align:center"><div class="pill" style="background:#9a6a1c">'+o.b.lang+'</div><div class="ar" style="margin-top:2px">'+o.b.script+'</div><div class="word" style="font-size:40px">'+o.b.word+'</div><div class="gloss">“'+o.b.gloss+'”</div></div></div>',
 chips:o=>'<div style="position:absolute;left:50%;'+(o.center?'top:46%;transform:translate(-50%,-50%) scale('+(o.zoom||1)+')':'bottom:70px;transform:translateX(-50%) scale('+(o.zoom||1)+');transform-origin:50% 100%')+';text-align:center;white-space:nowrap">'+(o.title?'<div class="card k" style="position:relative;display:inline-block;padding:8px 18px;margin-bottom:14px;color:var(--ink)">'+o.title+'</div><br>':'')+o.items.map(it=>chipHTML(o.plain?[it[0]]:it,o.plain?null:(o.src||"MALTESE"),o.src==="ITALIAN"?"#3f7d5a":o.src==="ENGLISH"?"#3d5f9a":null)).join("")+'</div>',
 caption:o=>'<div class="cap">'+o.text+'</div>',
 card:o=>'<div class="card" style="left:50%;top:50%;transform:translate(-50%,-50%);padding:30px 48px;font:900 56px/1.15 Fraunces;text-align:center;max-width:1200px">'+o.text+'</div>',
 stamp:o=>'<div class="stamp">'+o.text+'</div>',
 title:o=>'<div style="position:absolute;inset:0;background:rgba(5,24,36,.45)"></div><div class="card" style="left:50%;top:50%;transform:translate(-50%,-50%);padding:36px 70px 42px;text-align:center;width:1240px"><div class="k">LingoDude</div><div style="font:900 84px/1.06 Fraunces;margin-top:12px">'+D.title+'</div></div>',
 portrait:o=>'<div class="card" style="right:70px;top:150px;width:320px;padding:22px 20px 18px;text-align:center"><div style="width:220px;height:260px;margin:0 auto;border-radius:50%;border:4px solid var(--ink);overflow:hidden;background:#efe2c6;display:flex;align-items:flex-end;justify-content:center">'+(o.img?'<img src="'+o.img+'" style="width:118%;margin-bottom:-6px">':'<div style="font:900 140px Fraunces;line-height:260px">?</div>')+'</div><div style="font:900 36px/1.1 Fraunces;margin-top:16px">'+o.name+'</div><div class="k" style="margin-top:8px;font-size:16px;color:var(--soft)">'+o.role+'</div></div>',
 aside:o=>'<div class="card" style="'+(o.side==="left"?"left:70px":"right:70px")+';top:'+(o.top||170)+'px;width:'+(o.w||620)+'px;padding:24px 30px"><div class="k">'+o.kicker+'</div>'+o.rows.map(r=>'<div style="margin-top:14px"><div class="pill" style="background:'+(r[2]||D.C.red)+'">'+r[0]+'</div><div style="font:'+(r[3]||"italic 800 40px/1.2 Fraunces")+';margin-top:6px">'+r[1]+'</div></div>').join("")+(o.note?'<div style="font:500 20px/1.35 Inter;color:var(--soft);margin-top:14px">'+o.note+'</div>':'')+'</div>',
 claim:o=>'<div class="card" style="left:50%;top:'+(o.top||110)+'px;transform:translateX(-50%);width:1080px;padding:26px 36px"><div class="k">'+(o.kicker||"THE CLAIM")+'</div><div class="ct" style="position:relative;display:inline-block;font:900 50px/1.15 Fraunces;margin-top:8px">'+o.text+'<div class="strike" style="position:absolute;left:-6px;top:52%;height:7px;background:var(--red);width:0;border-radius:4px"></div></div><div class="rv" style="opacity:0;margin-top:16px;max-height:0;overflow:hidden"><span class="pill">'+(o.revisedTag||"THE EVIDENCE")+'</span><div style="font:900 46px/1.15 Fraunces;color:var(--red);margin-top:8px">'+o.revised+'</div>'+(o.source?'<div style="font:500 20px Inter;color:var(--soft);margin-top:8px">'+o.source+'</div>':'')+'</div></div>',
 doc:o=>'<div class="card" style="left:80px;top:200px;width:600px;padding:26px 32px"><div class="k">'+o.kicker+'</div><div style="font:italic 900 56px/1.1 Fraunces;margin:10px 0 12px">'+o.title+'</div>'+o.lines.map(l=>'<div style="font:500 28px/1.35 Inter;color:#4b4238">'+l+'</div>').join("")+'</div>',
 dots:o=>{const per=10;return '<div class="card" style="'+(o.center?"left:580px;top:"+(o.top||250)+"px;transform:scale("+(o.zoom||1)+");transform-origin:50% 0":"left:80px;top:170px")+';width:760px;padding:26px 32px"><div class="k">'+o.title+'</div>'+o.rows.map((r,i)=>'<div style="margin-top:16px"><span style="font:900 54px Fraunces;color:'+r[2]+'" class="n'+i+'"></span> <span class="k" style="color:var(--ink)">'+r[0]+'</span><div style="margin-top:8px;line-height:0">'+Array.from({length:Math.round(r[1]/per)},(_,j)=>'<span class="dot d'+i+'" style="background:'+r[2]+'"></span>').join("")+'</div></div>').join("")+'<div style="font:500 20px Inter;color:var(--soft);margin-top:12px">'+o.unit+'</div></div>'},
 bar:o=>'<div class="card" style="left:50%;bottom:80px;transform:translateX(-50%);width:1400px;padding:26px 32px"><div class="k">'+o.title+'</div><div style="display:flex;height:76px;margin-top:16px;border-radius:8px;overflow:hidden">'+o.parts.map(p=>'<div class="seg" style="width:'+p[1]+'%;background:'+p[2]+';display:flex;align-items:center;justify-content:center;font:800 28px Inter;color:#fff;white-space:nowrap;overflow:hidden">'+p[0]+'</div>').join("")+'</div>'+(o.note?'<div style="font:500 20px Inter;color:var(--soft);margin-top:10px">'+o.note+'</div>':'')+'</div>',
 gauge:o=>'<div class="card" style="left:50%;top:'+(o.top||80)+'px;transform:translateX(-50%) scale('+(o.zoom||1)+');transform-origin:50% 0;width:900px;padding:22px 32px 26px"><div class="k" style="color:var(--ink)">'+(o.q||"")+'</div><div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:6px"><div style="font:800 30px/1.25 Inter;max-width:600px">'+o.label+'</div><div style="font:900 84px Fraunces;color:var(--red)"><span class="n"></span>%</div></div><div style="height:14px;background:#e3d6bb;border-radius:7px;margin-top:10px"><div class="g" style="height:14px;background:var(--red);border-radius:7px;width:0"></div></div>'+(o.src?'<div style="font:500 18px Inter;color:var(--soft);margin-top:8px">'+o.src+'</div>':'')+'</div>',
 speaker:o=>'<div class="card" style="left:50%;bottom:90px;transform:translateX(-50%);width:700px;padding:24px 34px;text-align:center"><div class="pill">REAL RECORDING · MALTESE</div><div style="font:900 64px Fraunces;margin-top:8px">'+o.name+'</div><div class="k" style="color:var(--soft)">'+o.place+' · '+o.src+'</div><div class="wave" style="height:80px;margin-top:12px;display:flex;gap:6px;align-items:center;justify-content:center">'+Array.from({length:30},()=>'<i style="display:block;width:9px;border-radius:5px;background:var(--red);height:10px"></i>').join("")+'</div></div>',
 hear:o=>(o.quiet||o.word==="keith")?'':'<div class="card" style="left:50%;top:40px;transform:translateX(-50%);padding:10px 22px;display:flex;gap:14px;align-items:center;white-space:nowrap"><span class="pill">▶ LISTEN</span><span style="font:italic 800 38px Fraunces">'+(o.label||o.word)+'</span></div>',
 fadeout:o=>'<div style="position:absolute;inset:0;background:#000"></div>',
 tagline:o=>'<div class="tag"><i></i>'+o.text+'</div>',
 photo:o=>{const sc=Math.max(${W}/o.iw,${H}/o.ih),w=o.iw*sc,h=o.ih*sc,f=o.focus||[.5,.5];o._L=(${W}-w)/2;o._T=(${H}-h)/2;o._w=w;o._h=h;o._ox=o._L+f[0]*w;o._oy=o._T+f[1]*h;o._dx=${W}/2-o._ox;o._dy=${H}/2-o._oy;return '<div style="position:absolute;inset:0;overflow:hidden;background:#0d0d0d"><div class="phi" style="position:absolute;left:'+(o.path?0:o._L)+'px;top:'+(o.path?0:o._T)+'px;width:'+w+'px;height:'+h+'px;transform-origin:'+(o.path?"0 0":f[0]*100+'% '+f[1]*100+'%')+'"><img src="'+o.url+'" style="width:100%;height:100%;display:block">'+(o.hl?'<div class="hl" style="position:absolute;left:'+o.hl[0]*100+'%;top:'+o.hl[1]*100+'%;width:'+(o.hl[2]-o.hl[0])*100+'%;height:'+(o.hl[3]-o.hl[1])*100+'%;border:solid var(--red);border-radius:8px;box-shadow:0 0 0 9999px rgba(0,0,0,.45);opacity:0"></div>':'')+(o.sweep?'<div class="sw" style="position:absolute;left:'+o.sweep.box[0]*100+'%;top:'+o.sweep.box[1]*100+'%;height:'+(o.sweep.box[3]-o.sweep.box[1])*100+'%;width:0;background:rgba(184,51,42,.28);border-bottom:4px solid var(--red)"></div>':'')+(o.mark?'<div class="mk" style="position:absolute;left:'+o.mark[0]*100+'%;top:'+o.mark[1]*100+'%;width:'+(o.mark[2]-o.mark[0])*100+'%;height:'+(o.mark[3]-o.mark[1])*100+'%;border:solid var(--red);border-radius:50%;opacity:0"></div>':'')+'</div><div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0) 60%,rgba(0,0,0,.45) 100%)"></div></div>'+(o.caption?'<div class="card capc" style="left:56px;bottom:56px;padding:14px 22px;max-width:1100px"><div class="k">'+(o.kind||"PHOTO")+'</div><div style="font:800 34px/1.25 Inter;margin-top:4px">'+o.caption+'</div></div>':'')+(o.attrib?'<div class="card att" style="right:56px;bottom:56px;padding:14px 22px;max-width:760px;opacity:0"><div class="k">SOURCE</div><div style="font:600 26px/1.3 Inter;margin-top:4px">'+o.attrib+'</div></div>':'')+'<div style="position:absolute;right:20px;bottom:14px;font:500 16px Inter;color:rgba(255,255,255,.88);text-shadow:0 1px 3px #000">'+o.credit+'</div>'},
 frame:o=>{const fw=o.w||560,fh=Math.round(fw*(o.ih/o.iw));const f=o.focus||[.5,.5];return '<div class="card frm" style="'+(o.side==="center"?"left:"+((${W}-fw-28)/2)+"px":o.side==="left"?"left:90px":"right:90px")+';top:'+(o.top||150)+'px;padding:14px 14px 16px;width:'+(fw+28)+'px"><div style="overflow:hidden;width:'+fw+'px;height:'+fh+'px;border-radius:4px"><img class="fi" src="'+o.url+'" style="width:100%;height:100%;display:block;transform-origin:'+f[0]*100+'% '+f[1]*100+'%"></div>'+(o.caption?'<div style="font:800 26px/1.3 Inter;margin-top:10px">'+o.caption+'</div>':'')+'<div style="font:500 15px Inter;color:var(--soft);margin-top:4px">'+o.credit+'</div></div>'},
 video:o=>'<div style="position:absolute;inset:0;overflow:hidden;background:#000">'+(o.pillar?'<img class="vb" style="position:absolute;left:-60px;top:-60px;width:2040px;height:1200px;object-fit:cover;filter:blur(30px) brightness(.42)">':'')+'<img class="vf" style="position:absolute;'+(o.pillar?'left:0;right:0;top:0;margin:0 auto;height:100%;width:auto;box-shadow:0 0 60px rgba(0,0,0,.6)':'inset:0;width:100%;height:100%')+';transform-origin:'+((o.focus||[.5,.5])[0]*100)+'% '+((o.focus||[.5,.5])[1]*100)+'%"><div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0) 62%,rgba(0,0,0,.4) 100%)"></div></div>'+(o.caption?'<div class="card capc" style="left:56px;bottom:56px;padding:14px 22px;max-width:1100px"><div class="k">'+(o.kind||"FOOTAGE")+'</div><div style="font:800 34px/1.25 Inter;margin-top:4px">'+o.caption+'</div></div>':'')+'<div style="position:absolute;right:20px;bottom:14px;font:500 16px Inter;color:rgba(255,255,255,.88);text-shadow:0 1px 3px #000">'+o.credit+'</div>',
 lock:o=>{let h='<div class="lk" style="position:absolute;inset:0">'+(o.base?'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,#10283a,#06141d 75%)"></div>':'')+(o.dark?'<div style="position:absolute;inset:0;background:rgba(6,22,34,.88);backdrop-filter:blur(6px)"></div>':'');
   o.rows.forEach((r,i)=>{const y=(o.top||330)+i*(o.gap||230);h+='<div class="lr" data-i="'+i+'" style="position:absolute;left:0;right:0;top:'+y+'px;height:200px;opacity:0"><div class="lpl" style="position:absolute;left:110px;top:78px"><span class="pill" style="font-size:30px;padding:8px 16px;background:'+(r.color||D.C.red)+'">'+r.lang+'</span></div>'+(r.script?'<div class="ar lscript" style="position:absolute;right:120px;top:36px;font-size:84px;color:#f3e6cc;text-shadow:0 3px 10px rgba(0,0,0,.6)">'+r.script+'</div>':'')+r.parts.map((p,j)=>'<span class="lp" data-c="'+(p[1]?1:0)+'" data-col="'+(p[2]??-1)+'" style="position:absolute;left:0;top:70px;font:'+(p[1]?"italic 900 150px/1":"italic 800 150px/1")+' Fraunces;color:#f3e6cc;text-shadow:0 4px 14px rgba(0,0,0,.55);white-space:pre">'+p[0]+'</span>').join("")+(r.gloss?'<div class="lg" style="position:absolute;left:112px;top:140px;font:700 40px Inter;color:#e9dcc2">“'+r.gloss+'”</div>':'')+'</div>'});
   h+=(o.cols||["K","T","B"]).map((c,j)=>'<div class="lc" style="position:absolute;top:'+((o.top||330)-40)+'px;height:'+((o.rows.length)*(o.gap||230)+40)+'px;width:6px;background:var(--red);opacity:0;border-radius:3px"></div><div class="ll" style="position:absolute;top:'+((o.top||330)-110)+'px;font:900 64px Fraunces;color:var(--red);opacity:0">'+c+'</div>').join("");
   return h+'</div>'},
 twin:o=>{let h='<div class="tw" style="position:absolute;inset:0;background:linear-gradient(180deg,'+D.C.sea+','+D.C.sea2+')">';
   h+='<div class="tyear" style="position:absolute;left:50%;top:40px;transform:translateX(-50%);font:900 120px/1 Fraunces;color:#f3e6cc;text-shadow:0 4px 14px rgba(0,0,0,.4)"></div>';
   o.panels.forEach((p,i)=>{const x=i?980:40;h+='<div class="tpan" style="position:absolute;left:'+x+'px;top:190px;width:900px;height:620px;border-radius:14px;background:rgba(255,255,255,.05);border:2px solid rgba(243,230,204,.18)"><svg viewBox="0 0 900 620" style="position:absolute;inset:0;filter:drop-shadow(2px 6px 0 rgba(30,15,5,.45)) drop-shadow(4px 12px 14px rgba(0,0,0,.4))"><g transform="translate(450 330) scale('+p.z+') translate('+(-p.cx)+' '+(-p.cy)+')"><path class="tp" data-k="'+p.k+'" d="'+p.d+'" fill="'+D.C.arab+'" stroke="rgba(40,20,10,.5)" stroke-width="1" vector-effect="non-scaling-stroke"/></g></svg>'+(p.k==="malta"?'<div style="position:absolute;left:50%;top:330px;width:150px;height:150px;transform:translate(-50%,-50%);border:3px dashed rgba(243,230,204,.7);border-radius:50%"></div>':'')+'<div style="position:absolute;left:24px;top:18px;font:900 54px Fraunces;color:#f3e6cc">'+(p.k==="malta"?"MALTA":"SICILY")+'</div><div class="tst" data-k="'+p.k+'" style="position:absolute;right:20px;top:24px;padding:6px 14px;border-radius:6px;font:800 24px Inter;letter-spacing:.1em;color:#fff"></div><div class="tnote" data-k="'+p.k+'" style="position:absolute;left:24px;right:24px;bottom:20px;font:700 32px/1.25 Inter;color:#f3e6cc;text-shadow:0 2px 6px rgba(0,0,0,.5)"></div></div>'});
   h+='<div style="position:absolute;left:40px;right:40px;top:860px;height:6px;background:rgba(243,230,204,.25);border-radius:3px"></div><div class="tprog" style="position:absolute;left:40px;top:860px;height:6px;width:0;background:var(--red);border-radius:3px"></div>';
   let lastX=-999,row=0;o.steps.forEach((s,j)=>{const x=40+(s.year-o.y0)/(o.y1-o.y0)*1840;if(s.mark){row=(x-lastX<90)?1-row:0;lastX=x}h+='<div class="ttick" style="position:absolute;left:'+x+'px;top:846px;width:4px;height:34px;background:rgba(243,230,204,.6);opacity:0"></div>'+(s.mark?'<div class="tlab" style="position:absolute;left:'+x+'px;top:'+(890+row*30)+'px;transform:translateX(-50%);font:700 24px Inter;color:#f3e6cc;white-space:nowrap;opacity:0">'+s.mark+'</div>':'')});
   h+='<div style="position:absolute;left:40px;top:930px;font:600 22px Inter;color:rgba(243,230,204,.75)">Both islands drawn at the same scale</div></div>';return h},
table:o=>'', board:o=>'', desk:o=>'',
 plate:o=>'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 42%,#173246,#07131b 78%)"></div>'+(o.url?'<img src="'+o.url+'" style="position:absolute;inset:-40px;width:2000px;height:1160px;object-fit:cover;filter:blur(16px) brightness(.38) saturate(.8)">':'')+'<div style="position:absolute;inset:0;background:url(${furl(TEX)}) 0 0/900px;mix-blend-mode:overlay;opacity:.25"></div>',
 words:o=>{let h='<div style="position:absolute;inset:0;'+(o.bg==='dark'?'background:#0a1620':'background:linear-gradient(to bottom,rgba(4,12,18,0) 14%,rgba(4,12,18,.66) 34%,rgba(4,12,18,.66) 80%,rgba(4,12,18,0) 96%)')+'"></div>';
   o.items.forEach((it,i)=>{const y=(o.top||330)+i*(o.gap||250);h+='<div class="wrow" data-i="'+i+'" style="position:absolute;left:0;right:0;top:'+y+'px;text-align:center"><div class="wlab" style="display:inline-block;opacity:0;font:800 34px Inter;letter-spacing:.14em;color:#fff;background:'+(it.color||'#b8332a')+';border-radius:6px;padding:6px 18px">'+(it.label||'')+'</div><div class="wtxt" style="font:italic 900 160px/1.05 Fraunces;color:#f3e6cc;text-shadow:0 6px 22px rgba(0,0,0,.65);white-space:nowrap;transform-origin:50% 60%">'+[...it.text].map(ch=>'<span class="wl" style="opacity:0">'+ch+'</span>').join('')+(it.script?'<span class="ar wscr" style="font-size:104px;margin-left:46px;opacity:0;font-style:normal">'+it.script+'</span>':'')+'</div></div>'});return h},
 dist:o=>'', bubble:o=>'<div class="card bub" style="padding:10px 20px;font:italic 800 36px Fraunces;white-space:nowrap">'+o.text+'</div>',
};
D.OV.forEach((o,i)=>{const el=document.createElement("div");el.style.cssText="position:absolute;inset:0;opacity:0";el.innerHTML=BUILD[o.type](o);ov.appendChild(el);o.el=el;
  if(o.type==="dist"){R.insertAdjacentHTML("beforeend",'<path id="ds'+i+'" d="M'+o.a[0]+','+o.a[1]+' L'+o.b[0]+','+o.b[1]+'" stroke="#f3e6cc" stroke-width="3" stroke-dasharray="8 8" vector-effect="non-scaling-stroke" opacity="0"/>');el.innerHTML='<div class="card dl" style="padding:8px 16px;font:800 30px Inter;white-space:nowrap">'+o.text+'</div>'}
  if(o.type==="lock")o.measure=()=>{o.measured=1;const op=el.style.opacity;el.style.opacity=1;el.querySelectorAll(".lr").forEach((row,ri)=>{let x=120;const sp=row.querySelectorAll(".lp");sp.forEach(s=>{s.dataset.x0=x;s.dataset.w=s.offsetWidth||s.getBoundingClientRect().width;x+=+s.dataset.w});const width=x-120;const off=(${W}-width)/2-120;sp.forEach(s=>{s.dataset.x0=+s.dataset.x0+off;s.style.left=s.dataset.x0+"px"})});
    const colX=(o.colX||[620,960,1300]);o._colX=colX;el.querySelectorAll(".lc").forEach((c,j)=>c.style.left=(colX[j]+18)+"px");el.querySelectorAll(".ll").forEach((c,j)=>c.style.left=(colX[j]-4)+"px");el.style.opacity=op}});
// ───── v4 scenes: one shared 3D table, one investigation board, one desk per document ─────
const TB=D.table,BD=D.board,DK=D.docs;
function colAt(k,t){const K=D.fillK[k]||[];let col=[233,220,191,0],prev=col;for(const f of K){if(f.t>t)break;const target=hex(f.c);const kk=eo((t-f.t)/0.8);col=mix(prev,target,kk);prev=kk>=1?target:col}return col}
const rgba=(c)=>'rgba('+Math.round(c[0])+','+Math.round(c[1])+','+Math.round(c[2])+','+c[3]+')';
const lerpCam=(a,b,q)=>{const o={};for(const k in a)o[k]=a[k]+((b[k]??a[k])-a[k])*q;return o};
const dofMask=(y,band)=>{const a=(y-band/2)*100,b=(y+band/2)*100;return 'linear-gradient(to bottom, black 0%, black '+Math.max(0,a-16)+'%, transparent '+a+'%, transparent '+b+'%, black '+Math.min(100,b+16)+'%, black 100%)'};
const light='<div style="position:absolute;inset:0;background:radial-gradient(ellipse 70% 60% at 76% 14%,rgba(255,205,150,.13),transparent 70%);pointer-events:none"></div><div style="position:absolute;inset:0;background:radial-gradient(ellipse 88% 82% at 50% 46%,transparent 48%,rgba(0,0,0,.72) 100%);pointer-events:none"></div>';
function objHTML(ob){
  if(ob.kind==='coin')return '<div style="width:'+ob.w+'px;height:'+ob.w+'px;border-radius:50%;background:url('+ob.url+') '+(ob.bx??50)+'% '+(ob.by??50)+'%/'+(ob.bs??300)+'% auto no-repeat;box-shadow:inset -5px -7px 12px rgba(0,0,0,.5),inset 4px 5px 9px rgba(255,230,190,.25)"></div>';
  if(ob.kind==='print')return '<div style="background:#f3eee2;padding:14px 14px 0;box-shadow:0 2px 0 rgba(0,0,0,.25)"><img src="'+ob.url+'" style="width:100%;display:block"><div style="font:800 22px/44px Inter;color:#3a2c1e;text-align:center;white-space:nowrap;overflow:hidden">'+(ob.cap||'')+'</div></div>';
  return '<div style="background:#f6efdc;padding:22px 26px;border-top:12px solid '+(ob.color||'#b8332a')+';min-height:'+ob.h+'px"><div style="font:800 18px Inter;letter-spacing:.14em;color:#b8332a">'+(ob.title||'')+'</div><div style="font:800 34px/1.18 Fraunces;color:#1f1a14;margin-top:8px">'+(ob.text||'')+'</div></div>'}
let tbl=null,brd=null;const desks={};
if(TB){tbl=document.createElement('div');tbl.style.cssText='position:absolute;inset:0;opacity:0;display:none;background:#0b0806;overflow:hidden';
  let h='<div style="position:absolute;inset:0;perspective:1500px;perspective-origin:50% 40%"><div class="tbw" style="position:absolute;left:960px;top:540px;width:0;height:0;transform-style:preserve-3d">';
  h+='<div style="position:absolute;left:'+(-TB.w/2-2600)+'px;top:'+(-TB.h/2-3200)+'px;width:'+(TB.w+5200)+'px;height:'+(TB.h+5200)+'px;background:url('+TB.tex+') 0 0/1500px 1500px"></div>';
  h+='<div style="position:absolute;left:'+(-TB.w/2)+'px;top:'+(-TB.h/2)+'px;width:'+TB.w+'px;height:'+TB.h+'px;background:#efe4c9;overflow:hidden;box-shadow:24px 34px 60px rgba(0,0,0,.6)"><svg width="'+TB.w+'" height="'+TB.h+'" style="position:absolute;inset:0"><rect width="'+TB.w+'" height="'+TB.h+'" fill="#a3bec7"/>';
  h+=TB.grat.map(d=>'<path d="'+d+'" fill="none" stroke="rgba(40,70,90,.18)" stroke-width="2"/>').join('');
  h+='<path d="'+TB.land+'" fill="#efe3c6" stroke="#8f7a58" stroke-width="2.4" stroke-linejoin="round"/>';
  h+=Object.entries(TB.regs).map(([k,d])=>'<path class="trg" data-k="'+k+'" d="'+d+'" fill="transparent" stroke="#4a3826" stroke-width="3" stroke-opacity="0"/>').join('');
  h+=TB.arrows.map((a,i)=>'<path class="tar" data-i="'+i+'" d="'+a.d+'" fill="none" stroke="'+(a.color||'#6f8fb3')+'" stroke-width="'+(a.dash?7:12)+'" stroke-linecap="round" opacity="0"'+(a.dash?' data-dash="1"':'')+'/>'+(a.label?'<text class="tal" data-i="'+i+'" x="'+a.lx+'" y="'+a.ly+'" text-anchor="middle" font-family="Inter" font-weight="800" font-size="40" fill="#1f1a14" stroke="#efe4c9" stroke-width="9" paint-order="stroke" opacity="0">'+a.label+'</text>':'')).join('');
  h+=TB.labels.map(l=>'<text x="'+l.x+'" y="'+l.y+'" text-anchor="middle" font-family="Inter" font-weight="800" font-size="'+l.size+'" letter-spacing="'+(l.size*0.18)+'" fill="#33281c" stroke="#efe4c9" stroke-width="'+(l.size*0.16)+'" paint-order="stroke">'+l.txt+'</text>').join('');
  h+='<g transform="translate('+(TB.w-150)+',150)"><circle r="62" fill="none" stroke="#33281c" stroke-width="3"/><path d="M0,-52 L16,10 L0,0 L-16,10 Z" fill="#b8332a"/><text y="-70" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="#33281c">N</text></g>';
  h+='<g transform="translate(90,'+(TB.h-90)+')"><rect width="'+TB.km100+'" height="14" fill="#33281c"/><rect width="'+(TB.km100/2)+'" height="14" fill="#efe4c9" stroke="#33281c" stroke-width="2"/><text y="-14" font-family="Inter" font-weight="800" font-size="30" fill="#33281c">100 KM</text></g>';
  if(TB.title){const T2=TB.title;h+='<g class="tttl" opacity="0" transform="translate('+T2.xy[0]+','+T2.xy[1]+') rotate('+(T2.rot||-4)+')">'+T2.lines.map((ln,i)=>'<text y="'+(i*T2.size*1.12)+'" text-anchor="middle" font-family="Fraunces" font-weight="900" font-size="'+T2.size+'" fill="#b8332a" stroke="#efe4c9" stroke-width="'+(T2.size*0.12)+'" paint-order="stroke">'+ln+'</text>').join('')+'</g>'}
  h+='</svg><div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(80,50,20,0) 62%,rgba(80,50,20,.35) 100%)"></div></div>';
  TB.objs.forEach((ob,i)=>{h+='<div class="tob" data-i="'+i+'" style="position:absolute;left:'+(ob.x-TB.w/2)+'px;top:'+(ob.y-TB.h/2)+'px;width:0;height:0;transform-style:preserve-3d;opacity:0"><div class="tsh" style="position:absolute;left:'+(-ob.w/2+10)+'px;top:'+(-ob.h/2+16)+'px;width:'+ob.w+'px;height:'+ob.h+'px;border-radius:'+(ob.kind==='coin'?'50%':'6px')+';background:rgba(0,0,0,.6);filter:blur(12px);transform:rotate('+(ob.rot||0)+'deg)"></div><div class="tod" style="position:absolute;left:'+(-ob.w/2)+'px;top:'+(-ob.h/2)+'px;width:'+ob.w+'px;transform-origin:50% 50%">'+objHTML(ob)+'</div></div>'});
  h+='</div></div><div class="tdof" style="position:absolute;inset:0;pointer-events:none"></div>'+light;
  tbl.innerHTML=h;ov.prepend(tbl)}
if(BD){brd=document.createElement('div');brd.style.cssText='position:absolute;inset:0;opacity:0;display:none;background:#0a1117;overflow:hidden';
  const tagH=(c,def,col)=>'<div class="btag" style="display:inline-block;font:800 19px Inter;letter-spacing:.14em;color:#fff;background:'+(c.tagColor||col||'#6d5f4c')+';border-radius:5px;padding:5px 11px">'+(c.tag||def)+'</div>';
  const citeH=(c)=>c.cite?'<div style="font:600 21px/1.3 Inter;color:#6d5f4c;margin-top:10px">'+c.cite+'</div>':'';
  const card=(c)=>{const pin='<div style="position:absolute;left:50%;top:-14px;width:32px;height:32px;margin-left:-16px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#ee7a6b,#a3241b 60%,#5e120c);box-shadow:3px 7px 7px rgba(0,0,0,.55);z-index:2"></div>';let b;
    if(c.kind==='head')return '<div class="bc" data-i="'+c._i+'" style="position:absolute;left:'+(c.x-BD.w/2-c.w/2)+'px;top:'+(c.y-BD.h/2)+'px;width:'+c.w+'px;text-align:'+(c.align||'center')+'"><div style="font:900 '+(c.size||78)+'px/1 Fraunces;letter-spacing:.08em;color:'+(c.color||'#f3e6cc')+'">'+c.text+'</div>'+(c.sub?'<div style="font:700 24px Inter;letter-spacing:.16em;color:rgba(243,230,204,.62);margin-top:10px">'+c.sub+'</div>':'')+'</div>';
    if(c.kind==='q')b='<div style="background:#f6efdc;padding:28px 38px 32px;border-top:16px solid #b8332a"><div style="font:800 22px Inter;letter-spacing:.16em;color:#b8332a">'+(c.tag||'THE QUESTION')+'</div><div style="font:900 54px/1.08 Fraunces;color:#1f1a14;margin-top:12px">'+c.text+'</div></div>';
    else if(c.kind==='photo')b='<div style="background:#f4f0e6;padding:16px;display:flex;gap:20px;align-items:flex-start"><img src="'+c.url+'" style="width:'+(c.iw2||220)+'px;height:'+(c.crop||200)+'px;object-fit:cover;object-position:'+(c.pos||'50% 50%')+';display:block;flex:none"><div style="flex:1;min-width:0;padding-top:4px">'+(c.tag?tagH(c,'',c.tagColor||'#3d5f9a'):'')+'<div style="font:800 28px/1.2 Inter;color:#2a2018;margin-top:'+(c.tag?10:0)+'px">'+(c.title||'')+'</div>'+(c.text?'<div class="bold" style="position:relative;font:800 30px/1.18 Fraunces;color:#1f1a14;margin-top:6px">'+c.text+'</div>':'')+citeH(c)+'</div></div>';
    else if(c.kind==='word')b='<div style="background:#f6efdc;padding:24px 32px 28px;text-align:center"><div style="font:800 20px Inter;letter-spacing:.14em;color:#b8332a">'+(c.tag||'')+'</div><div style="font:italic 900 70px/1.1 Fraunces;color:#1f1a14;margin-top:6px">'+c.text+'</div>'+(c.sub?'<div style="font:600 26px/1.3 Inter;color:#6d5f4c;margin-top:8px">'+c.sub+'</div>':'')+'</div>';
    else if(c.kind==='conclusion')b='<div style="background:#f2c46b;padding:24px 30px 30px"><div style="font:800 19px Inter;letter-spacing:.14em;color:#7a1f18">'+(c.tag||'WHAT THE EVIDENCE SUPPORTS')+'</div><div style="font:900 40px/1.14 Fraunces;color:#1f1a14;margin-top:10px">'+c.text+'</div>'+(c.sub?'<div style="font:700 24px/1.35 Inter;color:#5a3a14;margin-top:12px">'+c.sub+'</div>':'')+'</div>';
    else if(c.kind==='find')b='<div style="background:#fbf3df;padding:20px 26px 24px;border-left:14px solid '+(c.edge||'#d39a3c')+'"><div style="font:800 18px Inter;letter-spacing:.14em;color:#8a5a14">'+(c.tag||'FINDING')+'</div><div class="bold" style="position:relative;font:800 34px/1.16 Fraunces;color:#1f1a14;margin-top:8px">'+c.text+'<div class="bstrike" style="position:absolute;left:-6px;top:50%;height:7px;width:0;background:#b8332a;border-radius:4px"></div></div><div class="bnew" style="font:800 34px/1.16 Fraunces;color:#b8332a;margin-top:8px"></div>'+citeH(c)+'</div>';
    else if(c.kind==='open')b='<div style="background:#ece6d6;padding:20px 26px 24px;outline:5px dashed #8c8577;outline-offset:-5px"><div style="font:800 18px Inter;letter-spacing:.14em;color:#5f594d">'+(c.tag||'OPEN QUESTION')+'</div><div style="font:italic 800 34px/1.16 Fraunces;color:#1f1a14;margin-top:8px">'+c.text+'</div>'+citeH(c)+'</div>';
    else b='<div style="background:#f3ead4;padding:22px 28px 26px">'+tagH(c,'NOTE')+'<div class="bold" style="position:relative;font:800 36px/1.16 Fraunces;color:#1f1a14;margin-top:12px">'+c.text+'<div class="bstrike" style="position:absolute;left:-6px;top:50%;height:7px;width:0;background:#b8332a;border-radius:4px"></div></div><div class="bnew" style="font:800 36px/1.16 Fraunces;color:#b8332a;margin-top:10px"></div>'+citeH(c)+'</div>';
    return '<div class="bc" data-i="'+c._i+'" style="position:absolute;left:'+(c.x-BD.w/2-c.w/2)+'px;top:'+(c.y-BD.h/2)+'px;width:'+c.w+'px;opacity:0;transform-origin:50% 0"><div style="position:relative;transform:rotate('+(c.rot||0)+'deg);box-shadow:6px 12px 18px rgba(0,0,0,.5)">'+pin+b+'<div class="bv" style="position:absolute;inset:-2px;background:#0a1117;opacity:0;z-index:3"></div></div></div>'};
  BD.cards.forEach((c,i)=>c._i=i);
  const LC={solid:'#c4372c',dash:'#c4372c',blue:'#3f74b8',honey:'#d9a03c',open:'#9a9384'};
  let h='<style>.hl{background:linear-gradient(rgba(242,196,107,.85),rgba(242,196,107,.85)) no-repeat 0 88%;background-size:0% 46%;-webkit-box-decoration-break:clone;box-decoration-break:clone;padding:0 2px}</style><div style="position:absolute;inset:0;perspective:1800px;perspective-origin:50% 45%"><div class="bw" style="position:absolute;left:960px;top:540px;width:0;height:0">';
  h+='<div style="position:absolute;left:'+(-BD.w/2-40)+'px;top:'+(-BD.h/2-40)+'px;width:'+(BD.w+80)+'px;height:'+(BD.h+80)+'px;background:#3a2a1c;box-shadow:0 20px 40px rgba(0,0,0,.6)"></div>';
  h+='<div style="position:absolute;left:'+(-BD.w/2)+'px;top:'+(-BD.h/2)+'px;width:'+BD.w+'px;height:'+BD.h+'px;background:radial-gradient(ellipse at 50% 40%,#29445a 0%,#16283a 62%,#0d1a26 100%)"></div>';
  h+='<svg width="'+BD.w+'" height="'+BD.h+'" style="position:absolute;left:'+(-BD.w/2)+'px;top:'+(-BD.h/2)+'px;overflow:visible">'+BD.lines.map(l=>'<line x1="'+l[0]+'" y1="'+l[1]+'" x2="'+l[2]+'" y2="'+l[3]+'" stroke="rgba(243,230,204,.35)" stroke-width="5" stroke-dasharray="'+(l[4]?'18 16':'none')+'" stroke-linecap="round"/>').join('')+'</svg>';
  h+=BD.cards.map(card).join('');
  h+='<svg class="bstr" width="'+BD.w+'" height="'+BD.h+'" style="position:absolute;left:'+(-BD.w/2)+'px;top:'+(-BD.h/2)+'px;overflow:visible">'+BD.links.map((l,i)=>'<g class="blg" data-i="'+i+'" opacity="0"><path class="bl" fill="none" stroke="'+LC[l.style]+'" stroke-width="6" stroke-linecap="round"'+(l.style==='dash'||l.style==='open'?' stroke-dasharray="20 14"':'')+'/><circle class="bp0" r="11" fill="'+LC[l.style]+'"/><circle class="bp1" r="11" fill="'+LC[l.style]+'"/></g>').join('')+'</svg>';
  h+=BD.links.map((l,i)=>l.label?'<div class="blab" data-i="'+i+'" style="position:absolute;opacity:0;transform:translate(-50%,-50%);font:800 24px Inter;letter-spacing:.14em;color:#fff;background:'+LC[l.style]+';border:3px solid #f3e6cc;border-radius:8px;padding:6px 14px;white-space:nowrap;box-shadow:3px 6px 10px rgba(0,0,0,.45)">'+(l.style==='open'?'? ':'')+l.label.toUpperCase()+'</div>':'').join('');
  h+='</div></div><div class="bdof" style="position:absolute;inset:0;pointer-events:none"></div>'+light;
  h+='<div class="bcap" style="position:absolute;left:50%;bottom:58px;transform:translateX(-50%);max-width:1560px;opacity:0;background:rgba(246,239,220,.96);border-left:12px solid #b8332a;padding:16px 28px 18px;box-shadow:0 10px 26px rgba(0,0,0,.5)"><div class="bck" style="font:800 20px Inter;letter-spacing:.16em;color:#b8332a"></div><div class="bct" style="font:800 40px/1.2 Fraunces;color:#1f1a14;margin-top:4px"></div></div>';
  brd.innerHTML=h;ov.prepend(brd)}
for(const k in DK){const d=DK[k],PW=1000,PH=Math.round(PW*d.ih/d.iw);d.PW=PW;d.PH=PH;const el=document.createElement('div');el.style.cssText='position:absolute;inset:0;opacity:0;display:none;background:#0b0705;overflow:hidden';
  el.innerHTML='<div style="position:absolute;inset:0;perspective:1500px;perspective-origin:50% 42%"><div class="dw" style="position:absolute;left:960px;top:540px;width:0;height:0;transform-style:preserve-3d"><div style="position:absolute;left:-3000px;top:-2200px;width:6000px;height:4400px;background:url('+d.tex+') 0 0/1400px 1400px"></div><div class="pg" style="position:absolute;left:'+(-PW/2)+'px;top:'+(-PH/2)+'px;width:'+PW+'px;height:'+PH+'px;box-shadow:12px 18px 34px rgba(0,0,0,.6)"><img src="'+d.url+'" style="width:100%;height:100%;display:block"><div style="position:absolute;inset:0;background:linear-gradient(225deg,rgba(255,214,160,.10) 0%,rgba(0,0,0,0) 40%,rgba(20,12,6,.30) 100%)"></div><div class="dsw" style="position:absolute;width:0;background:rgba(242,196,107,.42);border-bottom:3px solid #b8332a;opacity:0"></div><div class="dln" style="position:absolute;border:4px solid #b8332a;border-radius:6px;opacity:0"></div><div class="dmk" style="position:absolute;border:4px solid #b8332a;border-radius:50%;opacity:0"></div></div></div></div><div class="ddof" style="position:absolute;inset:0;pointer-events:none"></div>'+light+'<div style="position:absolute;left:22px;bottom:16px;font:500 16px Inter;color:rgba(225,225,225,.75)">'+d.credit+'</div>';
  ov.prepend(el);desks[k]=el}
let bdMeasured=false;
function boardMeasure(){bdMeasured=true;BD.cards.forEach(c=>{const e=brd.querySelector('.bc[data-i="'+c._i+'"]');c._h=e.offsetHeight});
  BD.links.forEach((l,i)=>{const A=BD.cards[l.a],B=BD.cards[l.b];const acx=A.x+(l.ax||0),acy=A.y+A._h/2,bcx=B.x+(l.bx||0),bcy=B.y+B._h/2,dx=bcx-acx,dy=bcy-acy;let p0,p2,c;
    if(l.route==='below'){p0=[acx,A.y+A._h];p2=[bcx,B.y+B._h];c=[(p0[0]+p2[0])/2,Math.max(p0[1],p2[1])+(l.sag||130)]}
    else if(Math.abs(dx)>Math.abs(dy)*1.1){const s=dx>0?1:-1;p0=[acx+s*A.w/2,acy];p2=[bcx-s*B.w/2,bcy];c=[(p0[0]+p2[0])/2,(p0[1]+p2[1])/2+46]}
    else{const s=dy>0?1:-1;p0=[acx,s>0?A.y+A._h:A.y];p2=[bcx,s>0?B.y:B.y+B._h];c=[(p0[0]+p2[0])/2+40,(p0[1]+p2[1])/2]}
    const g=brd.querySelector('.blg[data-i="'+i+'"]'),e=g.querySelector('.bl');e.setAttribute('d','M'+p0[0]+','+p0[1]+' Q'+c[0]+','+c[1]+' '+p2[0]+','+p2[1]);l._L=e.getTotalLength();
    g.querySelector('.bp0').setAttribute('cx',p0[0]);g.querySelector('.bp0').setAttribute('cy',p0[1]);g.querySelector('.bp1').setAttribute('cx',p2[0]);g.querySelector('.bp1').setAttribute('cy',p2[1]);
    const lb=brd.querySelector('.blab[data-i="'+i+'"]');if(lb){const u=l.at??0.5,w0=(1-u)*(1-u),w1=2*u*(1-u),w2=u*u;lb.style.left=(w0*p0[0]+w1*c[0]+w2*p2[0]-BD.w/2)+'px';lb.style.top=(w0*p0[1]+w1*c[1]+w2*p2[1]-BD.h/2)+'px'}})}
const BKF=()=>Math.min(1920*0.96/(BD.w+80),1080*0.94/(BD.h+80));
function bview(sp){let v=sp.view,x=0,y=0,k=BKF();
  if(sp.x!=null){x=sp.x-BD.w/2;y=sp.y-BD.h/2;k=sp.k||k}
  else if(v&&v!=='full'){const ids=Array.isArray(v)?v:[v];const cs=ids.map(id=>BD.cards.find(c=>c.id===id)).filter(Boolean);if(cs.length){const x0=Math.min(...cs.map(c=>c.x-c.w/2)),x1=Math.max(...cs.map(c=>c.x+c.w/2)),y0=Math.min(...cs.map(c=>c.y)),y1=Math.max(...cs.map(c=>c.y+c._h));x=(x0+x1)/2-BD.w/2;y=(y0+y1)/2-BD.h/2;
    k=sp.k||(cs.length===1?Math.min(0.6*1080/(y1-y0),0.6*1920/(x1-x0),2.1):Math.min(0.84*1920/(x1-x0+120),0.72*1080/(y1-y0+120),1.5))}}
  return {x:x+(sp.dx||0),y:y+(sp.dy||0),k}}
const bshot=(id)=>D.OV.find(o=>o.type==='board'&&o.bid===id);
function bend(o){const v=bview(o.spec);return {x:v.x,y:v.y,k:v.k*(1+(o.spec.push??0.04))}}
function bcam(o,t){const sp=o.spec,v1=bview(sp),dur=o.tOut-o.tIn,push=sp.push??0.04;let v0=null;
  if(sp.from)v0=bview({view:sp.from});else if(o.pbid!=null&&!o.cut){const p=bshot(o.pbid);if(p)v0=bend(p)}
  const tg=v0?Math.min(sp.glideT??1.3,dur*0.5):0;
  if(v0&&t-o.tIn<tg){const e=ease((t-o.tIn)/tg),dist=Math.hypot(v1.x-v0.x,v1.y-v0.y),dip=Math.min(0.4,dist*Math.min(v0.k,v1.k)/3200);
    return {x:v0.x+(v1.x-v0.x)*e,y:v0.y+(v1.y-v0.y)*e,k:Math.exp(Math.log(v0.k)*(1-e)+Math.log(v1.k)*e)*(1-dip*Math.sin(Math.PI*e))}}
  const q=cl((t-o.tIn-tg)/Math.max(0.1,dur-tg),0,1);return {x:v1.x,y:v1.y,k:v1.k*(1+push*Math.sin(q*Math.PI/2))}}
function blit(o,id){return !o.lit||o.lit.includes(id)?0:0.62}
function scenes(t){
  // table
  if(tbl){const a=D.OV.find(o=>o.type==='table'&&t>=o.tIn&&t<o.tOut);tbl.style.opacity=a?1:0;tbl.style.display=a?'block':'none';if(a){const q=ease(cl((t-a.tIn)/(a.tOut-a.tIn),0,1));const c=lerpCam(a.c0,a.c1,q);
    tbl.querySelector('.tbw').style.transform='rotateX('+c.tilt+'deg) rotateZ('+c.rz+'deg) scale('+c.zoom+') translate('+(-c.x)+'px,'+(-c.y)+'px)';
    tbl.querySelectorAll('.trg').forEach(e=>{const col=colAt(e.dataset.k,t);e.setAttribute('fill',rgba(col));e.setAttribute('stroke-opacity',col[3])});
    TB.objs.forEach((ob,i)=>{const e=tbl.querySelector('.tob[data-i="'+i+'"]');if(t<ob.t){e.style.opacity=0;return}const k=cl((t-ob.t)/0.42,0,1),z=(1-eo(k))*460;e.style.opacity=1;e.querySelector('.tod').style.transform='translateZ('+(z+2)+'px) rotate('+(ob.rot||0)+'deg)';const sh=e.querySelector('.tsh');sh.style.opacity=0.6*(1-z/700);sh.style.filter='blur('+(12+z/18)+'px)'});
    TB.arrows.forEach((ar,i)=>{const e=tbl.querySelector('.tar[data-i="'+i+'"]');if(t<ar.t){e.setAttribute('opacity',0);return}const L=e.getTotalLength();e.setAttribute('opacity',1);const pr=eo((t-ar.t)/1.2);if(e.dataset.dash){e.style.strokeDasharray='4 22';e.style.strokeDashoffset=0;e.style.clipPath='none';e.setAttribute('opacity',pr)}else{e.style.strokeDasharray=L;e.style.strokeDashoffset=L*(1-pr)}const tl=tbl.querySelector('.tal[data-i="'+i+'"]');if(tl)tl.setAttribute('opacity',eo((t-ar.t-0.6)/0.3))});
    if(TB.title){const g=tbl.querySelector('.tttl');g.setAttribute('opacity',cl((t-TB.title.t0)/0.35,0,1)*cl((TB.title.t1-t)/0.3,0,1))}
    const f=a.focus||{y:.5,band:.55,blur:Math.max(0,(c.tilt-24)/5)};const dv=tbl.querySelector('.tdof');if(f.blur>0.4){dv.style.backdropFilter='blur('+f.blur+'px)';dv.style.webkitMaskImage=dofMask(f.y,f.band)}else dv.style.backdropFilter='none'}}
  // board
  if(brd){const a=D.OV.find(o=>o.type==='board'&&t>=o.tIn&&t<o.tOut);brd.style.opacity=a?1:0;brd.style.display=a?'block':'none';if(a){if(!bdMeasured)boardMeasure();
    const cm=bcam(a,t),pa=a.pbid!=null&&!a.cut?bshot(a.pbid):null,mix=pa?eo((t-a.tIn)/0.6):1;
    brd.querySelector('.bw').style.transform='rotateX(6deg) rotateY(-2deg) scale('+cm.k+') translate('+(-cm.x)+'px,'+(-cm.y)+'px)';
    const veil=(id)=>pa?blit(pa,id)*(1-mix)+blit(a,id)*mix:blit(a,id);
    BD.cards.forEach(c=>{const e=brd.querySelector('.bc[data-i="'+c._i+'"]');const vv=e.querySelector('.bv');if(vv)vv.style.opacity=veil(c.id);if(c.fixed){e.style.opacity=1-veil(c.id)*0.9;return}if(t<c.t){e.style.opacity=0;return}const kk=eo((t-c.t)/0.3);e.style.opacity=kk;e.style.transform='scale('+(1.18-0.18*kk)+')';
      if(c.hlT<1e8){const p=eo((t-c.hlT)/0.7);e.querySelectorAll('.hl').forEach(m=>m.style.backgroundSize=(p*100)+'% 46%')}});
    BD.rewrites.forEach(rw=>{const e=brd.querySelector('.bc[data-i="'+rw.i+'"]');const st=e.querySelector('.bstrike'),nw=e.querySelector('.bnew'),tg=e.querySelector('.btag'),old=e.querySelector('.bold');if(!st)return;
      if(t<rw.t){st.style.width='0';nw.textContent='';return}const k1=eo((t-rw.t)/0.45);st.style.width='calc('+(k1*100)+'% + 12px)';old.style.color=k1>0.6?'rgba(31,26,20,.42)':'#1f1a14';
      const n=Math.max(0,Math.floor((t-rw.t-0.5)*42));nw.textContent=rw.text.slice(0,n);if(t>rw.t+0.45&&rw.tag&&tg){tg.textContent=rw.tag;tg.style.background=rw.tagColor||'#b8332a'}});
    BD.links.forEach((l,i)=>{const g=brd.querySelector('.blg[data-i="'+i+'"]'),lb=brd.querySelector('.blab[data-i="'+i+'"]');if(t<l.t){g.setAttribute('opacity',0);if(lb)lb.style.opacity=0;return}
      const A=BD.cards[l.a],B=BD.cards[l.b],dim=Math.max(veil(A.id),veil(B.id)),op=1-dim*0.75,e=g.querySelector('.bl'),pr=eo((t-l.t)/0.8);g.setAttribute('opacity',(l.style==='dash'||l.style==='open'?pr:1)*op);
      if(!(l.style==='dash'||l.style==='open')){e.style.strokeDasharray=l._L;e.style.strokeDashoffset=l._L*(1-pr)}
      if(lb){const lk=eo((t-l.t-0.55)/0.3);lb.style.opacity=lk*op;lb.style.transform='translate(-50%,-50%) scale('+(1.25-0.25*lk)+')'}});
    const cap=brd.querySelector('.bcap');if(a.cap){const cp=Array.isArray(a.cap)?a.cap:['',a.cap];cap.querySelector('.bck').textContent=cp[0];const ct=cap.querySelector('.bct');if(ct.dataset.s!==cp[1]){ct.dataset.s=cp[1];ct.innerHTML=cp[1].replace(/\u0101/g,'<span class="mac">a</span>')}const same=pa&&JSON.stringify(pa.cap)===JSON.stringify(a.cap);cap.style.opacity=same?1:eo((t-a.tIn-0.15)/0.3)}else cap.style.opacity=0;
    const dv=brd.querySelector('.bdof');if(cm.k>1.3){dv.style.backdropFilter='blur(3px)';dv.style.webkitMaskImage='radial-gradient(ellipse 52% 60% at 50% 50%, transparent 70%, black 100%)'}else dv.style.backdropFilter='none'}}
  // desks
  const da=D.OV.find(o=>o.type==='desk'&&t>=o.tIn&&t<o.tOut);
  for(const k in desks){const el=desks[k];if(!da||da.spec.doc!==k){el.style.opacity=0;el.style.display='none';continue}el.style.opacity=1;el.style.display='block';const d=DK[k],sp=da.spec,q=ease(cl((t-da.tIn)/(da.tOut-da.tIn),0,1));const c=lerpCam(sp.from,sp.to||sp.from,q);
    el.querySelector('.dw').style.transform='rotateX('+c.tilt+'deg) rotateZ('+c.rz+'deg) scale('+c.zoom+') translate('+(-(c.fx-0.5)*d.PW)+'px,'+(-(c.fy-0.5)*d.PH)+'px)';
    const sw=el.querySelector('.dsw');if(sp.sweep){const b=sp.sweep.box,p=sp.sweep.full?1:cl((q-(sp.sweep.q0??0.1))/((sp.sweep.q1??0.9)-(sp.sweep.q0??0.1)),0,1);sw.style.left=b[0]*100+'%';sw.style.top=b[1]*100+'%';sw.style.height=(b[3]-b[1])*100+'%';sw.style.width=(b[2]-b[0])*100*p+'%';sw.style.opacity=1}else sw.style.opacity=0;
    const ln=el.querySelector('.dln');if(sp.line){const b=sp.line;ln.style.left=b[0]*100+'%';ln.style.top=b[1]*100+'%';ln.style.width=(b[2]-b[0])*100+'%';ln.style.height=(b[3]-b[1])*100+'%';ln.style.opacity=eo((q-0.15)/0.15)}else ln.style.opacity=0;
    const mk=el.querySelector('.dmk');if(sp.mark){const b=sp.mark.box;mk.style.left=b[0]*100+'%';mk.style.top=b[1]*100+'%';mk.style.width=(b[2]-b[0])*100+'%';mk.style.height=(b[3]-b[1])*100+'%';mk.style.opacity=eo((q-(sp.mark.at??0.3))/0.1)}else mk.style.opacity=0;
    const f=sp.focus||{y:.5,band:.4,blur:Math.max(0,(c.tilt-18)/4)};const dv=el.querySelector('.ddof');if(f.blur>0.4){dv.style.backdropFilter='blur('+f.blur+'px)';dv.style.webkitMaskImage=dofMask(f.y,f.band)}else dv.style.backdropFilter='none'}
}
const labs=$("#labs");
async function setT(t){
  const c=cam(t),z=c.z,tr='translate('+(${W}/2)+' '+(${H}/2)+') scale('+z+') translate('+(-c.x)+' '+(-c.y)+')';
  ["cam","cam2","cam3"].forEach(id=>document.getElementById(id).setAttribute("transform",tr));
  const sp=(p)=>[(p[0]-c.x)*z+${W}/2,(p[1]-c.y)*z+${H}/2];
  $("#world").style.transform="perspective(1500px) rotateX("+c.tilt+"deg) rotateZ("+c.rot+"deg) scale("+(1+c.tilt/80)+")";
  for(const k in D.fillK){const K=D.fillK[k];let col=[233,220,191,0];let prev=col;for(const f of K){if(f.t>t)break;const target=hex(f.c);const kk=eo((t-f.t)/0.8);col=mix(prev,target,kk);prev=kk>=1?target:col}
    const e=document.getElementById("r_"+k);e.setAttribute("fill",'rgba('+col[0]+','+col[1]+','+col[2]+','+col[3]+')');e.setAttribute("stroke-opacity",col[3])}
  let L=null,Lt=0;for(const l of D.labelK){if(l.t<=t){L=l;Lt=l.t}}
  labs.innerHTML="";if(L){const a=Math.min(1,(t-Lt)/0.5);L.items.forEach(it=>{const p=sp(it.p);if(p[0]<-200||p[0]>${W}+200||p[1]<-100||p[1]>${H}+100)return;labs.insertAdjacentHTML("beforeend",'<div class="lab" style="left:'+p[0]+'px;top:'+(p[1]-36)+'px;opacity:'+a+'">'+it.txt+'</div>')})}
  D.routes.forEach((r,i)=>{const p=document.getElementById("rt"+i),h=document.getElementById("rh"+i);const k=eo((t-r.t)/1.6),out=1-cl((t-r.tOut)/0.5,0,1);const vis=(t>=r.t&&out>0)?out:0;p.style.opacity=vis;h.style.opacity=vis;if(!vis)return;
    const m=Math.max(1,Math.round(k*(r.pts.length-1)));p.setAttribute("d","M"+r.pts.slice(0,m+1).map(q=>q[0]+","+q[1]).join(" L"));const q=r.pts[m];h.setAttribute("cx",q[0]);h.setAttribute("cy",q[1]);h.setAttribute("r",9/z)});
  D.routes.forEach((r,i)=>{const out=1-cl((t-r.tOut)/0.5,0,1);[["a",r.a,0],["b",r.b,1.3]].forEach(([e,p,dl])=>{const el=document.getElementById("pin"+i+e);const v=t>=r.t+dl?Math.min(1,(t-r.t-dl)/0.3)*out:0;const s2=sp(p);el.style.opacity=v;el.style.left=s2[0]+"px";el.style.top=s2[1]+"px";el.style.transform="translate(-50%,-100%) scale("+(0.7+0.3*back((t-r.t-dl)/0.35))+")"})});
  let y=null;for(const k of D.yearK)if(k.t<=t)y=k;const ye=$("#year");if(y&&y.v){ye.textContent=y.v;ye.style.opacity=Math.min(1,(t-y.t)/0.3)}else ye.style.opacity=0;
  let kk=null;for(const k of D.kickK)if(k.t<=t)kk=k;const ke=$("#kick");if(kk&&t-kk.t<6){ke.innerHTML="<b></b>"+kk.v;const a=Math.min(1,(t-kk.t)/0.35)*Math.min(1,(kk.t+6-t)/0.5);ke.style.opacity=a;ke.style.transform="translateX("+(-30*(1-eo((t-kk.t)/0.4)))+"px)"}else ke.style.opacity=0;
  let hearWord=null;for(const o of D.OV)if(o.type==="hear"&&t>=o.tIn&&t<=o.tOut)hearWord=o.word;
  const live=(o)=>t>=o.tIn&&t<o.tOut;const fullEv=D.OV.some(o=>["photo","video"].includes(o.type)&&live(o));const evidence=D.OV.some(o=>["frame","doc","dots","claim","aside"].includes(o.type)&&live(o));
  const waits=[];
  scenes(t);
  D.OV.forEach((o,i)=>{const el=o.el;if(o.type==="table"||o.type==="board"||o.type==="desk"){el.style.opacity=0;el.style.display="none";return}const a=Math.min(o.cutIn?1:eo((t-o.tIn)/0.3),o.cutOut?1:1-eo((t-(o.tOut-0.25))/0.25));if(t<o.tIn-0.01||t>=o.tOut){el.style.display="none";el.style.opacity=0;if(o.type==="dist")document.getElementById("ds"+i).setAttribute("opacity",0);return}el.style.display="";
    el.style.opacity=Math.max(0,a);
    if(o.type==="video"){const fi=cl(Math.floor((t-o.tIn)*${FPS})+1,1,o.n);const im=el.querySelector(".vf");const src=o.dir+String(fi).padStart(5,"0")+".jpg";if(im.dataset.s!==src){im.src=src;im.dataset.s=src;waits.push(im.decode().catch(()=>0));const vb=el.querySelector(".vb");if(vb)vb.src=src}
      const q=cl((t-o.tIn)/(o.tOut-o.tIn),0,1);im.style.transform="scale("+((o.s0||1.0)+((o.s1||1.05)-(o.s0||1.0))*q)+")";
      el.style.opacity=Math.min(o.cutIn||o.enter==="cut"?1:eo((t-o.tIn)/0.3),o.cutOut?1:1-eo((t-(o.tOut-0.3))/0.3));
      const cc=el.querySelector(".capc");if(cc)cc.style.opacity=cl((t-o.tIn-(o.capDelay??0.6))/0.4,0,1)*cl((o.tOut-0.3-t)/0.3,0,1);return}
    if(o.type==="photo"){const d=o.tOut-o.tIn,q=cl((t-o.tIn)/d,0,1);const phi=el.querySelector(".phi");let sc;
      if(o.path){let a2=o.path[0],b2=o.path[o.path.length-1];for(let j=0;j<o.path.length-1;j++)if(q>=o.path[j][0]&&q<=o.path[j+1][0]){a2=o.path[j];b2=o.path[j+1]}
        const kq=ease((q-a2[0])/Math.max(1e-6,b2[0]-a2[0]));const fx=a2[1]+(b2[1]-a2[1])*kq,fy=a2[2]+(b2[2]-a2[2])*kq;sc=a2[3]+(b2[3]-a2[3])*kq;
        let tx=${W}/2-fx*o._w*sc,ty=${H}/2-fy*o._h*sc;tx=cl(tx,${W}-o._w*sc,0);ty=cl(ty,${H}-o._h*sc,0);phi.style.transform="translate("+tx+"px,"+ty+"px) scale("+sc+")"}
      else{const s0=o.from??1.04,s1=o.to??1.16;sc=s0+(s1-s0)*ease(q);const m=ease(q)*((o.hl||s1>=1.5)?1:0.3);const tx=cl(o._dx*m,${W}-(o._ox+(o._L+o._w-o._ox)*sc),-(o._ox+(o._L-o._ox)*sc)),ty=cl(o._dy*m,${H}-(o._oy+(o._T+o._h-o._oy)*sc),-(o._oy+(o._T-o._oy)*sc));phi.style.transform="translate("+tx+"px,"+ty+"px) scale("+sc+")"}
      const fo=o.cutOut?1:1-eo((t-(o.tOut-0.3))/0.3);if(o.cutIn||o.enter==="cut"){el.style.clipPath="none";el.style.opacity=fo}else{const w=eo((t-o.tIn)/0.55);el.style.clipPath=i%2?"inset(0 0 0 "+(100*(1-w))+"%)":"inset(0 "+(100*(1-w))+"% 0 0)";el.style.opacity=fo}
      const hl=el.querySelector(".hl");if(hl){hl.style.opacity=eo((q-(o.hlAt??0.55))/0.12);hl.style.borderWidth=(6/sc)+"px"}
      const sw=el.querySelector(".sw");if(sw){const p2=cl((q-o.sweep.q0)/(o.sweep.q1-o.sweep.q0),0,1);sw.style.width=((o.sweep.box[2]-o.sweep.box[0])*100*p2)+"%";sw.style.borderBottomWidth=(5/sc)+"px";sw.style.opacity=q>o.sweep.q0?1:0}
      const mk=el.querySelector(".mk");if(mk){mk.style.opacity=eo((q-o.markAt)/0.08);mk.style.borderWidth=(6/sc)+"px"}
      const at=el.querySelector(".att");if(at)at.style.opacity=eo((q-(o.attribAt??0.8))/0.08);
      const cc=el.querySelector(".capc");if(cc&&o.capAt!=null)cc.style.opacity=eo((q-o.capAt)/0.08);return}
    const p=eo((t-o.tIn)/0.35);
    if(o.type==="frame"){const d=o.tOut-o.tIn,q=cl((t-o.tIn)/d,0,1);const fr=el.querySelector(".frm");fr.style.transform="translateX("+((o.side==="left"?-1:1)*160*(1-eo((t-o.tIn)/0.45)))+"px) rotate("+(o.side==="left"?2.5:-2.5)+"deg)";el.querySelector(".fi").style.transform="scale("+(1.02+(o.zoom||0.12)*ease(q))+")";el.style.transform=""}
    if(o.type==="fadeout"){el.style.opacity=eo((t-o.tIn)/1.4);return}
    if(o.type==="twin"){const tw=el.querySelector(".tw");if(fullEv){el.style.opacity=0;return}el.style.opacity=Math.min(o.cutIn?1:eo((t-o.tIn)/0.3),o.cutOut?1:1-eo((t-(o.tOut-0.25))/0.25));el.querySelectorAll(".tpan").forEach(pn=>pn.style.opacity=evidence?0:1);let cur=null,prv=null;o.steps.forEach(s=>{if(s.t<=t){prv=cur;cur=s}});
      el.querySelectorAll(".ttick").forEach((tk,j)=>tk.style.opacity=o.steps[j].t<=t?1:0.25);el.querySelectorAll(".tlab").forEach((tk,j)=>{const s=o.steps.filter(x=>x.mark)[j];tk.style.opacity=s&&s.t<=t?1:0});
      if(cur){const k2=eo((t-cur.t)/0.9);const y0=prv?prv.year:cur.year;el.querySelector(".tyear").textContent=Math.round(y0+(cur.year-y0)*k2)+(cur.yearSuffix&&k2>=1?cur.yearSuffix:"");
        el.querySelector(".tprog").style.width=(((y0+(cur.year-y0)*k2)-o.y0)/(o.y1-o.y0)*1840)+"px";
        ["sic","mal"].forEach((sd,j)=>{const k=j?"malta":"sicily";let st=null;o.steps.forEach(s=>{if(s.t<=t&&s[sd])st={...s[sd],t:s.t}});if(!st)return;
          const pth=el.querySelector('.tp[data-k="'+k+'"]');pth.setAttribute("fill",st.c||D.C.arab);
          const ss=el.querySelector('.tst[data-k="'+k+'"]');ss.textContent=st.status||"";ss.style.background=st.c||D.C.arab;ss.style.opacity=st.status?1:0;
          const nt=el.querySelector('.tnote[data-k="'+k+'"]');if(nt.dataset.v!==st.note){nt.dataset.v=st.note||"";nt.textContent=st.note||""}nt.style.opacity=eo((t-st.t)/0.4)})}
      el.style.transform="";return}
    if(o.type==="lock"){if(!o.measured)o.measure();el.querySelectorAll(".lr").forEach((row,ri)=>{const r=o.rows[ri];row.style.opacity=eo((t-r.at+0.05)/0.25);const lk=eo((t-o.lockAt)/0.7);
        const parts=[...row.querySelectorAll(".lp")];parts.forEach((s,pi)=>{const isC=s.dataset.c==="1";const col=+s.dataset.col;const x0=+s.dataset.x0;let x1=isC?o._colX[col]:x0;
          if(!isC){const pv=parts.slice(0,pi).reverse().find(q=>q.dataset.c==="1"),nx=parts.slice(pi+1).find(q=>q.dataset.c==="1");
            if(pv&&nx){const ca=o._colX[+pv.dataset.col]+(+pv.dataset.w)/2,cb=o._colX[+nx.dataset.col]+(+nx.dataset.w)/2;x1=(ca+cb)/2-(+s.dataset.w)*0.55/2}}const y1=isC?0:62;const sc=isC?1:(1-0.45*lk);
          s.style.left=(x0+(x1-x0)*lk)+"px";s.style.transform="translateY("+(y1*lk)+"px) scale("+sc+")";s.style.transformOrigin="0 100%";s.style.color=isC?(lk>0.5?D.C.honeyLight:"#f3e6cc"):(lk>0.5?"rgba(243,230,204,.55)":"#f3e6cc")});
        const sp2=row.querySelector(".lscript");if(sp2)sp2.style.opacity=1});
      el.querySelectorAll(".lpl").forEach(p=>{const v=o.revealT==null?1:eo((t-o.revealT)/0.22);p.style.opacity=v;p.style.transform="scale("+(1.4-0.4*v)+")";p.style.transformOrigin="0 50%"});
      const lk=eo((t-o.lockAt-0.4)/0.5);el.querySelectorAll(".lc").forEach(c=>c.style.opacity=lk*0.85);el.querySelectorAll(".ll").forEach(c=>c.style.opacity=lk);el.style.transform="";return}
    if(o.type==="words"){o.items.forEach((it,i)=>{const row=el.querySelector('.wrow[data-i="'+i+'"]');const c=D.clips[it.ci];let rev=0,amp=0;
        if(c){const k=Math.floor((t-c.t)*${FPS});if(t>=c.t+c.d)rev=1;else if(k>=0){rev=c.cu[Math.min(k,c.cu.length-1)];amp=c.e[Math.min(k,c.e.length-1)]}}else rev=1;
        const sp=row.querySelectorAll('.wl');const n=Math.ceil(rev*sp.length-0.01);sp.forEach((s2,j)=>{s2.style.opacity=j<n?1:0});const sc2=row.querySelector('.wscr');if(sc2)sc2.style.opacity=rev>=1?1:0;
        row.querySelector('.wtxt').style.transform='scale('+(1+0.09*amp)+')';const lb=row.querySelector('.wlab');const lq=it.labelT!=null&&t>=it.labelT?eo((t-it.labelT)/0.22):0;lb.style.opacity=lq;lb.style.transform='scale('+(1.5-0.5*lq)+')'});el.style.transform='';return}
    if(o.type==="claim"){const d=o.tOut-o.tIn;const ra=o.tIn+d*(o.at??0.55);const k1=eo((t-ra)/0.45),k2=eo((t-ra-0.45)/0.4);el.querySelector(".strike").style.width=k1>0?"calc("+(k1*100)+"% + 12px)":"0";el.querySelector(".ct").style.color=k1>0.6?"rgba(31,26,20,.45)":"var(--ink)";el.querySelector(".rv").style.opacity=k2;el.querySelector(".rv").style.maxHeight=(k2>0?320*Math.min(1,k1*1.5):0)+"px";el.querySelector(".rv").style.transform="translateY("+(20*(1-k2))+"px)"}
    if(!["title","stamp","dist","bubble","frame","claim","plate","video","photo"].includes(o.type))el.style.transform="scale("+(0.95+0.05*back((t-o.tIn)/0.35))+")",el.style.transformOrigin="50% 60%";
    if(o.type==="stamp"){const s=el.firstChild;const q=Math.min(1,(t-o.tIn)/0.14);s.style.transform="translate(-50%,-50%) rotate(-8deg) scale("+(1.5-0.5*q)+")"}
    if(o.type==="number"){const q=eo((t-o.tIn)/1.1);const v=o.from+(o.to-o.from)*q;el.querySelector(".n").textContent=(o.prefix||"")+(o.decimals?v.toFixed(o.decimals):Math.round(v).toLocaleString("en-US"))+(o.suffix||"")}
    if(o.type==="gauge"){const q=eo((t-o.tIn-0.2)/1.1);el.querySelector(".n").textContent=(o.prefix||"")+Math.round(o.value*q);el.querySelector(".g").style.width=(o.value*q)+"%"}
    if(o.type==="dots"){o.rows.forEach((r,ri)=>{const st=o.tIn+0.3+ri*1.6;const q=eo((t-st)/1.2);el.querySelector(".n"+ri).textContent=Math.round(r[1]*q);el.querySelectorAll(".d"+ri).forEach((d,j,all)=>d.style.opacity=j<q*all.length?1:0)})}
    if(o.type==="bar"){el.querySelectorAll(".seg").forEach((s,j)=>{const q=eo((t-o.tIn-0.2-j*0.35)/0.6);s.style.width=(o.parts[j][1]*q)+"%"})}
    if(o.type==="speaker"){const on=D.OV.find(h=>h.type==="hear"&&h.word===o.hear&&t>=h.tIn&&t<=h.tOut);el.querySelectorAll(".wave i").forEach((b,j)=>{b.style.height=(on?10+60*Math.abs(Math.sin(t*9+j*1.7)*Math.sin(t*3.1+j*.6)):10)+"px"})}
    if(o.type==="dist"){const a2=sp(o.a),b2=sp(o.b);document.getElementById("ds"+i).setAttribute("opacity",Math.max(0,a));const d=el.firstChild;d.style.position="absolute";d.style.left=((a2[0]+b2[0])/2)+"px";d.style.top=((a2[1]+b2[1])/2)+"px";d.style.transform="translate(-50%,-50%)"}
    if(o.type==="bubble"){const p2=sp(o.p);const d=el.firstChild;d.style.position="absolute";d.style.left=p2[0]+"px";d.style.top=(p2[1]-70)+"px";d.style.transform="translate(-50%,-50%) scale("+(0.8+0.2*back((t-o.tIn)/0.35))+")"}
    el.querySelectorAll(".chip").forEach((ch,j)=>{ch.classList.toggle("on",ch.dataset.w===hearWord);const q=(t-o.tIn-0.05-j*0.13)/0.35;ch.style.opacity=cl(q*1.5,0,1);ch.style.transform="translateY("+(30*(1-back(q)))+"px)"});
  });
  await Promise.all(waits);
}
// Fraunces (this build) draws the macron of ā on the next letter: draw it with CSS over a plain a instead
(function(){const st=document.createElement('style');st.textContent='.mac{position:relative;display:inline-block;line-height:1}.mac::after{content:"";position:absolute;left:12%;right:6%;top:.17em;height:.075em;background:currentColor;border-radius:.04em}.mac.it::after{left:24%;right:-4%}';document.head.appendChild(st);
  const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),ns=[];while(w.nextNode()){const n=w.currentNode;if(/[āĀ]/.test(n.nodeValue)&&/Fraunces/.test(getComputedStyle(n.parentNode).fontFamily))ns.push(n)}
  ns.forEach(n=>{const it=getComputedStyle(n.parentNode).fontStyle==='italic',f=document.createDocumentFragment();n.nodeValue.split(/([āĀ])/).forEach(q=>{if(q==='ā'||q==='Ā'){const sp=document.createElement('span');sp.className='mac'+(it?' it':'');sp.textContent=q==='ā'?'a':'A';f.appendChild(sp)}else if(q)f.appendChild(document.createTextNode(q))});n.parentNode.replaceChild(f,n)})})();
window.setT=setT;
</script></body></html>`;

// ───────── render ─────────
const pageFile = path.join(CACHE, `page_${TAG}.html`); fs.writeFileSync(pageFile, html);
const OUT = path.join(HERE, "out");
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || "/opt/pw-browsers/chromium", args: ["--font-render-hinting=none", "--disable-lcd-text", "--allow-file-access-from-files", "--disable-gpu-watchdog", "--disable-dev-shm-usage"] });
const openPage = async () => { const p = await b.newPage({ viewport: { width: W, height: H } }); await p.goto(furl(pageFile)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300); return p; };
const stills = opt("still", null);
if (stills) {
  const p = await openPage();
  for (const s of String(stills).split(",")) {
    let tt; if (/^[\d.]+$/.test(s)) tt = +s; else { const [id, off] = s.split("@"); const r = byId(id); tt = off === "end" ? r.t1 - 0.3 : r.t0 + (off ? +off : 1.2); }
    await p.evaluate((x) => window.setT(x), tt); const f = path.join(OUT, `${TAG}_${tt.toFixed(1)}s.png`); await p.screenshot({ path: f }); console.log(f);
  }
  await b.close(); process.exit(0);
}
// sound: five stems, then the mix (longform_mix3.py)
const items = [];
for (const r of T) {
  if (r.vo) items.push({ track: "vo", f: r.vo, t: r.say0 });
  for (const c of r.clips) items.push({ track: "words", f: c.file, t: c.t });
  for (const s of r.sfx || []) items.push({ track: "sfx", f: sfxFile(s.s), t: (s.after ? r.t1 : r.t0) + (s.at || 0), gain: s.gain ?? 0 });
  for (const a of r.amb || []) items.push({ track: "amb", f: path.join(INC, EP.ambience[a.s].file), from: a.from ?? EP.ambience[a.s].from ?? 0, t: r.t0 + (a.at || 0), d: a.d ?? (r.t1 - r.t0), gain: a.gain ?? 0, fade: 0.6 });
}
for (const a of ambItems) items.push({ track: "amb", f: a.f, from: a.from, t: a.t - 0.5, d: a.d + 0.8, gain: a.gain, fade: 0.5, rate: a.rate });
// v4 location beds: one continuous bed per run of table / board / desk shots (runs separated by under 6 s merge),
// starting 0.6 s before the picture cuts in, plus Foley on every event (object placed, card pinned, claim rewritten, page)
const BEDS = EP.beds || {};
for (const kind of Object.keys(BEDS)) {
  const runs = [];
  for (const x of SHOTS.filter((q) => q.kind === kind)) { const last = runs[runs.length - 1]; if (last && x.t0 - last.t1 < 6) last.t1 = x.t1; else runs.push({ t0: x.t0, t1: x.t1 }); }
  const b = BEDS[kind];
  runs.forEach((ru, i) => items.push({ track: "amb", f: path.join(INC, b.file), from: (b.from || 0) + (i * 7.3) % (b.span || 20), t: ru.t0 - 0.6, d: ru.t1 - ru.t0 + 1.0, gain: b.gain ?? -8, fade: 0.6, loop: true }));
  if (b.sfxIn) runs.forEach((ru) => items.push({ track: "sfx", f: sfxFile(b.sfxIn), t: ru.t0 - 0.35, gain: b.sfxGain ?? -4 }));
}
const ev = (name, tt, gain) => { if (EP.sfx?.[name] && tt < END) items.push({ track: "sfx", f: sfxFile(name), t: tt, gain: gain ?? 0 }); };
if (TABLE) for (const ob of TABLE.objs) if (ob.t < 1e8) ev(ob.kind === "coin" ? "coin" : "paper", ob.t + 0.38, ob.kind === "coin" ? -3 : -8);
if (BOARD) { for (const c of BOARD.cards) if (c.t < 1e8 && !c.fixed) ev("tack", c.t + 0.25, -4); for (const rw of BOARD.rewrites) ev("pencil", rw.t + 0.45, -6); }
for (const x of SHOTS) for (const f of x.sfx || []) items.push({ track: "sfx", f: sfxFile(f.s), t: x.t0 + (f.at || 0), gain: f.gain ?? 0 });
const cues = (EP.score || []).filter((c) => T.some((x) => x.id === c.at)).map((c) => ({ ...c, t: byId(c.at).t0 + (c.off || 0) }));
const duckWords = T.flatMap((r) => r.clips.map((c) => [c.t - 0.25, c.t + c.d + 0.2])).concat(T.filter((r) => r.musicGap).map((r) => [r.t0, r.t1]));
const spec = { total: TOTAL, end: END, items, cues: cues.map((c) => ({ t: c.t, f: c.track ? path.join(INC, "score", EP.scoreFiles[c.track]) : null, from: c.from || 0, gain: c.gain || 0 })), silence: duckWords, stems: path.join(CACHE, "stems_" + TAG) };
fs.writeFileSync(path.join(CACHE, `project_${TAG}.json`), JSON.stringify({ episode: `longform/${key}/episode.mjs`, voice: VOICE, opening: OPEN, timeline: T.map(({ id, t0, t1, say, say0, sayDur, kicker }) => ({ id, t0: r1(t0), t1: r1(t1), say, kicker })), mix: spec }, null, 1));
const mixFile = path.join(CACHE, `mix_${TAG}.wav`);
fs.writeFileSync(path.join(CACHE, `mix_${TAG}.json`), JSON.stringify(spec));
const mx = spawnSync("python3", [path.join(HERE, "longform_mix3.py"), path.join(CACHE, `mix_${TAG}.json`), mixFile], { stdio: "inherit" });
if (mx.status) throw new Error("mix failed");
const workers = +opt("workers", 3), nF = Math.ceil(END * FPS), per = Math.ceil(nF / workers), parts = [];
// Segmented, resumable render: 8-second segments, each its own MP4, kept across runs (the folder name carries a hash
// of the page, so any edit invalidates them). Every worker has its own browser; a crashed page is relaunched and the
// frame redone, and a failed relaunch is retried, so a crash costs seconds, not the render.
const crypto = await import("node:crypto");
const SEGF = 240, segDir = path.join(CACHE, `seg_${TAG}_${crypto.createHash("md5").update(html).digest("hex").slice(0, 10)}`); fs.mkdirSync(segDir, { recursive: true });
const launchW = () => chromium.launch({ executablePath: process.env.CHROMIUM || "/opt/pw-browsers/chromium", args: ["--font-render-hinting=none", "--disable-lcd-text", "--allow-file-access-from-files", "--disable-gpu-watchdog", "--disable-dev-shm-usage", "--disable-gpu"] });
const pageOn = async (br) => { const p = await br.newPage({ viewport: { width: W, height: H } }); await p.goto(furl(pageFile)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300); return p; };
await b.close();
const nSeg = Math.ceil(nF / SEGF), segFile = (k) => path.join(segDir, `s${String(k).padStart(4, "0")}.mp4`);
let relaunchCount = 0;
await Promise.all(Array.from({ length: workers }, async (_, w) => {
  let br = null, p = null;
  const fresh = async () => { for (let k = 0; ; k++) { try { if (br) await br.close().catch(() => {}); br = await launchW(); p = await pageOn(br); return; } catch (e) { if (k > 20) throw e; await new Promise((r) => setTimeout(r, 3000)); } } };
  await fresh();
  for (let k = w; k < nSeg; k += workers) {
    if (fs.existsSync(segFile(k) + ".done")) continue;
    const f0 = k * SEGF, f1 = Math.min(nF, f0 + SEGF), tmp = segFile(k) + ".tmp.mp4";
    const ff = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-c:v", "mjpeg", "-r", String(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", tmp], { stdio: ["pipe", "inherit", "inherit"] });
    for (let f = f0; f < f1; f++) {
      let buf;
      for (let tries = 0; ; tries++) {
        try { await p.evaluate((x) => window.setT(x), f / FPS); buf = await p.screenshot({ type: "jpeg", quality: 90, timeout: 180000 }); break; }
        catch (e) { if (tries > 40) throw e; relaunchCount++; console.log(`  relaunch worker ${w} at frame ${f}: ${e.message.split("\n")[0]}`); await new Promise((r) => setTimeout(r, 1500 + 1500 * w)); await fresh(); }
      }
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    }
    ff.stdin.end(); await new Promise((r) => ff.on("close", r)); fs.renameSync(tmp, segFile(k)); fs.writeFileSync(segFile(k) + ".done", "");
    console.log(`  segment ${k + 1}/${nSeg} (worker ${w})`);
  }
  if (br) await br.close();
}));
console.log(`  ${relaunchCount} relaunches`);
parts.push(...[...Array(nSeg)].map((_, k) => segFile(k)));
fs.writeFileSync(path.join(CACHE, `parts_${TAG}.txt`), parts.map((p) => `file '${p}'`).join("\n"));
const final = path.join(OUT, `${TAG}.mp4`);
run("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", path.join(CACHE, `parts_${TAG}.txt`), "-i", mixFile, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", String(END), "-movflags", "+faststart", final]);
console.log(final);
