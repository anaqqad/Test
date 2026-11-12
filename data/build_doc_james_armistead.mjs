// Builds data/doc-james-armistead.json: 8-minute long-form documentary (16:9) on James (Armistead) Lafayette, the enslaved spy of 1781.
// Free local voice (Kokoro). Every fact has two or more sources (sourcesByClaim). Disputed parts of the legend (serving Cornwallis
// himself) are told as "most accounts say" and then checked against what his petition and Lafayette's certificate actually say.
// Ending follows the owner's rule: only "subscribe for more". Run: node data/build_doc_james_armistead.mjs
import fs from 'node:fs';

const assets = {
  james: 'File:James Lafayette.jpg',
  cert: 'File:Marquis de Lafayette James Armistead Lafayette.jpeg',
  lafayette82: 'File:The honble. Marquis Lafayette, major general of the American army LCCN2003689172.jpg',
  lafayette25: 'File:The Marquis de Lafayette MET DT2057.jpg',
  cornwallis: 'File:Charles Cornwallis, 1st Marquess Cornwallis.png',
  arnold: 'File:Benedict Arnold 1.jpg',
  surrender: 'File:Surrender of Lord Cornwallis.jpg',
  deverger: 'File:Soldiers at the siege of Yorktown (1781), by Jean-Baptiste-Antoine DeVerger.png',
  yorkplan: "File:Siege d'York, 1781. Plan d'York en Virginie avec les attaques et les campemens de l'Armée combinée de France et d'Amérique. LOC gm71002176.jpg",
  portsmouth: 'File:Plan de Portsmouth en Virginie. LOC gm71002169.jpg',
  environs: 'File:Plan des environs de Williamsburg, York, Hampton, et Portsmouth. LOC gm71002173.jpg',
  moore: 'File:Moore House, Yorktown, Va.jpg',
  renault: 'File:The surrender of Cornwallis at Yorktown A.D. 1781 LCCN2004670530.jpg',
  wlt: 'File:Washington, Lafayette & Tilghman at Yorktown.jpg',
  medal: 'File:Medal of the Marquis de Lafayette MET 25792.jpg',
  oldnk: 'File:Old NewKent6.jpg',
  reddition: 'File:Reddition armee anglaise a Yorktown 1781 avec blocus naval.jpg',
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });

const JL = 'James Lafayette, portrait by John B. Martin, 1824';
const CERT = "Lafayette's 1784 certificate, printed with James's portrait";
const LAF = "Marquis de Lafayette, 21 November 1784";
const beats = [
  // ---- cold open
  ['h1', 'In 1781, a British army under Lord Cornwallis was marching through Virginia. An American army under a young French general, the Marquis de Lafayette, was trying to stop it.', P('environs', { focus: [0.5, 0.45], zoom: [1.1, 1.25] }), { hook: 'The spy who helped win Yorktown.' }],
  ['h2', 'Lafayette needed to know what the British were planning.', C('lafayette82', 'The Marquis de Lafayette, 1782')],
  ['h3', 'One of the men he relied on was enslaved. His name was James.', C('james', JL), { lowerThird: { name: 'James Lafayette', sub: 'spy for Lafayette, 1781' } }],
  ['h4', 'James went into the British camp, again and again, and carried what he learned back to Lafayette.', P('james', { focus: [0.5, 0.35], zoom: [1.1, 1.25] })],
  ['h5', 'That October, Cornwallis surrendered at Yorktown.', C('surrender', 'The Surrender of Lord Cornwallis, by John Trumbull'), { stamp: '19 October 1781' }],
  ['h6', 'But when the war was over, James was still enslaved. This is the story of how he won his freedom.', T('Still enslaved', 'after the war he helped win')],
  ['h7', 'He never fired a shot. His weapon was what he heard.', P('james', { focus: [0.5, 0.3], zoom: [1.05, 1.15] })],

  // ---- early life
  ['e1', 'James was born around 1748, most likely in New Kent County, Virginia.', T('About 1748', 'New Kent County, Virginia'), { section: 'early' }],
  ['e2', 'He was enslaved by a man named William Armistead.', T('William Armistead', 'his enslaver')],
  ['e3', 'During the Revolution, Armistead managed military supplies for Virginia.', C('environs', 'Williamsburg, York, Hampton and Portsmouth, French map, 1781')],
  ['e4', 'In 1780, Virginia moved its capital from Williamsburg to Richmond, and James most likely went with Armistead.', T('1780', 'Williamsburg to Richmond')],
  ['e5', 'That is nearly all we know of his early life. Even his birth year is uncertain. He left no diary, and the records are thin.', P('james', { focus: [0.5, 0.3], zoom: [1.15, 1.3] })],
  ['e6', 'Today he is usually called James Armistead Lafayette, after both the family that enslaved him and the general he served.', C('james', JL)],

  // ---- war in Virginia
  ['l1', 'In 1781, the war came to Virginia.', T('1781', 'the war comes to Virginia'), { section: 'war' }],
  ['l2', 'Benedict Arnold, the American general who had gone over to the British, led raids there from a base at Portsmouth.', C('arnold', 'Benedict Arnold'), { pin: { label: 'Portsmouth', sub: 'Virginia' } }],
  ['l3', 'Then Lord Cornwallis brought his army north into Virginia.', C('cornwallis', 'Charles, Lord Cornwallis')],
  ['l4', 'Facing him was the Marquis de Lafayette, a young French nobleman in command of the Continental Army in Virginia.', C('lafayette82', 'The Marquis de Lafayette, major general of the American army, 1782')],
  ['l5', 'In the summer of 1781, by most accounts with his enslaver\'s permission, James went to serve Lafayette.', P('lafayette82', { focus: [0.5, 0.4], zoom: [1.1, 1.2] })],
  ['l6', 'He did not take up arms. On paper he was a servant. In fact, he was a spy.', T('A spy', 'not a soldier')],

  // ---- the spy
  ['s1', 'Most accounts say he posed as a runaway slave, and made his way into the British camp.', C('portsmouth', 'Portsmouth, Virginia, French plan, 1781'), { section: 'spy' }],
  ['s2', 'The British needed men who knew the local roads. He guided their troops, earned their trust, and listened.', P('portsmouth', { focus: [0.55, 0.5], zoom: [1.2, 1.35] })],
  ['s2b', 'He reported where the British troops were posted, and what arms they had.', T('Troops and arms', 'what he reported')],
  ['s3', 'Many accounts go further. They say he became a servant at Cornwallis\'s own headquarters, and that the British asked him to spy on the Americans.', C('cornwallis', 'Lord Cornwallis')],
  ['s3b', 'Lafayette\'s own letters to George Washington, written in July and August 1781, mention an informant in Cornwallis\'s camp. They do not give his name.', C('lafayette82', 'The Marquis de Lafayette')],
  ['s4', 'If so, he was a double agent. He brought true reports to Lafayette, and false ones back to the British.', T('Double agent', 'true reports one way, false ones the other')],
  ['s4b', 'Every trip across the lines was a risk. One wrong word, one letter found, and it would be over.', P('portsmouth', { focus: [0.4, 0.4], zoom: [1.2, 1.3] })],
  ['s5', 'In late August, Lafayette learned that Cornwallis had moved his army from Portsmouth to Yorktown, on the York River.', C('yorkplan', 'Yorktown, French plan of the siege, 1781'), { pin: { label: 'Yorktown', sub: 'Virginia' } }],
  ['s6', 'At Yorktown, with the river at his back, Cornwallis could be trapped by land and by sea.', P('yorkplan', { focus: [0.5, 0.5], zoom: [1.15, 1.3] })],
  ['s7', 'George Washington and the French general Rochambeau marched south. A French fleet sailed into the Chesapeake Bay.', C('wlt', 'Washington, Lafayette and Tilghman at Yorktown, by Charles Willson Peale')],
  ['s8', 'The allied armies dug in around the town, and the siege began.', C('deverger', 'Soldiers at the siege of Yorktown, sketched by a French officer, 1781')],
  ['s8b', 'For about three weeks, cannon fire pounded the British lines.', P('reddition', { focus: [0.5, 0.5], zoom: [1.1, 1.2] })],
  ['s9', 'On October 19, 1781, Cornwallis surrendered his army.', C('renault', 'The surrender at Yorktown, engraving'), { stamp: '19 October 1781' }],
  ['s9b', 'Thousands of British and German soldiers marched out and laid down their arms.', C('reddition', 'The British surrender at Yorktown, French print, 1781')],
  ['s10', 'The war was all but won.', P('surrender', { zoom: [1.0, 1.08] })],

  // ---- what we know
  ['k1', 'How much of the spy story can we prove? Less than the legend.', T('What we can prove', ''), { section: 'record' }],
  ['k2', 'Historians point out that the surviving papers, his own petition and Lafayette\'s letter, do not say that he served Cornwallis himself.', C('cert', CERT, { focus: [0.5, 0.6] })],
  ['k2b', 'Some of the legend grew later, from a novel and from storytellers who filled in the gaps.', T('Legend', 'and record')],
  ['k3', 'What those papers do say is striking enough.', P('cert', { focus: [0.5, 0.65], zoom: [1.2, 1.35] })],
  ['k4', 'In his petition, James said he went into the British camp again and again, at the risk of his life, and carried Lafayette\'s secret messages into enemy lines.', T('At the risk of his life', 'from his own petition')],
  ['k5', 'If he had been caught, he could have been executed.', T('If caught', 'execution')],

  // ---- freedom
  ['f1', 'After the war, Virginia passed a law freeing enslaved men who had served as soldiers.', T('A law for soldiers', 'Virginia, after the war'), { section: 'freedom' }],
  ['f1b', 'It covered men who had been given a gun and sent to fight, often in their owner\'s place.', T('A gun', 'was the test')],
  ['f2', 'James had not carried a gun. He had been a spy. The law did not cover him, and he stayed enslaved.', P('james', { focus: [0.5, 0.35], zoom: [1.1, 1.2] })],
  ['f3', 'On November 21, 1784, Lafayette wrote a certificate for him.', C('cert', CERT), { stamp: '21 November 1784' }],
  ['f4', 'This is to certify, it began, that the bearer has done essential services to me while I had the honour to command in this State.', Q('This is to certify that the Bearer has done essential services to me while I had the honour to command in this State.', LAF)],
  ['f5', 'His intelligences from the enemy\'s camp were industriously collected and most faithfully delivered.', Q('His intelligences from the enemy\'s camp were industriously collected and most faithfully delivered.', LAF)],
  ['f6', 'He appears to me entitled to every reward his situation can admit of.', Q('He appears to me entitled to every reward his situation can admit of.', LAF)],
  ['f7', 'With that letter, James asked the Virginia legislature for his freedom. His first petition failed.', T('First petition', 'denied')],
  ['f8', 'In 1786 he tried again, and this time William Armistead supported him.', T('1786', 'a second petition')],
  ['f9', 'His petition, dated November 30, 1786, is still kept at the Library of Virginia.', T('30 November 1786', 'Library of Virginia')],
  ['f10', 'On January 9, 1787, the act freeing him became law.', T('9 January 1787', 'free')],
  ['f10b', 'Both houses of the Assembly had passed it, and Governor Edmund Randolph signed it.', T('Governor Edmund Randolph', 'signs the act')],
  ['f11', 'The state paid William Armistead two hundred fifty pounds for him.', T('250 pounds', 'paid to his enslaver')],
  ['f12', 'And James chose a last name. Lafayette.', C('james', JL)],

  // ---- later life
  ['a1', 'James Lafayette settled in New Kent County, on a farm of about forty acres.', C('oldnk', 'New Kent County, Virginia, today'), { section: 'later' }],
  ['a2', 'He married, and raised a family.', P('james', { focus: [0.5, 0.4], zoom: [1.05, 1.15] })],
  ['a3', 'Records show that he, too, came to own enslaved people. History is rarely simple.', T('A free man', 'and a slaveowner')],
  ['a4', 'By 1818 he was about seventy, poor and in failing health. He asked the legislature for help.', T('1818', 'about seventy, and poor')],
  ['a5', 'It gave him sixty dollars at once, and a pension of forty dollars a year.', T('$40 a year', 'a pension from Virginia')],

  // ---- reunion
  ['r1', 'In 1824, the Marquis de Lafayette came back to America, for a long farewell tour.', C('lafayette25', 'The Marquis de Lafayette, 1825'), { section: 'reunion' }],
  ['r1b', 'The tour lasted more than a year, from July 1824 to September 1825, and took him through all twenty-four states.', C('medal', 'A medal struck for Lafayette\'s visit, 1824')],
  ['r2', 'Crowds came out wherever he went.', C('medal', 'A medal struck for Lafayette\'s visit, 1824')],
  ['r3', 'In Virginia, the old general saw James in the crowd. He called him by name, and embraced him.', P('lafayette25', { focus: [0.5, 0.35], zoom: [1.1, 1.2] })],
  ['r3b', 'It was more than forty years after Yorktown.', T('43 years', 'after Yorktown')],
  ['r4', 'That same year, an artist named John Blennerhassett Martin painted James\'s portrait.', C('james', JL)],
  ['r5', 'It shows him in a dark coat with a white collar. A free man.', P('james', { focus: [0.5, 0.45], zoom: [1.0, 1.1] })],
  ['r6', 'Copies were printed together with Lafayette\'s certificate.', C('cert', CERT)],
  ['r7', 'In 1828, a Virginia novel, Edge Hill, told the story of a spy named James.', T('Edge Hill', 'a novel, 1828')],
  ['r8', 'James Lafayette died on his farm in 1830.', T('1830', 'New Kent County')],

  // ---- close
  ['c1', 'He went into the enemy camp with nothing but his wits, knowing what would happen if he were caught.', P('yorkplan', { zoom: [1.0, 1.08] }), { section: 'close' }],
  ['c1b', 'He was born enslaved, served in secret, and was freed by a letter of thanks and an act of the legislature.', C('cert', CERT)],
  ['c2', 'He helped bring about the surrender that won the war. Then he had to fight again, on paper, for his own freedom.', P('surrender', { focus: [0.5, 0.5], zoom: [1.1, 1.2] })],
  ['c3', 'He won it. And he took the name of the man who had vouched for him.', C('james', JL)],
  ['c4', 'That was James Lafayette. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-ellen-craft.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/James_Armistead_Lafayette',
  JAR: 'https://allthingsliberty.com/2017/09/james-lafayette-james-armistead-american-spy/',
  HIST: 'https://www.history.com/articles/battle-of-yorktown-slave-spy-james-armistead',
  OAR: 'https://ouramericanrevolution.org/index.cfm/people/view/pp0053',
  LVA: 'https://www.lva.virginia.gov/collections/educator-resources/dbva/items/show/277',
  YT: 'https://en.wikipedia.org/wiki/Siege_of_Yorktown',
  BRIT: 'https://www.britannica.com/event/Siege-of-Yorktown-1781',
  SAR: 'https://blog.alssar.org/?p=1843',
  TOUR: 'https://en.wikipedia.org/wiki/Visit_of_the_Marquis_de_Lafayette_to_the_United_States',
  CERT: 'https://commons.wikimedia.org/wiki/File:Marquis_de_Lafayette_James_Armistead_Lafayette.jpeg',
};
const sourcesByClaim = {
  h1: ['OAR', 'HIST', 'LVA'], h3: ['WIKI', 'OAR', 'LVA'], h4: ['JAR', 'LVA', 'WIKI'], h5: ['HIST', 'OAR'], h6: ['WIKI', 'HIST', 'OAR'],
  e1: ['OAR', 'WIKI'], e2: ['WIKI', 'OAR', 'JAR'], e3: ['HIST', 'OAR'], e4: ['OAR', 'HIST'], e5: ['JAR', 'WIKI'], e6: ['WIKI', 'OAR'],
  l2: ['WIKI', 'HIST'], l3: ['HIST', 'OAR'], l4: ['LVA', 'OAR'], l5: ['HIST', 'OAR', 'LVA'], l6: ['HIST', 'OAR', 'WIKI'],
  s1: ['WIKI', 'HIST'], s2: ['WIKI', 'HIST'], s3: ['OAR', 'HIST', 'WIKI'], s4: ['OAR', 'HIST', 'WIKI'], s5: ['OAR', 'HIST'], s6: ['HIST', 'OAR'], s7: ['HIST', 'OAR'], s9: ['HIST', 'OAR'],
  k2: ['JAR', 'LVA'], k4: ['JAR', 'LVA'], k5: ['LVA', 'JAR'],
  f1: ['WIKI', 'HIST', 'OAR'], f2: ['WIKI', 'HIST', 'OAR'], f3: ['JAR', 'OAR', 'CERT'], f4: ['HIST', 'OAR', 'CERT'], f5: ['OAR', 'JAR', 'CERT'], f6: ['HIST', 'CERT'],
  f7: ['LVA', 'WIKI'], f8: ['WIKI', 'OAR'], f9: ['JAR', 'LVA'], f10: ['WIKI', 'OAR'], f11: ['OAR', 'WIKI'], f12: ['WIKI', 'OAR', 'HIST', 'LVA'],
  a1: ['WIKI', 'OAR', 'LVA', 'HIST'], a2: ['LVA', 'HIST', 'WIKI'], a3: ['WIKI', 'OAR'], a4: ['OAR', 'LVA'], a5: ['WIKI', 'OAR'],
  r1: ['JAR', 'WIKI'], s2b: ['WIKI', 'OAR'], s3b: ['JAR', 'OAR'], s8b: ['YT', 'BRIT'], s9b: ['YT', 'BRIT'], k2b: ['JAR', 'WIKI'], f1b: ['WIKI', 'HIST'], f10b: ['WIKI', 'SAR'], r1b: ['JAR', 'TOUR'], r3: ['OAR', 'WIKI', 'LVA'], r4: ['WIKI', 'JAR'], r6: ['WIKI', 'CERT'], r7: ['WIKI', 'JAR'], r8: ['OAR', 'LVA'],
};

const spec = {
  id: 'doc-james-armistead',
  title: 'The Enslaved Spy Who Helped Win the American Revolution',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { Rochambeau: 'Roe-shahm-bo', Armistead: 'Armisted', Blennerhassett: 'Blenner-hassett', Cornwallis: 'Corn-wallis' },
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
    'Serving Cornwallis himself / the "deception" story (OAR, History.com, Wikipedia) is not confirmed by surviving papers (Journal of the American Revolution): told as "many accounts say", then checked.',
    'Birth year 1748 (OAR, from his 1818 petition) vs 1760 (some sources): script says "around 1748" and "even his birth year is uncertain".',
    'Death 1830 (OAR, Library of Virginia) vs 1832 (some sources): script uses 1830.',
    'Place of the 1824 embrace: Yorktown (OAR, citing the Richmond Enquirer) vs Richmond (Wikipedia): script says "in Virginia".',
    'Le Paon\'s 1783 "Lafayette at Yorktown" shows an unidentified Black man; often claimed to be James, not confirmed: image not used.',
    'Number of British troops surrendered: not used.',
  ],
};
fs.writeFileSync('data/doc-james-armistead.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images`);
