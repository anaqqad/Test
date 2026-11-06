// Builds data/doc-dorie-miller.json: 8-minute long-form documentary (16:9) on Doris "Dorie" Miller.
// Every fact has two or more sources (sourcesByClaim). No graphic violence: no description of injuries.
// Ending follows the owner's rule: only "subscribe for more".
// Run: node data/build_doc_dorie_miller.mjs
import fs from 'node:fs';

const assets = {
  portrait: 'File:Dorie Miller - Restoration, full.jpg',
  uniform: 'File:Doris (Dorie) Miller in uniform at Pearl Harbor (10006682).jpg',
  nimitz: 'File:Nimitz and miller.jpg',
  nimitz2: 'File:Admiral Chester W. Nimitz pins the Navy Cross on Doris Miller, Pearl Harbor, May 27, 1942.jpg',
  awards: 'File:Doris Miller and other sailors presented with awards.jpg',
  speech: 'File:Doris Miller speaking at Naval Station Great Lakes January 1943.jpg',
  lakes: 'File:Doris Miller at Naval Station Great Lakes January 1943.jpg',
  poster: 'File:"Above and Beyond the Call of Duty.", 1943 - NARA - 535886.jpg',
  wv1: 'File:USS West Virginia2.jpg',
  wvafter: 'File:Aftermath of a Japanese sneak attack on these three stricken U.S. battleships, from left to right, USS West Virginia... - NARA - 196243.jpg',
  planeview: 'File:Attack on Pearl Harbor Japanese planes view.jpg',
  recon: 'File:Pearl Harbor Japanese recon photo of battleship row 80G30551.jpg',
  ph1: 'File:Pearl Harbor Attack, 7 December 1941 - 80-G-6683.jpg',
  ph2: 'File:Pearl Harbor Attack, 7 December 1941 - 80-G-32920.jpg',
  burning: 'File:Burning ships at Pearl Harbor.jpg',
  aftermath: 'File:Pearl harbor aftermath.jpg',
  liscome: 'File:USS Liscome Bay CVE56.jpg',
  frigate: 'File:USS Miller (FF-1091).jpg',
  commission: 'File:USS Miller (FF-1091) commissioning ceremony 1973.jpg',
  announce: 'File:Doris Miller Announcement 01.jpg',
  wvnew: 'File:USS West Virginia (BB-48) (69b306da-1dd8-b71b-0b8a-c53abdc88fff).jpg',
  profile: 'File:USS West Virginia (BB-48) inboard and outboard profiles 1930s.png',
  stamp: 'File:US Navy 100204-N-1281L-048 The Distinguished Sailors commemorative stamps series is unveiled.jpg',
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });

const PORTRAIT = 'Doris "Dorie" Miller, May 1942';
const beats = [
  // ---- cold open
  ['h1', 'On the morning of December 7, 1941, a young sailor was collecting laundry on a battleship at Pearl Harbor.', P('wv1', { focus: [0.5, 0.45], zoom: [1.0, 1.1] }), { hook: 'He was collecting laundry. *Then Pearl Harbor.*' }],
  ['h2', 'The Navy had given him one kind of job. Feed the officers. Serve their meals. It was the only branch open to a Black recruit.', C('portrait', PORTRAIT)],
  ['h3', 'Before that morning was over, he was behind a machine gun, firing at Japanese planes. He had never been trained to use it.', P('burning', { motion: 'panLeft', zoom: [1.0, 1.1] })],
  ['h4', 'The Navy praised his courage, but it did not give his name. A Black newspaper had to find it.', T('No name', "the Navy's first account")],
  ['h5', 'He became the first Black sailor to receive the Navy Cross. And he still went back to work as a mess attendant.', C('nimitz2', 'Admiral Nimitz pins the Navy Cross on Doris Miller, 27 May 1942')],
  ['h6', 'His name was Doris Miller. History knows him as Dorie. This is the story of the sailor the Navy was not ready for.', C('uniform', 'Doris Miller at Pearl Harbor, 1942'), { lowerThird: { name: 'Doris "Dorie" Miller', sub: '1919 – 1943' } }],

  // ---- Waco
  ['w1', 'Doris Miller was born on October 12, 1919, in Waco, Texas.', T('Waco', 'Texas, 1919'), { section: 'waco', year: { from: 1919, to: 1919 }, pin: { label: 'Waco', sub: 'Texas' } }],
  ['w2', 'His parents were farmers, and he was one of four sons. He worked the land with his family.', T('One of four sons', 'a farming family in Waco')],
  ['w3', 'He grew up big and strong, and he played fullback on his high school football team.', T('Fullback', 'Moore High School, Waco')],
  ['w4', 'But he left school without graduating. His family needed the money, and there were few good jobs around Waco for a young Black man.', P('portrait', { focus: [0.5, 0.16], zoom: [1.75, 1.85] })],
  ['w5', 'So he looked to the Navy, for steady pay and a way out of Waco.', T('The U.S. Navy', 'steady pay, and a way out')],
  ['w6', 'On September 16, 1939, two weeks after war broke out in Europe, he walked into a recruiting station in Dallas and signed up for six years.', T('16 September 1939', 'Dallas, Texas'), { pin: { label: 'Dallas', sub: 'Texas' } }],
  ['w7', 'He was nineteen years old.', T('19', 'years old')],

  // ---- the messman branch
  ['m1', 'But the Navy had a separate place for men like him.', P('poster', { focus: [0.5, 0.36], zoom: [1.0, 1.08] }), { section: 'navy' }],
  ['m2', 'At that time, a Black recruit had almost no choice. He went into the messman branch.', T('The messman branch', 'U.S. Navy, 1939')],
  ['m3', 'Messmen fed and served the white officers. They looked after their meals and their laundry. It was a segregated branch, made up mostly of Black and Filipino sailors.', T('Messmen', 'fed and served the officers')],
  ['m4', 'White sailors were not allowed to serve in it. And for Black sailors, there was almost no way out of it.', T('Segregated', 'by Navy policy')],
  ['m5', 'Miller enlisted as a mess attendant, third class. He trained at Norfolk, Virginia, and was sent to the ammunition ship Pyro.', T('Mess attendant', 'third class'), { pin: { label: 'Norfolk', sub: 'Virginia' } }],
  ['m6', 'Then, on January 2, 1940, he joined the crew of the battleship USS West Virginia.', C('wvnew', 'USS West Virginia'), { stamp: '2 January 1940' }],
  ['m7', 'On a ship full of men, he made his name another way. He became the heavyweight boxing champion of the West Virginia.', T('Heavyweight champion', 'USS West Virginia')],
  ['m8', 'His battle station, if the alarm ever rang, was below decks, at an ammunition magazine serving the anti-aircraft guns.', C('profile', 'USS West Virginia, inboard and outboard profiles, 1930s')],
  ['m9', 'He would pass the ammunition. Other men would do the fighting.', T('Pass the ammunition', 'his job in battle')],

  // ---- the attack
  ['a1', 'Sunday, December 7, 1941. Pearl Harbor, Hawaii.', P('recon', { zoom: [1.0, 1.08] }), { section: 'attack', stamp: '7 December 1941', pin: { label: 'Pearl Harbor', sub: 'Hawaii' } }],
  ['a2', 'West Virginia was moored along Battleship Row, with the rest of the Pacific Fleet around her.', P('recon', { focus: [0.5, 0.35], zoom: [1.3, 1.4] })],
  ['a3', 'Just before eight in the morning, Dorie Miller was below decks, collecting laundry.', T('7:55 a.m.', 'Pearl Harbor')],
  ['a4', 'Then Japanese planes came in over the harbor.', P('planeview', { zoom: [1.0, 1.1] })],
  ['a5', 'The first torpedo hit West Virginia. Then more. Water poured into the ship.', P('wv1', { focus: [0.4, 0.5], zoom: [1.15, 1.25] })],
  ['a6', 'Miller ran for his battle station. He found it destroyed.', P('ph2', { motion: 'panRight', zoom: [1.0, 1.1] })],
  ['a7', 'There was no ammunition to pass. So he started helping the injured men he could reach.', P('burning', { focus: [0.5, 0.6], zoom: [1.15, 1.25] })],
  ['a8', 'An officer sent him up to the bridge. The captain of the West Virginia, Mervyn Bennion, had been badly wounded.', P('wv1', { focus: [0.45, 0.25], zoom: [1.3, 1.4] }), { lowerThird: { name: 'Capt. Mervyn Bennion', sub: 'USS West Virginia' } }],
  ['a9', 'Miller was the ship\'s boxing champion. He and others carried the captain to a safer spot behind the conning tower.', P('wv1', { focus: [0.55, 0.3], zoom: [1.2, 1.3] })],
  ['a10', 'Captain Bennion did not survive the attack.', T('Capt. Mervyn Bennion', 'did not survive')],
  ['a11', 'Then came the moment people still remember.', P('ph1', { zoom: [1.0, 1.08] })],
  ['a12', 'Near the conning tower stood fifty-caliber anti-aircraft machine guns. Miller was told to help feed them ammunition.', T('.50 caliber', 'anti-aircraft machine guns')],
  ['a13', 'Then he took one of the guns himself.', C('poster', '"Above and Beyond the Call of Duty", U.S. Navy poster, 1943')],
  ['a14', 'He had never been trained on it. A mess attendant was not supposed to be there.', T('No training', 'on that gun')],
  ['a15', 'He aimed at the planes and fired, and he kept firing until the ammunition ran out.', P('ph2', { focus: [0.5, 0.5], zoom: [1.2, 1.3] })],
  ['a16', 'Afterward, he made it sound simple. It was not hard, he said. I just pulled the trigger, and she worked fine.', Q('I just pulled the trigger, and she worked fine.', 'Dorie Miller')],
  ['a17', 'How many planes he hit is still argued over. He believed he hit one. The Navy never settled it.', P('planeview', { focus: [0.5, 0.5], zoom: [1.2, 1.3] })],
  ['a18', 'And it almost does not matter. A man the Navy had trained to serve meals was shooting back.', P('poster', { focus: [0.5, 0.42], zoom: [1.3, 1.4] })],
  ['a19', 'West Virginia could not be saved. She settled onto the bottom of the harbor, on fire.', P('wvafter', { focus: [0.6, 0.5], zoom: [1.05, 1.15] })],
  ['a20', 'Miller helped pull sailors out of the water.', P('wv1', { focus: [0.5, 0.82], zoom: [1.3, 1.4] })],
  ['a21', 'More than a hundred men of the West Virginia were lost that morning.', T('100+', 'men of the West Virginia lost')],
  ['a22', 'Across Pearl Harbor, more than two thousand Americans died. The next day, the United States went to war.', P('aftermath', { zoom: [1.0, 1.1] })],

  // ---- the unnamed sailor
  ['u1', 'A few days later, Miller was transferred to the cruiser USS Indianapolis. He was back at work as a mess attendant.', T('USS Indianapolis', 'back at work as a mess attendant'), { section: 'unnamed' }],
  ['u2', 'Meanwhile, a story began to spread about a Black sailor at Pearl Harbor who had manned a machine gun.', T('The unnamed sailor', 'December 1941')],
  ['u3', 'Newspapers carried it before the month was out. There was no name.', P('burning', { focus: [0.4, 0.45], zoom: [1.2, 1.3] })],
  ['u4', 'On January 1, 1942, the Navy issued a commendation for the sailor. It still did not name him.', T('1 January 1942', 'commended, but not named'), { year: { from: 1942, to: 1942 } }],
  ['u5', 'Black Americans wanted to know who he was. And they wanted to know why the Navy would not say.', P('portrait', { focus: [0.5, 0.16], zoom: [1.75, 1.85] })],
  ['u6', 'The Pittsburgh Courier, one of the leading Black newspapers in the country, went looking for him.', T('The Pittsburgh Courier', 'looking for the sailor')],
  ['u7', 'In March 1942, it printed his name. It called him Dorie Miller. And that is the name that stuck.', C('portrait', PORTRAIT), { stamp: 'March 1942' }],
  ['u8', 'Now the pressure grew. Bills went to Congress calling for the Medal of Honor, the highest award there is.', T('Medal of Honor', 'bills in Congress, 1942')],
  ['u9', 'Navy Secretary Frank Knox recommended against it.', T('Frank Knox', 'Secretary of the Navy')],
  ['u10', 'On May 11, 1942, President Roosevelt approved a different award: the Navy Cross.', T('11 May 1942', 'the Navy Cross approved')],

  // ---- the Navy Cross
  ['c1', 'On May 27, 1942, sailors stood in lines on the flight deck of the carrier USS Enterprise, at Pearl Harbor.', P('awards', { motion: 'panLeft', zoom: [1.0, 1.1] }), { section: 'cross', stamp: '27 May 1942' }],
  ['c2', 'Admiral Chester Nimitz, commander of the Pacific Fleet, stepped up to Dorie Miller and pinned the medal on his chest.', C('nimitz', 'Nimitz and Miller on the USS Enterprise')],
  ['c3', 'The citation praised his distinguished devotion to duty, extraordinary courage, and disregard for his own personal safety.', Q('Distinguished devotion to duty, extraordinary courage and disregard for his own personal safety.', 'Navy Cross citation, 1942')],
  ['c4', 'He was the first Black sailor ever to receive it.', C('nimitz2', 'Doris Miller receives the Navy Cross')],
  ['c5', 'The Navy was starting to change, slowly. That April, it had said Black recruits could train for general service, at a new camp named for Robert Smalls, the man who sailed a Confederate ship to freedom.', P('lakes', { focus: [0.5, 0.4], zoom: [1.0, 1.1] })],
  ['c6', 'But Dorie Miller, now a national hero, was still a mess attendant.', C('portrait', PORTRAIT)],
  ['c7', 'Late in 1942, after nearly a year at sea, he was brought back, and the Navy sent him on a tour.', P('speech', { focus: [0.62, 0.4], zoom: [1.0, 1.1] })],
  ['c8', 'For more than two months, he spoke to crowds and to sailors, and helped sell war bonds.', P('speech', { focus: [0.68, 0.32], zoom: [1.2, 1.3] })],
  ['c9', 'In January 1943, he stood at Great Lakes, Illinois, in front of the first class of Black recruits to graduate from Camp Robert Smalls.', C('lakes', 'Doris Miller at Naval Station Great Lakes, January 1943'), { pin: { label: 'Great Lakes', sub: 'Illinois' } }],
  ['c10', 'They were training for jobs he had never been offered.', P('lakes', { focus: [0.5, 0.35], zoom: [1.2, 1.3] })],
  ['c11', 'That year, the Navy put his face on a recruiting poster. Above and beyond the call of duty, it said.', C('poster', '"Above and Beyond the Call of Duty", 1943')],
  ['c12', 'Then it sent him back to sea.', T('Back to sea', '1943')],

  // ---- Liscome Bay
  ['l1', 'In the spring of 1943, Miller joined a new escort carrier, the USS Liscome Bay.', C('liscome', 'USS Liscome Bay, 1943'), { section: 'liscome' }],
  ['l2', 'He was promoted to cook, third class. It was a higher rank, in the same kitchen.', T('Cook, third class', 'June 1943')],
  ['l3', 'In November, Liscome Bay sailed for the Gilbert Islands in the Pacific, for the invasion of Makin.', C('liscome', 'USS Liscome Bay'), { pin: { label: 'Makin', sub: 'Gilbert Islands' } }],
  ['l4', 'On November 24, 1943, a Japanese submarine fired a torpedo into her side.', T('24 November 1943', 'off Makin'), { year: { from: 1943, to: 1943 } }],
  ['l5', 'The blast set off the bombs stored aboard. The ship went down in about twenty-three minutes.', T('23 minutes', 'and she was gone')],
  ['l6', 'More than six hundred men were lost. Dorie Miller was one of them.', T('600+', 'men lost')],
  ['l7', 'He was twenty-four years old. His body was never recovered.', C('portrait', PORTRAIT)],

  // ---- legacy
  ['z1', 'Four months after he died, in March 1944, the Navy commissioned its first thirteen Black officers.', T('13', 'first Black Navy officers, 1944'), { section: 'legacy' }],
  ['z2', 'It came too late for the man who had helped force the question.', P('poster', { focus: [0.5, 0.36], zoom: [1.0, 1.08] })],
  ['z3', 'In 1973, the Navy commissioned a ship in his name, the USS Miller.', C('commission', 'Commissioning of the USS Miller, 1973')],
  ['z3b', 'She sailed for eighteen years.', P('frigate', { focus: [0.5, 0.5], zoom: [1.1, 1.2] })],
  ['z4', 'In 2010, he appeared on a United States postage stamp, among the distinguished sailors of the Navy.', P('stamp', { focus: [0.5, 0.45], zoom: [1.1, 1.2] })],
  ['z5', 'And on January 20, 2020, Martin Luther King Day, the Navy announced that a future aircraft carrier would be named USS Doris Miller.', C('announce', 'The USS Doris Miller announcement, 20 January 2020')],
  ['z6', 'It would be the first aircraft carrier named for a Black American, and the first named for an enlisted sailor.', T('CVN-81', 'announced as USS Doris Miller')],
  ['z7', 'In 2026, reports said the Navy was weighing a new name for that ship, and that the Medal of Honor was under consideration. So far, nothing has been announced.', T('2026', 'nothing announced so far')],
  ['z8', 'The first bills for his Medal of Honor went to Congress in 1942. People are still asking.', C('poster', 'Doris Miller, Navy poster, 1943')],

  // ---- close
  ['e1', 'A farm boy from Waco, who wanted a way out.', P('portrait', { focus: [0.5, 0.16], zoom: [1.75, 1.85] }), { section: 'close' }],
  ['e2', 'A sailor the Navy would let serve meals, but not much more.', P('wv1', { focus: [0.5, 0.45], zoom: [1.2, 1.3] })],
  ['e3', 'A hero it praised before it would name him, and sent back to the kitchen after it did.', C('nimitz', 'Nimitz and Miller, 1942')],
  ['e4', 'Nobody had trained him for that gun. He fired back anyway.', C('portrait', PORTRAIT)],
  ['e5', 'That was Dorie Miller. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const voiceSrc = JSON.parse(fs.readFileSync('data/doc-ellen-craft.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Doris_Miller',
  NHHC: 'https://www.history.navy.mil/research/histories/biographies-list/bios-m/miller-doris.html',
  HN: 'https://historynet.com/valor-pearl-harbors-unlikely-hero/',
  NT: 'https://www.navytimes.com/military-honor/salute-veterans/2019/11/01/how-dorie-millers-bravery-helped-fight-bigotry-in-the-navy/',
  MF: 'https://mentalfloss.com/article/642783/doris-miller-naval-cook-pearl-harbor-hero',
  SHIP: 'https://en.wikipedia.org/wiki/USS_Doris_Miller',
  STRIPES: 'https://www.stripes.com/branches/navy/2026-08-28/future-aircraft-carrier-doris-miller-name-change-22685891.html',
  NBC: 'https://www.nbcnews.com/politics/trump-administration/navy-discusses-renaming-aircraft-carrier-trump-black-uss-doris-miller-rcna593667',
  HILL: 'https://thehill.com/policy/defense/6044226-navy-doris-miller-trump-aircraft-carrier/',
};
const sourcesByClaim = {
  h1: ['WIKI', 'HN', 'MF'], h2: ['WIKI', 'NT'], h3: ['HN', 'MF', 'NT'], h4: ['WIKI', 'NT'], h5: ['WIKI', 'HN', 'NT'],
  w1: ['WIKI', 'MF', 'HN'], w2: ['WIKI', 'MF'], w3: ['WIKI', 'MF'], w4: ['WIKI', 'MF'], w6: ['NHHC', 'WIKI', 'NT', 'MF'],
  m2: ['WIKI', 'NT'], m3: ['WIKI', 'NT'], m4: ['WIKI', 'NT'], m5: ['NHHC', 'WIKI'], m6: ['NHHC', 'WIKI', 'NT', 'HN'], m7: ['WIKI', 'HN'], m8: ['HN', 'WIKI'],
  a3: ['WIKI', 'HN', 'MF'], a5: ['HN', 'WIKI'], a6: ['HN', 'WIKI'], a7: ['HN', 'WIKI'], a8: ['HN', 'WIKI', 'MF'], a9: ['HN', 'WIKI', 'MF'], a10: ['HN', 'WIKI'],
  a12: ['MF', 'HN', 'WIKI'], a13: ['HN', 'MF', 'NT'], a14: ['HN', 'MF', 'NT'], a15: ['WIKI', 'HN', 'MF'], a16: ['HN', 'MF'], a17: ['WIKI', 'MF'],
  a19: ['HN', 'WIKI'], a20: ['NT', 'MF'], a21: ['HN', 'MF'], u1: ['WIKI', 'NT'], u2: ['MF', 'NT'], u3: ['NT', 'MF'], u4: ['WIKI', 'NT'],
  u6: ['WIKI', 'NT', 'MF'], u7: ['WIKI', 'NT', 'MF'], u8: ['WIKI', 'MF'], u9: ['WIKI', 'NT'], u10: ['WIKI', 'NT'],
  c1: ['WIKI', 'NT', 'HN'], c2: ['WIKI', 'NT', 'HN', 'MF'], c3: ['HN', 'WIKI'], c4: ['HN', 'NT', 'WIKI'], c5: ['NT', 'WIKI'], c6: ['WIKI', 'HN'],
  c7: ['NT', 'HN'], c8: ['NT', 'WIKI'], c9: ['NT', 'WIKI'], c11: ['WIKI', 'MF'], l1: ['WIKI', 'HN', 'NT'], l2: ['WIKI', 'NT', 'HN'], l3: ['WIKI', 'HN'],
  l4: ['WIKI', 'HN', 'NT', 'MF'], l5: ['HN', 'WIKI', 'NT'], l6: ['MF', 'HN', 'WIKI'], l7: ['HN', 'NT', 'MF'], z1: ['NT', 'WIKI'], z3: ['WIKI', 'NT'],
  z3b: ['WIKI', 'SHIP'], z4: ['WIKI', 'SHIP'], z5: ['WIKI', 'MF', 'SHIP'], z6: ['WIKI', 'SHIP'], z7: ['STRIPES', 'NBC', 'HILL', 'WIKI'], z8: ['WIKI', 'STRIPES'],
};

const spec = {
  id: 'doc-dorie-miller',
  title: 'The Navy Made Him Serve Meals. At Pearl Harbor, He Manned a Machine Gun.',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: voiceSrc.voice,
  music: voiceSrc.music,
  mix: voiceSrc.mix,
  brand: { page: 'The Black History Room', cta: 'Subscribe', ctaLine: '', theme: 'bhr' },
  assets: Object.fromEntries(Object.entries(assets).map(([k, v]) => [k, { commons: v }])),
  beats: beats.map(([id, text, visual, overlays, extra]) => {
    const { section, ...ov } = overlays || {};
    return { id, text, visual, ...(Object.keys(ov).length ? { overlays: ov } : {}), ...(section ? { section } : {}), ...(extra || {}) };
  }),
  sourcesByClaim,
  sources: Object.fromEntries(Object.entries(sources).map(([k, url]) => [k, { url }])),
  notUsed: [
    'Number of planes hit: claims range from one to six; the script says it is argued over.',
    'Crew lost on West Virginia: 130 (HistoryNet) vs 106 (Mental Floss): script says more than a hundred.',
    'Liscome Bay dead: 644 (HistoryNet) vs 702 (Wikipedia): script says more than six hundred.',
    'Gun training: he attended a secondary-battery gunnery school on USS Nevada (HistoryNet, NHHC), which was not the .50-caliber gun; several sources say no training on that weapon, and Wikipedia also says officers instructed him during the attack.',
    'The "Dorie" typo story: the origin is uncertain. The script only says the Courier used the name and it stuck.',
    'His mother recognising the story; the "busboy" quote; Delano and Johnson by name: single source.',
    'Who else may be named for CVN-81 in the reports: left out on purpose. Re-check for any Navy announcement before publishing.',
  ],
};
fs.writeFileSync('data/doc-dorie-miller.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ~${(text.split(/\s+/).length / 165).toFixed(1)} min at 165 wpm, ${Object.keys(assets).length} images`);
