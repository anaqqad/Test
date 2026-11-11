// Builds data/doc-cathay-williams.json: 8-minute long-form documentary (16:9) on Cathay Williams, the only known woman Buffalo Soldier.
// Free local voice (Kokoro). Every fact has two or more sources (sourcesByClaim). No known photograph of her: photos are of
// her regiment's successors, the places she served and her own Army and pension papers, each captioned.
// Ending follows the owner's rule: only "subscribe for more". Run: node data/build_doc_cathay_williams.mjs
import fs from 'node:fs';

const assets = {
  buffA: 'File:Buffalo soldier, 25th Infantry, Co. A) - Goff LCCN2010645138.jpg',
  keogh: 'File:Buffalo soldiers of the 25th Infantry, some wearing buffalo robes, Ft. Keogh, Montana) - Chr. Barthelmess, photographer, Fort Keogh, Montana LCCN98501226.jpg',
  buff1890: 'File:Buffalo soldiers1.jpg',
  buffcuster: 'File:Buffalo Soldier, 25th Infantry, Co.) - Goff, photographer, Fort Cust(e)r, Mont LCCN2010645137.tif',
  discharge: "File:Cathay Williams' disability discharge document.png",
  pension1: 'File:Cathay Williams Pension 001.jpg',
  pension2: 'File:Cathay Williams Pension 002.jpg',
  pension3: 'File:Cathay Williams Pension 003.jpg',
  furuins: 'File:Fort Union National Monument archaeological ruins (a2df49b4174f49c4971f3c1b0f3a4428).JPG',
  fuview: 'File:Views of Fort Union National Monument, New Mexico (06febbf5-50ad-4dab-ae61-b3024469fceb).jpg',
  swales: 'File:View of swales near Fort Union National Monument (498c1cc0a9b94254a4a7afc6f385d8fd).JPG',
  map1867: 'File:Map northern new mexico 1867.jpg',
  sheridan: 'File:Philip Sheridan - Brady-Handy.jpg',
  jcity: 'File:"Breastworks Thrown up for the Defense of Jefferson City, Missouri.".jpg',
  jb: 'File:(Jefferson Barracks. St. Louis, Mo.) - (Two long brick build... (3110019799).jpg',
  riley: 'File:View on Kansas River, at Fort Riley, Kansas, 420 miles west of St. Louis, Mo, by Gardner, Alexander, 1821-1882.jpg',
  cummings: 'File:Near Fort Cummings - Flickr - aspidoscelis (3).jpg',
  cummings2: 'File:West-northwest of Fort Cummings - Flickr - aspidoscelis.jpg',
  recruit: 'File:Come and Join Us Brothers, by the Supervisory Committee For Recruiting Colored Regiments.jpg',
  mccook: 'File:Camp of General Alexander McDowell McCook near Stevenson, Alabama, summer 1862 LCCN2017647000.jpg',
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });

const CW = 'Cathay Williams, 1876';
const B25 = 'Buffalo Soldiers of the 25th Infantry, 1880s';
const beats = [
  // ---- cold open
  ['h1', 'In November 1866, a new recruit signed up at an Army recruiting office in St. Louis, Missouri. Three years, in the regular Army.', P('discharge', { focus: [0.4, 0.3], zoom: [1.3, 1.45] }), { hook: 'A Buffalo Soldier with a secret.' }],
  ['h2', 'The name on the papers was William Cathay. The medical exam was only a quick look.', T('William Cathay', 'Private, 1866')],
  ['h3', 'William Cathay was a woman. Her real name was Cathay Williams.', T('Cathay Williams', 'about 1844 to the 1890s')],
  ['h4', 'For almost two years, she served in one of the Army\'s new Black regiments, the soldiers who became known as the Buffalo Soldiers.', C('keogh', 'Buffalo Soldiers of the 25th Infantry, Fort Keogh, Montana')],
  ['h5', 'She is the only woman known to have served as one.', T('The only one', 'known woman Buffalo Soldier')],
  ['h6', 'And when she was old and sick, and asked her country for a pension, it said no.', C('pension2', 'Her pension file, National Archives', { focus: [0.5, 0.3] })],
  ['h7', 'This is her story.', P('keogh', { focus: [0.5, 0.45], zoom: [1.05, 1.12] })],

  // ---- early life
  ['e1', 'She was born in Independence, Missouri, in the 1840s. Her father was a free man. Her mother was enslaved, and so, under the law, was she.', T('Independence, Missouri', 'born in the 1840s'), { section: 'early' }],
  ['e2', 'As a girl, she worked as a house slave on a plantation outside Jefferson City, the state capital.', C('jcity', 'Jefferson City, Missouri, 1861')],
  ['e3', 'In 1861, the Civil War came to Missouri. Union troops occupied Jefferson City.', P('jcity', { focus: [0.5, 0.45], zoom: [1.1, 1.2] }), { stamp: '1861' }],
  ['e4', 'The Union army called the enslaved people it took in contraband of war. Many of them went to work for it, as cooks, laundresses and nurses.', C('mccook', 'A Union army camp, Alabama, 1862')],
  ['e5', 'Cathay Williams was about seventeen. She went to work for the Union army, cooking and washing for the soldiers.', P('mccook', { focus: [0.45, 0.55], zoom: [1.15, 1.25] })],
  ['e6', 'She had to learn to cook on the job, first for officers.', T('Army cook', 'at about seventeen')],
  ['e7', 'She followed the troops for the rest of the war. In time she worked for the staff of General Philip Sheridan, one of the Union\'s best-known commanders.', C('sheridan', 'Gen. Philip Sheridan'), { lowerThird: { name: 'Gen. Philip Sheridan', sub: 'Union Army' } }],
  ['e8', 'She spent years around soldiers. She saw how they lived, how they marched, and how they were paid.', P('sheridan', { focus: [0.5, 0.3], zoom: [1.1, 1.2] })],

  // ---- enlisting
  ['n1', 'The war ended in 1865. She was free. She was also poor, and on her own.', T('1865', 'free, and on her own'), { section: 'enlist' }],
  ['n2', 'After the war she went to St. Louis, and could not find steady work.', T('St. Louis', 'looking for work')],
  ['n3', 'Years later, she told a newspaper why she did what she did next.', C('recruit', 'Black Union soldiers, recruiting poster, 1865')],
  ['n4', 'I wanted to make my own living, she said, and not be dependent on relations or friends.', Q('I wanted to make my own living and not be dependent on relations or friends.', CW)],
  ['n5', 'In July 1866, Congress set the size of the peacetime Army. It created six regiments of Black soldiers. Two of cavalry, the ninth and tenth. And four of infantry, the thirty-eighth through the forty-first.', T('July 1866', 'six Black regiments')],
  ['n5b', 'The new regiments would be sent west, to forts on the frontier.', C('buffcuster', 'A Buffalo Soldier of the 25th Infantry, Montana, 1880s')],
  ['n6', 'Women could not enlist. So on November 15, 1866, in St. Louis, she enlisted as a man, William Cathay.', T('15 November 1866', 'St. Louis, Missouri')],
  ['n7', 'She signed up for three years, and was assigned to the thirty-eighth United States Infantry, Company A.', C('buffA', 'A Buffalo Soldier of the 25th Infantry, Company A, 1880s')],
  ['n7b', 'The recruiter wrote down her height, five feet nine inches, and her trade. Cook.', P('discharge', { focus: [0.5, 0.4], zoom: [1.25, 1.4] })],
  ['n8', 'Only two people in the regiment knew her secret. In her words, a cousin and a particular friend.', Q('Two persons, a cousin and a particular friend, members of the regiment, knew that I was a woman.', CW)],

  // ---- west
  ['w1', 'Soon after she enlisted, she caught smallpox, and went into the hospital.', T('Smallpox', 'weeks after enlisting'), { section: 'west' }],
  ['w2', 'Her company went on without her, to Fort Riley, Kansas. She caught up with it later.', C('riley', 'Fort Riley, Kansas, 1867'), { pin: { label: 'Fort Riley', sub: 'Kansas' } }],
  ['w3', 'In the summer of 1867, Company A marched more than five hundred miles, from Kansas to Fort Union, in New Mexico Territory.', C('swales', 'Santa Fe Trail ruts near Fort Union, New Mexico, today'), { pin: { label: 'Fort Union', sub: 'New Mexico Territory' } }],
  ['w4', 'Fort Union guarded the Santa Fe Trail. Its walls still stand in ruins today.', C('furuins', 'Fort Union National Monument, New Mexico')],
  ['w5', 'From there, the company marched hundreds of miles more, south, to Fort Cummings.', C('map1867', 'New Mexico Territory, 1867')],
  ['w6', 'Fort Cummings sat in dry desert country in the southwest of the territory. Company A stayed about eight months.', C('cummings2', 'The desert near Fort Cummings, New Mexico'), { pin: { label: 'Fort Cummings', sub: 'New Mexico' } }],
  ['w7', 'Across the West, the Buffalo Soldiers built roads, guarded posts and escorted the mail.', C('keogh', 'Buffalo Soldiers of the 25th Infantry, Fort Keogh, Montana')],
  ['w8', 'Private Cathay was sick often. Army records place her in four different hospitals, on five separate occasions.', T('5 hospital stays', 'in 4 hospitals')],
  ['w9', 'Each time, she was not found out.', P('cummings', { zoom: [1.0, 1.08] })],
  ['w9b', 'Think about what that took. Every day, in a barracks full of men, on long marches and in sick wards, she kept her secret.', P('cummings2', { zoom: [1.0, 1.08] })],

  // ---- discovery
  ['d1', 'In June 1868, Company A marched to Fort Bayard, near Silver City, New Mexico.', P('cummings2', { focus: [0.5, 0.3], zoom: [1.05, 1.15] }), { section: 'found', pin: { label: 'Fort Bayard', sub: 'New Mexico' } }],
  ['d2', 'Almost at once, she was in the post hospital again.', T('Fort Bayard', 'the post hospital, 1868')],
  ['d3', 'This time, the post surgeon discovered that Private William Cathay was a woman.', T('Found out', '1868')],
  ['d3b', 'Almost two years of hiding were over.', P('discharge', { focus: [0.5, 0.15], zoom: [1.1, 1.2] })],
  ['d4', 'On October 14, 1868, she was discharged at Fort Bayard, with a certificate of disability.', C('discharge', 'Discharge of "William Cathey," 14 October 1868', { focus: [0.5, 0.35] }), { stamp: '14 October 1868' }],
  ['d5', 'The paper never said she was a woman. It still called her he.', P('discharge', { focus: [0.5, 0.25], zoom: [1.2, 1.35] })],
  ['d6', 'It said the soldier was of feeble habit, and often unfit for duty, and that the condition went back to before enlisting.', P('discharge', { focus: [0.5, 0.6], zoom: [1.2, 1.35] })],
  ['d7', 'Her captain, Charles Clarke, signed it.', C('discharge', 'Signed by Capt. Charles E. Clarke, 38th Infantry')],
  ['d8', 'She later said the men turned on her once they knew.', Q('The men all wanted to get rid of me after they found out I was a woman.', CW)],
  ['d9', 'She had served in the Army for almost two years.', T('Almost two years', 'November 1866 to October 1868')],

  // ---- after
  ['a1', 'She did not go home. In 1869 and 1870, she worked back at Fort Union, as a cook for a colonel.', C('fuview', 'Fort Union National Monument, New Mexico, today'), { section: 'after' }],
  ['a2', 'Then she moved to Pueblo, Colorado, and married.', T('Pueblo, Colorado', 'a marriage')],
  ['a3', 'It did not last. Her husband stole her money and a team of horses. She had him arrested.', T('She had him arrested', '')],
  ['a4', 'She settled in Trinidad, Colorado, and made a living as a laundress and a seamstress.', T('Trinidad, Colorado', 'laundress and seamstress')],
  ['a5', 'Years later, a reporter from St. Louis heard rumors about a woman who had served as a soldier, and came to interview her.', T('A reporter', 'from St. Louis')],
  ['a6', 'On January 2, 1876, the St. Louis Daily Times printed her story.', T('St. Louis Daily Times', '2 January 1876')],
  ['a7', 'Why did she leave the Army? Her answer was plain. I got tired, and wanted to get off.', Q('I got tired and wanted to get off.', CW)],

  // ---- pension
  ['p1', 'By 1890, her health was failing. She went into the hospital and stayed a long time, by one account nearly a year and a half. She came out with no money.', T('1890', 'sick, and out of money'), { section: 'pension' }],
  ['p2', 'In June 1891, she applied for an Army pension, as a disabled veteran.', C('pension1', 'Cathay Williams\'s pension application, 1891', { focus: [0.5, 0.25] }), { stamp: 'June 1891' }],
  ['p3', 'There was a precedent. Deborah Sampson had disguised herself as a man to fight in the Revolution, and the government had given her a pension.', T('Deborah Sampson', 'a pension for a woman soldier')],
  ['p4', 'A Pension Bureau doctor came to examine her. He found that her toes had been amputated. She could walk only with a crutch.', C('pension2', 'Her pension file, National Archives', { focus: [0.5, 0.35] })],
  ['p5', 'He ruled that she was not eligible. Her claim was rejected.', C('pension3', '"Rejected": her pension file', { focus: [0.5, 0.3] })],
  ['p6', 'After that, she disappears from the record. No one knows when she died, or where she is buried.', P('swales', { zoom: [1.0, 1.08] })],

  // ---- memory
  ['m1', 'For more than a century, her story sat mostly in Army files and pension papers at the National Archives.', P('pension3', { focus: [0.5, 0.4], zoom: [1.1, 1.2] }), { section: 'memory' }],
  ['m2', 'In 1869, her old regiment, the thirty-eighth, was merged into the twenty-fifth Infantry, one of the Buffalo Soldier regiments that served on the frontier for decades.', C('buff1890', 'The 25th Infantry, about 1890')],
  ['m3', 'In 2016, a bronze bust of her was unveiled in Leavenworth, Kansas, beside a rose garden.', T('Leavenworth, Kansas', 'a bronze bust, 2016')],
  ['m4', 'The National Infantry Museum in Columbus, Georgia, added a bench in her honor on its Walk of Honor.', T('Walk of Honor', 'National Infantry Museum, Georgia')],
  ['m5', 'And today the National Park Service calls her the only known woman Buffalo Soldier.', C('discharge', 'Discharge of "William Cathey," 14 October 1868')],

  // ---- close
  ['c1', 'She was born enslaved. She cooked and washed for one army through a war.', C('mccook', 'A Union army camp, 1862'), { section: 'close' }],
  ['c2', 'Then she joined another, under a man\'s name, because she wanted to make her own living.', P('buff1890', { focus: [0.5, 0.5], zoom: [1.05, 1.15] })],
  ['c3', 'She marched across the West, through sickness, and kept going.', P('furuins', { zoom: [1.0, 1.08] })],
  ['c3b', 'And when it was over, she did not hide it. She told her story to a newspaper, in her own words.', Q('I wanted to make my own living.', CW)],
  ['c4', 'On Veterans Day, remember her. Private Cathay Williams, thirty-eighth United States Infantry.', P('keogh', { focus: [0.5, 0.5], zoom: [1.05, 1.15] })],
  ['c5', 'That was Cathay Williams. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-ellen-craft.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Cathay_Williams',
  NPS: 'https://www.nps.gov/people/cwilliams.htm',
  FOUN: 'https://www.nps.gov/foun/learn/historyculture/william-cathay.htm',
  LOA: 'https://www.legendsofamerica.com/cathay-williams/',
  HN: 'https://historynet.com/buffalo-soldier-secret-life-must-hard-conceal/',
  MT: 'https://www.militarytimes.com/military-honor/black-military-history/2018/02/07/this-ex-slave-pretended-to-be-a-man-and-served-in-the-army/',
  KC: 'https://kcblackhistory.org/articles/cathay-williams',
  LKS: 'https://www.leavenworthks.gov/visitors/page/cathay-williams',
  BSW: 'https://en.wikipedia.org/wiki/Buffalo_Soldier',
  STAT: 'https://memory.loc.gov/cgi-bin/ampage?collId=llsl&fileName=014/llsl014.db&recNum=371',
  MIL: 'https://www.military.com/history/cathay-williams-was-armys-only-female-buffalo-soldier-and-first-black-female-enlistee.html',
  BH: 'https://theblackherald.substack.com/p/pvt-cathay-williams',
};
const sourcesByClaim = {
  h1: ['WIKI', 'NPS', 'HN'], h2: ['WIKI', 'NPS', 'LOA'], h3: ['WIKI', 'NPS'], h4: ['WIKI', 'KC', 'FOUN'], h5: ['NPS', 'KC', 'LKS'], h6: ['WIKI', 'LOA', 'KC'],
  e1: ['WIKI', 'NPS', 'MT'], e2: ['WIKI', 'NPS', 'KC'], e3: ['WIKI', 'NPS', 'KC'], e4: ['WIKI', 'NPS'], e5: ['WIKI', 'NPS', 'KC'], e6: ['WIKI', 'NPS'], e7: ['NPS', 'LOA'],
  n1: ['KC', 'LKS'], n2: ['KC', 'LKS'], n3: ['FOUN', 'HN'], n4: ['FOUN', 'HN'], n5: ['BSW', 'STAT'], n6: ['WIKI', 'NPS', 'LKS'], n7: ['WIKI', 'LOA', 'FOUN'], n8: ['MT', 'LOA', 'WIKI'],
  w1: ['WIKI', 'NPS', 'FOUN'], w2: ['FOUN', 'LOA'], w3: ['FOUN', 'HN', 'LOA'], w5: ['FOUN', 'HN'], w6: ['LOA', 'FOUN'], w7: ['BSW', 'FOUN'], w8: ['LOA', 'WIKI'], w9: ['LOA', 'NPS'],
  d1: ['LOA', 'FOUN'], d2: ['FOUN', 'LOA'], d3: ['FOUN', 'HN', 'NPS'], d4: ['NPS', 'LOA', 'HN'], d5: ['FOUN', 'MT'], d6: ['FOUN', 'MT', 'LOA'], d7: ['NPS', 'WIKI'], d8: ['WIKI', 'HN', 'MT'], d9: ['MT', 'WIKI'],
  a1: ['WIKI', 'NPS', 'LOA'], a2: ['WIKI', 'NPS', 'HN'], a3: ['WIKI', 'NPS', 'HN'], a4: ['WIKI', 'NPS', 'LOA'], a5: ['NPS', 'WIKI'], a6: ['WIKI', 'NPS', 'HN'], a7: ['HN', 'MT'],
  p1: ['WIKI', 'LOA'], p2: ['WIKI', 'LOA'], p3: ['WIKI', 'NPS'], p4: ['WIKI', 'NPS'], p5: ['WIKI', 'NPS', 'LOA', 'KC'], p6: ['WIKI', 'HN', 'NPS'],
  m1: ['MT', 'WIKI'], n5b: ['BSW', 'FOUN'], n7b: ['FOUN', 'LOA'], c3b: ['NPS', 'WIKI'], m2: ['BSW', 'WIKI'], m3: ['WIKI', 'BH', 'LKS'], m4: ['WIKI', 'MIL'], m5: ['NPS', 'WIKI'],
};

const spec = {
  id: 'doc-cathay-williams',
  title: 'She Joined the Buffalo Soldiers Disguised as a Man',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { Cathay: 'Kathy', Cathey: 'Kathy', Sheridan: 'Sherridan', Bayard: 'Bye-erd', Leavenworth: 'Leven-worth' },
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
    'No authenticated photograph of Cathay Williams exists (HistoryNet); the painted/circulated portrait is not used. All soldier photos are captioned as other Buffalo Soldiers.',
    'Birth year: 1842 (NPS quick facts, Legends of America) vs 1844 (Wikipedia, NPS text) vs 1850 (BlackPast): script says "in the 1840s".',
    'Height 5 ft 9 (NPS Fort Union, Legends of America) vs 5 ft 7 (HistoryNet): not used.',
    'Pension denial year: 1892 (Wikipedia) vs 1893 (NPS): script gives no year.',
    'Cholera on the march and quarantine at Fort Union (NPS Fort Union only): not used.',
    'Little Rock, Shenandoah, Red River, Pea Ridge, Washington: single sources each, not used.',
    'Good Conduct Medal ("believed", Wikipedia only): not used.',
    'Bench year 2018 (Wikipedia) vs 2015 (Military.com): script gives no year.',
    'Who named the Buffalo Soldiers and why: sources disagree, not used.',
  ],
};
fs.writeFileSync('data/doc-cathay-williams.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images`);
