// Builds data/doc-black-wall-street.json: long-form documentary (16:9) on the 1921 destruction of Greenwood, Tulsa.
// Cluster "Black Wall Street", video 1 of 3. Free local voice (Kokoro). Every fact has two or more sources (sourcesByClaim).
// No graphic images: photos of the dead are not used. Images: Library of Congress (no known restrictions) and US public domain.
// New template features used here: chapter tags, karaoke subtitles with gold keywords, count-up stat cards,
// a gold marker on the 1921 newspaper headline, film grain. Ending follows the owner's rule: only "subscribe for more".
// Run: node data/build_doc_black_wall_street.mjs
import fs from 'node:fs';

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });
const CH = (num, title) => ({ kind: 'chapter', num, title });
const S = (to, label, image, o = {}) => ({ kind: 'stat', image, stat: { to, label, ...o } });

const LOC = 'Library of Congress';
const beats = [
  // ---- cold open
  ['h1', 'On the morning of June the first, 1921, black smoke rose over the north side of Tulsa, Oklahoma.', P('fire', { focus: [0.45, 0.4], zoom: [1.0, 1.12] }), { hook: 'Thirty-five blocks. *One morning.*' }],
  ['h2', 'By the afternoon, a whole Black neighborhood had burned. Homes, churches, shops, and a business district.', P('inflames', { zoom: [1.02, 1.12] })],
  ['h3', 'Its name was Greenwood. Its main street was called the Negro Wall Street. Today, we know it as Black Wall Street.', P('panorama', { motion: 'panRight', zoom: [1.0, 1.05] }), { pin: { label: 'Greenwood', sub: 'Tulsa, Oklahoma' } }],
  ['h4', 'What happened there was left out of the history books for most of a century.', T('Left out', 'for most of a century')],
  ['h5', 'This is the story of how Greenwood was built, how it was destroyed, and how it was forgotten.', P('smoke', { zoom: [1.0, 1.1] })],

  // ---- chapter 1: Greenwood
  ['g0', 'Chapter one. Greenwood.', CH(1, 'Greenwood'), null, { section: 'greenwood', captions: false }],
  ['g1', 'In the early 1900s, oil was found near Tulsa, and the town became a boom town.', C('oilwell', 'Shooting an oil well near Tulsa, about 1910', { crop: [0, 0.06, 1, 0.92] })],
  ['g2', 'Money poured in, and the city grew fast.', P('main1910', { motion: 'panLeft', zoom: [1.0, 1.04] }), { stamp: 'Tulsa, about 1910' }],
  ['g3', 'But Tulsa was a segregated city. Black residents were shut out of the white part of town.', P('boston1910', { motion: 'panRight', zoom: [1.0, 1.04] })],
  ['g4', 'So they built their own, north of the Frisco railroad tracks.', T('North of the tracks', 'the Frisco railroad line')],
  ['g5', 'Black landowners such as O. W. Gurley and J. B. Stradford bought land there, and sold lots to other Black families.', T('O. W. Gurley · J. B. Stradford', 'landowners and builders')],
  ['g6', 'Stradford built a modern brick hotel on Greenwood Avenue.', T('The Stradford Hotel', 'Greenwood Avenue')],
  ['g7', 'By 1921, about ten thousand Black people lived in Greenwood.', S(10000, 'people lived in Greenwood', 'panorama', { prefix: 'about ' })],
  ['g8', 'It had two newspapers, a public library branch, churches, and scores of businesses.', T('Two newspapers', 'a library branch · churches · scores of businesses')],
  ['g9', 'Grocers and barbers, tailors and cafés, doctors and lawyers. And a movie theater, the Dreamland.', T('The Dreamland', 'a theater on Greenwood Avenue')],
  ['g10', 'Booker T. Washington is said to have called it the Negro Wall Street.', Q('Negro Wall Street', 'a name attributed to Booker T. Washington')],
  ['g11', 'Most of its people were working people. Many worked in white homes and businesses across the tracks, and came home to Greenwood.', P('panorama', { motion: 'panLeft', zoom: [1.0, 1.05] })],
  ['g12', 'But what they built there was their own.', T('Their own', 'built by Black Tulsans')],

  // ---- chapter 2: the spark
  ['s0', 'Chapter two. The spark.', CH(2, 'The Spark'), null, { section: 'spark', captions: false }],
  ['s1', 'On Monday, May the thirtieth, 1921, a nineteen-year-old Black shoe shiner named Dick Rowland stepped into an elevator in the Drexel Building, downtown.', T('May 30, 1921', 'the Drexel Building, downtown Tulsa'), { lowerThird: { name: 'Dick Rowland', sub: 'shoe shiner, 19' } }],
  ['s2', 'The elevator operator was a seventeen-year-old white woman named Sarah Page.', P('main1910', { focus: [0.62, 0.5], zoom: [1.0, 1.06] })],
  ['s3', 'Something happened in that elevator. Most likely, he stepped on her foot, or stumbled. She cried out, and he ran.', T('Most likely', 'he stepped on her foot')],
  ['s4', 'The next morning, Rowland was arrested.', T('May 31', 'Rowland is arrested')],
  ['s5', 'That afternoon, the Tulsa Tribune ran a story on its front page. Nab Negro for Attacking Girl In an Elevator.', Q('Nab Negro for Attacking Girl In an Elevator', 'Tulsa Tribune, front page, May 31, 1921')],
  ['s6', 'Some people also remembered an editorial in the same paper, headlined To Lynch Negro Tonight.', Q('To Lynch Negro Tonight', 'an editorial, as some remembered it')],
  ['s7', 'No copy of it has ever been found. The page is missing from the archived copies of the paper.', T('Missing', 'cut from the archived copies')],
  ['s8', 'Either way, word spread fast.', P('boston1910', { focus: [0.5, 0.5], zoom: [1.0, 1.06] })],

  // ---- chapter 3: the night
  ['n0', 'Chapter three. The night.', CH(3, 'The Night'), null, { section: 'night', captions: false }],
  ['n1', 'By the evening, hundreds of white people had gathered outside the courthouse, where Rowland was held.', T('The courthouse', 'hundreds gather'), { stamp: '7:30 PM' }],
  ['n2', 'The sheriff refused to hand him over.', T('Refused', 'the sheriff')],
  ['n3', 'In Greenwood, people feared a lynching. Around nine, about twenty-five armed Black men, many of them veterans of the First World War, went to the courthouse to offer help.', T('About 25 men', 'many of them war veterans'), { stamp: '9:00 PM' }],
  ['n4', 'They were told they were not needed, and they went home.', P('smolder', { zoom: [1.0, 1.06] })],
  ['n5', 'Around ten, about seventy-five came back. By then, the white crowd had grown to about fifteen hundred.', S(1500, 'in the white crowd, against about 75', null, { prefix: 'about ' }), { stamp: '10:00 PM' }],
  ['n6', 'A white man tried to take a pistol from a Black veteran. A shot went off.', T('A shot', 'outside the courthouse')],
  ['n7', 'Then the shooting began.', P('smoke', { focus: [0.5, 0.35], zoom: [1.1, 1.2] })],
  ['n8', 'Outnumbered, the Black men fell back toward Greenwood. Fighting spread along the Frisco tracks.', T('The Frisco tracks', 'the line between two Tulsas')],
  ['n9', 'The police deputized white men from the crowd.', T('Deputized', 'white men from the crowd')],
  ['n10', 'By midnight, the first fires were burning at the edge of Greenwood.', P('smolder', { focus: [0.6, 0.3], zoom: [1.05, 1.15] }), { stamp: 'MIDNIGHT' }],

  // ---- chapter 4: the morning
  ['m0', 'Chapter four. The morning.', CH(4, 'The Morning'), null, { section: 'morning', captions: false }],
  ['m1', 'Through the night, thousands of armed white men gathered along the edge of Greenwood.', P('inflames', { focus: [0.5, 0.6], zoom: [1.05, 1.15] })],
  ['m2', 'At about five in the morning, a whistle sounded.', T('A whistle', 'at dawn'), { stamp: '5:00 AM' }],
  ['m3', 'And they crossed the tracks.', P('fire', { focus: [0.5, 0.35], zoom: [1.1, 1.22] })],
  ['m4', 'They went from house to house. They looted homes, and then they set them on fire.', C('furniture', `Belongings in the street, Greenwood, 1921 (${LOC})`)],
  ['m5', 'Black Tulsans fought back, from houses and from churches. But they were badly outnumbered.', P('smoke', { motion: 'panLeft', zoom: [1.05, 1.1] })],
  ['m6', 'From a grain elevator, at least one machine gun fired into the district.', T('A machine gun', 'from a grain elevator')],
  ['m7', 'Airplanes circled overhead. A Black lawyer named Buck Colbert Franklin wrote what he saw.', T('Buck Colbert Franklin', 'lawyer, eyewitness')],
  ['m8', 'I could see planes circling in mid-air. They grew in number and hummed, darted and dipped low.', Q('I could see planes circling in mid-air. They grew in number and hummed, darted and dipped low.', 'B. C. Franklin, eyewitness account, 1931')],
  ['m9', 'Historians still debate exactly what those planes did.', P('inflames', { focus: [0.5, 0.3], zoom: [1.1, 1.2] })],
  ['m10', 'Doctor A. C. Jackson was one of the best-known surgeons in Greenwood.', T('Dr. A. C. Jackson', 'surgeon')],
  ['m11', 'When the mob came to his home, he walked out with his hands up. He was shot, and he died of his wounds.', P('houses', { zoom: [1.0, 1.08] })],
  ['m12', 'Mount Zion Baptist Church had opened just weeks earlier. It burned.', C('church', `A church burns in Greenwood, June 1, 1921 (${LOC})`, { crop: [0, 0.08, 1, 0.82] })],
  ['m13', 'National Guard troops from Oklahoma City arrived around nine. By then, most of Greenwood was already burning.', C('truck_litan', `Soldiers and Black Tulsans on a truck downtown, 1921 (${LOC})`), { stamp: '9:15 AM' }],
  ['m14', 'Black residents were rounded up and taken away under guard.', C('truck', `A truck carrying Black Tulsans, 1921 (${LOC})`)],
  ['m15', 'At 11:49 that morning, the governor declared martial law.', T('Martial law', 'declared at 11:49 AM')],

  // ---- chapter 5: the ashes
  ['a0', 'Chapter five. The ashes.', CH(5, 'The Ashes'), null, { section: 'ashes', captions: false }],
  ['a1', 'When it was over, the heart of Greenwood was gone.', P('ruins', { motion: 'panRight', zoom: [1.0, 1.06] })],
  ['a2', 'Thirty-five city blocks had burned.', S(35, 'city blocks burned', 'district')],
  ['a3', 'One thousand two hundred fifty-six homes were burned. Two hundred fifteen more were looted.', S(1256, 'homes burned', 'houses')],
  ['a4', 'About ten thousand people were left homeless.', S(10000, 'people left homeless', 'ruins', { prefix: 'about ' })],
  ['a5', 'Newspapers across the country carried the story. Tulsa dead total eighty-five, said the Boston Daily Globe.', C('globe', 'Boston Daily Globe, June 2, 1921', { crop: [0, 0.02, 1, 0.5], mark: [0.04, 0.165, 0.92, 0.235] })],
  ['a6', 'The official count was later put at thirty-six. Historians believe the real number was far higher, perhaps as many as three hundred.', T('36 to 300', 'official count · historians\' estimates')],
  ['a7', 'Up to six thousand Black Tulsans were held under armed guard, at Convention Hall, the fairgrounds, and a baseball park.', S(6000, 'held under armed guard', 'camp', { prefix: 'up to ' })],
  ['a8', 'To leave, they had to carry identification cards.', C('camp', `Entrance to the camp at the fairgrounds, 1921 (${LOC})`)],
  ['a9', 'Thousands spent the winter in tents.', C('tents', `A tent home in Greenwood, 1921 (${LOC})`)],
  ['a10', 'Residents filed claims worth more than one point eight million dollars. The claims were turned down.', S(1800000, 'in claims, turned down', 'after', { prefix: '$' })],
  ['a11', 'The city passed a new fire ordinance that would have kept many from rebuilding.', C('shacks', `Rebuilding in Greenwood, 1921 (${LOC})`)],
  ['a12', 'Buck Colbert Franklin and other Black lawyers challenged it in court, working out of a tent. They won.', T('They won', 'the ordinance is struck down')],
  ['a13', 'A grand jury blamed the violence on Black Tulsans. No white person was ever sent to prison for it.', T('No one', 'was sent to prison')],
  ['a14', 'And Dick Rowland? The charges against him were dropped.', T('Dick Rowland', 'charges dropped')],

  // ---- chapter 6: the silence
  ['x0', 'Chapter six. The silence.', CH(6, 'The Silence'), null, { section: 'silence', captions: false }],
  ['x1', 'Greenwood rebuilt, house by house, with little help from the city.', C('rebuild', `Rebuilding Greenwood, 1921 (${LOC})`)],
  ['x2', 'But the massacre itself was left out of the history books. For decades, it was barely taught, even in Tulsa.', T('Silence', 'for decades')],
  ['x3', 'In 1997, Oklahoma created a commission to investigate. Its report, in 2001, recommended reparations.', T('2001', 'the Oklahoma Commission report')],
  ['x4', 'In 2020, researchers began searching Oaklawn Cemetery for the graves of victims.', C('oaklawn', 'Oaklawn Cemetery, Tulsa, 2020 (Carol M. Highsmith, Library of Congress)')],
  ['x5', 'In January 2025, the U.S. Justice Department called it a coordinated, military-style attack on Greenwood.', Q('A coordinated, military-style attack on Greenwood.', 'U.S. Department of Justice, January 2025')],
  ['x6', 'It also found that no one responsible was still alive to prosecute.', P('ruins', { focus: [0.5, 0.6], zoom: [1.05, 1.12] })],

  // ---- close
  ['c1', 'Greenwood was built by people who had been shut out, and who made something of their own.', P('panorama', { motion: 'panLeft', zoom: [1.0, 1.05] }), { section: 'close' }],
  ['c2', 'In one night and one morning, it was burned to the ground.', P('inflames', { zoom: [1.0, 1.08] })],
  ['c3', 'Then the story was buried, for most of a century.', P('after', { zoom: [1.0, 1.08] })],
  ['c4', 'That was Black Wall Street. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-ellen-craft.json', 'utf8'));
const sources = {
  OHS: 'https://www.okhistory.org/publications/enc/entry?entry=TU013',
  OHSG: 'https://www.okhistory.org/publications/enc/entry?entry=GR024',
  REPORT: 'https://www.okhistory.org/research/forms/freport.pdf',
  HIST: 'https://www.history.com/articles/tulsa-race-massacre',
  WIKI: 'https://en.wikipedia.org/wiki/Tulsa_race_massacre',
  WIKIG: 'https://en.wikipedia.org/wiki/Greenwood_District,_Tulsa',
  SMITH: 'https://www.smithsonianmag.com/smithsonian-institution/unseen-written-account-offers-eyewitness-perspective-tulsa-race-massacre-1921-180959192/',
  DOJ: 'https://www.justice.gov/crt/media/1384116/dl',
  AXIOS: 'https://www.axios.com/2025/01/10/tulsa-race-massacre-justice-department-report',
  GLOBE: 'https://commons.wikimedia.org/wiki/File:Boston_Daily_Globe_June_2,_1921.jpg',
  LOCOAK: 'https://www.loc.gov/item/2020743572/',
};
const sourcesByClaim = {
  h1: ['OHS', 'WIKI', 'HIST'], h2: ['OHS', 'HIST'], h3: ['WIKIG', 'WIKI', 'HIST'], h4: ['WIKI', 'HIST'],
  g1: ['REPORT', 'WIKI'], g3: ['OHSG', 'WIKIG'], g4: ['OHS', 'WIKIG'], g5: ['REPORT', 'WIKIG'], g6: ['REPORT', 'WIKIG'],
  g7: ['OHS', 'HIST', 'REPORT'], g8: ['OHS', 'REPORT'], g9: ['REPORT', 'WIKIG'], g10: ['WIKIG', 'HIST'], g11: ['REPORT', 'WIKIG'],
  s1: ['OHS', 'WIKI', 'HIST'], s2: ['WIKI', 'HIST'], s3: ['OHS', 'HIST'], s4: ['OHS', 'WIKI'], s5: ['WIKI', 'HIST'], s6: ['OHS', 'WIKI'], s7: ['OHS', 'WIKI'],
  n1: ['OHS', 'HIST'], n2: ['OHS', 'HIST'], n3: ['OHS', 'HIST'], n4: ['OHS', 'HIST'], n5: ['OHS', 'HIST', 'WIKI'], n6: ['OHS', 'WIKI'], n8: ['OHS', 'REPORT'], n9: ['OHS', 'SMITH', 'DOJ'], n10: ['OHS', 'WIKI'],
  m1: ['OHS', 'WIKI'], m2: ['REPORT', 'WIKI'], m4: ['OHS', 'HIST'], m5: ['OHS', 'REPORT'], m6: ['OHS', 'REPORT'], m7: ['SMITH', 'WIKI'], m8: ['SMITH', 'WIKI'], m9: ['WIKI', 'REPORT'],
  m10: ['OHS', 'REPORT'], m11: ['OHS', 'REPORT'], m12: ['REPORT', 'WIKI'], m13: ['OHS', 'WIKI'], m14: ['WIKI', 'HIST'], m15: ['WIKI', 'GLOBE'],
  a2: ['OHSG', 'HIST', 'WIKI', 'SMITH'], a3: ['REPORT', 'HIST', 'WIKI'], a4: ['REPORT', 'WIKI'], a5: ['GLOBE'], a6: ['HIST', 'WIKI', 'REPORT'],
  a7: ['REPORT', 'WIKI', 'HIST'], a8: ['REPORT', 'WIKI'], a9: ['OHS', 'REPORT'], a10: ['REPORT', 'WIKI'], a11: ['REPORT', 'WIKI'], a12: ['SMITH', 'WIKI', 'REPORT'], a13: ['OHS', 'REPORT', 'WIKI'], a14: ['HIST', 'OHS'],
  x1: ['OHS', 'OHSG', 'SMITH'], x2: ['WIKI', 'HIST'], x3: ['OHS', 'WIKI', 'HIST'], x4: ['WIKI', 'LOCOAK'], x5: ['DOJ', 'WIKI', 'AXIOS'], x6: ['DOJ', 'AXIOS'],
};

const spec = {
  id: 'doc-black-wall-street',
  title: 'The Destruction of Black Wall Street',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { Gurley: 'Gurlee', Stradford: 'Stradferd', Drexel: 'Drexel', Oaklawn: 'Oak-lawn' },
  music: base.music,
  mix: base.mix,
  brand: { page: 'The Black History Room', cta: 'Subscribe', ctaLine: '', theme: 'bhr' },
  assets: {},
  keywords: ['Greenwood', 'Tulsa', 'Black Wall Street', 'Wall Street', 'Rowland', 'Stradford', 'Gurley', 'Dreamland', 'Jackson', 'Franklin', 'Mount Zion',
    '1921', 'thirty-five', 'ten thousand', 'six thousand', 'fifteen hundred', 'eighty-five', 'thirty-six', 'three hundred', 'martial law', 'whistle', 'machine gun',
    'reparations', 'Oaklawn', 'military-style', 'Justice Department'],
  chapters: { greenwood: 'Greenwood', spark: 'The Spark', night: 'The Night', morning: 'The Morning', ashes: 'The Ashes', silence: 'The Silence' },
  grain: true,
  beats: beats.map(([id, text, visual, overlays, extra]) => {
    const { section, ...ov } = overlays || {};
    const v = Object.fromEntries(Object.entries(visual).filter(([, x]) => x !== null && x !== undefined));
    return { id, text, visual: v, ...(Object.keys(ov).length ? { overlays: ov } : {}), ...(section ? { section } : {}), ...(extra || {}) };
  }),
  sourcesByClaim,
  sources: Object.fromEntries(Object.entries(sources).map(([k, url]) => [k, { url }])),
  notUsed: [
    'Photos of the dead (several LOC and Commons images): not used.',
    'Tulsa population in 1921 (sources differ, about 72,000 to 100,000): not used.',
    '"Largest Black-owned hotel in the country" for the Stradford: not confirmed by two sources; script says "a modern brick hotel".',
    'Dreamland seating (750, Report only): not used.',
    'Gurley buying 40 acres "only to Black buyers" (Report notes it may be apocryphal): script says he bought land and sold lots to Black families.',
    'Turpentine bombs dropped from planes: disputed (Report, Wikipedia); script says historians still debate what the planes did.',
    'The "To Lynch Negro Tonight" editorial: no copy survives; told as "some people remembered".',
    'Green cards / white employer vouching for release (Report only): script says identification cards.',
    'Church photo: LOC caption calls it a church "where ammunition was stored" (a 1921 claim); not identified as Mount Zion on screen, captioned "a church burns".',
    'Hours: 7:30 PM, 9 PM, 10 PM, 5 AM, 9:15 AM are approximate (OHS, Report); martial law 11:49 AM (Wikipedia, Globe subhead).',
  ],
};
fs.writeFileSync('data/doc-black-wall-street.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters`);
const missing = beats.filter((b) => !sourcesByClaim[b[0]] && !['chapter', 'endcard'].includes(b[2].kind)).map((b) => b[0]);
console.log('no sources:', missing.join(' '));
