// Builds data/doc-joe-louis.json: ~9-minute long-form documentary (16:9) on Joe Louis (1914-1981).
// Real fight film only: the 1938 Schmeling rematch from The Negro Soldier (1944, U.S. War Department)
// and newsreels of the 1937 Braddock and 1951 Marciano fights inside The Joe Louis Story (1953).
// The actor scenes of The Joe Louis Story are not used. Public-domain photos from Wikimedia Commons.
// Free local voice (Kokoro). Every fact has two or more sources (sourcesByClaim).
// Ending follows the owner's rule: only "subscribe for more". Run: node data/build_doc_joe_louis.mjs
import fs from 'node:fs';

const assets = {
  p1935: 'File:Joe Louis 1935 headshot by ACME Newspictures.jpg',
  acme1935: 'File:Joe Louis 1935 portrait by Acme.jpg',
  ap1935: 'File:Joe Louis 1935 portrait by the Associated Press.jpg',
  ugood: 'File:Joe Louis 1936 portrait by the Associated Press.jpg',
  vanvechten: 'File:Joe Louis by van Vechten.jpg',
  fist1937: 'File:International News Photos Portrait of Joe Louis with fist, 1937.jpg',
  smile1937: 'File:Joe Louis smiling 1937 portrait by ACME Newspictures.jpg',
  shadow1937: 'File:Joe Louis shadowed headshot 1937 by International News Photos.jpg',
  owens: 'File:Joe Louis and Jesse Owens 1935.jpg',
  visit1935: 'File:Max Schmeling visiting Joe Louis 1935 press photo.jpg',
  poster1936: 'File:Joe Louis vs. Max Schmeling ad poster.jpg',
  loss1936: 'File:Joe Louis counted out against Max Schmeling 1936.jpg',
  ring1936: 'File:Joe Louis - Max Schmeling - 1936.jpg',
  medical: 'File:Joe Louis medical for Braddock fight.jpg',
  braddock: 'File:Hal Totten raising the hand of Joe Louis after his victory over Jim Braddock.jpg',
  farr: 'File:Joe Louis and Tommy Farr square off.jpg',
  weighin: 'File:Joe Louis vs. Max Schmeling II weigh in.jpg',
  standing: 'File:Joe Louis standing over Max Schmeling 1938.jpg',
  kayo: 'File:New York Daily News, June 23, 1938 - Joe Kayos Max in 1st.jpg',
  harlem: 'File:Celebrations in Harlem after Joe Louis knocked out Max Schmeling (1).jpg',
  harlem2: 'File:Celebrations in Harlem after Joe Louis knocked out Max Schmeling (2).jpg',
  reading: 'File:Joe Louis reading about his victory over Max Schmeling in the New York Daily News.jpg',
  ringmedal: 'File:Joe Louis admires a medal awarded to him by The Ring in 1939.jpg',
  conn: 'File:Billy Conn and Joe Louis 1942.jpg',
  baer: 'File:Joe Louis and Buddy Baer 1941.jpg',
  army: 'File:Joe Louis army ACME 1942.jpg',
  ready: 'File:Joe Louis is ready to crush Hitler, Hirochito and Mussolini.jpg',
  alston: 'File:SGT. JOE LOUIS - CHAMPION OF CHAMPIONS - NARA - 535687.jpg',
  sewing: 'File:Joe louis barrow.jpg',
  hospital: 'File:Boxer Joe Louis at Christie St. hospital, signing autographs (I0002781).jpg',
  p1946: 'File:Joe Louis 1946.jpg',
  charles: 'File:Ezzard Charles vs Joe Louis 1950.jpg',
  after50: 'File:Joe Louis after match with Ezzard Charles 1950.jpg',
  p1951: 'File:Joe Louis June 1951 by International News Photos.jpg',
  liston: 'File:Sonny Liston and Joe Louis in 1963.jpg',
  schmeling71: 'File:Joe Louis and Max Schmeling 1971 Press Photo.jpg',
  medal: 'File:1981 Joe Louis Congressional Gold Medal front.jpg',
};

const NS = 'File:"The Negro Soldier" 1944.webm';
const JLS = 'File:The Joe Louis Story (1953).ogv';
const ns = (start, dur, o = {}) => ({ file: 'negro_soldier.webm', commons: NS, start, dur, ...o });
const jl = (start, dur, o = {}) => ({ file: 'joe_louis_story.ogv', commons: JLS, start, dur, ...o });
const clips = {
  ring38a: ns(177.6, 5.4),
  ring38b: ns(184, 6),
  down38: ns(194.2, 2.6, { speed: 0.5 }),
  crowd37: jl(2670, 3, { speed: 0.7 }),
  braddock: jl(2680, 8),
  braddock2: jl(2722, 10),
  braddock3: jl(2744, 10),
  braddock4: jl(2764, 10),
  marciano0: jl(4936, 8),
  marciano1: jl(4960, 8),
  marciano: jl(5054, 10),
  ropes: jl(5068, 10),
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const V = (clip, focus = [0.5, 0.45], o = {}) => ({ kind: 'video', clip, focus, anchor: [0.5, focus[1]], zoom: [1.0, 1.06], ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });
const pf = (fx, fy, z = [1.05, 1.15]) => ({ focus: [fx, fy], zoom: z, anchor: [fx, Math.min(0.5, fy + 0.05)] });

const beats = [
  // ---- cold open
  ['o1', 'He knocked out the Nazis\' favorite boxer in two minutes and four seconds. Then his own government chased him for a debt he could never pay.', P('p1935', pf(0.5, 0.35, [1.1, 1.18])), { hook: 'He beat the Nazis\' champion in 124 seconds. *Then America came for everything.*' }, { captions: false }],
  ['o2', 'On a June night in 1938, seventy thousand people packed Yankee Stadium. Millions more were listening on the radio, in America and in Germany.', V('ring38a'), { stamp: '22 June 1938' }],
  ['o3', 'It took him two minutes and four seconds to win.', V('down38', [0.5, 0.6])],
  ['o4', 'He held the heavyweight title for almost twelve years. He gave his prize money to the war effort. And then the government sent him the bill.', P('alston', pf(0.5, 0.4))],
  ['o4b', 'It is one of the strangest stories in American sport: the champion his country celebrated, and then would not let go of.', P('vanvechten', pf(0.5, 0.3, [1.05, 1.12]))],
  ['o5', 'His name was Joe Louis. This is his story.', T('Joe Louis', 'the Brown Bomber')],

  // ---- Alabama and Detroit
  ['e1', 'Joseph Louis Barrow was born on May 13th, 1914, in Chambers County, Alabama.', P('acme1935', pf(0.5, 0.3)), { section: 'early', pin: { label: 'Chambers County, Alabama' } }],
  ['e2', 'He was the seventh of eight children. His parents were sharecroppers, and both were the children of people who had been enslaved.', T('Sharecroppers\' son', 'the seventh of eight children')],
  ['e3', 'When Joe was two, his father was committed to a mental hospital. Joe would hardly know him.', C('shadow1937', 'Joe Louis, 1937')],
  ['e4', 'In 1926, like millions of Black families in the Great Migration, they moved north, to Detroit.', T('Detroit', '1926'), { pin: { label: 'Detroit, Michigan' } }],
  ['e5', 'There, Joe found a boxing gym. As an amateur, he won fifty of his fifty-four fights, forty-three by knockout.', P('fist1937', pf(0.55, 0.4))],
  ['e6', 'In 1934 he won the national amateur light heavyweight title. That summer, he turned professional.', C('ap1935', 'Joe Louis, 1935')],

  // ---- the rules
  ['r1', 'His first pro fight was on July 4th, 1934. He won in the first round.', P('smile1937', pf(0.5, 0.35)), { section: 'rules', stamp: '4 July 1934' }],
  ['r2', 'His managers were two Black businessmen, John Roxborough and Julian Black.', P('ugood', pf(0.5, 0.3))],
  ['r2b', 'They hired a trainer, the former fighter Jack Blackburn. He taught Joe to stay calm, set up his punches, and finish fights.', P('ap1935', pf(0.5, 0.3, [1.2, 1.3]))],
  ['r3', 'They knew what had happened to the last Black heavyweight champion, Jack Johnson. He had enraged white America, and for years after him, Black fighters were kept away from the title.', T('After Jack Johnson', 'the title was kept from Black fighters')],
  ['r3b', 'When Johnson won the title in 1908, white promoters started hunting for a Great White Hope to take it back from him. Newspapers mocked him for years.', T('A Great White Hope', 'the hunt began in 1908')],
  ['r4', 'So they gave Joe rules. Never be photographed with a white woman. Never gloat over a beaten opponent. Keep a straight face.', T('The rules', 'never gloat, keep a straight face')],
  ['r5', 'He followed them. And he kept winning. In 1935, he beat the former champion Primo Carnera.', C('owens', 'Joe Louis and Jesse Owens, 1935'), { stamp: '1935' }],
  ['r6', 'The press called him the Brown Bomber.', C('p1935', 'Joe Louis, 1935')],

  // ---- the first Schmeling fight
  ['s1', 'Then, in June 1936, he met the German former champion Max Schmeling at Yankee Stadium.', C('poster1936', 'Louis vs. Schmeling, June 1936'), { section: 'schmeling1', stamp: '19 June 1936' }],
  ['s2', 'Louis was the favorite. But in the twelfth round, Schmeling knocked him out.', C('loss1936', 'Louis counted out, 1936')],
  ['s3', 'It was the first loss of his professional career.', P('ring1936', pf(0.5, 0.45))],
  ['s4', 'In Germany, the Nazi regime made Schmeling a national hero.', T('A Nazi hero', 'Max Schmeling, 1936')],

  // ---- champion
  ['c1', 'Louis went back to work. A year later, on June 22nd, 1937, he fought the champion, James Braddock, in Chicago.', V('crowd37', [0.5, 0.5]), { section: 'champion', stamp: '22 June 1937', pin: { label: 'Chicago' } }],
  ['c2', 'Braddock knocked him down in the first round.', V('braddock', [0.5, 0.45])],
  ['c3', 'Louis got up, and wore him down.', V('braddock2', [0.5, 0.45])],
  ['c4', 'In the eighth round, he knocked Braddock out.', V('braddock3', [0.5, 0.45])],
  ['c5', 'He was the heavyweight champion of the world. The first Black heavyweight champion in twenty-two years.', C('braddock', 'Louis declared the winner over Braddock, 1937')],
  ['c6', 'But one loss still stood on his record.', V('braddock4', [0.5, 0.45])],

  // ---- the rematch
  ['m1', 'The rematch with Schmeling was set for June 22nd, 1938, at Yankee Stadium.', C('weighin', 'The weigh-in, 22 June 1938'), { section: 'rematch' }],
  ['m2', 'By then it was more than a boxing match. Many Americans saw it as a contest between their country and Nazi Germany.', T('Two countries', 'June 1938')],
  ['m3', 'President Roosevelt reportedly told Louis: Joe, we need muscles like yours to beat Germany.', Q('Joe, we need muscles like yours to beat Germany.', 'President Roosevelt to Joe Louis, as reported')],
  ['m4', 'Seventy thousand people came. Radio carried the fight around the world, including to Germany.', V('ring38a', [0.5, 0.42]), { stamp: '22 June 1938' }],
  ['m5', 'Louis came out punching, and he never stopped.', V('ring38b', [0.5, 0.42])],
  ['m6', 'Schmeling went down. His corner threw in the towel.', V('down38', [0.5, 0.6])],
  ['m7', 'It was over in two minutes and four seconds.', T('2 minutes, 4 seconds', 'round one')],
  ['m8', 'In Harlem, people poured into the streets and celebrated through the night.', P('harlem', pf(0.5, 0.45))],
  ['m9', 'Black Americans, and much of white America too, had a hero.', P('harlem2', pf(0.5, 0.4))],
  ['m10', 'The next morning, the champion read about himself in the paper.', C('reading', 'Louis reading the New York Daily News, 23 June 1938')],

  // ---- the long reign
  ['l1', 'Over the next years, he fought almost anyone who would get in the ring with him.', C('ringmedal', 'Louis with a medal from The Ring, 1939'), { section: 'reign' }],
  ['l2', 'Between 1939 and 1941, he defended the title thirteen times. Reporters called his opponents the Bum of the Month Club.', T('Bum of the Month', '13 defenses, 1939 to 1941')],
  ['l3', 'In 1941, the young Billy Conn was ahead on the scorecards. Louis knocked him out in the thirteenth round.', C('conn', 'Billy Conn and Joe Louis')],
  ['l3b', 'He was now one of the most famous men in America, Black or white. Children in every city knew his name.', C('ringmedal', 'Louis in 1939')],
  ['l4', 'In all, he would defend the title twenty-five times, and hold it for almost twelve years. Both are still heavyweight records.', P('vanvechten', pf(0.5, 0.3))],

  // ---- war
  ['w1', 'Then came Pearl Harbor.', T('December 1941', 'America goes to war'), { section: 'war' }],
  ['w2', 'In January 1942, Louis fought Buddy Baer, and gave his purse to the Navy Relief Society.', C('baer', 'Joe Louis and Buddy Baer'), { stamp: 'January 1942' }],
  ['w3', 'Two months later, he fought Abe Simon, and gave that purse to the Army Relief Fund.', P('ready', pf(0.5, 0.4))],
  ['w4', 'That same year, he joined the Army, an army that still kept Black and white soldiers apart.', C('army', 'Joe Louis in the Army, 1942')],
  ['w5', 'He never saw combat. Instead he boxed in almost a hundred exhibitions for the troops, and toured camps and hospitals.', C('hospital', 'Louis signing autographs at a military hospital, about 1945')],
  ['w6', 'The government put him on its posters.', C('alston', 'Office of War Information poster, 1943')],

  // ---- debt
  ['t1', 'But there was a problem with the money he gave away.', P('hospital', pf(0.5, 0.4)), { section: 'debt' }],
  ['t2', 'The tax collectors counted those charity purses as his income. He owed tax on money he never kept.', T('Taxed', 'on the money he gave away')],
  ['t2b', 'He had given away the money. He still had to pay the tax on it, and the interest on the tax.', C('sewing', 'Joe Louis receives his stripes, 1945')],
  ['t3', 'And in those years, the top income tax rates reached ninety percent. The more he earned, the more he owed.', P('p1946', pf(0.5, 0.3))],
  ['t4', 'On March 1st, 1949, Joe Louis retired, still the champion.', P('vanvechten', pf(0.5, 0.28, [1.2, 1.3])), { stamp: '1 March 1949' }],
  ['t5', 'By 1950, the government said he owed more than half a million dollars. With interest and penalties, it kept growing, past one million.', T('Over $1,000,000', 'his tax debt, with interest')],

  // ---- comeback
  ['k1', 'So, at thirty-six, he came back.', V('marciano0', [0.5, 0.45]), { section: 'comeback' }],
  ['k2', 'On September 27th, 1950, he lost a fifteen-round decision to the new champion, Ezzard Charles.', C('charles', 'Ezzard Charles vs. Joe Louis, 1950'), { stamp: '27 September 1950' }],
  ['k3', 'He kept fighting.', C('after50', 'Louis after the Charles fight, 1950')],
  ['k3b', 'In January 1951, he beat Freddie Beshore. He won his next fights too. For a moment, it looked like the old champion was back.', P('p1951', pf(0.5, 0.3, [1.15, 1.25]))],
  ['k4', 'On October 26th, 1951, he met a young Rocky Marciano at Madison Square Garden.', V('marciano1', [0.5, 0.45]), { stamp: '26 October 1951' }],
  ['k5', 'In the eighth round, Marciano knocked him through the ropes.', V('ropes', [0.5, 0.5])],
  ['k6', 'Joe Louis never boxed again.', V('marciano', [0.5, 0.45])],

  // ---- after
  ['a1', 'The debt did not go away. He took whatever work he could find.', P('p1951', pf(0.5, 0.35)), { section: 'after' }],
  ['a2', 'He became a professional wrestler, then a wrestling referee.', C('liston', 'Joe Louis with Sonny Liston, 1963')],
  ['a3', 'Later he worked in Las Vegas, as a greeter at Caesars Palace, shaking hands with tourists.', T('Caesars Palace', 'Las Vegas')],
  ['a3b', 'In 1954, he was voted into the boxing Hall of Fame. But a plaque could not pay the tax bill.', T('Hall of Fame', '1954')],
  ['a4', 'He struggled with drugs and with his mental health.', C('shadow1937', 'Joe Louis')],
  ['a5', 'One old opponent helped him. Max Schmeling, the man he had beaten in 1938, became his friend.', C('schmeling71', 'Joe Louis and Max Schmeling, 1971')],

  // ---- end
  ['d1', 'On April 12th, 1981, Joe Louis watched a heavyweight title fight in Las Vegas. Hours later, his heart failed. He was 66.', P('vanvechten', pf(0.5, 0.3, [1.1, 1.2])), { section: 'end', stamp: '12 April 1981' }],
  ['d2', 'He had not served enough to be buried at Arlington National Cemetery by the usual rules. President Reagan waived them.', T('Arlington', 'a waiver from the President')],
  ['d3', 'He was buried there with full military honors. Max Schmeling helped pay for the funeral, and was a pallbearer.', P('alston', pf(0.5, 0.35, [1.15, 1.25]))],
  ['d4', 'In 1982, Congress awarded him its Gold Medal.', C('medal', 'Joe Louis Congressional Gold Medal')],
  ['d4b', 'Detroit, the city where he learned to box, had already named its new hockey arena for him: the Joe Louis Arena, opened in 1979.', T('Joe Louis Arena', 'Detroit, 1979')],

  // ---- close
  ['z1', 'He beat the Nazis\' champion. He gave his purses to his country.', V('ring38b', [0.5, 0.42], { zoom: [1.06, 1.12] }), { section: 'close' }],
  ['z2', 'And his country taxed him for it, for the rest of his life.', C('p1935', 'Joe Louis, 1914-1981')],
  ['z3', 'That was Joe Louis. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-paul-robeson.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Joe_Louis',
  ENC: 'https://www.encyclopedia.com/people/sports-and-games/sports-biographies/joe-louis',
  HIST: 'https://www.history.com/topics/boxing/joe-louis',
  PBS: 'https://www.pbs.org/wgbh/americanexperience/features/fight-john-roxborough-and-julian-black',
  PBS2: 'https://www.pbs.org/wgbh/americanexperience/features/fight-black-boxers-and-idea-great-white-hope/',
  PBS3: 'https://www.pbs.org/wgbh/americanexperience/features/fight-louis-and-schmeling-chronology/',
  NPR: 'https://www.npr.org/transcripts/6515548',
  ESPN: 'https://www.espn.in/boxing/story/_/id/9404398/more-just-fight',
  HNN: 'https://www.historynewsnetwork.org/article/on-this-day-in-1938-joe-louis-and-max-schmeling-we',
  LIB: 'https://libertarianinstitute.org/articles/joe-louis-vs-the-tax-man',
  CRB: 'https://claremontreviewofbooks.com/digital/terminator-irs-hounded-joe-louis-into-poverty',
  ANC: 'https://www.arlingtoncemetery.mil/Explore/Notable-Graves/Sports/Joe-Louis',
  MOSAIC: 'https://mosaicmagazine.com/picks/history-ideas/2023/07/although-made-into-an-avatar-of-nazi-germany-max-schmeling-was-among-the-righteous/',
  COMMONS: 'https://commons.wikimedia.org/wiki/Category:Joe_Louis',
  JLA: 'https://en.wikipedia.org/wiki/Joe_Louis_Arena',
};
const sourcesByClaim = {
  o2: ['WIKI', 'HIST', 'NPR'], o3: ['WIKI', 'HIST', 'ESPN'], o4: ['WIKI', 'HIST', 'LIB'],
  e1: ['WIKI', 'HIST', 'ENC'], e2: ['WIKI', 'ENC'], e3: ['WIKI', 'ENC', 'HIST'], e4: ['WIKI', 'ENC'], e5: ['WIKI', 'HIST', 'ENC'], e6: ['WIKI', 'ENC'],
  r1: ['WIKI', 'ENC'], r2: ['WIKI', 'PBS'], r3: ['WIKI', 'PBS2'], r4: ['WIKI', 'PBS'], r5: ['WIKI', 'PBS3'], r6: ['WIKI', 'HIST'],
  s1: ['WIKI', 'HIST', 'PBS3'], s2: ['WIKI', 'HIST', 'ENC'], s3: ['WIKI', 'HIST'], s4: ['WIKI', 'HNN'],
  c1: ['WIKI', 'HIST', 'ENC'], c2: ['WIKI', 'PBS3'], c3: ['WIKI', 'PBS3'], c4: ['WIKI', 'ENC'], c5: ['HIST', 'WIKI'], c6: ['WIKI', 'HIST'],
  m1: ['WIKI', 'HIST'], m2: ['WIKI', 'HNN', 'PBS3'], m3: ['WIKI', 'HNN'], m4: ['WIKI', 'HIST', 'NPR'], m5: ['WIKI', 'ESPN'], m6: ['WIKI', 'ESPN'], m7: ['WIKI', 'HIST', 'ESPN'],
  m8: ['COMMONS', 'HNN'], m9: ['WIKI', 'HNN'], m10: ['COMMONS', 'WIKI'],
  l1: ['WIKI', 'HIST'], l2: ['WIKI', 'HIST'], l3: ['WIKI', 'ENC'], l4: ['WIKI', 'ENC', 'HIST'],
  w1: ['WIKI', 'HIST'], w2: ['WIKI', 'LIB'], w3: ['WIKI', 'LIB'], w4: ['WIKI', 'HIST', 'ENC'], w5: ['WIKI', 'ENC', 'HIST'], w6: ['COMMONS', 'WIKI'],
  t1: ['WIKI', 'LIB'], t2: ['WIKI', 'LIB', 'CRB'], t3: ['WIKI', 'LIB', 'CRB'], t4: ['ENC', 'HIST'], t5: ['WIKI', 'ENC', 'LIB'],
  k1: ['WIKI', 'HIST'], k2: ['WIKI', 'ENC'], k3: ['WIKI', 'HIST'], k4: ['WIKI', 'ENC', 'HIST'], k5: ['WIKI', 'ENC'], k6: ['WIKI', 'ENC', 'HIST'],
  a1: ['WIKI', 'LIB'], a2: ['WIKI', 'ENC'], a3: ['WIKI', 'ENC', 'HIST'], a4: ['WIKI', 'HIST'], a5: ['WIKI', 'MOSAIC'],
  d1: ['WIKI', 'ENC', 'HIST'], d2: ['ANC', 'HIST', 'WIKI'], d3: ['WIKI', 'ANC', 'MOSAIC'], d4: ['WIKI', 'COMMONS'],
  z1: ['WIKI', 'HIST'], z2: ['WIKI', 'LIB'],
};

const spec = {
  id: 'doc-joe-louis',
  title: 'He Beat the Nazis\' Champion. Then America Taxed Him for Life: The Joe Louis Story',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { Schmeling: 'Shmelling', Ezzard: 'Ezzerd', Caesars: 'Seezers', Roxborough: 'Rocks-burrow', Carnera: 'Car-nair-ah' },
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
    'Tax debt resolution: special act of Congress (HIST) vs 1962 settlement (other accounts): not said.',
    'Final record 66-3 (WIKI) vs 68-3 (HIST): not said.',
    'Charity purse amounts differ by source ($47,000/$36,146 net vs $65,200/$45,882): not said.',
    'Knockdowns in the 1938 rematch: three (WIKI) vs two (other accounts): not said.',
    'The Joe Louis Story (1953) actor scenes (Coley Wallace) are not used; only its real fight newsreels.',
  ],
};
fs.writeFileSync('data/doc-joe-louis.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images, ${Object.keys(clips).length} clips`);
