// Builds data/doc-ellen-craft.json: the 8-minute long-form documentary (16:9) on Ellen and William Craft.
// Facts: data/reel-ellen-craft.json ("facts", "sources") plus the long-form research below ("sourcesByClaim"),
// every fact with two or more sources. Ending follows the owner's rule: only "subscribe for more".
// Run: node data/build_doc_ellen_craft.mjs
import fs from 'node:fs';

const assets = {
  // from the reel (public/pd/reel-ellen-craft): ellen + titlepage are Internet Archive scans, copied in
  couple: 'File:Ellen and William Craft (72a234fc-4e0a-4e3a-95f9-71aa2401000b).jpg',
  siebert: 'File:Ellen Craft escaped slave.jpg',
  baltimore: 'File:President St Depot & City Block - Baltimore 1869.jpg',
  poster: 'File:Slave kidnap post 1851 boston.jpg',
  steamboat: 'File:Bay State (1846 steamboat).jpg',
  // new for the documentary
  train: 'File:American railroad scene- lightning express trains leaving the junction LCCN90708612.jpg',
  savmap: 'File:1855 U.S. Coast Survey Chart or Map of the Savanna River, Georgia - Geographicus - SavannahRiver-uscs-1855.jpg',
  philly: 'File:Cansler Philadelphia ca1845 LC 24863v.jpg',
  boston: "File:1850 bird's-eye view map of Boston.jpg",
  bostonharbor: 'File:Thomas Chambers - Boston Harbor (National Gallery of Art).jpg',
  fsl: 'File:Effects of the Fugitive-Slave-Law LCCN2008661523.jpg',
  parker: 'File:Theodore Parker BPL c1855-crop.jpg',
  hayden: 'File:Lewis Hayden Portrait.png',
  halifax: 'File:Halifax Nova Scotia town & shipping dressed with flags H.M. birthday 1853 LCCN2004662174.jpg',
  ship: 'File:Quarter-deck of an emigrant ship - the roll call LCCN2003670834.jpg',
  crystal: "File:Crystal Palace from the northeast from Dickinson's Comprehensive Pictures of the Great Exhibition of 1851. 1854.jpg",
  auction: 'File:Slave Auction at Richmond Virginia (c6f8eee2-62a3-4b28-9ee7-eaf9aa29b998).jpg',
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });

const beats = [
  // ---- cold open
  ['h1', 'In December 1848, a young white gentleman boarded a train in Macon, Georgia. He wore a top hat and green glasses. His right arm was in a sling.', P('ellen', { focus: [0.5, 0.3], zoom: [1.05, 1.18] }), { hook: 'A *thousand miles* in disguise.' }],
  ['h2', 'His enslaved servant travelled with him, a tall young man who never left his side.', P('couple', { focus: [0.5, 0.4], zoom: [1.0, 1.1] })],
  ['h3', 'But the gentleman was not a gentleman. He was not white, and he was not free. He was an enslaved woman. And the servant was her husband.', P('ellen', { focus: [0.5, 0.25], zoom: [1.2, 1.3] })],
  ['h4', 'For four days, they would travel through the heart of the slave South, by train and by steamboat, in plain sight.', P('train', { motion: 'panRight', zoom: [1.0, 1.08] })],
  ['h5', 'Their names were Ellen and William Craft. And getting out of Georgia was only the first time they would have to run.', P('couple', { focus: [0.5, 0.35], zoom: [1.1, 1.2] }), { lowerThird: { name: 'Ellen & William Craft', sub: 'Escaped December 1848' } }],

  // ---- Macon
  ['m1', 'Ellen was born in 1826, in Clinton, Georgia.', P('savmap', { zoom: [1.0, 1.1] }), { section: 'macon', year: { from: 1826, to: 1826 }, pin: { label: 'Clinton', sub: 'Georgia' } }],
  ['m2', 'Her mother, Maria, was enslaved. Her father was the man who enslaved them both, a wealthy planter named James Smith.', P('ellen', { focus: [0.5, 0.35], zoom: [1.0, 1.08] })],
  ['m3', 'Ellen looked so much like her father that she could pass for white. And his wife resented her for it.', P('ellen', { focus: [0.5, 0.25], zoom: [1.1, 1.2] })],
  ['m4', 'When Ellen was eleven years old, she was given away. A wedding present, for her white half-sister.', T('Age 11', 'given away as a wedding present')],
  ['m5', 'She was taken to Macon, to work in the house of the sister who now owned her.', P('savmap', { motion: 'panLeft', zoom: [1.1, 1.2] }), { pin: { label: 'Macon', sub: 'Georgia' } }],
  ['w1', 'William Craft was born in 1824, also in Georgia.', P('couple', { focus: [0.62, 0.4], zoom: [1.2, 1.3] }), { year: { from: 1824, to: 1824 } }],
  ['w2', 'When he was sixteen, his owner sold the family apart to pay his debts. His mother, his father, his brother and his sister all went to different slaveholders.', P('auction', { motion: 'panRight', zoom: [1.0, 1.1] })],
  ['w3', 'William later wrote that watching his sister sold at auction filled him with red-hot indignation.', Q('Red-hot indignation.', 'William Craft, on watching his sister sold')],
  ['w4', 'In Macon, he was trained as a cabinetmaker and hired out. Most of what he earned went to his owner. But he was allowed to keep a little, and he saved it.', P('couple', { focus: [0.68, 0.4], zoom: [1.3, 1.4] })],
  ['w5', 'In 1846, William and Ellen were married.', T('1846', 'William and Ellen marry')],
  ['w6', 'But no law protected an enslaved family. Any child they had could be sold away, the way William\'s family had been.', P('couple', { focus: [0.5, 0.4], zoom: [1.05, 1.15] })],

  // ---- the plan
  ['p1', 'So they began to talk about escape. But Georgia was deep in the South, about a thousand miles from the free states, and every road was watched.', P('savmap', { focus: [0.5, 0.5], zoom: [1.15, 1.25] }), { section: 'plan' }],
  ['p2', 'Then William had an idea. Ellen could pass for white. What if she travelled as a white slaveholder, and he travelled as her slave?', P('ellen', { focus: [0.5, 0.3], zoom: [1.0, 1.1] })],
  ['p3', 'And she would not go as a lady. She would go as a man.', T('A man', 'a young white planter')],
  ['p4', 'William bought the pieces of the disguise one at a time, in different shops, so no one would notice.', P('ellen', { focus: [0.5, 0.65], zoom: [1.1, 1.2] })],
  ['d1', 'Ellen cut her hair short. She put on men\'s clothes, a top hat, and a pair of green-tinted glasses.', C('ellen', 'Ellen Craft in her disguise, from their 1860 book')],
  ['d2', 'She tied a bandage around her face, like a man with a bad toothache, to hide that she had no beard.', P('ellen', { focus: [0.5, 0.22], zoom: [1.3, 1.4] })],
  ['d3', 'And she put her right arm in a sling.', P('ellen', { focus: [0.45, 0.6], zoom: [1.2, 1.3] })],
  ['d4', 'The sling was the cleverest part of the plan. Neither of them could read or write. In Georgia, it was against the law to teach them.', T('The sling', 'because she could not write')],
  ['d5', 'If someone asked the gentleman to sign his name, he could not. But with his arm in a sling, no one would ask.', C('siebert', 'Ellen Craft, engraving, 1898')],
  ['d6', 'Ellen\'s new name was William Johnson. A young planter, very sick, on his way to Philadelphia to see a doctor.', P('ellen', { focus: [0.5, 0.3], zoom: [1.15, 1.25] }), { lowerThird: { name: '"Mr. William Johnson"', sub: 'Ellen Craft, in disguise' } }],
  ['d7', 'Just before Christmas, both of them asked for a few days off. Holiday passes were common, and they were trusted. So their owners said yes.', T('Christmas', 'a few days\' head start')],

  // ---- the journey
  ['j1', 'On the morning of December the twenty-first, 1848, they slipped out to the station.', P('train', { focus: [0.4, 0.5], zoom: [1.05, 1.15] }), { section: 'journey', stamp: '21 Dec 1848' }],
  ['j2', 'Before they parted, William later wrote, he told her: come, my dear, let us make a desperate leap for liberty.', Q('Come, my dear, let us make a desperate leap for liberty!', 'William Craft, 21 December 1848')],
  ['j3', 'Ellen took her seat on the train to Savannah. William rode separately.', P('train', { motion: 'panLeft', zoom: [1.05, 1.12] })],
  ['j4', 'Then a man sat down right next to her. Mr. Cray. A close friend of the man who had enslaved her.', P('ellen', { focus: [0.5, 0.3], zoom: [1.25, 1.35] })],
  ['j5', 'He turned to her and said: it is a very fine morning, sir.', T('"A very fine morning, sir."', 'Mr. Cray, a friend of her enslaver')],
  ['j6', 'Ellen pretended she could not hear him. For the rest of the ride, she played deaf. And he left her alone.', P('train', { focus: [0.6, 0.5], zoom: [1.15, 1.25] })],
  ['j7', 'In Savannah, they boarded a steamer for Charleston, South Carolina.', P('steamboat', { motion: 'panRight' }), { pin: { label: 'Savannah', sub: 'Georgia' } }],
  ['j8', 'Ellen had a cabin. William had nowhere to sleep. He spent the night outside on the deck.', P('steamboat', { focus: [0.5, 0.5], zoom: [1.1, 1.2] })],
  ['j9', 'At breakfast, a slave dealer at the table offered to buy William from his young master. Ellen said no.', P('steamboat', { focus: [0.4, 0.5], zoom: [1.15, 1.25] })],
  ['j10', 'In Charleston, they needed tickets north. And the ticket office wanted the gentleman to sign for himself, and for his slave.', P('savmap', { focus: [0.7, 0.4], zoom: [1.2, 1.3] }), { pin: { label: 'Charleston', sub: 'South Carolina' } }],
  ['j11', 'With his arm in a sling, Mr. Johnson could not. And the clerk would not sign for him.', T('Sign here', 'the one thing she could not do')],
  ['j12', 'Then an army officer who had travelled with them on the steamer stepped in, and vouched for the young planter. They got their tickets.', P('couple', { focus: [0.4, 0.4], zoom: [1.15, 1.25] })],
  ['j13', 'From there, a steamer to Wilmington, North Carolina. Then train after train. Richmond. Washington. And finally, Baltimore.', P('train', { focus: [0.5, 0.5], zoom: [1.2, 1.3] })],
  ['j14', 'Baltimore was the last stop in a slave state before Pennsylvania. And it was the most dangerous station of all.', C('baltimore', 'President Street Station, Baltimore')],
  ['j15', 'It was Christmas Eve.', T('Christmas Eve', '24 December 1848')],
  ['j16', 'An officer stopped them. No one could take a slave into Pennsylvania, he said, without proof of ownership.', P('baltimore', { focus: [0.5, 0.6], zoom: [1.1, 1.2] })],
  ['j17', 'They had no proof. They had come all this way, and now, a few hours from freedom, they were stuck.', P('ellen', { focus: [0.5, 0.3], zoom: [1.3, 1.4] })],
  ['j18', 'Then a train conductor spoke up for them. The bell rang for departure. And the officer, looking at the sick young man in bandages, let them go.', P('train', { motion: 'panRight', zoom: [1.1, 1.18] })],
  ['j19', 'On Christmas morning, 1848, William saw the lights of Philadelphia.', P('philly', { zoom: [1.0, 1.12] }), { pin: { label: 'Philadelphia', sub: 'Pennsylvania' } }],
  ['j20', 'They were in a free state. They were free.', T('Free', 'Christmas Day, 1848')],

  // ---- Boston and the slave catchers
  ['b1', 'Abolitionists in Philadelphia took them in, and began to teach them to read and write.', P('philly', { zoom: [1.0, 1.1] }), { section: 'boston' }],
  ['b2', 'A few weeks later, they moved on to Boston, a city full of people who hated slavery.', P('boston', { motion: 'panRight', zoom: [1.0, 1.1] }), { pin: { label: 'Boston', sub: 'Massachusetts' } }],
  ['b3', 'They lived in the boarding house of Lewis and Harriet Hayden, on Beacon Hill.', P('hayden', { focus: [0.5, 0.3], zoom: [1.0, 1.08] }), { lowerThird: { name: 'Lewis Hayden', sub: 'Abolitionist, Boston' } }],
  ['b4', 'William worked as a cabinetmaker again. Ellen worked as a seamstress. This time, they were paid for their own work.', P('bostonharbor', { zoom: [1.0, 1.1] })],
  ['b5', 'And they began to tell their story at anti-slavery meetings all across New England. People came to see the woman who had fooled the slave South.', P('couple', { focus: [0.5, 0.4], zoom: [1.1, 1.2] })],
  ['k1', 'Then, in September 1850, Congress passed the Fugitive Slave Act.', P('fsl', { zoom: [1.0, 1.1] }), { year: { from: 1850, to: 1850 } }],
  ['k2', 'It forced the free states to help capture people who had escaped slavery, and send them back. Suddenly, Boston was not safe.', P('fsl', { focus: [0.4, 0.5], zoom: [1.15, 1.25] })],
  ['k3', 'In October 1850, two men arrived in Boston from Macon. Willis Hughes and John Knight. They had come for the Crafts.', T('Hughes & Knight', 'slave catchers from Macon')],
  ['k4', 'They got a warrant for their arrest.', P('poster', { focus: [0.5, 0.4], zoom: [1.0, 1.1] })],
  ['k5', 'But Boston fought back. The Vigilance Committee, Black and white Bostonians together, hid Ellen and moved her from house to house.', C('poster', 'Warning poster, Boston, 1851')],
  ['k6', 'The slave catchers were hounded through the city. Within days, they gave up, and left Boston without them.', P('boston', { focus: [0.6, 0.5], zoom: [1.15, 1.25] })],
  ['k7', 'Before the Crafts left Boston, the minister Theodore Parker married them again. This time, he said, according to the laws of a free state.', P('parker', { focus: [0.5, 0.3], zoom: [1.0, 1.08] }), { lowerThird: { name: 'Theodore Parker', sub: 'Minister and abolitionist' } }],
  ['k8', 'Because Hughes and Knight would not be the last. As long as they stayed in America, the Crafts could be taken.', Q('According to the laws of a free State.', 'Theodore Parker, marrying the Crafts, November 1850')],

  // ---- England
  ['e1', 'So they ran again. North through Maine and Canada to Halifax, and from there, across the Atlantic to Liverpool.', P('halifax', { motion: 'panRight' }), { section: 'england' }],
  ['e2', 'They had escaped from slavery. Now they had to escape from the United States itself.', P('ship', { zoom: [1.0, 1.1] })],
  ['e3', 'In England, they went to school, at Ockham in Surrey. Two people who had been forbidden to learn now studied in a classroom.', T('Ockham', 'Surrey, England')],
  ['e4', 'In 1851, at the Great Exhibition in London, they walked among the crowds to protest American slavery, in front of the world.', P('crystal', { zoom: [1.0, 1.12] }), { year: { from: 1851, to: 1851 } }],
  ['e5', 'They had five children. All of them born free.', T('5', 'children, born free')],
  ['e6', 'In 1852, a rumor spread in America that Ellen was unhappy in England, and wanted to go back.', P('ellen', { focus: [0.5, 0.3], zoom: [1.05, 1.15] })],
  ['e7', 'She answered in print. She would much rather starve in England, a free woman, than be a slave.', Q('I had much rather starve in England, a free woman, than be a slave.', 'Ellen Craft, 1852')],
  ['e8', 'And in 1860, they published their story in a book. Running a Thousand Miles for Freedom.', C('titlepage', 'Running a Thousand Miles for Freedom, London, 1860')],

  // ---- home
  ['r1', 'In 1865, the Civil War ended, and slavery ended with it.', P('crystal', { focus: [0.5, 0.5], zoom: [1.1, 1.2] }), { section: 'home', year: { from: 1865, to: 1865 } }],
  ['r2', 'In 1868, after almost twenty years in England, the Crafts came home. To Georgia.', P('savmap', { zoom: [1.0, 1.12] }), { year: { from: 1868, to: 1868 } }],
  ['r3', 'They settled near Savannah, and in 1873 they opened the Woodville Co-operative Farm School, to teach and employ people who had just been freed.', T('1873', 'Woodville Co-operative Farm School')],
  ['r4', 'A school and a farm, run by two people who had once been forbidden to learn to read.', P('couple', { focus: [0.5, 0.4], zoom: [1.0, 1.1] })],
  ['r5', 'It did not last. Funders accused William of misusing money. He sued for libel in 1878, and lost. Cotton prices fell, and the school closed.', P('savmap', { motion: 'panLeft', zoom: [1.15, 1.25] })],
  ['r6', 'In 1890, they moved to Charleston, to live with their daughter.', P('bostonharbor', { focus: [0.5, 0.5], zoom: [1.15, 1.25] })],
  ['r7', 'Ellen Craft died in 1891. William died in 1900.', P('ellen', { focus: [0.5, 0.3], zoom: [1.12, 1.0] }), { year: { from: 1891, to: 1891 } }],

  // ---- close
  ['c1', 'A girl, given away as a wedding present.', P('ellen', { focus: [0.5, 0.25], zoom: [1.15, 1.22] }), { section: 'close' }],
  ['c2', 'A boy who watched his family sold off, one by one.', P('auction', { focus: [0.5, 0.5], zoom: [1.1, 1.18] })],
  ['c3', 'Together, they bought a top hat, a pair of green glasses and a sling, and rode a thousand miles to freedom, in plain sight.', P('couple', { focus: [0.5, 0.4], zoom: [1.0, 1.12] })],
  ['c4', 'That was Ellen and William Craft. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

// Images too small to fill a 1920x1080 frame without visible upscaling are shown as captioned cards.
const CARD_CAPTIONS = {
  auction: 'A slave auction in Richmond, Virginia',
  philly: 'Philadelphia, about 1845',
  parker: 'Theodore Parker',
  hayden: 'Lewis Hayden',
  poster: 'Warning poster, Boston, 1851',
  steamboat: 'A coastal steamboat of the 1840s',
  siebert: 'Ellen Craft, engraving, 1898',
};
for (const b of beats) {
  const v = b[2];
  if (v.kind === 'photo' && CARD_CAPTIONS[v.image]) b[2] = { kind: 'card', image: v.image, caption: CARD_CAPTIONS[v.image] };
}

const reel = JSON.parse(fs.readFileSync('data/reel-ellen-craft.json', 'utf8'));
const longform = {
  NPSA: 'https://www.nps.gov/articles/-a-desperate-leap-for-liberty-the-escape-of-william-and-ellen-craft.htm',
  NPSP: 'https://www.nps.gov/people/ellen-craft.htm',
  HIST: 'https://www.history.com/articles/slavery-escape-william-ellen-craft',
  NATGEO: 'https://www.nationalgeographic.com/history/history-magazine/article/ellen-craft-the-appearance-of-freedom',
  LOC: 'https://blogs.loc.gov/loc/2018/12/an-1848-christmas-story-the-gift-of-freedom/',
  WIKI: 'https://en.wikipedia.org/wiki/Ellen_and_William_Craft',
  RTM: 'https://archive.org/details/runningthousandm00craf',
};
const sourcesByClaim = {
  m1: ['NPSP', 'HIST', 'WIKI'], m2: ['HIST', 'LOC'], m3: ['NPSA', 'HIST', 'LOC'], m4: ['HIST', 'NPSP', 'NATGEO', 'WIKI'],
  w1: ['NPSA', 'HIST'], w2: ['HIST', 'NATGEO'], w3: ['NPSA', 'RTM'], w4: ['NPSA', 'HIST', 'LOC', 'NATGEO'], w5: ['HIST', 'WIKI'],
  p2: ['NPSA', 'HIST'], p4: ['NPSA', 'HIST'], d1: ['NPSA', 'HIST', 'NATGEO'], d2: ['NPSA', 'HIST', 'NATGEO'], d4: ['NPSA', 'HIST', 'LOC'],
  d6: ['NPSA', 'NATGEO', 'LOC'], d7: ['NPSA', 'LOC'], j1: ['NPSA', 'NPSP', 'HIST'], j2: ['NPSA', 'RTM'], j4: ['NPSA', 'HIST', 'LOC'],
  j5: ['HIST', 'LOC'], j6: ['NPSA', 'HIST'], j7: ['NPSA', 'HIST'], j8: ['NPSA', 'HIST'], j9: ['NPSA', 'HIST'], j10: ['NPSA', 'LOC'],
  j12: ['NPSA', 'LOC'], j13: ['NPSA', 'HIST', 'NATGEO'], j16: ['NPSA', 'HIST', 'NATGEO'], j18: ['NPSA', 'HIST'], j19: ['NPSA', 'HIST', 'NPSP'],
  b1: ['NATGEO', 'NPSA'], b2: ['NPSA', 'HIST'], b3: ['NPSA', 'NPSP'], b4: ['NPSA', 'HIST', 'NPSP'], b5: ['NPSA', 'HIST', 'NPSP'],
  k1: ['NPSA', 'HIST'], k3: ['NPSA', 'HIST', 'WIKI'], k4: ['NPSA', 'NPSP'], k5: ['NPSA', 'NPSP', 'HIST'], k6: ['NPSA', 'WIKI'],
  k7: ['NPSA', 'NPSP'], e1: ['NPSA', 'WIKI'], e3: ['NPSA', 'WIKI'], e4: ['NPSA', 'NPSP'], e5: ['NPSA', 'HIST', 'NATGEO', 'WIKI'],
  e6: ['NPSP', 'NATGEO'], e7: ['NATGEO', 'WIKI'], e8: ['NPSA', 'NATGEO', 'LOC'], r2: ['NATGEO', 'WIKI', 'NPSA'], r3: ['NPSA', 'NPSP', 'WIKI', 'HIST'],
  r5: ['NPSA', 'NATGEO', 'WIKI'], r6: ['NATGEO', 'WIKI', 'NPSA'], r7: ['NPSA', 'NATGEO', 'WIKI'],
};

const spec = {
  id: 'doc-ellen-craft',
  title: 'She Escaped Slavery Disguised as a White Man. Her Husband Played Her Slave.',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { ...reel.voice, speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1.0 },
  music: reel.music,
  mix: { ...(reel.mix || {}), hookBoostDb: 0 },
  brand: { page: 'The Black History Room', cta: 'Subscribe', ctaLine: '', theme: 'bhr' },
  assets: Object.fromEntries(Object.entries(assets).map(([k, v]) => [k, { commons: v }])),
  beats: beats.map(([id, text, visual, overlays, extra]) => {
    // a `section` written among the overlays belongs on the beat itself
    const { section, ...ov } = overlays || {};
    return { id, text, visual, ...(Object.keys(ov).length ? { overlays: ov } : {}), ...(section ? { section } : {}), ...(extra || {}) };
  }),
  facts: reel.facts,
  sourcesByClaim,
  sources: { ...reel.sources, ...Object.fromEntries(Object.entries(longform).map(([k, url]) => [k, { url }])) },
  notUsed: [
    ...(reel.notUsed || []),
    'Gunpowder keg under the Hayden house, 200 guards, revolver from Parker (NPS only).',
    'Schools burned by night riders in 1870 (National Geographic only).',
    'Harriet Martineau arranging the Ockham schooling (Wikipedia only).',
  ],
};
fs.writeFileSync('data/doc-ellen-craft.json', JSON.stringify(spec, null, 1) + '\n');
const words = beats.map((b) => b[1]).join(' ').split(/\s+/).length;
console.log(`${beats.length} beats, ${words} words, ${beats.map((b) => b[1]).join(' ').length} characters, ~${(words / 165).toFixed(1)} min at 165 wpm, ${Object.keys(assets).length + 2} images`);
