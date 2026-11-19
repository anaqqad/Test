// Builds data/doc-lena-horne.json: ~8-minute long-form documentary (16:9) on Lena Horne (1917-2010).
// Film: The Duke Is Tops (1938) and Boogie Woogie Dream (1944), public domain on Wikimedia Commons.
// Every fact has two or more sources (sourcesByClaim). Ending: only "subscribe for more".
// Voice: `node data/build_doc_lena_horne.mjs [kokoro|elevenlabs]` (elevenlabs is paid: ask first).
import fs from 'node:fs';

const VOICE = process.argv[2] || 'kokoro';
const assets = {
  p1941: 'File:Lena Horne - 1941.jpg',
  vv1941: 'File:Portrait of Lena Horne LCCN2004663037.jpg',
  p1946: 'File:Lena Horne, 1946.jpg',
  p1947: 'File:Lena Horne 1947.JPG',
  p1955: 'File:Lena Horne 1955.JPG',
  p1961: 'File:Lena Horne 1961.JPG',
  govprop: 'File:Lena Horne govprop.jpg',
  gottlieb: 'File:(Portrait of Lena Horne, New York, N.Y., between 1946 and 1948) (LOC) (4843132965).jpg',
  hayton: 'File:(Portrait of Lena Horne and Lennie Hayton, New York, N.Y., between 1946 and 1948) (LOC) (5354168293).jpg',
  fuel: 'File:"Lena Horne conserves fuel (gas).", ca. 1941 - ca. 1945 - NARA - 535820.jpg',
  bronze: 'File:The Bronze Venus, 1943 film poster 01.jpg',
  cabin: 'File:Cabin in the Sky (1943) 1.jpg',
  stormy: 'File:Stormy Weather (1943 film poster).jpg',
  stormylc: 'File:Stormy Weather (1943 lobby card - Horne & Robinson).jpg',
  stormy3: 'File:Stormy Weather - Robinson, Horne, and Calloway.jpg',
  clouds: 'File:Lena Horne in Till the Clouds Roll By 1.jpg',
  sailor: 'File:Lena Horne in Two Girls and a Sailor (1944).png',
  carver: 'File:Lena Horne launching SS George Washington Carver.jpg',
  tuskegee: 'File:Lena Horne with Tuskegee airmen.png',
  march: 'File:Civil Rights March on Washington, D.C. (Actor Lena Horne, a close-up view.) - NARA - 542057.tif',
  jfk: 'File:President John F. Kennedy with Democratic Party Fundraisers JFKWHP-AR8252-B.jpg',
};

const DUKE = 'File:The Duke is Tops (1938).webm';
const BWD = 'File:Boogie Woogie Dream (1944).webm';
const d = (start, dur, o = {}) => ({ file: 'The_Duke_is_Tops_(1938).webm', commons: DUKE, start, dur, ...o });
const bw = (start, dur, o = {}) => ({ file: 'Boogie_Woogie_Dream_(1944).webm', commons: BWD, start, dur, ...o });
const clips = {
  stage: d(430, 8), stage2: d(438, 7),
  sing1: d(446, 8), sing2: d(467.5, 6.5), sing3: d(479, 8), sing4: d(488, 4.5), sing5: d(497, 4.5),
  cooper: d(864, 10), cooper2: d(886, 9),
  bwd1: bw(249, 3, { speed: 0.6 }), bwd2: bw(262, 4.8), bwd3: bw(243, 5),
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const V = (clip, focus = [0.5, 0.35], o = {}) => ({ kind: 'video', clip, focus, anchor: [0.5, focus[1]], zoom: [1.0, 1.06], ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });

const beats = [
  // ---- open
  ['o1', 'Hollywood made her a star. Then it filmed her songs so that theaters in the South could cut her out of the movie.', P('p1946', { focus: [0.5, 0.3], zoom: [1.0, 1.05], anchor: [0.62, 0.4] }), { hook: 'Hollywood made her a star. *Then filmed her so the South could cut her out.*' }, { captions: false }],
  ['o2', 'She was the first Black woman in decades to sign a long-term contract with a major Hollywood studio.', V('sing1')],
  ['o3', 'She would not play maids. So the studio barely let her act at all.', V('sing3')],
  ['o3b', 'This is the story of a woman Hollywood wanted to show off, and hide, at the same time. And of how she refused to stay hidden.', C('p1955', 'Lena Horne')],
  ['o4', 'Her name was Lena Horne. This is her story.', T('Lena Horne', 'singer, actor, activist')],

  // ---- Brooklyn
  ['e1', 'Lena Mary Calhoun Horne was born on June 30th, 1917, in Brooklyn, New York.', C('p1947', 'Lena Horne'), { section: 'early', pin: { label: 'Brooklyn, New York' } }],
  ['e2', 'Her family belonged to the educated Black middle class of New York. Relatives held posts in the NAACP and the Urban League.', T('Brooklyn', 'the Black middle class')],
  ['e3', 'Her father left when she was three. Her mother was an actress who toured with a Black theater company.', C('p1941', 'Lena Horne, 1941')],
  ['e4', 'So Lena was raised mostly by her grandparents, Cora and Edwin Horne, with long stretches traveling with her mother, including years in Georgia.', T('Georgia', 'part of her childhood'), { pin: { label: 'Fort Valley, Georgia' } }],
  ['e5', 'At sixteen, she left school.', C('govprop', 'Lena Horne')],
  ['e5b', 'By then she had already learned what it meant to be a Black girl moving between North and South, and between her mother\'s world and her grandmother\'s.', P('govprop', { focus: [0.5, 0.3], zoom: [1.15, 1.25], anchor: [0.5, 0.42] })],

  // ---- Harlem
  ['h1', 'In 1933 she joined the chorus line at the Cotton Club in Harlem.', V('stage'), { section: 'harlem', stamp: '1933' }],
  ['h2', 'The performers were Black. The audience was white only.', T('The Cotton Club', 'Black performers, white audience')],
  ['h3', 'Then she sang with Noble Sissle\'s orchestra, and made her first records.', V('stage2')],
  ['h4', 'In 1937 she married Louis Jones. Their daughter Gail was born that December.', C('p1946', 'Lena Horne, 1946'), { stamp: '1937' }],
  ['h5', 'In 1938, she starred in her first feature film, The Duke Is Tops, made for Black audiences.', V('cooper', [0.62, 0.32]), { lowerThird: { name: 'The Duke Is Tops', sub: '1938' } }],
  ['h6', 'It was a low-budget picture. She later said she was never paid for it.', V('cooper2', [0.62, 0.32])],
  ['h7', 'Years later, when she was famous, it was sold again under a new name, with her on top of the poster.', C('bronze', 'The Bronze Venus, the same film re-released')],
  ['h7b', 'But in 1938, she was still a band singer, earning very little.', V('sing5', [0.5, 0.32], { zoom: [1.06, 1.12] })],

  // ---- the band years
  ['b1', 'In 1940 she joined the white bandleader Charlie Barnet on tour.', V('sing2'), { section: 'band', stamp: '1940' }],
  ['b2', 'She was the only Black member of the band. On the road, she faced discrimination, and she quit.', T('The only Black member', 'Charlie Barnet\'s band')],
  ['b3', 'In 1941 she sang at Cafe Society in Greenwich Village, New York\'s first integrated nightclub.', V('sing4'), { stamp: '1941' }],
  ['b4', 'There she worked with Paul Robeson, the singer and activist.', C('p1941', 'Lena Horne, 1941')],

  // ---- MGM
  ['m1', 'Then Hollywood came calling. In 1942, MGM signed her to a seven-year contract.', C('vv1941', 'Lena Horne, photographed by Carl Van Vechten, 1941'), { section: 'mgm', stamp: '1942' }],
  ['m2', 'It was the first long-term contract a major studio had given a Black woman in decades.', T('Seven years', 'MGM, 1942')],
  ['m3', 'And it said she would not be cast as a maid or as comic relief.', C('fuel', 'Lena Horne, World War II poster')],
  ['m3b', 'Her first film for MGM was Panama Hattie, in 1942.', T('Panama Hattie', 'MGM, 1942')],
  ['m4', 'The NAACP\'s leader, Walter White, told her she was a test case for how Hollywood would treat Black women.', T('A test case', 'Walter White, NAACP')],
  ['m5', 'But MGM did not know what to do with her.', V('sing5')],
  ['m6', 'In most of her films she simply sang, alone, in a scene of her own, with no white star beside her.', C('clouds', 'Lena Horne in Till the Clouds Roll By, 1946')],
  ['m6b', 'In Ziegfeld Follies and in Words and Music, it was the same: a song, a spotlight, and a scene that could be lifted out of the film without breaking the story.', P('p1946', { focus: [0.5, 0.3], zoom: [1.15, 1.25], anchor: [0.5, 0.42] })],
  ['m7', 'That was on purpose. Those scenes could be cut out easily, for theaters in the South that would not show Black performers.', T('Made to be cut', 'for theaters in the South')],
  ['m8', 'In some cities, including Memphis, they were.', C('sailor', 'Lena Horne in Two Girls and a Sailor, 1944')],
  ['m8b', 'She was one of the most photographed women in Hollywood. And in much of the country, audiences never saw her on screen at all.', C('gottlieb', 'Lena Horne, 1940s')],

  // ---- 1943
  ['s1', 'In 1943 she got two real roles, both in films with all-Black casts.', C('cabin', 'Cabin in the Sky, 1943'), { section: 'stormy', stamp: '1943' }],
  ['s2', 'In Cabin in the Sky, she played the temptress Georgia Brown.', P('cabin', { focus: [0.5, 0.4], zoom: [1.1, 1.2] })],
  ['s3', 'Then MGM lent her to another studio for Stormy Weather.', C('stormy', 'Stormy Weather, 1943')],
  ['s4', 'She starred beside the great tap dancer Bill Robinson.', C('stormylc', 'Lena Horne and Bill Robinson, Stormy Weather')],
  ['s5', 'And the title song, Stormy Weather, became her song for the rest of her life.', C('stormy3', 'Bill Robinson, Lena Horne and Cab Calloway')],

  // ---- war
  ['w1', 'During World War II, she was a favorite of Black soldiers. Her picture hung in barracks across the country.', C('tuskegee', 'Lena Horne with Tuskegee airmen, 1945'), { section: 'war' }],
  ['w2', 'She helped launch a Liberty ship named for George Washington Carver.', C('carver', 'Launching the SS George Washington Carver, 1943')],
  ['w3', 'And she sang for the troops. At one Army camp, she came on stage and saw the seating.', V('bwd3', [0.55, 0.35])],
  ['w4', 'German prisoners of war sat in the front rows. The Black American soldiers sat behind them.', T('In the front rows', 'German prisoners of war')],
  ['w5', 'She walked off the stage, past the prisoners, and sang to the Black soldiers at the back.', V('bwd2', [0.55, 0.35])],
  ['w6', 'She also complained to the NAACP. She refused to perform for segregated audiences.', P('govprop', { focus: [0.5, 0.3], zoom: [1.1, 1.2], anchor: [0.5, 0.42] })],
  ['w7', 'She also worked with Eleanor Roosevelt to push for laws against lynching.', T('Against lynching', 'with Eleanor Roosevelt')],

  // ---- love and the blacklist
  ['l1', 'After the war, she fell in love with Lennie Hayton, MGM\'s white musical director.', C('hayton', 'Lena Horne and Lennie Hayton'), { section: 'love' }],
  ['l2', 'In California, a marriage between them was against the law.', T('Against the law', 'California, 1940s')],
  ['l3', 'So in December 1947 they married in Paris. They stayed together until his death.', C('gottlieb', 'Lena Horne, about 1947'), { stamp: 'December 1947', pin: { label: 'Paris' } }],
  ['l4', 'Then came the part she wanted most. MGM was remaking Show Boat, with a role she had already played on screen: Julie, a woman of mixed race.', C('clouds', 'Lena Horne as Julie, Till the Clouds Roll By, 1946')],
  ['l5', 'The role went to Ava Gardner, a white actress.', T('Julie', 'Show Boat, 1951')],
  ['l6', 'By 1950 she had left MGM. And in the early 1950s, she was blacklisted for her political ties, including her friendship with Paul Robeson.', C('p1955', 'Lena Horne, 1955'), { stamp: '1950s' }],
  ['l6b', 'For a few years, the television and radio work dried up. She was cleared by the mid-1950s, and she later spoke out against communism.', C('p1947', 'Lena Horne')],

  // ---- nightclubs
  ['n1', 'Hollywood had shut its doors. So she went back to where she started: the nightclub stage.', V('bwd1', [0.55, 0.35]), { section: 'clubs' }],
  ['n2', 'She signed with RCA Victor and became one of the top nightclub stars in America.', T('Nightclub star', 'RCA Victor, 1956')],
  ['n3', 'In 1957 she starred on Broadway in the musical Jamaica.', C('p1955', 'Lena Horne'), { stamp: '1957' }],
  ['n4', 'The woman Hollywood had kept in separate scenes was now the star of the whole show.', V('bwd1', [0.55, 0.35], { zoom: [1.06, 1.12] })],

  // ---- civil rights
  ['r1', 'In the 1960s, she put her fame to work for civil rights.', C('p1961', 'Lena Horne, 1961'), { section: 'rights' }],
  ['r2', 'In 1963 she sang at a civil rights rally in Jackson, Mississippi, where Medgar Evers spoke. Days later, he was murdered.', T('Jackson, Mississippi', '1963')],
  ['r3', 'That August, she joined the March on Washington.', C('march', 'Lena Horne at the March on Washington, 1963'), { stamp: '28 August 1963' }],
  ['r4', 'Three months later, she was at the White House with President Kennedy, two days before he was killed.', C('jfk', 'At the White House, 20 November 1963')],
  ['r5', 'She was no longer just a singer who happened to be Black. She was using her name to ask the country to change.', P('p1961', { focus: [0.5, 0.3], zoom: [1.1, 1.2], anchor: [0.5, 0.42] })],

  // ---- losses
  ['x1', 'Then came the hardest years of her life.', P('gottlieb', { focus: [0.5, 0.35], zoom: [1.1, 1.2], anchor: [0.5, 0.45] }), { section: 'losses' }],
  ['x2', 'In 1970 her father died, and so did her son, Teddy.', T('1970', 'her father, her son')],
  ['x3', 'In 1971, Lennie Hayton died too.', T('1971', 'Lennie Hayton')],
  ['x4', 'She stopped performing for a time.', C('p1947', 'Lena Horne, 1947')],
  ['x5', 'In 1978 she came back to the screen, playing Glinda the Good Witch in the film The Wiz.', T('The Wiz', 'Glinda, 1978')],

  // ---- the comeback
  ['c1', 'Then, in May 1981, at sixty-three, she opened a one-woman show on Broadway: Lena Horne, The Lady and Her Music.', V('sing2', [0.5, 0.32], { zoom: [1.06, 1.12] }), { section: 'broadway', stamp: 'May 1981' }],
  ['c2', 'It ran for 333 performances.', T('333 performances', 'Broadway, 1981 to 1982')],
  ['c3', 'It closed on her sixty-fifth birthday. It won her a special Tony Award, and the album won two Grammy Awards.', V('sing3', [0.5, 0.32], { zoom: [1.06, 1.12] })],
  ['c4', 'In 1984 she received the Kennedy Center Honors.', T('Kennedy Center Honors', '1984')],
  ['c5', 'In 2022, a Broadway theater was renamed the Lena Horne Theatre, the first Broadway house named for a Black woman.', T('The Lena Horne Theatre', 'Broadway, 2022')],

  // ---- end
  ['d1', 'Lena Horne died on May 9th, 2010, in New York. She was 92.', C('vv1941', 'Lena Horne, 1917-2010'), { section: 'end', stamp: '9 May 2010' }],
  ['d2', 'She had spent her life being told where she could sing, where she could sit, and whom she could marry.', C('hayton', 'Lena Horne and Lennie Hayton')],
  ['z1', 'Hollywood filmed her so she could be cut out. She made sure she never was.', V('sing1', [0.5, 0.32], { zoom: [1.06, 1.12] }), { section: 'close' }],
  ['z2', 'That was Lena Horne. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-joe-louis.json', 'utf8'));
const VOICES = {
  kokoro: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  elevenlabs: { engine: 'elevenlabs', voiceId: 'gUABw7pXQjhjt0kNFBTF', voiceName: 'Andrew - Smooth audio books', model: 'eleven_multilingual_v2', stability: 0.6, similarity: 0.75, style: 0, speed: 1.0, seed: 1234, leadInSeconds: 0.4, sectionGapSeconds: 1 },
};
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Lena_Horne',
  ENC: 'https://www.encyclopedia.com/people/literature-and-arts/music-popular-and-jazz-biographies/lena-horne',
  TCM: 'https://www.tcm.com/articles/featured-actors/021865/lena-horne-goddess-reclaimed',
  HEINZ: 'https://www.heinzhistorycenter.org/blog/western-pennsylvania-history-words-and-music-a-holiday-turning-point/',
  THR: 'https://www.hollywoodreporter.com/lifestyle/lifestyle-news/lena-horne-book-excerpt-actress-singer-mgm-1235613032/',
  SCPR: 'https://www.southcarolinapublicradio.org/2023-10-31/a-new-book-tells-the-life-story-of-screen-and-song-legend-lena-horne',
  ARMY: 'https://www.army.mil/article/217981/fort_knox_general_club_director_host_black_entertainers_ease_tensions_in_pre_integrated_army',
  NPS: 'https://home.nps.gov/features/malu/feat0002/wof/Lena_Horne.htm',
  COMMONS: 'https://commons.wikimedia.org/wiki/Category:Lena_Horne',
  NATION: 'https://www.thenation.com/article/archive/lena-horne-tireless-campaigner-social-and-economic-justice/',
  IBDB: 'https://www.ibdb.com/broadway-production/lena-horne-the-lady-and-her-music-4120',
  BWD: 'https://broadwaydirect.com/the-lena-horne-theatre-becomes-a-part-of-broadway-history/',
  YAHOO: 'https://www.yahoo.com/entertainment/lena-horne-ultimate-lifetime-achievement-220042021.html',
};
const sourcesByClaim = {
  o2: ['ENC', 'TCM'], o3: ['TCM', 'SCPR', 'WIKI'],
  e1: ['WIKI', 'ENC'], e2: ['WIKI', 'ENC'], e3: ['WIKI', 'ENC'], e4: ['WIKI', 'ENC'], e5: ['WIKI', 'ENC'],
  h1: ['WIKI', 'ENC', 'TCM'], h2: ['WIKI', 'ENC'], h3: ['WIKI', 'ENC'], h4: ['WIKI', 'ENC'], h5: ['TCM', 'COMMONS'], h6: ['TCM', 'WIKI'], h7: ['TCM', 'COMMONS'],
  b1: ['WIKI', 'ENC'], b2: ['ENC', 'WIKI'], b3: ['WIKI', 'ENC'], b4: ['WIKI', 'ENC'],
  m1: ['WIKI', 'ENC', 'TCM'], m2: ['ENC', 'TCM'], m3: ['TCM', 'SCPR'], m4: ['THR', 'SCPR'], m5: ['TCM', 'WIKI'], m6: ['WIKI', 'TCM'], m7: ['WIKI', 'TCM'], m8: ['HEINZ', 'WIKI'],
  s1: ['WIKI', 'ENC', 'TCM'], s2: ['TCM', 'WIKI'], s3: ['WIKI', 'TCM'], s4: ['WIKI', 'COMMONS'], s5: ['TCM', 'WIKI'],
  w1: ['WIKI', 'ENC'], w2: ['COMMONS', 'WIKI'], w3: ['ARMY', 'NPS'], w4: ['ARMY', 'NPS'], w5: ['ARMY', 'NPS'], w6: ['NPS', 'WIKI'],
  l1: ['WIKI', 'ENC'], l2: ['ENC', 'WIKI'], l3: ['WIKI', 'ENC'], l4: ['TCM', 'WIKI'], l5: ['WIKI', 'TCM'], l6: ['TCM', 'WIKI', 'ENC'],
  n1: ['TCM', 'ENC'], n2: ['WIKI', 'ENC'], n3: ['WIKI', 'TCM', 'ENC'],
  r1: ['WIKI', 'ENC'], r2: ['WIKI', 'NATION'], r3: ['WIKI', 'ENC', 'COMMONS'], r4: ['WIKI', 'COMMONS'],
  x1: ['ENC', 'WIKI'], x2: ['ENC', 'WIKI'], x3: ['ENC', 'WIKI'], x4: ['ENC', 'WIKI'],
  c1: ['WIKI', 'ENC'], c2: ['WIKI', 'IBDB'], c3: ['WIKI', 'ENC'], c4: ['WIKI', 'ENC'],
  m3b: ['WIKI', 'ENC'],
  m6b: ['TCM', 'WIKI'],
  w7: ['WIKI', 'ENC'],
  l6b: ['ENC', 'WIKI'],
  x5: ['ENC', 'WIKI'],
  c5: ['BWD', 'YAHOO'],
  d1: ['WIKI', 'TCM'], z1: ['WIKI', 'TCM'],
};
const spec = {
  id: 'doc-lena-horne',
  title: 'Filmed So the South Could Cut Her Out: The Lena Horne Story',
  format: 'doc', fps: 30, width: 1920, height: 1080,
  voice: VOICES[VOICE],
  pronounce: { Sissle: 'Sissel', Hayton: 'Hay-ton', 'World War II': 'World War Two', 'Urban League': 'Ur-bun League', Ziegfeld: 'Zig-feld', Eleanor: 'Ella-nor', Glinda: 'Glinn-da' },
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
    'Army camp venue: Fort Riley (NPS) vs Camp Robinson (forum): not named.',
    'The Duke Is Tops pay: TCM says Ralph Cooper never paid her; phrased as "she later said she was never paid".',
    'Exact MGM contract clause wording: phrased as "would not be cast as a maid or as comic relief" (TCM).',
  ],
};
fs.writeFileSync('data/doc-lena-horne.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images, voice ${VOICE}`);
