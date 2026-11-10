// Builds data/doc-six-triple-eight.json: 8-minute long-form documentary (16:9) on the 6888th Central Postal Directory Battalion.
// Free local voice (Kokoro). Every fact has two or more sources (sourcesByClaim). No graphic detail of the July 1945 accident.
// Ending follows the owner's rule: only "subscribe for more". Run: node data/build_doc_six_triple_eight.mjs
import fs from 'node:fs';

const assets = {
  arrive: 'File:"The first Negro WACs to arrive (on) the continent of Europe were 800 girls of the 6888th Central Postal Directory Bn, w - NARA - 531333.jpg',
  wedding: 'File:"Chaplain William T. Green reads the benediction at the marriage ceremony of Pfc. Florence A. Collins, a WAC of the 6888 - NARA - 531314.jpg',
  inspect: 'File:"Somewhere in England, Maj. Charity E. Adams...and Capt. Abbie N. Campbell...inspect the first contingent of Negro mem - NARA - 531249.jpg',
  adams43: 'File:"WAAC Capt. Charity Adams of Columbia, NC, who was commissioned from the first officer candidate class, and the first of - NARA - 531334.jpg',
  adams: 'File:Charity Adams Earley.jpg',
  parade: "File:Members of the 6888th Central Postal Directory Battalion take part in a parade ceremony in honor of Joan d'Arc at the marketplace where she was burned at the stake.jpg",
  parade2: "File:Negro WAC battalion's first parade on the continent.jpg",
  members: 'File:Members of the 6888th Central Postal Directory Battalion.webp',
  medal1: 'File:6888th Central Postal Directory Batallion Congressional Gold Medal 1.jpg',
  cer18: 'File:Congressional Gold Medal award ceremony in honor of the 6888th Central Postal Directory Battalion’s contributions during WWII, on April 29, 2025, Washington, D.C - 18.jpg',
  cer48: 'File:Congressional Gold Medal award ceremony in honor of the 6888th Central Postal Directory Battalion’s contributions during WWII, on April 29, 2025, Washington, D.C - 48.jpg',
  greenock: 'File:U.S. Army nurses, newly arrived, line the rail of their vessel as it pulls into port of Greenock, Scotland, in European - NARA - 531204.jpg',
  bust: 'File:Lt. Col. Charity Adams bust statue.jpg',
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });

const ADAMS = 'Charity Adams';
const beats = [
  // ---- cold open
  ['h1', 'In February 1945, in Birmingham, England, warehouses were filled with mail that no one had delivered. About seventeen million letters and packages, for American soldiers fighting in Europe.', P('inspect', { focus: [0.5, 0.45], zoom: [1.1, 1.2] }), { hook: 'Seventeen million letters. *Nobody could deliver them.*' }],
  ['h2', 'Some had been sitting there for months. Soldiers were going without word from home, and the Army believed it was hurting morale.', T('17 million', 'letters and packages')],
  ['h3', 'The Army estimated the job would take six months. Then it sent eight hundred fifty-five Black women to do it.', C('arrive', 'Women of the 6888th, 1945')],
  ['h4', 'They cleared it in three.', T('3 months', 'instead of 6')],
  ['h5', 'They were the six thousand eight hundred eighty-eighth Central Postal Directory Battalion. The Six Triple Eight.', P('parade', { zoom: [1.0, 1.08] }), { lowerThird: { name: 'The Six Triple Eight', sub: '6888th Central Postal Directory Battalion' } }],

  // ---- origins
  ['o1', 'When the war began, women could serve in the Army through an auxiliary corps. In July 1943, Congress made it the Women\'s Army Corps, the WAC.', T('Women\'s Army Corps', 'July 1943'), { section: 'origins' }],
  ['o2', 'Black women joined it too. But for most of the war, the Army kept them at home, and many were given menial jobs.', C('adams43', 'Black WAC officers and enlisted women, 1943')],
  ['o3', 'Mary McLeod Bethune, the educator and adviser to the President, pushed to change that. So did First Lady Eleanor Roosevelt.', T('Mary McLeod Bethune', 'and Eleanor Roosevelt')],
  ['o4', 'They wanted a role for Black women in the war overseas.', P('adams43', { focus: [0.5, 0.5], zoom: [1.1, 1.2] })],
  ['o5', 'In 1944, the War Department agreed. It created a new unit, made up of Black women.', T('1944', 'the 6888th is created')],
  ['o5b', 'The women came from across the country. Most were African American, and some were of Caribbean and Mexican descent.', C('adams43', 'Black WAC officers and enlisted women, 1943')],
  ['o5c', 'They went through four to six weeks of basic training, and then weeks more of specialist training, before they were sent overseas.', P('adams43', { focus: [0.6, 0.5], zoom: [1.15, 1.25] })],
  ['o6', 'To lead it, the Army chose Major Charity Adams.', C('adams', ADAMS), { lowerThird: { name: 'Maj. Charity Adams', sub: 'commanding officer' } }],
  ['o7', 'She was from Columbia, South Carolina, and she had been in the first officer candidate class of the women\'s corps. She was now the highest ranking Black woman officer in the Army.', C('adams', ADAMS)],

  // ---- crossing
  ['s1', 'On February 3, 1945, the first of them sailed for Britain, on the liner Ile de France.', T('3 February 1945', 'sailing for Britain'), { section: 'crossing' }],
  ['s2', 'On February 12, they landed at Greenock, near Glasgow in Scotland, and went south by train to Birmingham.', C('greenock', 'U.S. Army nurses arriving at Greenock, Scotland, 1944'), { pin: { label: 'Birmingham', sub: 'England' } }],
  ['s3', 'Three days after they landed, two generals came to inspect them.', C('inspect', 'Maj. Charity Adams and Capt. Abbie Campbell inspect the first women to arrive, February 1945')],
  ['s4', 'The battalion had eight hundred fifty-five women in five companies, both officers and enlisted.', P('inspect', { focus: [0.3, 0.5], zoom: [1.2, 1.3] })],
  ['s4b', 'There was a headquarters company and four more, A through D. And they ran their own camp from the start.', P('inspect', { focus: [0.7, 0.5], zoom: [1.2, 1.3] })],
  ['s5', 'And they did not only sort mail. They had their own cooks, mechanics, medics and military police.', T('Self-sufficient', 'cooks, mechanics, medics, police')],

  // ---- Birmingham
  ['b1', 'What they found in Birmingham was a mess.', T('Birmingham', 'February 1945'), { section: 'birmingham' }],
  ['b2', 'The mail was stacked in cold, dark buildings, with the windows blacked out against air raids. There was little heat.', T('Cold and dark', 'windows blacked out')],
  ['b3', 'Rats had gotten into packages of food sent from home.', T('Rats', 'in the packages')],
  ['b4', 'And so much of it could not be delivered. Letters were addressed only to a first name, or to a nickname, or to "Junior, U.S. Army."', T('"Junior, U.S. Army"', 'a typical address')],
  ['b5', 'There were about seven million Americans in Europe, and they kept moving. In one account, seven thousand five hundred of them were named Robert Smith.', T('7,500', 'soldiers named Robert Smith')],
  ['b6', 'So the women built a system. They kept index cards for soldiers, with their serial numbers and their units, and updated them as men moved.', C('members', 'Members of the 6888th, 1945')],
  ['b7', 'In time, the card file grew to seven million cards.', T('7 million', 'index cards')],
  ['b7b', 'Mail for a soldier who had been wounded, or moved, or killed, had to be traced through those cards, one name at a time.', C('members', 'Members of the 6888th, 1945')],
  ['b8', 'They worked three shifts, eight hours each, seven days a week. Each shift handled about sixty-five thousand pieces of mail.', T('65,000', 'pieces of mail per shift')],
  ['b9', 'Their motto was simple. No mail, low morale.', Q('No mail, low morale.', 'Motto of the 6888th')],

  // ---- the general
  ['g1', 'Not everyone welcomed them.', P('inspect', { focus: [0.7, 0.45], zoom: [1.2, 1.3] }), { section: 'general' }],
  ['g2', 'One day, a white general came to inspect, and found only some of the women in formation. He asked where the rest were.', C('adams', ADAMS)],
  ['g3', 'Adams told him. A third were on duty, a third were sleeping, after the night shift.', T('Three shifts', 'a third always working')],
  ['g4', 'He said he was going to send a white first lieutenant down to show her how to run things.', Q('I\'m going to send a white first lieutenant down here to show you how to run things.', 'A visiting general, 1945')],
  ['g5', 'Her answer became famous. Over my dead body, sir.', Q('Over my dead body, sir.', 'Maj. Charity Adams')],
  ['g6', 'Her staff found an official memo warning commanders against language that stressed racial segregation. The general backed down.', T('He backed down', '')],
  ['g7', 'When the Red Cross tried to put the women in a separate hotel in London, Adams refused that too.', C('adams43', 'Charity Adams with Black WAC trainees, 1943')],
  ['g8', 'And when they were offered separate facilities, they ran their own. Their own dining hall, their own beauty shop, their own snack bar.', C('wedding', 'A wedding in the 6888th, 1945')],

  // ---- three months
  ['m1', 'By May 1945, the backlog in Birmingham was gone. The Army had expected six months. It took them three.', T('Three months', 'Birmingham, cleared'), { section: 'done' }],
  ['m2', 'The war in Europe had just ended. And there was more mail waiting in France.', T('More mail', 'waiting in France')],
  ['m3', 'In the spring of 1945, the battalion moved to Rouen.', C('arrive', 'Women of the 6888th, 1945'), { pin: { label: 'Rouen', sub: 'France' } }],
  ['m4', 'There, they marched in a parade in honor of Joan of Arc, in the marketplace where she had been burned at the stake.', P('parade', { zoom: [1.0, 1.08] })],
  ['m4b', 'In Rouen, they were housed in old French barracks, and they worked in cold, damp buildings that were no better than the ones in England.', T('Rouen', 'old barracks, cold, damp buildings')],
  ['m5', 'The people of Rouen watched American women in uniform, Black women, marching through their square.', P('parade2', { focus: [0.5, 0.6], zoom: [1.1, 1.2] })],
  ['m6', 'In July, three of them, Mary Bankston, Mary Barlow and Dolores Browne, were killed in a jeep accident.', T('July 1945', 'three women lost in Rouen')],
  ['m7', 'They are buried at the Normandy American Cemetery, among the very few women buried there.', T('Normandy', 'American Cemetery')],
  ['m8', 'The Rouen backlog was cleared too. In October 1945, the unit moved to Paris.', P('parade2', { zoom: [1.0, 1.08] }), { pin: { label: 'Paris', sub: 'October 1945' } }],

  // ---- home and memory
  ['r1', 'In February 1946, the last of them returned to the United States. The battalion was disbanded at Fort Dix, New Jersey.', C('wedding', 'Members of the 6888th, 1945'), { section: 'home' }],
  ['r2', 'There was no parade. No public ceremony. No welcome home.', T('No parade', 'February 1946')],
  ['r3', 'Many of them went to college on the GI Bill and became teachers, nurses, and civil rights workers.', C('members', 'Members of the 6888th, 1945')],
  ['r4', 'Charity Adams left the Army as a lieutenant colonel. In 1989, she published her memoir, One Woman\'s Army.', C('adams', 'Charity Adams Earley')],
  ['r4b', 'In 1981, some of the veterans went back to Birmingham, where the mayor honored them. In 1996, the Smithsonian\'s National Postal Museum honored Charity Adams.', T('1981 and 1996', 'Birmingham, then the Smithsonian')],
  ['r4c', 'In 2019, a blue plaque went up at King Edward\'s School in Birmingham, where the women had worked through the mail.', T('Blue plaque', 'King Edward\'s School, Birmingham, 2019')],
  ['r5', 'Slowly, the country began to remember. A monument at Fort Leavenworth in 2018. A unit commendation from the Army in 2019.', T('2018 and 2019', 'a monument, a commendation')],
  ['r5b', 'In 2021, the Senate passed a measure to honor them.', T('2021', 'the Senate acts')],
  ['r6', 'In February 2022, the House of Representatives voted four hundred twenty-two to zero to award the battalion the Congressional Gold Medal. President Biden signed the bill that March.', T('422 to 0', 'the House vote, 2022')],
  ['r7', 'In 2023, the Army renamed Fort Lee, in Virginia, as Fort Gregg-Adams, in part for Charity Adams.', C('bust', 'Lt. Col. Charity Adams, Fort Gregg-Adams')],
  ['r8', 'On April 29, 2025, the medal was presented in Emancipation Hall at the U.S. Capitol. More than three hundred descendants of the women were there.', C('cer18', 'The Congressional Gold Medal ceremony, U.S. Capitol, 29 April 2025'), { stamp: '29 April 2025' }],
  ['r9', 'Charity Adams\'s son accepted it on her behalf.', C('cer48', 'The Congressional Gold Medal of the 6888th')],
  ['r9b', 'And in December 2024, a film about them, The Six Triple Eight, put their story in front of millions of people who had never heard it.', T('The Six Triple Eight', 'a film, December 2024')],

  // ---- close
  ['e1', 'Seventeen million letters. Three months.', C('medal1', 'The Congressional Gold Medal of the 6888th'), { section: 'close' }],
  ['e2', 'They worked in the cold and the dark, against a deadline and against the doubts of their own Army.', P('inspect', { focus: [0.5, 0.45], zoom: [1.1, 1.2] })],
  ['e3', 'And every letter they moved meant a soldier somewhere finally heard from home.', P('parade', { focus: [0.5, 0.6], zoom: [1.15, 1.25] })],
  ['e4', 'That was the Six Triple Eight. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-ellen-craft.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/6888th_Central_Postal_Directory_Battalion',
  NPS: 'https://home.nps.gov/articles/000/6888th.htm',
  NWW2: 'https://www.nationalww2museum.org/war/articles/the-sixtripleeight-6888th-battalion',
  HH: 'https://www.historyhit.com/no-mail-low-morale-who-were-the-6888th-central-postal-directory-battalion/',
  ARMY: 'https://www.army.mil/article/285120',
  GMA: 'https://www.goodmorningamerica.com/news/story/only-black-female-wwii-unit-receives-congressional-gold-medal-121276809',
  NBC: 'https://www.nbcnews.com/news/us-news/black-female-wwii-unit-recognized-congressional-honor-rcna18071',
  BIO: 'https://www.biography.com/military-figures/a63023908/the-six-triple-eight-true-story',
  DB: 'https://www.database-memoire.eu/prive/en-us/menu-colleville-us/19-colleville-b-us/6708-barlow-mary-j-6888-cpdb-wac',
};
const sourcesByClaim = {
  h1: ['WIKI', 'ARMY', 'NWW2'], h2: ['WIKI', 'NPS'], h3: ['NPS', 'HH', 'WIKI'], h4: ['NPS', 'NWW2', 'ARMY'], o1: ['NPS', 'WIKI'], o3: ['WIKI', 'NPS'],
  o5: ['NPS', 'HH'], o6: ['WIKI', 'NPS'], o7: ['NPS', 'WIKI'], s1: ['WIKI', 'NPS'], s2: ['WIKI', 'HH'], s3: ['WIKI', 'NWW2'], s4: ['WIKI', 'HH'], s5: ['NWW2', 'HH'],
  b2: ['NPS', 'HH', 'WIKI'], b3: ['ARMY', 'HH'], b4: ['WIKI', 'HH'], b5: ['HH', 'WIKI'], b6: ['HH', 'WIKI'], b7: ['WIKI', 'HH'], b8: ['NPS', 'WIKI', 'HH'], b9: ['NPS', 'ARMY', 'HH'],
  g2: ['NWW2', 'HH'], g3: ['NWW2', 'HH'], g4: ['NWW2', 'HH'], g5: ['NWW2', 'HH'], g6: ['NWW2', 'WIKI'], g7: ['NWW2', 'WIKI'], g8: ['HH', 'WIKI'],
  m1: ['WIKI', 'NPS', 'NWW2'], m3: ['WIKI', 'NWW2'], m4: ['WIKI', 'HH'], m6: ['NWW2', 'DB', 'WIKI'], m7: ['NWW2', 'DB'], m8: ['NPS', 'HH'],
  r1: ['WIKI', 'HH'], r2: ['NPS', 'HH'], r3: ['NWW2', 'HH'], r4: ['NPS', 'HH'], r5: ['WIKI', 'NWW2'], r6: ['NPS', 'HH', 'WIKI'], r7: ['WIKI', 'ARMY'],
  r8: ['GMA', 'ARMY'], r9: ['ARMY', 'GMA'], o5b: ['NPS', 'HH'], o5c: ['NPS', 'WIKI'], s4b: ['HH', 'WIKI'], b7b: ['HH', 'WIKI'], m4b: ['HH', 'NWW2'], r4b: ['NPS', 'HH'], r4c: ['WIKI', 'NWW2'], r5b: ['NPS', 'HH'], r9b: ['BIO', 'WIKI'],
};

const spec = {
  id: 'doc-six-triple-eight',
  title: '17 Million Letters. 855 Black Women. They Did It in Half the Time.',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { Rouen: 'Roo-on', Greenock: 'Green-uck', Eleanor: 'Ellen-or', 'Ile de France': 'Eel duh France', Bankston: 'Bank-stun' },
  music: base.music,
  mix: base.mix,
  brand: { page: 'The Black History Room', cta: 'Subscribe', ctaLine: '', theme: 'bhr' },
  assets: Object.fromEntries(Object.entries(assets).map(([k, v]) => [k, { commons: v }])),
  beats: beats.map(([id, text, visual, overlays, extra]) => {
    const { section, ...ov } = overlays || {};
    return { id, text, visual, ...(Object.keys(ov).length ? { overlays: ov } : {}), ...(section ? { section } : {}), ...(extra || {}) };
  }),
  sourcesByClaim,
  sources: Object.fromEntries(Object.entries(sources).map(([k, url]) => [k, { url }])),
  notUsed: [
    'Number of women: 855 (Wikipedia, History Hit) vs "over 800" / "800 girls" (National WWII Museum, NARA caption): script uses 855.',
    'The Greenock photo shows U.S. Army nurses in 1944, not the 6888th; it is captioned as such.',
    'Exact date and cause of the Rouen accident: left at "July, jeep accident"; no detail.',
    'Promotion of Adams to colonel in 2025: not confirmed.',
  ],
};
fs.writeFileSync('data/doc-six-triple-eight.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images`);
