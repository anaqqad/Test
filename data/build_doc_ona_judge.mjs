// Builds data/doc-ona-judge.json: 8-minute long-form documentary (16:9) on Ona Judge (about 1773-1848).
// Free local voice (Kokoro). Every fact has two or more sources (sourcesByClaim).
// Ending follows the owner's rule: only "subscribe for more". Run: node data/build_doc_ona_judge.mjs
import fs from 'node:fs';

const assets = {
  gw: 'File:Gilbert Stuart Williamstown Portrait of George Washington.jpg',
  mw: 'File:Portrait of Martha Washington by Rembrandt Peale adj.JPG',
  mw2: 'File:Martha Dandridge Washington (Engraved Portrait).jpg',
  mv: 'File:Mount Vernon 1858.jpg',
  house: "File:Mansion of Richard Penn (President's House) HSP.jpg",
  eliza: 'File:Elizabeth Parke Custis Law.jpg',
  ferry: "File:Arch Street Ferry Birch's Views Plate 4.jpg",
  ad: 'File:Oney Judge Runaway Ad.jpg',
  family: 'File:Edward Savage - The Washington Family - Google Art Project.jpg',
  highst: 'File:High Street, with the First Presbyterian church Philadelphia. Taken down in 1820 - designed & published by W. Birch enamel painter, 1800. LCCN2013650033.jpg',
  statehouse: 'File:Back of the State House, Philadelphia - designed & published by W. Birch enamel painter, 1800. LCCN2010646072.jpg',
  fedhall: 'File:Federal Hall, N.Y. 1789 ppmsca.15703.jpg',
  wolcott: 'File:Oliver Wolcott Jr by Gilbert Stuart circa 1820.jpeg',
  brig: "File:The Brig 'Ariel' RMG BHC3203.tiff",
  langdonhouse: 'File:Gov. Langdon House, Portsmouth, NH.jpg',
  tomb: 'File:Mount Vernon tomb of Washington LCCN2003655710.jpg',
  greenland: 'File:Greenland, New Hampshire Parade, circa 1880.jpg',
  liberator: 'File:The Liberator masthead, 1861 Jan 11.jpg',
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });

const beats = [
  // ---- cold open
  ['h1', 'On the evening of May 21, 1796, the President of the United States sat down to dinner in Philadelphia.', P('gw', { focus: [0.55, 0.3], zoom: [1.45, 1.55], anchor: [0.8, 0.42] }), { hook: 'She ran away from George Washington.' }],
  ['h2', 'While George and Martha Washington ate, a young woman they enslaved walked out of the house.', C('house', "The President's House, Philadelphia")],
  ['h3', 'She never came back. And for the rest of his life, the most powerful man in America tried to get her back.', P('gw', { focus: [0.5, 0.32], zoom: [1.15, 1.3] })],
  ['h4', 'He wrote letters. He asked his Treasury Department for help. He sent his own nephew to seize her.', C('ad', 'Runaway ad for Oney Judge, May 1796')],
  ['h5', 'Her name was Ona Judge. This is the story of the woman who escaped George Washington, and was never caught.', T('Ona Judge', 'about 1773 to 1848')],

  // ---- Mount Vernon
  ['e1', 'Ona Judge was born around 1773 at Mount Vernon, the Washingtons\' plantation in Virginia.', C('mv', 'Mount Vernon, Virginia'), { section: 'early', stamp: 'about 1773' }],
  ['e2', 'Her mother, Betty, was enslaved. Her father, Andrew Judge, was a white English tailor working as an indentured servant.', P('mv', { focus: [0.5, 0.5], zoom: [1.1, 1.22] })],
  ['e3', 'Under Virginia law, a child followed the status of the mother. So Ona was born enslaved.', T('Born enslaved', 'the law followed the mother')],
  ['e4', 'Betty belonged to Martha Washington\'s first husband\'s estate. People like her were called dower slaves.', C('mw2', 'Martha Washington')],
  ['e5', 'That mattered. Legally, George Washington could not free them, even if he wanted to. They were held for Martha\'s heirs.', T('Dower slaves', 'held for the Custis heirs')],
  ['e6', 'When Ona was about ten, she was brought into the mansion house.', P('mv', { focus: [0.5, 0.45], zoom: [1.2, 1.32] })],
  ['e7', 'She became Martha Washington\'s personal maid. She dressed her, served her, and went wherever she went.', C('mw', 'Martha Washington'), { lowerThird: { name: 'Martha Washington', sub: 'First Lady' } }],

  // ---- the presidency
  ['p1', 'In 1789, George Washington became the first President of the United States.', C('fedhall', 'Federal Hall, New York, 1789'), { section: 'president', stamp: '1789' }],
  ['p2', 'The government sat in New York, and the Washingtons brought enslaved people from Mount Vernon to run the household. Ona, about sixteen, was one of them.', P('fedhall', { focus: [0.5, 0.5], zoom: [1.1, 1.22] })],
  ['p3', 'The next year, the capital moved to Philadelphia. Ona was one of nine enslaved people taken to the President\'s House.', C('highst', 'High Street, Philadelphia, 1800')],
  ['p4', 'But Pennsylvania had a law. Under its Gradual Abolition Act, an enslaved person brought into the state who stayed for six months in a row could claim freedom.', C('statehouse', 'The State House, Philadelphia, 1800')],
  ['p5', 'So the Washingtons kept the clock from running out. They rotated the people they enslaved out of Pennsylvania, back to Virginia or across the state line, before the six months were up.', T('Six months', 'and never a day longer')],
  ['p6', 'In 1791, Martha Washington took Ona to Trenton, New Jersey, for two days. Just long enough to reset the clock.', P('mw', { focus: [0.55, 0.36], zoom: [1.3, 1.45] })],
  ['p7', 'Philadelphia had a large and growing free Black community. Ona saw, every day, people like her living free.', C('highst', 'Philadelphia, 1800', { focus: [0.5, 0.6] })],

  // ---- the gift
  ['g1', 'In the spring of 1796, Washington was in his last year as President. Soon the family would go home to Virginia for good.', P('family', { focus: [0.5, 0.45], zoom: [1.05, 1.15] }), { section: 'gift' }],
  ['g2', 'Then Ona learned something. Martha Washington planned to give her away, to her granddaughter, Eliza Custis Law.', C('eliza', 'Eliza Custis Law, Martha Washington\'s granddaughter')],
  ['g3', 'She would be handed over like property, to a new owner, and taken back to Virginia.', P('eliza', { focus: [0.5, 0.35], zoom: [1.15, 1.28] })],
  ['g4', 'Decades later, she remembered what she thought.', Q('I knew that if I went back to Virginia, I should never get my liberty.', 'Ona Judge, 1845')],
  ['g5', 'So while the Washingtons packed to go to Virginia, she packed too. She did not know where she was going.', T('Packing', 'May 1796')],
  ['g6', 'She had friends among the free Black people of Philadelphia. Quietly, her belongings were carried out of the house ahead of time.', C('ferry', 'The Philadelphia waterfront, 1800')],

  // ---- the escape
  ['x1', 'On May 21, 1796, while the President and the First Lady sat at dinner, Ona Judge walked out the door.', C('house', "The President's House, Philadelphia"), { section: 'escape', stamp: '21 May 1796' }],
  ['x2', 'Her friends got her onto a ship commanded by Captain John Bowles, bound north for Portsmouth, New Hampshire.', C('brig', 'A sailing brig, painted in 1811')],
  ['x3', 'Three days after she vanished, an advertisement appeared in the Philadelphia Gazette.', C('ad', 'Philadelphia Gazette, May 24, 1796'), { stamp: '24 May 1796' }],
  ['x4', 'Absconded from the household of the President of the United States, it read. It described her freckles, her very black eyes, and her bushy hair.', P('ad', { focus: [0.5, 0.35], zoom: [1.3, 1.45] })],
  ['x5', 'The reward was ten dollars, to anyone who brought her back.', T('$10', 'the reward for her return')],
  ['x6', 'But by then, she was already at sea.', P('brig', { focus: [0.5, 0.5], zoom: [1.1, 1.22] })],

  // ---- found
  ['f1', 'In Portsmouth, Ona Judge found work, and began a new life among the town\'s free Black residents.', C('langdonhouse', 'Portsmouth, New Hampshire'), { section: 'found' }],
  ['f2', 'Then, one day that summer, someone recognized her on the street.', P('langdonhouse', { focus: [0.5, 0.5], zoom: [1.1, 1.22] })],
  ['f3', 'It was Elizabeth Langdon, the daughter of a United States senator, John Langdon. She had visited the Washingtons, and she knew exactly who Ona was.', T('Recognized', 'Portsmouth, summer 1796')],
  ['f4', 'Word reached the President.', C('gw', 'George Washington')],
  ['f5', 'On September 1, 1796, Washington wrote to his Secretary of the Treasury, Oliver Wolcott, asking for help to have her seized and sent back by ship.', C('wolcott', 'Oliver Wolcott Jr., Secretary of the Treasury'), { stamp: '1 September 1796' }],
  ['f6', 'Wolcott passed the job to the customs collector in Portsmouth, Joseph Whipple.', P('wolcott', { focus: [0.5, 0.35], zoom: [1.1, 1.22] })],
  ['f7', 'Whipple found Ona and asked her to board a ship back to Virginia.', T('Joseph Whipple', 'customs collector, Portsmouth')],
  ['f8', 'She said no. But she made an offer. She would go back, if the Washingtons promised to free her when they died.', T('An offer', 'freedom, someday')],
  ['f9', 'Whipple would not force her onto a ship. He passed her offer to the President.', P('langdonhouse', { focus: [0.5, 0.45], zoom: [1.2, 1.32] })],
  ['f10', 'Washington refused. To enter into such a compromise, he wrote, was totally inadmissible.', Q('To enter into such a compromise... is totally inadmissible.', 'George Washington, 1796')],

  // ---- the hunt
  ['k1', 'Ona Judge stayed. In early 1797, she married a free Black sailor named Jack Staines.', T('Ona Staines', 'married, 1797'), { section: 'hunt' }],
  ['k2', 'That March, Washington left the presidency and went home to Mount Vernon. He had not forgotten her.', C('mv', 'Mount Vernon')],
  ['k3', 'In August 1799, he wrote to his nephew, Burwell Bassett Junior, who was going to New Hampshire on business.', P('gw', { focus: [0.5, 0.32], zoom: [1.35, 1.5] }), { stamp: 'August 1799' }],
  ['k4', 'His request: seize Ona, and her baby, and bring them back to Virginia.', T('Seize her', 'and her child')],
  ['k5', 'Bassett found her, and tried to talk her into coming back. She refused.', P('langdonhouse', { focus: [0.5, 0.5], zoom: [1.05, 1.15] })],
  ['k6', 'So he planned to take her by force. And he made a mistake. He told Senator Langdon.', C('langdonhouse', 'The Langdon House, Portsmouth')],
  ['k7', 'Langdon sent her a secret warning. That night, Ona Judge took her baby daughter and fled to the town of Greenland, a few miles away.', C('greenland', 'Greenland, New Hampshire')],
  ['k8', 'Bassett went home empty-handed.', T('Empty-handed', 'September 1799')],
  ['k9', 'On December 14, 1799, George Washington died at Mount Vernon.', C('tomb', 'The tomb of George Washington, Mount Vernon'), { stamp: '14 December 1799' }],
  ['k10', 'He had chased her for more than three years. He never got her back.', P('tomb', { focus: [0.5, 0.5], zoom: [1.1, 1.22] })],

  // ---- still not free
  ['n1', 'In his will, Washington freed the people he himself enslaved, after Martha\'s death.', C('family', 'The Washington Family, by Edward Savage'), { section: 'free' }],
  ['n2', 'But Ona was not his. She was a dower slave, held for the Custis heirs. Nothing in that will could free her, or her children.', P('family', { focus: [0.35, 0.5], zoom: [1.2, 1.32] })],
  ['n3', 'Martha Washington died in 1802. In law, Ona Judge was still a fugitive slave.', P('mw2', { focus: [0.5, 0.35], zoom: [1.1, 1.22] })],
  ['n4', 'A federal law, the Fugitive Slave Act of 1793, signed by George Washington himself, allowed people who escaped to be captured and returned.', T('Fugitive Slave Act', '1793')],
  ['n5', 'For the rest of her life, she lived with that.', C('greenland', 'Greenland, New Hampshire')],

  // ---- a hard freedom
  ['l1', 'Freedom was hard. Ona and Jack had three children. Then, in 1803, Jack Staines died.', T('1803', 'Jack Staines dies'), { section: 'later' }],
  ['l2', 'She could not support her family alone. She moved in with the Jacks family in Greenland.', P('greenland', { focus: [0.5, 0.5], zoom: [1.1, 1.22] })],
  ['l3', 'Her daughters were bound out as indentured servants. Both died before her.', T('Her daughters', 'Eliza and Nancy')],
  ['l4', 'In old age, she was poor, and relied on gifts from her community.', P('greenland', { focus: [0.4, 0.55], zoom: [1.2, 1.32] })],
  ['l5', 'But she had chosen her own faith, and her own church. And she had chosen her own life.', C('greenland', 'Greenland, New Hampshire')],

  // ---- her own words
  ['v1', 'In 1845, an abolitionist newspaper in New Hampshire, the Granite Freeman, published an interview with her. A second one followed in The Liberator.', C('liberator', 'The Liberator'), { section: 'words', stamp: '1845' }],
  ['v2', 'She was in her seventies. She told how she had walked out on the President of the United States.', P('liberator', { focus: [0.5, 0.5], zoom: [1.1, 1.22] })],
  ['v3', 'She was asked if she was sorry she had ever left the Washingtons.', T('Any regrets?', 'The Granite Freeman, 1845')],
  ['v5', 'Her answer: No, I am free, and have, I trust, been made a child of God by the means.', Q('No, I am free, and have, I trust, been made a child of God by the means.', 'Ona Judge, 1845')],

  // ---- end
  ['d1', 'Ona Judge died in Greenland, New Hampshire, on February 25, 1848. She was about seventy-five.', T('25 February 1848', 'Greenland, New Hampshire'), { section: 'end' }],
  ['d2', 'She had outlived George Washington by almost fifty years. By law, she was still a fugitive.', C('gw', 'George Washington')],
  ['d3', 'Today, at the site of the President\'s House in Philadelphia, her story is told where it happened.', C('house', "The President's House, Philadelphia")],

  // ---- close
  ['c1', 'She was enslaved by the first President of the United States.', P('mw', { focus: [0.55, 0.36], zoom: [1.05, 1.15] }), { section: 'close' }],
  ['c2', 'She walked out of his house while he ate dinner, and he spent the rest of his life trying to get her back.', C('ad', 'Runaway ad for Oney Judge, 1796')],
  ['c3', 'He never did.', P('gw', { focus: [0.5, 0.32], zoom: [1.05, 1.15] })],
  ['c4', 'That was Ona Judge. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-charles-young.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Ona_Judge',
  NPS: 'https://www.nps.gov/articles/independence-oneyjudge.htm',
  HIST: 'https://www.history.com/articles/george-washington-and-the-slave-who-got-away',
  AD: 'https://commons.wikimedia.org/wiki/File:Oney_Judge_Runaway_Ad.jpg',
};
const sourcesByClaim = {
  h1: ['NPS', 'HIST', 'WIKI'], h2: ['NPS', 'HIST', 'WIKI'], h3: ['HIST', 'WIKI'], h4: ['NPS', 'WIKI', 'HIST'], h5: ['NPS', 'WIKI'],
  e1: ['WIKI', 'HIST'], e2: ['WIKI', 'HIST'], e3: ['WIKI', 'HIST'], e4: ['WIKI', 'HIST'], e5: ['WIKI', 'HIST'], e6: ['WIKI', 'HIST'], e7: ['WIKI', 'HIST'],
  p1: ['WIKI', 'HIST'], p2: ['WIKI', 'HIST'], p3: ['NPS', 'WIKI', 'HIST'], p4: ['WIKI', 'HIST'], p5: ['WIKI', 'HIST'], p6: ['WIKI', 'HIST'], p7: ['HIST', 'WIKI'],
  g1: ['HIST', 'WIKI'], g2: ['NPS', 'HIST', 'WIKI'], g3: ['NPS', 'WIKI'], g4: ['NPS', 'WIKI'], g5: ['WIKI', 'NPS'], g6: ['WIKI', 'HIST'],
  x1: ['NPS', 'HIST', 'WIKI'], x2: ['HIST', 'WIKI'], x3: ['WIKI', 'AD'], x4: ['WIKI', 'AD'], x5: ['WIKI', 'AD'],
  f1: ['HIST', 'WIKI'], f2: ['NPS', 'HIST', 'WIKI'], f3: ['NPS', 'HIST', 'WIKI'], f4: ['NPS', 'HIST'], f5: ['WIKI', 'NPS'], f6: ['NPS', 'HIST', 'WIKI'], f7: ['NPS', 'HIST', 'WIKI'], f8: ['NPS', 'HIST', 'WIKI'], f9: ['WIKI', 'NPS'], f10: ['HIST', 'WIKI'],
  k1: ['WIKI', 'HIST', 'NPS'], k2: ['WIKI', 'HIST'], k3: ['WIKI', 'HIST', 'NPS'], k4: ['NPS', 'HIST'], k5: ['WIKI', 'NPS'], k6: ['WIKI', 'NPS'], k7: ['NPS', 'HIST', 'WIKI'], k8: ['HIST', 'WIKI'], k9: ['WIKI', 'HIST'], k10: ['HIST', 'WIKI'],
  n1: ['WIKI', 'HIST'], n2: ['WIKI', 'HIST'], n3: ['WIKI', 'HIST', 'NPS'], n4: ['WIKI', 'NPS'],
  l1: ['WIKI', 'HIST', 'NPS'], l2: ['WIKI', 'HIST'], l3: ['WIKI', 'HIST'], l4: ['WIKI', 'HIST'], l5: ['HIST', 'WIKI'],
  v1: ['WIKI', 'NPS', 'HIST'], v2: ['NPS', 'HIST'], v3: ['NPS', 'WIKI'], v5: ['NPS', 'HIST', 'WIKI'],
  d1: ['WIKI', 'NPS'], d2: ['NPS', 'WIKI'], d3: ['NPS', 'WIKI'],
};

const spec = {
  id: 'doc-ona-judge',
  title: 'She Ran Away From George Washington. He Never Stopped Hunting Her.',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { Ona: 'Oh-nah', Oney: 'Oh-nee', Wolcott: 'Wool-cut', Custis: 'Kus-tiss', Burwell: 'Burr-well', dower: 'dow-er' },
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
    'Ship name, the Nancy (Wikipedia only): not used; captain John Bowles is in History.com and Wikipedia.',
    'Five-day voyage, and Whipple posing as an employer looking for a maid (History.com only): not used.',
    'Whipple warning of riots, and Washington "neither politic or just" (Wikipedia only): not used.',
    'Delphy freed in 1807, Ona Judge Day in Philadelphia (2026), Virginia marker (2021): one source each, not used.',
    'Age at moving into the mansion: about 10 (Wikipedia) vs 9 (History.com): script says "about ten".',
    'Bassett trip: August-September 1799 (Wikipedia, History.com); NPS says about two years after the escape: script uses 1799.',
  ],
};
fs.writeFileSync('data/doc-ona-judge.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images`);
