// Turns a voiced long-form Doc spec (16:9) into a vertical Reel spec (1080x1920) of the same length, for Facebook.
// No TTS: it reuses the doc's timeline.json and mix.wav, and its images.
// Usage: node scripts/doc_to_vertical.mjs robert-smalls
//   reads  data/doc-<slug>.json, public/generated/doc-<slug>/, public/pd/doc-<slug>/
//   writes data/reel-long-<slug>.json, public/generated/reel-long-<slug>/, public/pd/reel-long-<slug>/
import fs from 'node:fs';
import path from 'node:path';

const slug = process.argv[2];
if (!slug) throw new Error('usage: node scripts/doc_to_vertical.mjs <slug>');
const doc = JSON.parse(fs.readFileSync(`data/doc-${slug}.json`, 'utf8'));
const id = `reel-long-${slug}`;

// audio + timings: copy (not move) so the YouTube doc can still be re-rendered
const gSrc = `public/generated/doc-${slug}`, gDst = `public/generated/${id}`;
fs.mkdirSync(gDst, { recursive: true });
for (const f of ['timeline.json', 'mix.wav']) fs.copyFileSync(path.join(gSrc, f), path.join(gDst, f));

// images
const pSrc = `public/pd/doc-${slug}`, pDst = `public/pd/${id}`;
fs.mkdirSync(pDst, { recursive: true });
for (const f of fs.readdirSync(pSrc)) fs.copyFileSync(path.join(pSrc, f), path.join(pDst, f));
const credits = JSON.parse(fs.readFileSync(path.join(pSrc, 'credits.json'), 'latin1'));

const beats = doc.beats.map((b) => {
  let v = { ...b.visual };
  if (v.kind === 'quote') {
    // the reel template has no quote card: show it as a title card with the quote as the sub-line
    v = { kind: 'title', title: '“', sub: `${v.quote} — ${v.by}` };
  } else if (v.kind === 'photo') {
    const c = credits[v.image];
    // a vertical frame already crops a landscape picture about 3x: drop the doc's extra zoom,
    // and frame very wide or small pictures as cards instead of blowing them up
    if (c && (c.height < 900 || c.width / c.height > 2.2)) v = { kind: 'card', image: v.image };
    else v = { ...v, zoom: [1.0, 1.06] };
  }
  return { ...b, visual: v };
});

const spec = {
  ...doc,
  id,
  format: 'reel',
  width: 1080,
  height: 1920,
  brand: { page: 'The Black History Room', cta: 'Follow The Black History Room for more.', ctaLine: 'for more.', theme: 'bhr' },
  beats,
};
delete spec.assets;
fs.writeFileSync(`data/${id}.json`, JSON.stringify(spec, null, 1) + '\n');
const kinds = beats.reduce((m, b) => ((m[b.visual.kind] = (m[b.visual.kind] || 0) + 1), m), {});
console.log(id, beats.length, 'beats', JSON.stringify(kinds));
