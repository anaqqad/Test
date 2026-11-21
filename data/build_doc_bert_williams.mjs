// Builds data/doc-bert-williams.json: ~8-minute long-form documentary (16:9) on Bert Williams (1874-1922).
// Film: A Natural Born Gambler (Biograph, 1916), public domain on Wikimedia Commons; it holds his silent poker routine.
// Every fact has two or more sources (sourcesByClaim). Ending: only "subscribe for more".
// Voice: `node data/build_doc_bert_williams.mjs [kokoro|elevenlabs]` (elevenlabs is paid: ask first).
import fs from 'node:fs';

const VOICE = process.argv[2] || 'kokoro';
const assets = {
  suit1921: 'File:BertWilliamsPhotoPortraitWithCigarette.jpg',
  suit1921b: 'File:Bert Williams -31 LCCN2004674530.jpg',
  cork: 'File:Bert Williams blackface 2.jpg',
  wave: 'File:Bert Williams -10 LCCN2004674535.jpg',
  hands: 'File:Bert Williams -12 LCCN2014645145.jpg',
  bowtie: 'File:Bert Williams cph.3a03399.jpg',
  young1896: 'File:BertWilliams1896.jpg',
  young1902: 'File:Bert Williams, stage actor (SAYRE 11054).jpg',
  grin1905: 'File:Bert Williams, stage comedian (SAYRE 1063).jpg',
  oval1903: 'File:BertWilliamsJonahMan.jpg',
  whitetie: 'File:Harvard Theatre Collection - Bert Williams TCS 1.1119.jpg',
  bowler: 'File:Harvard Theatre Collection - Bert Williams TCS 1.1120.jpg',
  ww: 'File:Maud Cuney Hare-williams and walker-159.jpg',
  coons: 'File:Williams and Walker poster 1903.jpg',
  dahomey: 'File:In Dahomey 1903.jpg',
  cakewalk: 'File:In Dahomey, Cakewalk.jpg',
  jonah: 'File:WilliamsWalkerJohnahMan.jpg',
  bandanna: 'File:Bon Bon Buddy cover.jpg',
  palace: 'File:Charles B. Falls - Bert Williams Palace Theatre poster.jpg',
  follies1919: 'File:Johnny Dooley, Eddie Cantor, Gus Van, Bert Williams, Joe Schenck, Eddie Dowling, & Ray Dooley, Follies of 1919.jpg',
  limekiln: 'File:Lime kiln field day cast.jpg',
  uniform: 'File:1916 United States Army Captain Bert Williams, portrait, facing right, singing a psalm at the first regimental open air service for the 15th Regiment of the New York National Guard - LCCN96521643 (cropped).jpg',
  tophat: 'File:BertWilliamsBlackfaceTophatSmile.jpg',
};

const NBG = 'File:A Natural Born Gambler (1916).webm';
const g = (start, dur, o = {}) => ({ file: 'gambler.webm', commons: NBG, start, dur, ...o });
const clips = {
  title: g(0, 6),
  bar0: g(22, 8), bar1: g(68, 8), bar2: g(78, 12), bar3: g(96, 8), bar4: g(104, 10),
  lodge: g(140, 9), lodge2: g(160, 10), yard: g(270, 8), crowd: g(450, 8), table: g(500, 8),
  court0: g(1124, 12), court1: g(1110, 12), court2: g(1150, 5), court3: g(1164, 5),
  cell: g(1205, 13),
  pk1: g(1223, 13), pk2: g(1239, 11), pk3: g(1251, 7), pk4: g(1257, 11), pk5: g(1269, 17), pk6: g(1287, 13),
  pk7: g(1303, 13), pk8: g(1317, 18), pk9: g(1337, 13), pk10: g(1350, 6),
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const V = (clip, focus = [0.5, 0.35], o = {}) => ({ kind: 'video', clip, focus, anchor: [0.5, focus[1]], zoom: [1.0, 1.06], ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const PZ = (key, fy = 0.25) => P(key, { focus: [0.5, fy], zoom: [1.05, 1.15], anchor: [0.5, 0.4] });
const PK = [0.7, 0.3]; // Bert's face in the poker routine

const beats = [
  // ---- open
  ['o1', 'He was the highest-paid Black entertainer in America. And every night, before he walked on stage, he had to paint his face black.', P('suit1921', { focus: [0.5, 0.22], zoom: [1.0, 1.05], anchor: [0.5, 0.36] }), { hook: 'America\'s highest-paid Black star. *Every night, he had to black up.*' }, { captions: false }],
  ['o2', 'He was the first Black man to star on Broadway, and the only Black star in the biggest white show of its day.', V('pk4', PK)],
  ['o3', 'W. C. Fields called him the funniest man he ever saw, and the saddest man he ever knew.', V('pk1', PK)],
  ['o4', 'His name was Bert Williams. This is his story.', T('Bert Williams', '1874 to 1922')],

  // ---- early life
  ['e1', 'Egbert Austin Williams was born on November 12th, 1874, in Nassau, in the Bahamas.', C('young1896', 'Bert Williams as a young man'), { section: 'early', pin: { label: 'Nassau, Bahamas' } }],
  ['e2', 'His family moved to the United States while he was a boy, and he grew up partly in California.', T('California', 'a long way from Broadway')],
  ['e3', 'As a teenager, he joined traveling minstrel shows. In 1893, in San Francisco, he met another young performer, George Walker.', C('ww', 'Bert Williams and George Walker'), { stamp: '1893' }],
  ['e4', 'They teamed up. Walker was the flashy one, a strutting dandy. Bert was the slow, sad-faced one, who always got the worst of it.', C('jonah', 'Williams and Walker')],
  ['e5', 'In 1896 they reached New York.', V('bar0', [0.5, 0.4]), { stamp: '1896' }],

  // ---- the mask
  ['m1', 'There was a catch. In those days, Black performers were expected to wear blackface, just like the white minstrels who mocked them.', P('cork', { focus: [0.4, 0.4], zoom: [1.05, 1.15], anchor: [0.45, 0.5] }), { section: 'mask' }],
  ['m2', 'Bert was light-skinned. So before every show, he burned cork, and smeared it over his face.', PZ('bowtie', 0.15)],
  ['m3', 'Then he walked out on stage, and played the slow, unlucky fool the crowds expected.', PZ('wave', 0.15)],
  ['m4', 'Williams and Walker even billed themselves as Two Real Coons, to set themselves apart from the white men in burnt cork.', C('coons', 'Williams and Walker poster, 1903')],
  ['m5', 'Off stage, they dressed in sharp suits, and posed for elegant photographs. The contrast was the point.', C('young1902', 'Bert Williams, 1902')],
  ['m6', 'In 1901, they recorded for the Victor company. They were among the very first Black artists to record for a major label.', T('1901', 'Victor records')],

  // ---- broadway
  ['b1', 'In 1903, they opened In Dahomey, a musical written, directed and performed by an all-Black cast.', C('dahomey', 'In Dahomey, 1903'), { section: 'broadway', stamp: '1903' }],
  ['b2', 'It was the first all-Black musical to play a major Broadway theater.', C('cakewalk', 'In Dahomey: the cakewalk')],
  ['b3', 'But inside that theater, the seats were segregated. Black fans watched their own stars from a separate section.', V('crowd', [0.5, 0.4])],
  ['b4', 'Then the show sailed for England. It was a hit in London, and the company gave a command performance at Buckingham Palace.', P('coons', { focus: [0.5, 0.3], zoom: [1.1, 1.2], anchor: [0.5, 0.4] })],
  ['b5', 'In Scotland, Bert became a Freemason. American lodges would not admit Black men.', C('oval1903', 'Bert Williams, 1903')],
  ['b6', 'Back home, they followed it with Abyssinia, in 1906, and Bandanna Land, in 1908.', C('bandanna', 'Bandanna Land sheet music, 1907')],
  ['b7', 'In those years Bert introduced the song that would follow him for the rest of his life. It was called Nobody.', P('grin1905', { focus: [0.5, 0.4], zoom: [1.05, 1.15], anchor: [0.5, 0.45] })],
  ['b8', 'A sad, slow song about a man nobody ever helps. Audiences demanded it at almost every show.', V('pk6', PK)],

  // ---- alone
  ['a1', 'Then George Walker fell ill. In 1909 he collapsed on stage, and never performed again. He died in 1911.', P('ww', { focus: [0.5, 0.35], zoom: [1.1, 1.2], anchor: [0.5, 0.4] }), { section: 'alone', stamp: '1911' }],
  ['a2', 'Bert went on alone, in vaudeville. Many white performers refused to share a bill with him.', V('bar3', [0.65, 0.3])],
  ['a3', 'On tour, he usually had to travel, eat and sleep apart from the rest of the company.', PZ('suit1921b', 0.2)],

  // ---- ziegfeld
  ['z1', 'Then, in 1910, came an offer nobody expected. Florenz Ziegfeld wanted him for the Follies, the most famous revue on Broadway.', C('palace', 'Bert Williams poster, about 1918'), { section: 'follies', stamp: '1910' }],
  ['z2', 'Bert would be the only Black star in an all-white cast.', V('bar1', [0.65, 0.3])],
  ['z3', 'Some of the cast gave Ziegfeld an ultimatum. Fire him, or we walk.', V('lodge', [0.5, 0.4])],
  ['z4', 'Ziegfeld refused. He reportedly told them: I can replace every one of you, except him.', V('court1', [0.25, 0.3])],
  ['z5', 'When the show opened that June, Bert was the sensation of the night.', V('pk2', PK)],
  ['z6', 'Columbia Records signed him. His records sold all over the country, and he made dozens of them.', T('Columbia Records', 'an exclusive contract')],
  ['z7', 'He became one of the stars of the Follies for most of the next decade, alongside W. C. Fields, Fanny Brice, Will Rogers, and his close friend Eddie Cantor.', C('follies1919', 'Ziegfeld Follies of 1919, with Eddie Cantor')],
  ['z8', 'He was the highest-paid Black entertainer in America.', P('whitetie', { focus: [0.5, 0.2], zoom: [1.05, 1.15], anchor: [0.5, 0.35] })],

  // ---- the insult
  ['i1', 'But fame did not open every door.', PZ('bowler', 0.2), { section: 'insult' }],
  ['i2', 'When he came back to his hotel after a show, he was told to use the freight elevator.', P('suit1921', { focus: [0.5, 0.22], zoom: [1.1, 1.2], anchor: [0.5, 0.36] })],
  ['i3', 'He told Eddie Cantor: It wouldn\'t be so bad, Eddie, if I didn\'t still hear the applause ringing in my ears.', V('cell', [0.2, 0.72])],
  ['i4', 'Once, a bartender at a fancy New York bar tried to get rid of him. He said a drink would cost fifty dollars.', V('bar2', [0.65, 0.3])],
  ['i5', 'Bert pulled out a pile of big bills, put it on the bar, and kept ordering.', V('bar4', [0.65, 0.3])],
  ['i6', 'In his only known essay, he wrote that he had never found anything disgraceful in being a colored man. But he had often found it inconvenient. In America.', PZ('tophat', 0.15)],

  // ---- on film
  ['f1', 'He also tried the movies. In 1913 he starred in a comedy with an all-Black cast, called Lime Kiln Field Day.', C('limekiln', 'Lime Kiln Field Day, 1913'), { section: 'film', stamp: '1913' }],
  ['f2', 'It was never released. The footage sat in a museum vault for a century, until the Museum of Modern Art restored it in 2014.', P('limekiln', { focus: [0.5, 0.4], zoom: [1.1, 1.2], anchor: [0.5, 0.45] })],
  ['f3', 'In 1916, the Biograph company filmed him in a short comedy, A Natural Born Gambler. It survives.', V('title', [0.5, 0.5]), { stamp: '1916' }],
  ['f4', 'He plays the head of a lodge, who cannot stay away from the card table.', V('table', [0.5, 0.4])],
  ['f5', 'And at the end, locked in a cell, he performs his most famous routine.', V('pk3', PK)],
  ['f6', 'A poker game, with no cards, no table, and no other players. Just one man, under a light.', V('pk5', PK)],
  ['f7', 'You can follow every hand in his face. The hope, the bluff, the bad card, the loss.', V('pk7', PK)],

  // ---- nobody
  ['n1', 'In August 1919, Broadway\'s actors went on strike. The whole Follies cast walked out.', T('August 1919', 'the actors\' strike'), { section: 'strike' }],
  ['n2', 'Nobody told Bert. He showed up for work, and found an empty theater.', V('cell', [0.2, 0.72], { zoom: [1.06, 1.12] })],
  ['n3', 'After more than twenty years on the New York stage, the actors\' union had never invited him to join.', PZ('suit1921b', 0.2)],
  ['n4', 'Friends said he grew quieter, and sadder. W. C. Fields, who was close to him, said the strike helped break his health.', V('pk8', PK)],

  // ---- the end
  ['d1', 'By 1922 he was starring in a new show, Under the Bamboo Tree. He caught pneumonia, but kept performing.', C('uniform', 'Bert Williams'), { section: 'end' }],
  ['d2', 'In February 1922, on tour in Detroit, he collapsed on stage.', T('February 1922', 'Detroit, Michigan')],
  ['d3', 'At first, the audience thought it was part of the act.', V('pk9', PK)],
  ['d4', 'They helped him to his dressing room. He reportedly said: That\'s a nice way to die. They was laughing when I made my last exit.', V('pk3', PK, { zoom: [1.06, 1.12] })],
  ['d5', 'He was taken home to New York. On March 4th, 1922, Bert Williams died.', P('uniform', { focus: [0.45, 0.3], zoom: [1.1, 1.2], anchor: [0.45, 0.42] }), { stamp: 'March 4, 1922' }],
  ['d6', 'Thousands of people lined up to see his coffin.', V('court0', [0.5, 0.4])],
  ['d7', 'And the Masons of New York, whose lodges had shut him out, gave him a Masonic funeral. He was the first Black man buried with Masonic honors.', PZ('young1902', 0.3)],

  // ---- legacy
  ['l1', 'His song Nobody outlived him by a century.', V('pk6', PK, { zoom: [1.06, 1.12] }), { section: 'legacy' }],
  ['l2', 'Singers kept coming back to it for generations. In the year 2000, Johnny Cash recorded it.', T('Nobody', 'Johnny Cash, 2000')],
  ['l3', 'He spent his whole career behind a mask other people made for him. And he was still the best in the business.', P('cork', { focus: [0.4, 0.4], zoom: [1.1, 1.2], anchor: [0.45, 0.5] })],

  // ---- close
  ['x1', 'He came from Nassau. He reached Broadway, London and the Follies. And every night, he painted on a face that wasn\'t his.', P('suit1921', { focus: [0.5, 0.22], zoom: [1.1, 1.2], anchor: [0.5, 0.36] }), { section: 'close' }],
  ['x2', 'That was Bert Williams. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-joe-louis.json', 'utf8'));
const VOICES = {
  kokoro: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  elevenlabs: { engine: 'elevenlabs', voiceId: 'gUABw7pXQjhjt0kNFBTF', voiceName: 'Andrew - Smooth audio books', model: 'eleven_multilingual_v2', stability: 0.6, similarity: 0.75, style: 0, speed: 1.0, seed: 1234, leadInSeconds: 0.4, sectionGapSeconds: 1 },
};
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Bert_Williams',
  ENC: 'https://www.encyclopedia.com/people/literature-and-arts/theater-biographies/bert-williams',
  PBS: 'https://www.pbs.org/wnet/broadway/stars/bert-williams/',
  UA: 'https://sites.arizona.edu/vaudeville/bert-williams-vaudevilles-biggest-black-superstar-by-david-soren',
  FASSLER: 'https://ronfassler.org/post/2418/A-COMEDIAN-S-TRAGEDY-THE-STORY-OF-BERT-WILLIAMS',
  TMANIA: 'https://www.theatermania.com/news/bert-williams-americas-first-black-star-part-ii_70442',
  FIELDS: 'https://rd.springer.com/chapter/10.1057/978-1-349-94986-1_9',
  NORMAN: 'https://normanstudios.org/blog/2017/01/26/the-iconic-mr-nobody-an-analysis-of-silent-film-legend-bert-williams/',
  WHIP: 'https://cablecarguy.blogspot.com/2022/03/bert-williams-100-years-march-4-2022.html',
  FILM: 'https://commons.wikimedia.org/wiki/File:A_Natural_Born_Gambler_(1916).webm',
  CASH: 'https://en.wikipedia.org/wiki/American_III:_Solitary_Man',
};
const sourcesByClaim = {
  o1: ['WIKI', 'UA', 'ENC'], o2: ['WIKI', 'ENC', 'UA'], o3: ['WIKI', 'ENC', 'PBS', 'TMANIA'],
  e1: ['WIKI', 'ENC', 'FASSLER'], e2: ['WIKI', 'ENC', 'FASSLER'], e3: ['WIKI', 'ENC', 'PBS'], e4: ['WIKI', 'ENC'], e5: ['WIKI', 'ENC', 'PBS'],
  m1: ['WIKI', 'UA'], m2: ['WIKI', 'UA', 'ENC'], m3: ['WIKI', 'ENC'], m4: ['WIKI', 'ENC'], m5: ['WIKI', 'TMANIA'], m6: ['WIKI', 'FASSLER', 'ENC'],
  b1: ['WIKI', 'ENC', 'PBS'], b2: ['WIKI', 'ENC'], b3: ['WIKI', 'UA'], b4: ['WIKI', 'ENC', 'FASSLER'], b5: ['WIKI', 'ENC'], b6: ['WIKI', 'ENC', 'PBS'],
  b7: ['WIKI', 'ENC', 'PBS', 'TMANIA'], b8: ['WIKI', 'TMANIA'],
  a1: ['WIKI', 'PBS', 'ENC'], a2: ['WIKI', 'PBS'], a3: ['WIKI', 'PBS', 'UA'],
  z1: ['WIKI', 'PBS', 'UA', 'ENC'], z2: ['WIKI', 'UA', 'FASSLER'], z3: ['WIKI', 'FASSLER', 'ENC'], z4: ['WIKI', 'FASSLER'], z5: ['WIKI', 'FASSLER'],
  z6: ['WIKI', 'ENC', 'FASSLER'], z7: ['WIKI', 'UA', 'TMANIA', 'PBS'], z8: ['WIKI', 'ENC'],
  i1: ['ENC', 'PBS'], i2: ['ENC', 'PBS'], i3: ['ENC', 'PBS'], i4: ['WIKI', 'TMANIA'], i5: ['WIKI', 'TMANIA'], i6: ['WIKI', 'ENC'],
  f1: ['WIKI', 'TMANIA'], f2: ['WIKI', 'TMANIA'], f3: ['WIKI', 'UA', 'PBS', 'FILM'], f4: ['FILM', 'FASSLER'], f5: ['WIKI', 'FASSLER', 'FILM'], f6: ['WIKI', 'PBS'], f7: ['WIKI', 'PBS'],
  n1: ['WIKI', 'FIELDS', 'NORMAN'], n2: ['WIKI', 'NORMAN'], n3: ['FIELDS', 'NORMAN'], n4: ['FIELDS', 'WIKI'],
  d1: ['WIKI', 'ENC'], d2: ['WIKI', 'ENC', 'FASSLER'], d3: ['WIKI', 'FASSLER'], d4: ['WIKI', 'FASSLER'], d5: ['WIKI', 'ENC', 'PBS'],
  d6: ['WIKI', 'WHIP'], d7: ['WIKI', 'UA', 'ENC'],
  l1: ['WIKI', 'TMANIA'], l2: ['WIKI', 'CASH'], l3: ['WIKI', 'UA'],
};
const spec = {
  id: 'doc-bert-williams',
  title: 'He Had to Black Up Every Night: The Bert Williams Story',
  format: 'doc', fps: 30, width: 1920, height: 1080,
  voice: VOICES[VOICE],
  pronounce: { Nassau: 'Nass-saw', Ziegfeld: 'Zigfeld', Florenz: 'Florents', Dahomey: 'Da-homey', Egbert: 'Egg-burt', Abyssinia: 'Abbysinnia', Biograph: 'Bio-graph', Bandanna: 'Ban-danna' },
  music: base.music, mix: base.mix,
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
    'Age at death (46 or 47) differs: not said.',
    'Date of the Detroit collapse (Feb 21 / 25 / 27) differs: month only.',
    'Year of the Buckingham Palace performance (1903 / 1904) differs: no year said.',
    'Booker T. Washington "smiled his way into people\'s hearts" quote: attribution disputed (Washington vs Carver): not used.',
    '"Nobody wants me" (strike) quote: single source: not used.',
    'Year he married Lottie Thompson (1899 / 1900) differs: marriage not used.',
    'Bar story details differ (a roll of hundreds and a round for the room / a $500 bill and ten drinks): kept general.',
    'Funeral crowd 5,000 (Wikipedia) vs 7,000 (Chicago Whip): "thousands".',
  ],
};
fs.writeFileSync('data/doc-bert-williams.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images, voice ${VOICE}`);
