// Builds data/doc-charles-young.json: 8-minute long-form documentary (16:9) on Colonel Charles Young (1864-1922).
// Free local voice (Kokoro). Every fact has two or more sources (sourcesByClaim).
// Ending follows the owner's rule: only "subscribe for more". Run: node data/build_doc_charles_young.mjs
import fs from 'node:fs';

const assets = {
  young03: 'File:Captain Charles Young 9th Cavalry 1903 hpc-000569.jpg',
  sequoia: 'File:Captain Charles Young, 9th Cavalry, Acting Superintendent of Sequoia National Park (2371cf1606774e7889f5aba6c3a53dac).jpg',
  major16: 'File:Major Charles Young of the 10th Cavalry who will be made Lieutenant Colonel shortly., 1916 - NARA - 523009.tif',
  colonel: 'File:COL. CHARLES YOUNG - WEST POINT GRADUATE, MILITARY ATTACHE TO HAITI, LIBERIA - NARA - 535679.jpg',
  colonel2: 'File:Charles.Young.1919.jpg',
  funeral: 'File:Funeral, Col. Chas. Young, (6-1-23) LOC npcc.08935.jpg',
  young: 'File:Charles Young.jpg',
  house: 'File:Colonel Charles Young House, front.jpg',
  cabin: 'File:The Charles Young birth cabin (4bd75f9b-bec8-4ca1-bc2b-2993fb01331c).jpg',
  broadside: 'File:Men of Color Civil War Recruitment Broadside 1863.png',
  wp: 'File:Cadet\'s Quarters, U. S. Military Academy, West Point New York, N. Y (NYPL b12647398-62364).tiff',
  wphudson: 'File:Cavalry Drill, U. S. Military Academy, West Point, N. Y (NYPL b12647398-73774).tiff',
  buffalo: 'File:Buffalo Soldier, 9th Cavalry, Company D, sharpshooter collar insignia) - C. C. McBride, Crawford, Nebraska LCCN2010645133.jpg',
  ftrob: 'File:Fort Robinson cavalry barracks.jpg',
  father: 'File:Father of the Forest, 400 feet long, Cal, by Littleton View Co..jpg',
  pap: 'File:Port-au-Prince 1907.jpg',
  monrovia: 'File:JONES(1922) Monrovia, Market Street.jpg',
  charge: 'File:Practice charge of the 8th Gun Cavalry during the punitive expedition in Mexico LCCN96503334.jpg',
  baker: 'File:Newton D. Baker, 47th United States Secretary of War.jpg',
  wilson: 'File:Thomas Woodrow Wilson, Harris & Ewing bw photo portrait, 1919.jpg',
  dubois: 'File:WEB DuBois 1918.jpg',
  lagos: 'File:Lagos Railway Station in the 1920s.jpg',
  amph: 'File:Amphitheater at Arlington National Cemetery, Arlington, Virginia 1920 (30689583561).jpg',
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });

const CY = 'Charles Young';
const beats = [
  // ---- cold open
  ['h1', 'In June 1918, a fifty-four-year-old Army officer saddled his horse in Wilberforce, Ohio, and started riding east.', C('colonel2', 'Colonel Charles Young'), { hook: 'He rode 497 miles to prove them wrong.' }],
  ['h2', 'His destination was Washington, D.C., almost five hundred miles away.', T('497 miles', 'Wilberforce, Ohio, to Washington, D.C.')],
  ['h3', 'The Army had just told him he was too sick to lead men into the First World War.', P('colonel2', { focus: [0.5, 0.35], zoom: [1.1, 1.22] })],
  ['h4', 'He was the highest-ranking Black officer in the United States Army. And many believed the real reason he was sidelined had nothing to do with his health.', C('major16', 'Charles Young, 1916'), { lowerThird: { name: 'Charles Young', sub: 'colonel, United States Army' } }],
  ['h5', 'His name was Charles Young. He was born enslaved. This is his story.', P('colonel2', { focus: [0.5, 0.35], zoom: [1.05, 1.15] })],

  // ---- early life
  ['e1', 'Charles Young was born on March 12, 1864, in Mays Lick, Kentucky, to enslaved parents, Gabriel and Arminta Young.', C('cabin', 'The Charles Young birth cabin'), { section: 'early', stamp: '12 March 1864' }],
  ['e2', 'The Civil War was still being fought. Within a year, his father escaped across the Ohio River.', P('cabin', { focus: [0.5, 0.5], zoom: [1.1, 1.2] })],
  ['e3', 'In February 1865, Gabriel Young joined the Union Army, in the Fifth United States Colored Heavy Artillery. His service helped secure the family\'s freedom.', C('broadside', 'A call to men of color to join the Union Army, 1863')],
  ['e4', 'After the war, the family settled across the river, in Ripley, Ohio.', T('Ripley, Ohio', 'on the Ohio River')],
  ['e5', 'His mother could read, and she taught him at home. He went on to study French and German, and he played the piano and the violin.', T('Languages and music', 'Ripley, Ohio')],
  ['e6', 'In 1881, at seventeen, he graduated with honors from Ripley\'s high school, the only Black student in his class.', T('1881', 'honors graduate, age 17')],
  ['e7', 'Then he became a teacher, at the town\'s school for Black children.', T('A teacher', 'Ripley, Ohio')],

  // ---- West Point
  ['w1', 'In 1883, he sat the entrance exam for the United States Military Academy at West Point, and scored second highest.', C('wphudson', 'Cavalry drill, U.S. Military Academy, West Point'), { section: 'westpoint' }],
  ['w2', 'The next year, an Ohio congressman nominated him. In June 1884, he entered West Point.', C('wp', 'Cadets\' quarters, West Point'), { stamp: 'June 1884' }],
  ['w3', 'Very few Black cadets had made it through. White cadets used what was called silencing. They would not speak to Black cadets unless they had to.', T('Silencing', 'West Point, 1880s')],
  ['w4', 'He was given a heavy load of demerits. He failed mathematics in his first year, and had to repeat it.', P('wp', { focus: [0.5, 0.5], zoom: [1.1, 1.22] })],
  ['w5', 'Near the end, he failed an engineering course. He studied all summer, took it again, and passed.', T('One more test', 'and he passed')],
  ['w6', 'In 1889, Charles Young graduated. He was only the third Black graduate in West Point\'s history.', T('1889', 'the third Black graduate of West Point')],
  ['w7', 'The next would not come until 1936.', T('1936', 'forty-seven years later')],

  // ---- Buffalo Soldiers
  ['b1', 'As a second lieutenant, he joined the Ninth Cavalry, one of the Army\'s Black regiments, the men known as Buffalo Soldiers.', C('buffalo', 'A Buffalo Soldier of the Ninth Cavalry, Nebraska'), { section: 'buffalo' }],
  ['b2', 'He served at Fort Robinson, Nebraska, and then at Fort Duchesne, Utah.', C('ftrob', 'Cavalry barracks, Fort Robinson, Nebraska')],
  ['b3', 'In 1894, he went to Wilberforce University in Ohio, a historically Black college, to teach military science.', T('Wilberforce University', 'Ohio, 1894')],
  ['b4', 'There he became close friends with a young professor named W. E. B. Du Bois.', C('dubois', 'W. E. B. Du Bois')],
  ['b5', 'In 1898, during the war with Spain, he was made a major of volunteers and given command of the Ninth Ohio, a Black battalion.', T('Major Young', '9th Ohio, 1898')],
  ['b6', 'The war ended before his men were sent overseas. He went back to the regular Army, and later served in the Philippines.', P('buffalo', { focus: [0.5, 0.4], zoom: [1.1, 1.2] })],

  // ---- Sequoia
  ['q1', 'In the summer of 1903, Captain Young led a company of Buffalo Soldiers into the Sierra Nevada.', C('young03', 'Captain Charles Young, Ninth Cavalry, 1903'), { section: 'sequoia' }],
  ['q2', 'He was made acting superintendent of Sequoia and General Grant national parks. He was the first Black superintendent of a national park.', C('sequoia', 'Captain Charles Young, Acting Superintendent of Sequoia National Park')],
  ['q3', 'His soldiers guarded the giant trees, and built roads and trails.', C('father', 'A fallen giant sequoia, California')],
  ['q4', 'By mid-August, wagons could reach the Giant Forest for the first time.', P('father', { focus: [0.5, 0.5], zoom: [1.1, 1.2] })],
  ['q5', 'He also built a road toward Moro Rock, and urged the government to buy up private land inside the park.', P('sequoia', { focus: [0.5, 0.4], zoom: [1.1, 1.2] })],

  // ---- abroad
  ['a1', 'In 1904, the Army sent him to Haiti, as one of its first military attaches.', C('pap', 'Port-au-Prince, Haiti, 1907'), { section: 'abroad' }],
  ['a2', 'For about three years, he gathered intelligence, and mapped much of Haiti and the neighboring Dominican Republic.', P('pap', { focus: [0.5, 0.5], zoom: [1.1, 1.2] })],
  ['a3', 'In 1912, he was promoted to major, the first Black man to hold that rank in the regular Army.', T('Major', 'August 1912')],
  ['a4', 'That year he went to Liberia, as military attache. He helped train the Liberian Frontier Force, and supervised the building of roads.', C('monrovia', 'Market Street, Monrovia, Liberia')],

  // ---- Mexico
  ['m1', 'In 1916, after Pancho Villa\'s raid on Columbus, New Mexico, the Army sent troops into Mexico to hunt him down.', C('charge', 'U.S. cavalry in Mexico, 1916'), { section: 'mexico' }],
  ['m2', 'Major Young commanded a squadron of the Tenth Cavalry.', C('major16', 'Major Charles Young, Tenth Cavalry, 1916')],
  ['m3', 'On April 1, 1916, at Agua Caliente, he led a cavalry pistol charge against Villa\'s forces.', P('charge', { focus: [0.5, 0.5], zoom: [1.1, 1.22] }), { stamp: '1 April 1916' }],
  ['m4', 'They drove back about a hundred and fifty men. His squadron did not lose a single soldier.', T('No losses', 'Agua Caliente, 1916')],
  ['m5', 'That summer he was promoted to lieutenant colonel. The NAACP awarded him its Spingarn Medal.', P('major16', { focus: [0.5, 0.35], zoom: [1.1, 1.2] })],

  // ---- sidelined
  ['s1', 'In April 1917, the United States entered the First World War.', T('April 1917', 'America goes to war'), { section: 'sidelined' }],
  ['s2', 'Charles Young was the highest-ranking Black officer in the Army. He was in line for promotion, and for command in France.', C('major16', 'Lieutenant Colonel Charles Young')],
  ['s3', 'But some white officers said they would not take orders from a Black man.', T('"Unwilling to take orders"', 'white officers under Young')],
  ['s4', 'President Woodrow Wilson heard from Southern members of Congress. He wrote to his Secretary of War, Newton Baker, about a lieutenant who found it practically impossible to serve under a colored commander.', C('wilson', 'President Woodrow Wilson')],
  ['s5', 'That summer, an Army medical board examined Young. It found high blood pressure.', C('baker', 'Newton D. Baker, Secretary of War')],
  ['s6', 'In July 1917, he was promoted to colonel, and in the same stroke retired, as medically unfit.', T('Colonel', 'and retired, July 1917')],
  ['s7', 'He would not lead troops in the war.', P('major16', { focus: [0.5, 0.35], zoom: [1.1, 1.2] })],

  // ---- the ride
  ['r1', 'So Charles Young decided to prove them wrong.', C('house', 'Colonel Charles Young\'s house, Wilberforce, Ohio'), { section: 'ride' }],
  ['r2', 'On June 6, 1918, he left his home in Wilberforce on horseback.', P('house', { focus: [0.5, 0.5], zoom: [1.05, 1.15] }), { stamp: '6 June 1918' }],
  ['r3', 'He rode through Ohio, West Virginia, Maryland and Virginia.', T('Four states', 'Ohio, West Virginia, Maryland, Virginia')],
  ['r4', 'On June 22, he rode into Washington. He had covered four hundred ninety-seven miles in a little over two weeks.', T('497 miles', 'arrived 22 June 1918')],
  ['r5', 'A Black newspaper, The Crisis, reported that he arrived in first class condition.', Q('Arrived in first class condition.', 'The Crisis, 1918')],
  ['r6', 'He met with Secretary Baker. Baker did not change the decision.', C('baker', 'Newton D. Baker')],
  ['r7', 'On November 6, 1918, the Army called him back to active duty, and sent him to Camp Grant, in Illinois.', T('6 November 1918', 'recalled to duty')],
  ['r8', 'Five days later, the war was over.', T('11 November 1918', 'the Armistice')],

  // ---- Africa
  ['f1', 'In 1920, he returned to Liberia as military attache.', C('monrovia', 'Monrovia, Liberia'), { section: 'africa' }],
  ['f2', 'In late 1921, on a trip to Nigeria, he fell seriously ill.', C('lagos', 'Lagos, Nigeria, 1920s')],
  ['f3', 'On January 8, 1922, Charles Young died at the British hospital in Lagos, of a kidney infection. He was fifty-seven.', T('8 January 1922', 'Lagos, Nigeria')],
  ['f4', 'British law required that he be buried there, for a year.', P('lagos', { focus: [0.5, 0.5], zoom: [1.1, 1.2] })],
  ['f5', 'His wife and many others pressed to bring him home.', T('Bring him home', '')],
  ['f6', 'In May 1923, his body reached New York, where crowds came out to meet it.', C('colonel', 'A newspaper tribute to Colonel Young after his death')],
  ['f7', 'On June 1, 1923, he was given a funeral in the Memorial Amphitheater at Arlington National Cemetery. He was only the fourth soldier to be honored there.', C('funeral', 'Funeral of Colonel Charles Young, Arlington, 1 June 1923'), { stamp: '1 June 1923' }],
  ['f7b', 'He was buried at Arlington with full military honors.', C('amph', 'Memorial Amphitheater, Arlington National Cemetery, 1920')],
  ['f8', 'W. E. B. Du Bois said the life of Charles Young was a triumph of tragedy.', Q('The life of Charles Young was a triumph of tragedy.', 'W. E. B. Du Bois')],

  // ---- legacy
  ['l1', 'In 2013, his home in Wilberforce became a national monument, the Charles Young Buffalo Soldiers National Monument.', C('house', 'The Charles Young Buffalo Soldiers National Monument'), { section: 'legacy' }],
  ['l2', 'And a century after his death, the Army promoted him to brigadier general. The ceremony was held in 2022, at West Point.', T('Brigadier General', '2022')],

  // ---- close
  ['c1', 'He was born enslaved, and became a colonel.', C('cabin', 'The Charles Young birth cabin'), { section: 'close' }],
  ['c2', 'He made it through West Point, guarded the giant sequoias, mapped Haiti, and led a charge in Mexico.', P('sequoia', { focus: [0.5, 0.4], zoom: [1.05, 1.15] })],
  ['c3', 'When the Army said he was too sick to serve, he rode nearly five hundred miles to show them otherwise.', C('colonel2', 'Colonel Charles Young')],
  ['c4', 'That was Charles Young. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-ellen-craft.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Charles_Young_(United_States_Army_officer)',
  NPS: 'https://www.nps.gov/chyo/learn/historyculture/charles-young.htm',
  RIDE: 'https://www.nps.gov/articles/000/-h-our-history-lesson-fit-for-service-colonel-charles-young-s-protest-ride.htm',
  RET: 'https://www.nps.gov/articles/000/chyoretirement.htm',
  NMUSA: 'https://thenmusa.org/?p=18101',
  ARMY: 'https://www.army.mil/article/129675/colonel_charles_young_buffalo_soldier_and_intelligence_officer',
  WILSON: 'https://presidentwilson.org/items/show/15726',
};
const sourcesByClaim = {
  h1: ['RIDE', 'RET'], h2: ['RIDE', 'NMUSA', 'RET'], h3: ['NMUSA', 'RET', 'WIKI'], h4: ['ARMY', 'WIKI', 'RET'], h5: ['NPS', 'WIKI'],
  e1: ['NPS', 'WIKI', 'NMUSA'], e2: ['NPS', 'WIKI'], e3: ['NPS', 'WIKI'], e4: ['NPS', 'WIKI'], e5: ['WIKI', 'NPS'], e6: ['NPS', 'WIKI'], e7: ['NPS', 'WIKI'],
  w1: ['NPS', 'WIKI'], w2: ['NPS', 'WIKI', 'NMUSA'], w3: ['NMUSA', 'WIKI'], w4: ['WIKI', 'NPS'], w5: ['NPS', 'WIKI'], w6: ['NPS', 'WIKI', 'NMUSA', 'ARMY'], w7: ['WIKI', 'NMUSA'],
  b1: ['NPS', 'WIKI'], b2: ['NPS', 'WIKI'], b3: ['NPS', 'WIKI'], b4: ['WIKI', 'NPS'], b5: ['WIKI', 'NPS'], b6: ['WIKI', 'NPS'],
  q1: ['NPS', 'WIKI'], q2: ['NPS', 'WIKI', 'ARMY'], q3: ['NPS', 'WIKI'], q4: ['WIKI', 'NPS'], q5: ['WIKI', 'NPS'],
  a1: ['WIKI', 'NPS', 'ARMY'], a2: ['WIKI', 'ARMY'], a3: ['WIKI', 'NPS'], a4: ['NPS', 'ARMY', 'WIKI'],
  m1: ['WIKI', 'NPS'], m2: ['WIKI', 'NMUSA'], m3: ['WIKI', 'ARMY', 'NPS'], m4: ['ARMY', 'WIKI'], m5: ['WIKI', 'NMUSA', 'NPS'],
  s2: ['ARMY', 'WIKI'], s3: ['RET', 'WIKI'], s4: ['WILSON', 'RET', 'WIKI'], s5: ['RET', 'NMUSA', 'WIKI'], s6: ['NPS', 'RET', 'WIKI'], s7: ['ARMY', 'RIDE'],
  r2: ['RIDE', 'RET'], r3: ['RIDE', 'NPS'], r4: ['RIDE', 'RET', 'NMUSA'], r5: ['RIDE', 'WIKI'], r6: ['RIDE', 'NPS', 'NMUSA'], r7: ['RET', 'WIKI', 'NPS'], r8: ['RET', 'NPS'],
  f1: ['NPS', 'WIKI'], f2: ['NPS', 'WIKI'], f3: ['WIKI', 'NMUSA', 'NPS'], f4: ['NPS', 'WIKI'], f5: ['NPS', 'WIKI'], f6: ['NPS', 'WIKI'], f7: ['NPS', 'WIKI', 'NMUSA'], f7b: ['NMUSA', 'NPS'], f8: ['WIKI', 'NPS'],
  l1: ['WIKI', 'NPS'], l2: ['WIKI', 'NMUSA', 'NPS'],
};

const spec = {
  id: 'doc-charles-young',
  title: 'Born Enslaved, He Rode 500 Miles to Prove the Army Wrong',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { attaches: 'attashays', attache: 'attashay', Duchesne: 'Doo-shayn', 'Du Bois': 'Doo Boyce', Huachuca: 'Wah-choo-kah', 'Agua Caliente': 'Ahgwa Calyenteh', Arminta: 'Ar-minta' },
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
    'Ride length: 16 days (NPS ride article, The Crisis) vs 17 days (NPS retirement article): script says "a little over two weeks". Distance 497 miles (NPS x2, NMUSA); the Cleveland Advocate said 650: not used.',
    'Ride year: 1918 (NPS x2, Wikipedia) vs 1917 and "at 53" (army.mil): script uses June 1918; age 54 from birth date.',
    'Promotion to brigadier general: approved November 1, 2021 (NPS, Wikipedia), effective February 1, 2022, ceremony at West Point April 29, 2022 (Wikipedia, NMUSA citing army.mil): script says "the ceremony was held in 2022, at West Point".',
    'Young\'s answer "Combatant!" to Baker (NPS retirement article only): not used, one source.',
    'Bright\'s disease (army.mil) vs kidney infection (Wikipedia, NMUSA) as cause of death: script uses kidney infection; Bright\'s disease not used.',
  ],
};
fs.writeFileSync('data/doc-charles-young.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images`);
