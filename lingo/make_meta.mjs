// node make_meta.mjs <video> -> meta/<video>.md (YouTube title, description with chapters + credits, tags)
import fs from "node:fs";
import { VIDEOS } from "./videos.mjs";
const k = process.argv[2], v = VIDEOS[k];
const man = JSON.parse(fs.readFileSync(`cache/audio/${k}/manifest.json`));
const INTRO = 3.2, seg = (it) => (v.layout === "ranking" ? 11.0 : +(1.4 + 5.0 * it.cards.length + 1.2).toFixed(2));
const ts = (t) => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, "0")}`;
const clean = (s) => String(s).replace(/</g, "under ").replace(/>/g, "over ").replace(/~/g, "~");
const items = v.items.filter((it) => man[it.name]);
const tl = fs.existsSync(`out/${k}_timeline.json`) ? Object.fromEntries(JSON.parse(fs.readFileSync(`out/${k}_timeline.json`)).map((e) => [e.name, e])) : {};
let t = INTRO;
const chapters = ["0:00 Intro"];
for (const it of items) {
  if (tl[it.name]) t = tl[it.name].start;
  const extra = v.layout === "ranking" ? `${it.score}/10` : it.speakers ? (/^[~<\d][\d,.~<kM–]*$/.test(it.speakers) ? `${clean(it.speakers)} ${/^~?1$/.test(it.speakers) ? "speaker" : "speakers"}` : it.speakers === "revival" ? "revival" : (/native$/.test(it.speakers) ? `${clean(it.speakers)} speakers` : `speakers: ${clean(it.speakers)}`)) : "";
  chapters.push(`${ts(t)} ${it.name}${extra ? ` (${extra})` : ""}`);
  t += tl[it.name] ? tl[it.name].dur : seg(it);
}
const credits = [];
const lic = new Set();
const artistOf = (a) => a
  .replace(/^Spoken by (.+?); recorded and published by (.+)$/, "$2 (speaker: $1)")
  .replace(/^No machine-readable author provided\. (\S+) assumed.*$/, "$1")
  .replace(/^Speaker: (.+?) Recorder: .*$/, "$1")
  .replace(/^The original uploader was (.+?) at (.+?)\.?$/, "$1 ($2)")
  .replace(/^https?:\/\/\S*wikitongues\S*$/i, "Wikitongues")
  .replace(/^Max (Max Planck.*)$/, "$1")
  .replace(/~commonswiki$/, "")
  .replace(/^Wikitongues, Inc$/, "Wikitongues");
for (const it of items) {
  const groups = new Map();
  for (const c of man[it.name].credits || []) {
    const key = artistOf(c.artist) + "|" + c.license;
    const word = c.title.slice(5).replace(/\.\w+$/, "").trim();
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(/^LL-Q/.test(word) ? word.replace(/-$/, "").split(")-").slice(-1)[0].split("-").slice(1).join("-") || word : word);
    if (/BY-SA 4/.test(c.license)) lic.add("https://creativecommons.org/licenses/by-sa/4.0/");
    else if (/BY-SA 3/.test(c.license)) lic.add("https://creativecommons.org/licenses/by-sa/3.0/");
    else if (/BY 4/.test(c.license)) lic.add("https://creativecommons.org/licenses/by/4.0/");
    else if (/BY 3/.test(c.license)) lic.add("https://creativecommons.org/licenses/by/3.0/");
    else if (/BY 2.5/.test(c.license)) lic.add("https://creativecommons.org/licenses/by/2.5/");
  }
  for (const [key, titles] of groups) {
    const [artist, license] = key.split("|");
    const isWords = (man[it.name].credits || []).some((c) => /^File:LL-Q/.test(c.title));
    credits.push(isWords ? `${it.name}: ${titles.length > 1 ? "words" : "word"} ${titles.map((t) => `"${t}"`).join(", ")} by ${artist} (Lingua Libre), ${license}` : `${it.name}: ${titles.map((t) => `"${t}"`).join(", ")} by ${artist}, ${license}`);
  }
}
const intro = {
  extinct: "Some of these languages have only a handful of speakers left. Some are being brought back from the brink. Every voice you hear is a real recording of the language.",
  niche: "Languages you've probably never heard of, with real speakers you can hear. Every voice in this video is a real recording of the language.",
  sounds: "Clicks, whistles, tones and words with no vowels. Every sound you hear is a real recording of the language.",
  conlangs: "Languages that somebody simply invented, and the people who actually speak them. Every voice you hear is a real recording.",
  revived: "Languages that died, or nearly did, and came back. Every voice you hear is a real recording of the language.",
  hardest: "How hard is each language for an English speaker? Based on the US Foreign Service Institute's estimates of class time. Every voice you hear is a real recording.",
}[k] || "";
const tags = {
  extinct: "nearly extinct languages, endangered languages, extinct languages, languages be like, rare languages, dying languages, last speakers, language isolate, Wymysorys, Kusunda, Nuxalk, Cherokee language, Vepsian, Lakota language, Yugambeh, Ladino, Boruca, linguistics, Wikitongues, LingoDude",
  niche: "niche languages, rare languages, minority languages, languages be like, Romansh, Faroese, North Frisian, Siwi, Mingrelian, Tuvan, Gagauz, Jerriais, Mirandese, Greenlandic, Luxembourgish, linguistics, LingoDude",
  sounds: "weird languages, click languages, whistled language, tonal languages, languages be like, Xhosa, Taa, Silbo Gomero, Hmong, Yoruba, Piraha, Cantonese, Georgian, Czech, Danish, Welsh, Hawaiian, linguistics, LingoDude",
  conlangs: "constructed languages, conlangs, invented languages, Esperanto, Toki Pona, Klingon, Volapuk, Lojban, Ido, languages be like, linguistics, LingoDude",
  revived: "revived languages, language revival, dead languages, Hebrew, Cornish, Manx, Maori, Latin, Sanskrit, languages be like, linguistics, LingoDude",
  hardest: "hardest languages, language difficulty, FSI, ranking languages, languages for English speakers, learn languages, linguistics, LingoDude",
}[k] || "";
const title = v.title;
const desc = [intro, "", "Which language should we cover next? Tell us in the comments 👇", "", ...chapters, "",
  "Audio credits (all via Wikimedia Commons):", ...credits, `Licences: ${[...lic].join(" and ")}`,
  "Speaker counts are estimates; sources disagree for many small languages.", "", "#languages #linguistics #languagesbelike"].join("\n").replace(/[<>]/g, "");
fs.mkdirSync("meta", { recursive: true });
fs.writeFileSync(`meta/${k}.md`, `# YouTube metadata: ${title}\n\n## Title\n${title}\n\n## Description\n${desc}\n\n## Tags\n${tags}\n\n## Settings\n- Category: Education\n- Made for kids: No\n- Thumbnail: lingo/out/brand/thumb_${k}.png\n`);
console.log(`meta/${k}.md`);
