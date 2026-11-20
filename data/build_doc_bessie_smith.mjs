// Builds data/doc-bessie-smith.json: ~8-minute long-form documentary (16:9) on Bessie Smith (1892?-1937).
// Film: St. Louis Blues (1929), her only film, public domain on Wikimedia Commons (Library of Congress copy).
// Every fact has two or more sources (sourcesByClaim). Ending: only "subscribe for more".
// Voice: `node data/build_doc_bessie_smith.mjs [kokoro|elevenlabs]` (elevenlabs is paid: ask first).
import fs from 'node:fs';

const VOICE = process.argv[2] || 'kokoro';
const assets = {
  vv1936: 'File:Bessie Smith (1936) by Carl Van Vechten.jpg',
  vv72: 'File:Portrait of Bessie Smith LCCN2004663572.jpg',
  vv74: 'File:Portrait of Bessie Smith LCCN2004663574.jpg',
  vv75: 'File:Bessie Smith, three-quarter length portrait, standing, facing front, with left hand raised LCCN2004663575.jpg',
  feathers: 'File:Portrait of Bessie Smith holding feathers LCCN2004663573.jpg',
  young: 'File:Bessiesmith3.jpg',
  bs: 'File:Bessiesmith.jpg',
  rainey: 'File:Ma Rainey, 1923.jpg',
  ad1923: 'File:Columbia Records ad, Chicago Tribune, May 19, 1923.jpg',
  ad2: 'File:Popular Songs, June 20, 1923 Columbia Records ad.png',
  label: 'File:ColumbiaLabelBSmith.jpg',
  fho: 'File:FletcherHendersonOrchestra1925.jpg',
  handy: 'File:WCHandy.jpg',
  poster: 'File:St. Louis Blues (poster for 1929 film).jpg',
  death: 'File:Death certificate (1).jpg',
  grave: 'File:Bessie Smith grave.jpg',
  joplin: 'File:Janis Joplin seated 1970.JPG',
};

const STL = 'File:St. Louis Blues.webm';
const s = (start, dur, o = {}) => ({ file: 'St._Louis_Blues.webm', commons: STL, start, dur, ...o });
const clips = {
  titlecard: s(21, 6),
  hall: s(52, 7), hall2: s(65, 8),
  dance: s(122, 7),
  enter: s(273, 7), withman: s(292, 7), argue: s(336, 8),
  floor: s(410, 8), close1: s(423, 6), close2: s(429, 5), close3: s(435.5, 4),
  band: s(488, 7), band2: s(495, 6),
  bar3: s(512.5, 7.5), crowd: s(541, 8), bar8: s(608, 8), bar8b: s(622, 8),
  bar12: s(885, 10), bar13: s(900, 9), bar14: s(929.5, 6.5),
  swing: s(728, 8), embrace: s(781, 7),
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const V = (clip, focus = [0.5, 0.35], o = {}) => ({ kind: 'video', clip, focus, anchor: [0.5, focus[1]], zoom: [1.0, 1.06], ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const PZ = (key) => P(key, { focus: [0.5, 0.3], zoom: [1.05, 1.15], anchor: [0.5, 0.42] });

const beats = [
  // ---- open
  ['o1', 'In the 1920s, she was the biggest blues star in America. Then she lay in an unmarked grave for thirty-three years.', P('vv1936', { focus: [0.5, 0.3], zoom: [1.0, 1.05], anchor: [0.5, 0.4] }), { hook: 'The biggest blues star in America. *Then 33 years in an unmarked grave.*' }, { captions: false }],
  ['o2', 'She sold records by the hundreds of thousands, at a time when record companies had barely noticed Black buyers.', V('close1')],
  ['o3', 'She faced down the Ku Klux Klan alone. And she made one film. This is it.', V('bar8', [0.62, 0.35])],
  ['o4', 'Her name was Bessie Smith. They called her the Empress of the Blues. This is her story.', T('Bessie Smith', 'the Empress of the Blues')],

  // ---- Chattanooga
  ['e1', 'Bessie Smith was born in Chattanooga, Tennessee, in the early 1890s. Even the year is uncertain.', C('young', 'Bessie Smith'), { section: 'early', pin: { label: 'Chattanooga, Tennessee' } }],
  ['e2', 'Her father, William, was a laborer and a part-time Baptist preacher. He died when she was too young to remember him.', T('Chattanooga', 'a poor family')],
  ['e3', 'By the time she was nine, her mother and a brother had died too. Her older sister Viola raised the children.', C('bs', 'Bessie Smith')],
  ['e4', 'There was no money for school. So Bessie and her brother Andrew went out to the streets.', C('vv72', 'Bessie Smith')],
  ['e5', 'He played the guitar. She sang and danced, for pennies, on a corner in front of the White Elephant Saloon.', T('Street corners', 'singing for pennies')],

  // ---- the road
  ['r1', 'In 1904, her oldest brother, Clarence, left home to join a traveling show. He left without telling her, because she would have followed him.', C('vv74', 'Bessie Smith, photographed by Carl Van Vechten'), { section: 'road', stamp: '1904' }],
  ['r2', 'In 1912 he came back with the show, and got her an audition.', T('1912', 'the Moses Stokes show')],
  ['r3', 'They hired her as a dancer, because the company already had a star singer: Ma Rainey, the Mother of the Blues.', C('rainey', 'Ma Rainey, 1923')],
  ['r4', 'People later said Ma Rainey taught Bessie to sing. That is probably a myth. But she likely helped her learn to own a stage, and they stayed friends for life.', P('rainey', { focus: [0.5, 0.35], zoom: [1.1, 1.2], anchor: [0.5, 0.42] })],
  ['r5', 'By 1913 she had her own act in Atlanta, at the 81 Theater, for about ten dollars a week.', V('dance', [0.5, 0.4]), { stamp: '1913' }],
  ['r6', 'For the next ten years she toured the South, in tent shows and Black theaters, until her name was known all along the East Coast.', V('hall', [0.5, 0.4])],

  // ---- Columbia
  ['c1', 'Then in 1920, another singer, Mamie Smith, no relation, sold a huge number of copies of a record called Crazy Blues.', T('Crazy Blues', 'Mamie Smith, 1920'), { section: 'columbia' }],
  ['c2', 'The record companies suddenly realized Black Americans would buy records. They went looking for blues women.', V('band', [0.5, 0.4])],
  ['c3', 'One small Black-owned label, Black Swan, auditioned Bessie, and turned her down. They found her too rough.', T('Black Swan Records', 'too rough')],
  ['c4', 'In February 1923, Columbia Records signed her.', C('ad1923', 'Columbia Records advertisement, May 1923'), { stamp: 'February 1923' }],
  ['c5', 'Her very first record was Downhearted Blues. It sold about 780,000 copies in six months.', C('label', 'A Bessie Smith record on Columbia')],
  ['c6', 'That June, she married Jack Gee, a security guard from Philadelphia.', C('ad2', 'Columbia Records advertisement, June 1923')],

  // ---- the empress
  ['m1', 'Over the next ten years, she made about 160 records for Columbia.', V('band2', [0.5, 0.4]), { section: 'empress' }],
  ['m2', 'She recorded with the best musicians alive, among them Louis Armstrong and Fletcher Henderson. With Armstrong, in 1925, she recorded St. Louis Blues.', C('fho', 'The Fletcher Henderson Orchestra, 1925, with Louis Armstrong')],
  ['m3', 'Columbia called her the Queen of the Blues. The newspapers promoted her to Empress.', C('feathers', 'Bessie Smith')],
  ['m4', 'She became the highest-paid Black entertainer of her day, earning up to two thousand dollars a week.', V('crowd', [0.5, 0.4])],
  ['m5', 'She toured with a show of up to forty performers, and they traveled in her own private railroad car, seventy-two feet long.', T('Her own railroad car', '72 feet long')],
  ['m6', 'Her songs were about poor women, prison, drinking, love and freedom. She sang them in a voice that needed no microphone.', V('bar8b', [0.62, 0.35])],

  // ---- the klan
  ['k1', 'In July 1927, her tent show was playing in Concord, North Carolina.', T('July 1927', 'Concord, North Carolina'), { section: 'klan' }],
  ['k2', 'During the show, members of her band saw hooded Klansmen outside, pulling up the tent stakes.', V('hall2', [0.5, 0.4])],
  ['k3', 'The musicians ran. Bessie did not.', V('enter', [0.5, 0.4])],
  ['k4', 'She walked straight out to the hooded men, alone. She cursed them, and told them to leave.', V('argue', [0.3, 0.3])],
  ['k5', 'And they did. Then she went back inside and finished the show.', V('bar3', [0.62, 0.35])],

  // ---- the film
  ['f1', 'In 1929, the composer W. C. Handy wanted her for a short film built around his most famous song, St. Louis Blues.', C('handy', 'W. C. Handy'), { section: 'film', stamp: '1929' }],
  ['f2', 'It was filmed in Astoria, in Queens, New York, by the director Dudley Murphy. It was one of the early sound films.', V('titlecard', [0.5, 0.5])],
  ['f3', 'Bessie played a woman whose man is cheating on her.', V('withman', [0.5, 0.4])],
  ['f4', 'He knocks her to the floor and walks out with another woman.', V('floor', [0.35, 0.45])],
  ['f5', 'So she goes to a bar, and sings her heart out.', V('close2')],
  ['f6', 'It is the only film she ever made, the only time we can see and hear her at once. In 2006, it was added to the National Film Registry.', V('bar12', [0.62, 0.35])],
  ['f7', 'This is Bessie Smith, singing, in 1929.', V('close3')],

  // ---- the fall
  ['d1', 'But 1929 was also the year everything turned. She starred in a Broadway musical called Pansy. It flopped, though critics said she was the only good thing in it.', C('poster', 'St. Louis Blues, 1929'), { section: 'fall' }],
  ['d2', 'She also left Jack Gee, after his affair with another singer.', PZ('young')],
  ['d3', 'Then the Great Depression hit. People stopped buying records. In 1931, Columbia dropped her.', T('1931', 'Columbia drops her')],
  ['d4', 'She had to sell her railroad car.', V('swing', [0.5, 0.4])],
  ['d5', 'In 1933 she made her last records, for a flat fee of thirty-seven dollars and fifty cents a song.', T('Her last records', '1933')],
  ['d6', 'But she kept singing. With a new partner, an old friend named Richard Morgan, she toured again, and changed her style to fit the new swing music.', V('embrace', [0.5, 0.4])],
  ['d7', 'By 1937, people were talking about a comeback.', V('bar13', [0.62, 0.35])],

  // ---- the crash
  ['x1', 'On September 26th, 1937, Richard Morgan was driving her down Highway 61 in Mississippi.', T('September 26, 1937', 'Highway 61, Mississippi'), { section: 'crash' }],
  ['x2', 'He misjudged the speed of a slow truck ahead of them. Their car hit it side-on, and the roof was torn away.', T('The crash', 'between Memphis and Clarksdale')],
  ['x3', 'Bessie, in the passenger seat, took the full impact. Her right arm was almost torn off.', PZ('vv75')],
  ['x4', 'A Memphis doctor, Hugh Smith, was first on the scene. He bandaged her arm and sent for an ambulance.', T('Dr. Hugh Smith', 'first on the scene')],
  ['x5', 'She was taken to the G. T. Thomas Afro-American Hospital in Clarksdale. Doctors amputated her arm. She died that morning without waking.', C('death', 'Bessie Smith\'s death certificate'), { pin: { label: 'Clarksdale, Mississippi' } }],
  ['x6', 'Within weeks, a different story spread: that a white hospital had refused to treat her, and she bled to death at its door.', T('A story', 'that was not true')],
  ['x7', 'It was not true. The doctor who was there said later that no ambulance in the Deep South would even have tried to take her to a white hospital.', C('vv72', 'Bessie Smith, 1936')],

  // ---- the grave
  ['g1', 'In Philadelphia, about ten thousand people filed past her coffin. The funeral home was too small, so her body was moved to a larger hall.', PZ('vv1936'), { section: 'grave', stamp: 'October 1937' }],
  ['g2', 'About seven thousand people came to the funeral.', V('close1', [0.5, 0.4], { zoom: [1.06, 1.12] })],
  ['g3', 'She was buried at Mount Lawn Cemetery, outside Philadelphia. But her grave got no headstone.', T('No headstone', 'Mount Lawn Cemetery, Pennsylvania')],
  ['g4', 'Her husband, Jack Gee, blocked every attempt to buy one, and reportedly pocketed the money raised for it.', C('feathers', 'Bessie Smith, 1936')],
  ['g5', 'Year after year, the Empress of the Blues lay in an unmarked grave.', V('close3', [0.5, 0.4], { zoom: [1.06, 1.12] })],

  // ---- janis
  ['j1', 'Then, in 1970, a young white rock singer heard the story.', C('joplin', 'Janis Joplin, 1970'), { section: 'joplin' }],
  ['j2', 'Janis Joplin idolized Bessie Smith. She called her one of the biggest influences on her own singing.', V('close2', [0.5, 0.4], { zoom: [1.06, 1.12] })],
  ['j3', 'Janis split the cost of a headstone with Juanita Green, who had done housework for Bessie as a girl.', T('Two women', 'Janis Joplin and Juanita Green')],
  ['j4', 'On August 7th, 1970, the stone went up, thirty-three years after the funeral.', C('grave', 'Bessie Smith\'s headstone, Mount Lawn Cemetery'), { stamp: 'August 7, 1970' }],
  ['j5', 'It reads: The greatest blues singer in the world will never stop singing.', P('grave', { focus: [0.5, 0.5], zoom: [1.1, 1.2] })],
  ['j6', 'Two months later, Janis Joplin was dead. She was twenty-seven.', T('October 1970', 'Janis Joplin dies at 27')],

  // ---- legacy
  ['l1', 'In 1989, Bessie Smith was inducted into the Rock and Roll Hall of Fame.', PZ('vv75'), { section: 'legacy' }],
  ['l2', 'In 2002, Downhearted Blues, her first record, was added to the National Recording Registry.', C('label', 'Bessie Smith on Columbia')],
  ['l3', 'And the hospital where she died is now the Riverside Hotel, on the Mississippi Blues Trail.', T('The Riverside Hotel', 'Clarksdale, Mississippi')],

  // ---- close
  ['z1', 'She came from a street corner in Chattanooga. She became the Empress of the Blues. And for thirty-three years, nobody marked where she lay.', V('bar14', [0.62, 0.35]), { section: 'close' }],
  ['z2', 'That was Bessie Smith. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-joe-louis.json', 'utf8'));
const VOICES = {
  kokoro: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  elevenlabs: { engine: 'elevenlabs', voiceId: 'gUABw7pXQjhjt0kNFBTF', voiceName: 'Andrew - Smooth audio books', model: 'eleven_multilingual_v2', stability: 0.6, similarity: 0.75, style: 0, speed: 1.0, seed: 1234, leadInSeconds: 0.4, sectionGapSeconds: 1 },
};
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Bessie_Smith',
  ENC: 'https://www.encyclopedia.com/people/literature-and-arts/music-popular-and-jazz-biographies/bessie-smith',
  NPS: 'https://www.nps.gov/locations/lowermsdeltaregion/bessie-smith.htm',
  AH: 'https://www.americanheritage.com/untitled-230',
  CHARLOTTE: 'https://www.aol.com/news/push-commemorate-night-bessie-smith-095600223.html',
  UDISC: 'https://www.udiscovermusic.com/stories/janis-joplin-bessie-smith-headstone/',
  CURRENT: 'https://thecurrent.org/feature/2017/08/04/today-in-music-history-janis-joplin-bought-a-headstone-for-bessie-smith',
  DHB: 'https://en.wikipedia.org/wiki/Downhearted_Blues',
  FILMW: 'https://en.wikipedia.org/wiki/St._Louis_Blues_(1929_film)',
  FILM: 'https://commons.wikimedia.org/wiki/File:St._Louis_Blues.webm',
  JOPLIN: 'https://en.wikipedia.org/wiki/Janis_Joplin',
  PSAUDIO: 'https://psaudio.com/article/bessie-smith-part-2/',
  ROCKHALL: 'https://rockhall.com/wp-content/uploads/2024/03/Bessie_Smith_1989.pdf',
  RIVERSIDE: 'https://en.wikipedia.org/wiki/Riverside_Hotel_(Clarksdale,_Mississippi)',
};
const sourcesByClaim = {
  o2: ['ENC', 'WIKI'], o3: ['AH', 'WIKI', 'FILM'],
  e1: ['WIKI', 'ENC', 'NPS'], e2: ['WIKI', 'ENC'], e3: ['WIKI', 'ENC'], e4: ['WIKI', 'ENC'], e5: ['WIKI', 'ENC'],
  r1: ['WIKI', 'ENC'], r2: ['WIKI', 'ENC'], r3: ['WIKI', 'ENC', 'NPS'], r4: ['WIKI', 'ENC'], r5: ['WIKI', 'ENC'], r6: ['WIKI', 'ENC'],
  c1: ['WIKI', 'ENC'], c2: ['WIKI', 'ENC'], c3: ['WIKI', 'ENC'], c4: ['WIKI', 'ENC', 'DHB'], c5: ['ENC', 'NPS', 'DHB'], c6: ['WIKI', 'ENC'],
  m1: ['WIKI', 'ENC'], m2: ['WIKI', 'ENC'], m3: ['WIKI', 'ENC'], m4: ['WIKI', 'NPS', 'ENC'], m5: ['WIKI', 'ENC'], m6: ['WIKI', 'ENC'],
  k1: ['AH', 'CHARLOTTE', 'ENC'], k2: ['AH', 'CHARLOTTE'], k3: ['AH', 'CHARLOTTE'], k4: ['AH', 'CHARLOTTE'], k5: ['AH', 'CHARLOTTE'],
  f1: ['FILMW', 'ENC'], f2: ['WIKI', 'FILMW'], f3: ['FILMW', 'FILM'], f4: ['FILMW', 'FILM'], f5: ['FILMW', 'FILM'], f6: ['FILMW', 'WIKI'],
  d1: ['WIKI', 'ENC'], d2: ['WIKI', 'ENC'], d3: ['ENC', 'PSAUDIO', 'ROCKHALL'], d4: ['ENC', 'PSAUDIO', 'ROCKHALL'], d5: ['WIKI', 'ENC'], d6: ['WIKI', 'ENC'], d7: ['ENC', 'WIKI'],
  x1: ['WIKI', 'NPS', 'ENC'], x2: ['WIKI', 'ENC'], x3: ['WIKI', 'NPS'], x4: ['WIKI', 'ENC'], x5: ['WIKI', 'NPS', 'RIVERSIDE'], x6: ['WIKI', 'ENC'], x7: ['WIKI', 'ENC'],
  g1: ['WIKI', 'ENC'], g2: ['WIKI', 'ENC'], g3: ['WIKI', 'UDISC'], g4: ['WIKI', 'UDISC'],
  j1: ['UDISC', 'CURRENT'], j2: ['UDISC', 'CURRENT', 'JOPLIN'], j3: ['WIKI', 'UDISC', 'CURRENT'], j4: ['WIKI', 'UDISC'], j5: ['ENC', 'UDISC'], j6: ['UDISC', 'JOPLIN'],
  l1: ['WIKI', 'ROCKHALL'], l2: ['WIKI', 'DHB'], l3: ['WIKI', 'RIVERSIDE'],
};
const spec = {
  id: 'doc-bessie-smith',
  title: '33 Years in an Unmarked Grave: The Bessie Smith Story',
  format: 'doc', fps: 30, width: 1920, height: 1080,
  voice: VOICES[VOICE],
  pronounce: { 'St. Louis': 'Saint Lewis', Janis: 'Jan-iss', 'W. C. Handy': 'W. C. Handee', 'G. T. Thomas': 'G. T. Tomas', Viola: 'Vy-ola', Mamie: 'May-me', Juanita: 'Wah-neeta', Concord: 'Conkerd' },
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
    'Birth year disputed (1892 / 1894): said "early 1890s".',
    'Film shooting month (June vs November 1929) differs between sources: no month said.',
    'Klan story comes from Chris Albertson\'s biography (via American Heritage and the Charlotte Observer); Encyclopedia.com says "reportedly".',
  ],
};
fs.writeFileSync('data/doc-bessie-smith.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images, voice ${VOICE}`);
