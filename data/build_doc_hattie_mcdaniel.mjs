// Builds data/doc-hattie-mcdaniel.json: 8-minute long-form documentary (16:9) on Hattie McDaniel (1890s-1952).
// Built on public-domain film clips of her (Judge Priest, 1934; Nothing Sacred, 1937) plus public-domain photos.
// Free local voice (Kokoro). Every fact has two or more sources (sourcesByClaim).
// Ending follows the owner's rule: only "subscribe for more". Run: node data/build_doc_hattie_mcdaniel.mjs
import fs from 'node:fs';

const assets = {
  mammy: 'File:Hattie McDaniel as "Mammy" in Gone With the Wind promotional image.webp',
  studio: 'File:Studio publicity Hattie McDaniel.jpg',
  h1941: 'File:1941hattie.jpg',
  gwtw: 'File:Gone With The Wind featuring McDaniel & de Havilland & Leigh.jpg',
  beulah48: 'File:Hattie Mc Daniel Beulah 1948.jpg',
  beulah51: 'File:Hattie McDaniel Beulah 1951.jpg',
  victory: 'File:"Hattie McDaniel (center), Chairman of the Negro Division of the Hollywood Victory Committee, takes time off from rehear - NARA - 535875.jpg',
  bigwheel: 'File:Hattie McDaniel and Mary Hatcher in The Big Wheel (1949).jpg',
  jet1: 'File:Jet 20 Nov 1952 pg PA61.jpg',
  jet2: 'File:Jet 16 Oct 1952 pg PA60.jpg',
  grove: 'File:World famous cocoanut grove at the Ambassador Hotel, Los Angeles, California (62250).jpg',
  grove2: 'File:Ambassador Hotel Cocoanut Grove.jpg',
  premiere: 'File:Gone With the Wind Atlanta premiere 1939.jpg',
  poster: 'File:Gone With the Wind Poster 1939.jpg',
  star: "File:Hattie.McDaniel's.star.jpg",
  rosedale: 'File:Rosedale pyramid.jpg',
  usct: 'File:District of Columbia. Company E, 4th U.S. Colored Infantry, at Fort Lincoln LOC cwpb.04294.jpg',
  denver: 'File:Sixteenth Street, Denver, Colo. (NBY 186).jpg',
  cbs: 'File:CBS radio hollywood.JPG',
  monique: "File:Mo'Nique attending the 82nd Academy Awards 2010 (cropped).jpg",
};

const JP = 'File:Judge Priest (1934).webm';
const NS = 'File:Nothing Sacred (1937) by William A. Wellman.webm';
const clips = {
  laundry: { file: 'judge_priest.webm', commons: JP, start: 393, dur: 11 },
  laundry2: { file: 'judge_priest.webm', commons: JP, start: 399, dur: 7 },
  yard: { file: 'judge_priest.webm', commons: JP, start: 413, dur: 12 },
  porch: { file: 'judge_priest.webm', commons: JP, start: 2334, dur: 12 },
  ladies: { file: 'judge_priest.webm', commons: JP, start: 2384, dur: 12 },
  kitchen: { file: 'judge_priest.webm', commons: JP, start: 2583, dur: 7 },
  kitchen2: { file: 'judge_priest.webm', commons: JP, start: 2601, dur: 9 },
  stairs: { file: 'judge_priest.webm', commons: JP, start: 3794, dur: 10 },
  sacred: { file: 'nothing_sacred_clip.mp4', commons: NS, start: 0.9, dur: 2.9, speed: 0.45 },
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const V = (clip, focus = [0.4, 0.35], o = {}) => ({ kind: 'video', clip, focus, anchor: [0.5, focus[1]], zoom: [1.0, 1.06], ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });

const beats = [
  // ---- cold open
  ['o1', 'She won an Oscar. And Hollywood still would not let her be buried in its cemetery.', P('mammy', { focus: [0.5, 0.36], zoom: [1.5, 1.58], anchor: [0.75, 0.45] }), { hook: 'She won an Oscar. *Hollywood still wouldn\'t let her be buried there.*' }, { captions: false }],
  ['o2', 'On the night of February 29th, 1940, Hollywood\'s biggest stars gathered at the Ambassador Hotel in Los Angeles, for the Academy Awards.', C('grove', 'The Cocoanut Grove, Ambassador Hotel')],
  ['o3', 'One nominee did not sit with the rest of her film\'s stars. She sat at a small table, against the far wall.', P('h1941', { focus: [0.5, 0.2], zoom: [1.1, 1.2] })],
  ['o4', 'Then they read out her name. She had just become the first Black person ever to win an Oscar.', V('porch', [0.3, 0.32])],
  ['o5', 'Twelve years later, she asked for one last thing: to be buried in Hollywood Cemetery. The answer was no.', T('Whites only', 'Hollywood Cemetery, 1952')],
  ['o6', 'Her name was Hattie McDaniel. This is her story.', T('Hattie McDaniel', 'the first Black Oscar winner')],

  // ---- Denver
  ['e1', 'Hattie McDaniel was born in Wichita, Kansas, in the 1890s, the youngest of thirteen children.', P('studio', { focus: [0.47, 0.3], zoom: [1.05, 1.15], anchor: [0.65, 0.4] }), { section: 'early', pin: { label: 'Wichita, Kansas' } }],
  ['e2', 'Her parents had both been born into slavery. Her father, Henry, had fought for the Union in the Civil War.', C('usct', 'Black Union soldiers, Civil War')],
  ['e3', 'In the early 1900s, the family moved to Colorado, and settled in Denver.', C('denver', 'Sixteenth Street, Denver')],
  ['e4', 'Hattie loved to perform. At East Denver High School, she won a gold medal in a recitation contest, for a poem called Convict Joe.', T('Gold medal', 'East Denver High School')],
  ['e5', 'Her father and her brothers started a minstrel show, and soon she was on the road with them, singing and dancing.', V('laundry', [0.42, 0.35])],
  ['e6', 'She and her sister Etta even started a show of their own.', T('The McDaniel Sisters', 'Denver, 1914')],
  ['e7', 'In the 1920s, she toured with George Morrison\'s orchestra, and sang on Denver radio. She is often called the first Black woman to sing on American radio.', P('beulah48', { focus: [0.5, 0.28], zoom: [1.05, 1.15], anchor: [0.62, 0.42] })],

  // ---- stranded
  ['s1', 'Then her luck ran out. A touring show she was in went broke, and she ended up stranded in Milwaukee.', T('Stranded', 'Milwaukee, Wisconsin'), { section: 'stranded' }],
  ['s1b', 'She was far from home, with no show, and no money.', V('yard', [0.3, 0.32])],
  ['s2', 'The only work she could find was at a nightclub outside the city, Sam Pick\'s Club Madrid. Not on the stage. In the washroom, as an attendant.', T('Washroom attendant', 'Club Madrid, Milwaukee')],
  ['s3', 'Black performers were not allowed on that stage. She talked the owner into letting her sing anyway, and she became a regular.', V('laundry2', [0.42, 0.35])],
  ['s4', 'In 1931, she moved to Los Angeles to try the movies. Her brother Sam and her sister Etta were actors too.', C('cbs', 'Hollywood, 1930s')],

  // ---- Hollywood
  ['h1', 'Hollywood had one kind of part for her, again and again. The maid. The cook. The mammy.', V('kitchen', [0.3, 0.32]), { section: 'hollywood' }],
  ['h2', 'In 1934, the director John Ford cast her in Judge Priest, opposite Will Rogers. It was her first major role.', V('porch', [0.3, 0.32], { zoom: [1.06, 1.12] }), { lowerThird: { name: 'Judge Priest', sub: '1934' } }],
  ['h3', 'She even sang a duet with Rogers.', V('yard', [0.3, 0.32])],
  ['h4', 'Bigger parts followed, including The Little Colonel, with Shirley Temple.', V('ladies', [0.27, 0.32])],
  ['h4b', 'In film after film, she stole scenes from the stars, with a look, a line, or a song.', V('laundry2', [0.42, 0.35])],
  ['h5', 'She would appear in hundreds of films. In most of them, her name was not even on the screen.', V('sacred', [0.24, 0.4]), { lowerThird: { name: 'Nothing Sacred', sub: '1937' } }],
  ['h6', 'When people criticized her for the roles she took, her reported answer became famous.', V('kitchen2', [0.35, 0.32])],
  ['h7', 'Why should I complain about making seven hundred dollars a week playing a maid? If I didn\'t, I\'d be making seven dollars a week being one.', Q('Why should I complain about making $700 a week playing a maid? If I didn\'t, I\'d be making $7 a week being one.', 'Hattie McDaniel')],

  // ---- Gone with the Wind
  ['g1', 'In 1939, the producer David Selznick was casting Gone with the Wind.', C('poster', 'Gone with the Wind, 1939'), { section: 'gwtw' }],
  ['g2', 'Hattie McDaniel won the part of Mammy, the house servant of Scarlett O\'Hara\'s family.', P('gwtw', { focus: [0.14, 0.22], zoom: [1.5, 1.6], anchor: [0.4, 0.4] })],
  ['g3', 'The film opened in Atlanta on December 15th, 1939, at Loew\'s Grand Theatre.', C('premiere', 'Loew\'s Grand Theatre, Atlanta, 1939'), { stamp: '15 December 1939' }],
  ['g3b', 'It should have been one of the biggest nights of her career.', V('stairs', [0.25, 0.35])],
  ['g4', 'Hattie McDaniel was not there. Under Georgia\'s segregation laws, the theatre was for white audiences only. None of the film\'s Black actors could go.', P('premiere', { focus: [0.5, 0.5], zoom: [1.1, 1.22] })],
  ['g5', 'Her co-star Clark Gable was so angry, he threatened to boycott the premiere. She convinced him to go anyway.', P('poster', { focus: [0.5, 0.15], zoom: [1.6, 1.7], anchor: [0.5, 0.4] })],
  ['g6', 'In the South, the studio even cut the Black actors out of the film\'s publicity.', C('jet2', 'Jet magazine, 1952', { crop: [0, 0.5, 1, 0.98] })],

  // ---- Oscar night
  ['a1', 'Then came the nominations. Hattie McDaniel was nominated for Best Supporting Actress. No Black actor had ever been nominated before.', P('mammy', { focus: [0.5, 0.35], zoom: [1.1, 1.2] }), { section: 'oscar' }],
  ['a1b', 'Her co-star Olivia de Havilland was nominated in the very same category, for the very same film.', P('gwtw', { focus: [0.5, 0.25], zoom: [1.3, 1.4] })],
  ['a2', 'The ceremony was held at the Cocoanut Grove, in the Ambassador Hotel. The hotel did not normally admit Black guests.', C('grove2', 'The Cocoanut Grove, Ambassador Hotel')],
  ['a3', 'She was let in. But she and her escort were seated at a separate table, on the far side of the room, away from her co-stars.', P('grove2', { focus: [0.8, 0.5], zoom: [1.3, 1.4] })],
  ['a4', 'She wore white gardenias in her hair.', P('h1941', { focus: [0.5, 0.15], zoom: [1.3, 1.4], anchor: [0.5, 0.35] })],
  ['a5', 'Then the winner was announced. Hattie McDaniel.', V('laundry2', [0.42, 0.35]), { stamp: '29 February 1940' }],
  ['a6', 'She said: I sincerely hope I shall always be a credit to my race, and to the motion picture industry.', Q('I sincerely hope I shall always be a credit to my race and to the motion picture industry.', 'Hattie McDaniel, 1940')],
  ['a7', 'Her award was not the famous golden statuette. Supporting winners then received a small plaque.', C('jet1', 'Hattie McDaniel and her Oscar plaque', { crop: [0, 0, 1, 0.42] })],
  ['a8', 'It would be half a century before another Black woman won an acting Oscar.', T('50 years', 'until the next Black woman won')],

  // ---- critics and the war
  ['c1', 'Not everyone celebrated. The NAACP, and its leader Walter White, criticized her for playing maids and mammies, roles that kept racist stereotypes alive.', V('kitchen2', [0.35, 0.32]), { section: 'critics' }],
  ['c2', 'She kept working. During World War Two, she led the Negro Division of the Hollywood Victory Committee, bringing entertainment to Black soldiers.', C('victory', 'Hattie McDaniel (center), Hollywood Victory Committee')],

  // ---- Sugar Hill
  ['k1', 'By then she owned a large house in West Adams, a Los Angeles neighborhood so popular with Black stars that it was nicknamed Sugar Hill.', P('h1941', { focus: [0.5, 0.4], zoom: [1.05, 1.15] }), { section: 'home' }],
  ['k2', 'In 1945, some white neighbors went to court. They wanted to use old racial covenants to force the Black homeowners out.', T('Sugar Hill', 'Los Angeles, 1945'), { stamp: '1945' }],
  ['k3', 'Hattie McDaniel helped rally her neighbors to fight back. The judge threw the case out.', V('ladies', [0.27, 0.32])],
  ['k4', 'Three years later, the Supreme Court ruled that courts could not enforce racial covenants anywhere in the country.', T('1948', 'covenants unenforceable')],

  // ---- Beulah
  ['b1', 'In 1947, she took over the lead in a radio comedy, The Beulah Show.', P('beulah48', { focus: [0.5, 0.3], zoom: [1.25, 1.35], anchor: [0.62, 0.42] }), { section: 'beulah' }],
  ['b2', 'Later, she began playing Beulah on television too. But she managed only six episodes. She was ill with breast cancer.', P('beulah51', { focus: [0.6, 0.22], zoom: [1.1, 1.2], anchor: [0.6, 0.4] })],

  // ---- last wish
  ['b3', 'The role went to Louise Beavers, another actress who lived on Sugar Hill.', P('beulah48', { focus: [0.45, 0.3], zoom: [1.1, 1.2] })],
  ['d1', 'Hattie McDaniel died on October 26th, 1952. She was 59.', P('studio', { focus: [0.47, 0.3], zoom: [1.15, 1.25] }), { section: 'end', stamp: '26 October 1952' }],
  ['d2', 'Some three thousand mourners came to her funeral.', V('stairs', [0.25, 0.35])],
  ['d2b', 'But Hollywood had one more insult left for her.', T('One last wish', '1952')],
  ['d3', 'In her will, she made one request. She wanted to be buried in Hollywood Cemetery.', T('Her last wish', 'Hollywood Cemetery')],
  ['d4', 'The cemetery refused. It did not bury Black people.', T('Refused', 'whites only')],
  ['d5', 'She was buried across town, at Rosedale Cemetery.', C('rosedale', 'Rosedale Cemetery, Los Angeles')],
  ['d6', 'She left her Oscar plaque to Howard University, the historically Black university in Washington.', C('jet1', 'Jet magazine, November 1952', { crop: [0, 0, 1, 0.62] })],
  ['d7', 'It was displayed there for years. Then, around 1970, it disappeared. It has never been found.', P('jet1', { focus: [0.62, 0.18], zoom: [1.8, 1.95] })],

  // ---- legacy
  ['l1', 'In 1999, the cemetery that refused her had a new owner. He offered to move her there. Her family said no.', T('1999', 'Hollywood Forever'), { section: 'legacy' }],
  ['l2', 'So the cemetery put up a memorial to her instead. It stands there today.', V('porch', [0.3, 0.32], { zoom: [1.1, 1.16] })],
  ['l3', 'She has two stars on the Hollywood Walk of Fame, one for film, and one for radio.', C('star', 'Hollywood Walk of Fame')],
  ['l4', 'In 2010, when Mo\'Nique won the same Oscar, she wore a blue dress and a gardenia in her hair, as Hattie McDaniel had seventy years before.', C('monique', 'Mo\'Nique, 2010')],
  ['l5', 'And in 2023, the Academy gave Howard University a replacement for her lost Oscar. The ceremony was called Hattie\'s Come Home.', T('Hattie\'s Come Home', 'Howard University, 2023')],

  // ---- close
  ['z1', 'Her parents were born into slavery. She cleaned washrooms. She played maids in hundreds of films.', V('laundry', [0.42, 0.35]), { section: 'close' }],
  ['z2', 'And she won Hollywood\'s highest honor, at a table set apart from everyone else.', P('mammy', { focus: [0.5, 0.36], zoom: [1.05, 1.15] })],
  ['z2b', 'Her Oscar is still missing. But her name is not.', C('star', 'Hollywood Walk of Fame')],
  ['z3', 'That was Hattie McDaniel. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-ona-judge.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Hattie_McDaniel',
  DPL: 'https://history.denverlibrary.org/colorado-biographies/hattie-mcdaniel-1893-1952',
  KSHS: 'https://www.kansashistory.gov/kansapedia/hattie-mcdaniel/12142',
  ENC: 'https://www.encyclopedia.com/history/encyclopedias-almanacs-transcripts-and-maps/mcdaniel-hattie',
  BP: 'https://www.blackpast.org/african-american-history/mcdaniel-hattie-1895-1952/',
  MKE: 'https://milwaukeebronzevillehistories.org/items/show/7',
  BRIT: 'https://www.britannica.com/biography/Hattie-McDaniel',
  BIO: 'https://www.biography.com/actors/hattie-mcdaniel',
  JET: 'https://commons.wikimedia.org/wiki/File:Jet_20_Nov_1952_pg_PA61.jpg',
  JET2: 'https://commons.wikimedia.org/wiki/File:Jet_16_Oct_1952_pg_PA60.jpg',
  AJC: 'https://www.ajc.com/news/years-ago-actress-hattie-mcdaniel-broke-the-color-barrier-the-oscars/vtEEXYKtaeJqKIEFPhIjAM/',
  WEEK: 'https://theweek.com/articles/539316/remembering-hattie-mcdaniel-75-years-since-historic-oscar-win',
  YAHOO: 'https://ca.movies.yahoo.com/news/oscar-s-first-black-winner-accepted-her-honor-in-a-segregated--no-blacks--hotel-in-l-a-213002304.html',
  AND: 'https://andscape.com/features/film-academy-replaces-hattie-mcdaniels-long-lost-oscar/',
  CBS: 'https://www.cbsnews.com/colorado/news/hattie-mcdaniel-missing-academy-award-replacement-gift-howard-university',
  NBCLA: 'https://nbclosangeles.com/news/local/monique-hattie-mcdaniel-and-west-adams/1867946',
  HF: 'https://en.wikipedia.org/wiki/Hollywood_Forever_Cemetery',
  NARA: 'https://commons.wikimedia.org/wiki/File:%22Hattie_McDaniel_(center),_Chairman_of_the_Negro_Division_of_the_Hollywood_Victory_Committee,_takes_time_off_from_rehear_-_NARA_-_535875.jpg',
  FAG: 'https://www.findagrave.com/memorial/7101',
  AMS: 'https://amsterdamnews.com/news/2017/03/02/film-immortal-hattie-mcdaniel/',
};
const sourcesByClaim = {
  o2: ['WIKI', 'AND'], o3: ['WIKI', 'AND', 'CBS'], o4: ['WIKI', 'AND', 'KSHS'], o5: ['WIKI', 'NBCLA', 'DPL'],
  e1: ['WIKI', 'KSHS', 'DPL'], e2: ['WIKI', 'DPL', 'KSHS'], e3: ['KSHS', 'DPL'], e4: ['WIKI', 'DPL', 'BP'], e5: ['WIKI', 'DPL'], e6: ['WIKI', 'DPL'], e7: ['DPL', 'ENC', 'WIKI'],
  s1: ['MKE', 'DPL', 'WIKI'], s2: ['WIKI', 'MKE', 'DPL'], s3: ['WIKI', 'MKE'], s4: ['WIKI', 'KSHS', 'DPL'],
  h1: ['WIKI', 'JET2'], h2: ['WIKI', 'BRIT', 'ENC'], h3: ['WIKI', 'BRIT'], h4: ['BIO', 'WIKI'], h5: ['WIKI', 'JET2'], h6: ['WIKI', 'AMS'], h7: ['WIKI', 'AMS'],
  g1: ['WIKI', 'ENC'], g2: ['WIKI', 'KSHS', 'ENC'], g3: ['WIKI', 'AJC'], g4: ['WIKI', 'ENC', 'DPL', 'AJC'], g5: ['WIKI', 'AJC', 'WEEK'], g6: ['WIKI', 'ENC'],
  a1: ['WIKI', 'AND'], a1b: ['WIKI', 'AND'], a2: ['WIKI', 'YAHOO'], a3: ['WIKI', 'AND', 'CBS'], a4: ['WIKI', 'NBCLA'], a5: ['WIKI', 'AND'], a6: ['WIKI', 'AND'], a7: ['WIKI', 'AND'], a8: ['AND', 'WIKI'],
  c1: ['WIKI', 'AJC'], c2: ['WIKI', 'NARA'],
  k1: ['NBCLA', 'WIKI'], k2: ['WIKI', 'NBCLA'], k3: ['WIKI', 'NBCLA'], k4: ['NBCLA', 'WIKI'],
  b1: ['ENC', 'WIKI'], b2: ['WIKI', 'ENC'], b3: ['WIKI', 'NBCLA'],
  d1: ['WIKI', 'AND'], d2: ['WIKI', 'FAG'], d3: ['WIKI', 'NBCLA', 'DPL'], d4: ['WIKI', 'NBCLA', 'DPL'], d5: ['WIKI', 'NBCLA'], d6: ['WIKI', 'AND', 'JET'], d7: ['AND', 'DPL', 'WIKI'],
  l1: ['WIKI', 'HF'], l2: ['HF', 'NBCLA'], l3: ['WIKI', 'NBCLA'], l4: ['WIKI', 'NBCLA'], l5: ['AND', 'CBS', 'WIKI'],
};

const spec = {
  id: 'doc-hattie-mcdaniel',
  title: 'She Won an Oscar. Hollywood Wouldn\'t Let Her Be Buried There.',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { Cocoanut: 'Coconut', Etta: 'Et-tah', "Mo'Nique": 'Moe-neek' },
  music: base.music,
  mix: base.mix,
  brand: { page: 'The Black History Room', cta: 'Subscribe', ctaLine: '', theme: 'bhr' },
  assets: Object.fromEntries(Object.entries(assets).map(([k, v]) => [k, { commons: v }])),
  clips,
  beats: beats.map(([id, text, visual, overlays, extra]) => {
    const { section, ...ov } = overlays || {};
    return { id, text, visual, ...(Object.keys(ov).length ? { overlays: ov } : {}), ...(section ? { section } : {}), ...(extra || {}) };
  }),
  sourcesByClaim,
  sources: Object.fromEntries(Object.entries(sources).map(([k, url]) => [k, { url }])),
  notUsed: [
    'Birth year 1893 (Wikipedia, Denver Public Library) vs 1895 (Kansas Historical Society): script says "in the 1890s".',
    'Year she was stranded in Milwaukee: 1929 (Wikipedia, Milwaukee Bronzeville) vs 1926 (Denver Public Library): no year said.',
    'Audition in an authentic maid\'s uniform; Hollywood premiere on Dec 28, 1939; USO shows; working as a maid between film roles: one source each, not used.',
    'Will asking for white gardenias and a white casket: weak sources only, not used.',
    'The $700 quote: wording differs between sources; introduced as her "reported" answer.',
    'Oscar disappearance: late 1960s (Andscape), 1972 (Denver Public Library): script says "around 1970".',
  ],
};
fs.writeFileSync('data/doc-hattie-mcdaniel.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images, ${Object.keys(clips).length} clips`);
