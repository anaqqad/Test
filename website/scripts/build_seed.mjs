// Builds draft Story data from the reel write-ups (publish/reels/*.md), reel specs (data/reel-*.json) and image
// credits (public/pd/reel-*/credits.json). Output: JSON consumed by seed_stories.php. Text is taken as written
// (already fact-checked with two sources per fact); nothing new is written here. All stories are created as DRAFTS.
// Usage (repo root): node website/scripts/build_seed.mjs > seed.json
import { readFileSync, readdirSync, existsSync } from 'node:fs';

// Section / domains / country / era per story (editorial choice, review in WordPress).
const MAP = {
  'bass-reeves': ['african-american-history', ['law-justice'], 'us', '19th-century'],
  'bessie-coleman': ['african-american-history', ['exploration', 'women-in-history'], 'us', '20th-century'],
  'booker-t-washington': ['african-american-history', ['education', 'politics-government'], 'us', '20th-century'],
  'ellen-craft': ['african-american-history', ['slavery-emancipation', 'women-in-history'], 'us', '19th-century'],
  'frederick-douglass': ['african-american-history', ['slavery-emancipation', 'civil-rights-activism'], 'us', '19th-century'],
  'garrett-morgan': ['african-american-history', ['science-medicine-invention'], 'us', '20th-century'],
  'george-washington-carver': ['african-american-history', ['science-medicine-invention', 'education'], 'us', '20th-century'],
  'harriet-tubman-raid': ['african-american-history', ['military', 'slavery-emancipation', 'women-in-history'], 'us', '19th-century'],
  'henry-box-brown': ['african-american-history', ['slavery-emancipation'], 'us', '19th-century'],
  'hiram-revels': ['african-american-history', ['politics-government'], 'us', '19th-century'],
  'ida-b-wells': ['african-american-history', ['civil-rights-activism', 'women-in-history'], 'us', '19th-century'],
  'jack-johnson': ['african-american-history', ['sports'], 'us', '20th-century'],
  'jesse-owens': ['african-american-history', ['sports'], 'us', '20th-century'],
  'major-taylor': ['african-american-history', ['sports'], 'us', '19th-century'],
  'mansa-musa': ['global-african-history', ['politics-government', 'religion'], 'ml', 'before-1500'],
  'muhammad-ali': ['african-american-history', ['sports', 'civil-rights-activism'], 'us', '20th-century'],
  'robert-smalls': ['african-american-history', ['military', 'politics-government'], 'us', '19th-century'],
  'rosa-parks': ['african-american-history', ['civil-rights-activism', 'women-in-history'], 'us', '20th-century'],
  'sojourner-truth': ['african-american-history', ['slavery-emancipation', 'civil-rights-activism', 'women-in-history'], 'us', '19th-century'],
};
const COUNTRY_NAMES = { us: 'United States', ml: 'Mali' };

const out = [];
for (const slug of Object.keys(MAP)) {
  const mdPath = `publish/reels/${slug}.md`;
  if (!existsSync(mdPath)) continue;
  const md = readFileSync(mdPath, 'utf8').replace(/\r/g, '');
  const lines = md.split('\n');
  const spec = JSON.parse(readFileSync(`data/reel-${slug}.json`, 'utf8'));

  // Name from the heading: "# Reel: Robert Smalls, "The Man..."".
  const name = (lines[0].match(/^# Reel: (.+?), ["“]/) || [])[1] || slug;

  // Years from the lower third, e.g. "Deputy U.S. Marshal · 1838 – 1910" or "c. 1818 – 1895".
  let birth = '', death = '';
  for (const b of spec.beats) {
    const sub = b.overlays && b.overlays.lowerThird && b.overlays.lowerThird.sub;
    if (!sub) continue;
    const m = sub.match(/((?:c\. )?\d{3,4})\s*[–-]\s*(\d{3,4})/);
    if (m) { birth = m[1]; death = m[2]; }
    break;
  }

  // Post text: after the "Post text" line, up to the reader question / support line / sources.
  let i = lines.findIndex((l) => /^(## )?Post text:?\s*$/i.test(l.trim()));
  const body = [];
  if (i >= 0) {
    for (i += 1; i < lines.length; i++) {
      const l = lines[i];
      if (/^(Had you|Have you|Did you|Which |What |Would you)/.test(l.trim()) && l.trim().endsWith('?')) break;
      if (/^(Researching|Sources:|#BlackHistory|## )/.test(l.trim())) break;
      body.push(l);
    }
  }
  const paras = body.join('\n').trim().split(/\n\s*\n/).map((p) => p.replace(/\s*\n\s*/g, ' ').trim()).filter(Boolean);

  // Sources: "Sources:" followed by "- item" lines, or "Sources: a; b; c."
  const sources = [];
  const si = lines.findIndex((l) => /^Sources:/.test(l.trim()));
  if (si >= 0) {
    const inline = lines[si].replace(/^Sources:\s*/, '').trim();
    if (inline) {
      inline.replace(/\.$/, '').split(/;\s*/).forEach((s) => sources.push(s.trim()));
    } else {
      for (let j = si + 1; j < lines.length && /^\s*- /.test(lines[j]); j++) sources.push(lines[j].replace(/^\s*- /, '').trim());
    }
  }

  // Image credits paragraph ("Images: ...").
  const ii = lines.findIndex((l) => /^Images:/.test(l.trim()));
  let images = '';
  if (ii >= 0) {
    const buf = [];
    for (let j = ii; j < lines.length && lines[j].trim(); j++) buf.push(lines[j].trim());
    images = buf.join(' ').replace(/^Images:\s*/, '');
  }

  // Cover: the image of the first beat (the face used as the reel cover).
  const key = spec.beats[0].visual && spec.beats[0].visual.image;
  const credits = JSON.parse(readFileSync(`public/pd/reel-${slug}/credits.json`, 'utf8'));
  const c = credits[key] || {};
  const file = readdirSync(`public/pd/reel-${slug}`).find((f) => f.startsWith(key + '.'));

  const [section, domains, country, era] = MAP[slug];
  out.push({
    slug: slug.replace(/-raid$/, ''),
    reel: slug,
    title: name,
    excerpt: paras[0] || '',
    paragraphs: paras.slice(1),
    birth, death,
    sources,
    image_credit: images,
    cover: file ? `public/pd/reel-${slug}/${file}` : '',
    cover_name: file ? `${slug.replace(/-raid$/, '')}-${file}` : '',
    cover_caption: [c.title ? c.title.replace(/^File:/, '').replace(/\.[a-z]+$/i, '') : '', c.artist, c.date, c.license].filter(Boolean).join('. '),
    cover_source: c.source || '',
    section, domains, country, country_name: COUNTRY_NAMES[country], era,
  });
}
// Podcast episodes: publish/podcast/podcast-epNN-<slug>.md
const episodes = [];
for (const f of readdirSync('publish/podcast').filter((f) => /^podcast-ep\d+-.+\.md$/.test(f)).sort()) {
  const md = readFileSync(`publish/podcast/${f}`, 'utf8').replace(/\r/g, '');
  const lines = md.split('\n');
  const [, num, person] = f.match(/^podcast-ep(\d+)-(.+)\.md$/);
  const ti = lines.findIndex((l) => /^Episode title:/.test(l));
  const title = ti >= 0 ? lines[ti + 1].trim() : person;
  const di = lines.findIndex((l) => /^Description/.test(l));
  const desc = [];
  for (let j = di + 1; j < lines.length && !/^Chapters/.test(lines[j]); j++) desc.push(lines[j]);
  const paras = desc.join('\n').trim().split(/\n\s*\n/).map((p) => p.replace(/\s*\n\s*/g, ' ').trim()).filter(Boolean);
  const src = (lines.find((l) => /^Sources:/.test(l)) || '').replace(/^Sources:\s*/, '').replace(/\.$/, '');
  episodes.push({
    number: parseInt(num, 10), slug: person, story: person, title, paragraphs: paras,
    sources: src ? src.split(/;\s*/) : [],
    cover: existsSync(`publish/podcast/podcast-ep${num}-cover.jpg`) ? `publish/podcast/podcast-ep${num}-cover.jpg` : '',
  });
}

process.stdout.write(JSON.stringify({ stories: out, episodes }, null, 1));
console.error(out.map((s) => `${s.slug}: ${s.paragraphs.length} paras, ${s.sources.length} sources, years ${s.birth}-${s.death}, cover ${s.cover ? 'yes' : 'NO'}`).join('\n'));
console.error(episodes.map((e) => `episode ${e.number} ${e.title}: ${e.paragraphs.length} paras, ${e.sources.length} sources`).join('\n'));
