// Builds data/concepts.json: English base concepts ranked by frequency (wordfreq), each with its
// main part of speech from WordNet 3.1 (the POS with the most sense-tagged occurrences).
// Usage: node tools/build_concepts.mjs <path to wordnet dict dir>
import fs from 'node:fs';
import nlp from 'compromise';
const WN = process.argv[2];
const here = (p) => new URL('../' + p, import.meta.url);
const wn = new Map(); // lemma -> {n,v,a,r} tagsense counts (+0.001 per sense so untagged still count)
for (const [file, p] of [['index.noun', 'n'], ['index.verb', 'v'], ['index.adj', 'a'], ['index.adv', 'r']]) {
  for (const line of fs.readFileSync(`${WN}/${file}`, 'utf8').split('\n')) {
    if (!line || line.startsWith(' ')) continue;
    const f = line.split(' '); const lemma = f[0]; if (!/^[a-z]+$/.test(lemma)) continue;
    const pc = +f[3]; const senses = +f[4 + pc]; const tagged = +f[5 + pc];
    const e = wn.get(lemma) || {}; e[p] = tagged + senses * 0.001; wn.set(lemma, e);
  }
}
const words = fs.readFileSync(here('data/freq_raw.txt'), 'utf8').split('\n');
const closed = new Set(fs.readFileSync(here('data/closed_class.txt'), 'utf8').split(/\s+/).filter(Boolean));
const block = new Set(fs.readFileSync(here('data/blocklist.txt'), 'utf8').split(/\s+/).filter(Boolean));
const TWO = new Set(['go','ox','ax','ox','ma','pa']);
const P = { n: 'noun', v: 'verb', a: 'adj', r: 'adv' };
const seen = new Set(); const out = [];
for (const w of words) {
  if ((w.length < 3 && !TWO.has(w)) || closed.has(w) || block.has(w)) continue;
  const t = nlp(w).terms().json()[0]?.terms?.[0]; if (!t) continue;
  const tags = new Set(t.tags);
  if (['Person', 'Place', 'Organization', 'Acronym', 'Contraction', 'Value'].some(x => tags.has(x))) continue;
  let lemma = w;
  if (tags.has('Plural')) { const s = nlp(w).nouns().toSingular().text().toLowerCase(); if (wn.has(s)) lemma = s; }
  if (tags.has('PastTense') || tags.has('Gerund') || tags.has('Participle') || (tags.has('PresentTense') && !tags.has('Infinitive'))) {
    const s = nlp(w).verbs().toInfinitive().text().toLowerCase(); if (wn.has(s) && wn.get(s).v) lemma = s;
  }
  if (!wn.has(lemma) || closed.has(lemma) || block.has(lemma) || seen.has(lemma)) continue;
  const e = wn.get(lemma); const pos = Object.keys(e).sort((x, y) => e[y] - e[x] || 'nvar'.indexOf(x) - 'nvar'.indexOf(y))[0];
  seen.add(lemma); out.push([lemma, P[pos]]);
  if (out.length >= 20000) break;
}
fs.writeFileSync(here('data/concepts.json'), '[\n' + out.map(x => JSON.stringify(x)).join(',\n') + '\n]\n');
const c = {}; out.forEach(([, p]) => c[p] = (c[p] || 0) + 1);
console.log(out.length, c); console.log(out.slice(0, 80).map(x => x.join('/')).join(' '));
console.log(out.slice(5000, 5040).map(x => x.join('/')).join(' '));
