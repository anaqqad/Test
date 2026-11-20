// Credits for a long-form episode, built from what the episode actually uses: node longform_credits.mjs malta3
// Reads licences from incoming/<assets>/v3/meta.json and score/meta.json (as listed on each Commons file page) and
// EP.photos; writes out/longform_<key>_credits.txt (pasted into the YouTube description).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const key = process.argv[2];
const EP = (await import(pathToFileURL(path.join(HERE, "longform", key, "episode.mjs")).href)).default;
const INC = path.join(HERE, "incoming", EP.assets || key);
const meta = {};
for (const f of ["v3/meta.json", "v4/meta.json", "score/meta.json"]) if (fs.existsSync(path.join(INC, f))) Object.assign(meta, JSON.parse(fs.readFileSync(path.join(INC, f))));
const who = (m) => m.artist.replace(/\s*Recorder:.*$/s, "").replace(/^Speaker:\s*/, "").trim();
const page = (f) => "https://commons.wikimedia.org/wiki/File:" + encodeURIComponent(path.basename(f).replace(/ /g, "_"));
const strip = (f) => path.basename(f).replace(/\.[a-z0-9]+$/i, "");

const lines = [...Object.values(EP.openings || {}).flat(), ...EP.lines];
const heard = new Set(), shown = new Set();
for (const L of lines) {
  (L.hear || []).forEach((w) => heard.add(w)); (L.show || []).forEach((s) => s.src && shown.add(s.src));
  for (const x of L.shots || []) { // v4 shots: base layer + its own overlays
    for (const k of ["video", "photo"]) if (typeof x[k] === "string") shown.add(x[k]);
    if (x.plate?.src || typeof x.plate === "string") shown.add(x.plate.src || x.plate);
    (x.over || []).forEach((s) => s.src && shown.add(s.src));
  }
}
for (const ob of Object.values(EP.table?.objects || {})) if (ob.src) shown.add(ob.src);
for (const c of Object.values(EP.board?.cards || {})) if (c.src) shown.add(c.src);
for (const d of Object.values(EP.docs || {})) shown.add(d);
const out = ["Audio credits (all via Wikimedia Commons):"];
const ll = [...heard].filter((w) => !EP.sounds?.[w] || /GħawdxiVeru/.test(EP.sounds[w].file));
if (ll.length) out.push(`Maltese words and phrases (${ll.join(", ")}): recorded by GħawdxiVeru for Lingua Libre, CC0`);
for (const w of heard) {
  const s = EP.sounds?.[w]; if (!s || /GħawdxiVeru/.test(s.file)) continue;
  if (/Keith/.test(s.file)) { out.push('Maltese speech: "WIKITONGUES- Keith speaking Maltese" by Wikitongues and Irena Dahl, CC BY-SA 4.0'); continue; }
  const m = meta[s.file.replace(/^v[34]\//, "")]; if (!m) throw new Error("no licence for " + s.file);
  out.push(`${s.label}: "${strip(s.file)}", spoken by ${who(m)} for Lingua Libre, ${m.license}`);
}
for (const [k, s] of Object.entries(EP.sfx || {})) { const m = meta[s.file.replace(/^v[34]\//, "")]; out.push(`Sound effect (${k}): "${strip(s.file)}" by ${who(m)}, ${m.license}`); }
const tracks = new Set((EP.score || []).filter((c) => c.track && lines.concat(EP.lines).some((l) => l.id === c.at)).map((c) => EP.scoreFiles[c.track]));
for (const f of tracks) { const m = meta[f]; out.push(`Music: "${strip(f).replace(/ \(ISRC.*\)/, "")}" by ${m.artist} (incompetech.com), ${m.license}`); }
out.push("", "Footage (all via Wikimedia Commons):");
for (const [k, v] of Object.entries(EP.videos || {})) if (shown.has(k)) out.push(`${k === "bakery" ? "Baking the Best Persian Bread in a Traditional Oven - Iranian Bakeries (stand-in footage)" : strip(v.file) + (["lind", "bl"].includes(k) ? " (stand-in footage)" : "")}: ${v.by}, ${v.lic}`);
if (EP.table) out.push("Table and desk texture: \"Wood table large diff 8k (JPG)\" by Rico Cilliers, Charlotte Baglioni et al. (Poly Haven), CC0");
out.push("", "Photos, paintings and documents (all via Wikimedia Commons):");
for (const [k, [f, by, lic]] of Object.entries(EP.photos || {})) if (shown.has(k)) out.push(`${strip(f)}: ${by}, ${lic}`);
out.push("Licences: https://creativecommons.org/licenses/by-sa/4.0/ , https://creativecommons.org/licenses/by-sa/3.0/ , https://creativecommons.org/licenses/by/4.0/ , https://creativecommons.org/licenses/by/3.0/");
out.push("Narration: AI voice (Kokoro). Script, maps and research by LingoDude. Map data: Natural Earth (public domain) via world-atlas.");
const file = path.join(HERE, "out", `longform_${key}_credits.txt`);
fs.writeFileSync(file, out.join("\n") + "\n");
console.log(out.join("\n"));
