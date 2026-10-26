// Builds the Markdown tables used in the competitive analysis report from the scraped datasets.
// Run from the repo root: node docs/youtube/data/build_tables.mjs <outDir>
import fs from 'node:fs';
const out = process.argv[2] || '.';
const ch = JSON.parse(fs.readFileSync('docs/youtube/data/channels-2026-10-26.json', 'utf8'));
const meta = {
  '@BlackJournals': ['Direct', 'Erased origins, inventions, slavery myths, Black biblical history', 'Essays 13-25 min, daily'],
  '@countryboi': ['Direct', 'Clever survival stories under Jim Crow, little-known events', 'Single-story explainers ~10 min'],
  '@UnseenFrontlines': ['Direct (military)', 'Black soldiers vs the Klan, erased war heroes, political hooks', 'Single-event docs 21-36 min'],
  '@BlackHistoryExposed': ['Direct', 'Black royalty, millionaires, erased families', 'Lists and mysteries 17-28 min'],
  '@BlackStatusHQ': ['Adjacent (wealth)', 'Richest Black families, celebrity wealth', '20-25 min wealth tours'],
  '@Potlikker_Official': ['Adjacent (heritage food)', 'What Black ancestors ate to survive', '45-52 min numbered lists'],
  '@unsungblackhistory': ['Direct', 'Overlooked names', 'Mixed (not verified)'],
  '@AfricanCoreVideos': ['Adjacent (Africa)', 'African culture, places, people', 'High volume (format not verified)'],
  '@One54Africa': ['Adjacent (Africa)', 'Africa facts, myths, entertainment', 'High volume, 2,534 videos'],
  '@hometeamhistory806': ['Direct (Africa)', 'African history from an African perspective', 'Essays 8-13 min, ~1 per month now'],
  '@HistoricalAfrica': ['Direct (Africa)', 'Tribes, kingdoms, culture', 'High volume, ~20 min'],
  '@blackcultureunlocked': ['Adjacent (culture)', 'Celebrities, where are they now', '~25 min'],
  '@OfficialBlackWallStreet': ['Direct (wealth)', 'Black business and communities', '~9 min'],
  '@RootsPreserved78': ['Direct (archive)', 'Old documentaries, speeches, debates', 'Archive uploads'],
  '@TheRealMerkabah': ['Direct (Afrocentric)', 'Lectures, conspiracy-leaning', 'Daily lectures'],
  '@blackstoriesuntold458': ['Direct', 'Soldiers, philosophers, untold figures', '12-17 min'],
  '@BlackHistoryinTwoMinutes': ['Direct', 'Gates-narrated explainers', '3 min, inactive ~3 years'],
  '@HistoryWithNoChaser': ['Direct', 'Biographies and terms', '~13 min, slow'],
  '@WhispersOfThePast-j5x': ['Direct (rage-bait)', 'Reaction and outrage framing', '~30 min, several a day'],
  '@FromNothing': ['Direct (Africa)', 'Sub-Saharan history, myths', '15-25 min, slow'],
  '@ArcofAges369': ['Direct', 'History stories', '~40 min'],
  '@forgottenblackhistory': ['Drifted', 'Now police and news clips', 'Mixed'],
  '@PushBlack': ['Direct', 'Culture essays', '~10 min'],
  '@the_fat_electrician': ['Adjacent (military heroes)', 'Forgotten American war heroes, incl. Eugene Bullard', '45-90 min, comedic narration'],
  '@SeriousHistory': ['Adjacent', 'Themed compilations: revenge, last stands', '17-29 min'],
  '@pbsorigins': ['Adjacent', '"They Don\'t Teach You About" series, race and US myths', '11-19 min'],
  '@PeopleProfiles': ['Adjacent (biography)', 'Full-life biographies', '45-60 min'],
  '@HistoryMatters': ['Adjacent', 'Animated why-questions', '~9 min'],
  '@TheUntoldPast': ['Adjacent', 'Executions, WW2 brutality', '9-55 min'],
  '@WeirdHistory': ['Adjacent', 'Life in past eras', '~26 min'],
  '@FORGOTTENHISTORYCHANNEL': ['Adjacent', 'Forgotten events, corruption', '20-30 min'],
  '@ChatHistoryCompilations': ['Adjacent (sleep)', '2-hour fact compilations', '2 h'],
  '@BeginningToNoww': ['Adjacent', '"Entire history of X"', '2-4 h'],
};
const fmt = (n) => n == null ? '–' : n >= 1e6 ? (n / 1e6).toFixed(n >= 1e7 ? 0 : 1) + 'M' : n >= 1e3 ? (n / 1e3).toFixed(n >= 1e5 ? 0 : 1) + 'K' : String(n);
let t = '| Channel | Type | Subs | Videos | Total views | Joined | Median views, last 15 uploads | Median ÷ subs | Uploads / month (est.) | Typical length | Main topics |\n|---|---|---:|---:|---:|---|---:|---:|---:|---|---|\n';
const rows = ch.filter((c) => meta[c.handle]).map((c) => {
  const s = c.latest.map((v) => v.views).filter(Boolean).sort((a, b) => a - b);
  const med = s.length ? s[Math.floor(s.length / 2)] : null;
  const ages = c.latest.map((v) => v.ageMonths).filter((x) => x !== null);
  const span = ages.length ? Math.max(...ages) : 0;
  const upm = c.latest.length && span ? c.latest.length / Math.max(span, 0.3) : null;
  return { c, med, upm };
}).sort((a, b) => (b.c.views || 0) - (a.c.views || 0));
for (const { c, med, upm } of rows) {
  const m = meta[c.handle];
  t += `| [${c.handle}](https://www.youtube.com/${c.handle}) | ${m[0]} | ${fmt(c.subs)} | ${c.videos} | ${fmt(c.views)} | ${c.joined || '–'} | ${med ? fmt(med) : '–'} | ${med ? (med / c.subs * 100).toFixed(1) + '%' : '–'} | ${upm ? (upm > 30 ? '30+' : upm.toFixed(1)) : '–'} | ${m[2]} | ${m[1]} |\n`;
}
fs.writeFileSync(out + '/frag_channels.md', t);
const top = JSON.parse(fs.readFileSync('docs/youtube/data/top100-hits.json', 'utf8'));
let v = '| # | Video | Channel | Views | Views ÷ subs | Length | Age |\n|---:|---|---|---:|---:|---:|---|\n';
top.forEach((x, i) => { v += `| ${i + 1} | [${x.title.replace(/\|/g, '/')}](https://www.youtube.com/watch?v=${x.id}) | ${x.h} | ${x.viewsText} | ${(x.views / x.subs).toFixed(1)}× | ${x.len || '–'} | ${x.when || '–'} |\n`; });
fs.writeFileSync(out + '/frag_top.md', v);
const own = JSON.parse(fs.readFileSync('docs/youtube/data/own-channel-2026-10-26.json', 'utf8'));
let o = '| Short | Views |\n|---|---:|\n';
[...own.videos].sort((a, b) => b[2] - a[2]).forEach((x) => { o += `| [${x[1]}](https://www.youtube.com/shorts/${x[0]}) | ${x[2].toLocaleString('en-US')} |\n`; });
fs.writeFileSync(out + '/frag_own.md', o);
console.log(rows.length, 'channels;', top.length, 'videos');
