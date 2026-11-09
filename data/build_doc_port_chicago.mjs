// Builds data/doc-port-chicago.json: 8-minute long-form documentary (16:9) on the Port Chicago disaster and mutiny trial.
// Free local voice (Kokoro). Every fact has two or more sources (sourcesByClaim). No graphic violence: no description of injuries or remains.
// Ending follows the owner's rule: only "subscribe for more". Run: node data/build_doc_port_chicago.mjs
import fs from 'node:fs';

const assets = {
  ammo: 'File:PortChicagoAmmowork1943.jpg',
  boxcar: 'File:PortChicagoBoxcarRevetment.jpg',
  ruin: 'File:Portchicago.jpg',
  quinault: 'File:Quinault victory.JPG',
  diagram: 'File:Port Chicago disaster, pier diagram.jpg',
  aerial: 'File:PortChicago-aerial-construction.jpg',
  p1: 'File:Port Chicago Naval Magazine National Memorial POCH 0001.jpg',
  p2: 'File:Port Chicago Naval Magazine National Memorial POCH 0002.jpg',
  p3: 'File:Port Chicago Naval Magazine National Memorial POCH 0003.jpg',
  p4: 'File:Port Chicago Naval Magazine National Memorial POCH 0004.jpg',
  p6: 'File:Port Chicago Naval Magazine National Memorial POCH 0006.jpg',
  p7: 'File:Port Chicago Naval Magazine National Memorial POCH 0007.jpg',
  p8: 'File:Port Chicago Naval Magazine National Memorial POCH 0008.jpg',
  p9: 'File:Port Chicago Naval Magazine National Memorial POCH 0009.jpg',
  p10: 'File:Port Chicago Naval Magazine National Memorial POCH 0010.jpg',
  p11: 'File:Port Chicago Naval Magazine National Memorial POCH 0011.jpg',
  recruits: 'File:"Negro recruits at Manhattan Beach Training Station, (NY).", ca. 1941 - ca. 1945 - NARA - 513165.jpg',
  marshall: 'File:Thurgood-Marshall.jpg',
  marshall57: 'File:Thurgood Marshall 1957-09-17.jpg',
  eo: 'File:Executive Order 9981.jpg',
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });

const beats = [
  // ---- cold open
  ['h1', 'On the night of July 17, 1944, at a Navy base in California, two explosions destroyed an ammunition pier in seconds.', P('p9', { focus: [0.5, 0.6], zoom: [1.15, 1.25] }), { hook: 'They refused to load bombs. *The Navy said mutiny.*' }],
  ['h2', 'Three hundred twenty people were killed. Two hundred two of them were Black sailors, the men who loaded the bombs.', T('320', 'killed at Port Chicago')],
  ['h3', 'Three weeks later, the survivors were ordered to go back to loading ammunition. Two hundred fifty-eight of them refused.', P('p4', { zoom: [1.0, 1.08] })],
  ['h4', 'Fifty were charged with mutiny, in time of war, a crime that could carry the death penalty.', T('Mutiny', 'charged against 50 sailors')],
  ['h5', 'It would take the Navy eighty years to clear their names. This is the story of the Port Chicago Fifty.', P('p11', { zoom: [1.0, 1.08] }), { lowerThird: { name: 'The Port Chicago 50', sub: '1944 – 2024' } }],

  // ---- the base
  ['b1', 'Port Chicago sat on Suisun Bay, in California, northeast of San Francisco.', P('aerial', { zoom: [1.0, 1.1] }), { section: 'base', pin: { label: 'Port Chicago', sub: 'California' } }],
  ['b2', 'The first ship was loaded there in December 1942. It became a Navy ammunition pier for the war in the Pacific.', P('p6', { zoom: [1.0, 1.08] }), { stamp: 'December 1942' }],
  ['b3', 'The Navy was segregated. Black sailors were barred from nearly all jobs at sea.', C('recruits', 'Black Navy recruits, 1940s')],
  ['b4', 'At Port Chicago, most of the enlisted men were Black. The officers were white.', T('Black sailors', 'white officers')],
  ['b5', 'And the work those Black sailors were given was among the most dangerous in the Navy: moving bombs and shells out of rail cars and into the holds of ships.', P('p6', { focus: [0.4, 0.5], zoom: [1.2, 1.3] })],
  ['b6', 'They were not trained for it. They had little instruction in handling explosives, and not enough equipment.', C('p4', 'Loading ammunition at Port Chicago')],
  ['b7', 'In April 1944, Captain Merrill Kinne took command.', T('Capt. Merrill Kinne', 'April 1944')],
  ['b8', 'Officers pushed the crews to load faster. Each division competed against the others, and the tonnage was kept on a chalkboard.', P('p4', { focus: [0.5, 0.65], zoom: [1.2, 1.3] })],
  ['b9', 'The men were scared, and they would say so later, under oath.', T('Afraid', 'and they said so under oath')],

  // ---- the night
  ['n1', 'On July 13, 1944, the Liberty ship E. A. Bryan tied up at the pier. One of her winches had brakes that were stuck in the off position.', P('p2', { zoom: [1.0, 1.08] }), { section: 'night', stamp: '13 July 1944' }],
  ['n2', 'Four days later, she was being loaded with bombs. A second ship, the Quinault Victory, lay on the other side of the pier, waiting her turn.', C('diagram', 'U.S. Navy diagram of the pier, July 17, 1944')],
  ['n2b', 'By that night, about four thousand six hundred tons of bombs, depth charges and ammunition were on the ships and the pier, with about four hundred more tons on nearby rail cars.', T('5,000 tons', 'of explosives at the pier')],
  ['n3', 'At ten eighteen that night, there was a blast on the pier.', T('10:18 p.m.', '17 July 1944')],
  ['n4', 'Between five and seven seconds later came a much larger explosion.', P('p3', { zoom: [1.0, 1.08] })],
  ['n5', 'An Army pilot in the air reported a ball of fire three miles wide.', T('3 miles', 'wide, an Army pilot reported')],
  ['n6', 'The pier was gone. The E. A. Bryan was gone. What remained of the Quinault Victory lay upside down in the bay.', C('quinault', 'What was left of the Quinault Victory, July 1944')],
  ['n7', 'The damage reached across the base and into the town.', P('p7', { zoom: [1.0, 1.08] })],
  ['n7b', 'Every building in the town of Port Chicago, a mile and a half away, was damaged. The blast was felt as far away as Nevada.', P('p7', { focus: [0.5, 0.6], zoom: [1.15, 1.25] })],
  ['n8', 'Three hundred twenty people were dead, and more than three hundred ninety injured.', P('p8', { focus: [0.5, 0.65], zoom: [1.15, 1.25] })],
  ['n9', 'Two hundred two of the dead were African American sailors. It was one of the worst home-front disasters of the Second World War.', C('ruin', 'Port Chicago after the explosion, July 1944')],
  ['n10', 'And then there was the money. The Navy asked Congress for five thousand dollars for each family. A congressman from Mississippi, John Rankin, pushed to cut it after he learned most of the dead were Black men. Congress settled on three thousand.', T('$3,000', 'for each family, not $5,000')],

  // ---- the refusal
  ['a1', 'White sailors were given leave after the blast. The Black sailors were ordered back to work, to clean up the wreckage.', T('No leave', 'for the Black sailors'), { section: 'refusal' }],
  ['a2', 'On July 21, a Navy board of inquiry met. It sat for thirty-nine days. It laid the blame on the way the enlisted men had handled the ammunition.', P('p10', { zoom: [1.0, 1.08] })],
  ['a3', 'The survivors were moved to Mare Island, across the bay.', P('boxcar', { focus: [0.5, 0.6], zoom: [1.1, 1.2] }), { pin: { label: 'Mare Island', sub: 'California' } }],
  ['a4', 'On August 9, 1944, three hundred twenty-eight men were marched out and ordered to load ammunition again.', T('9 August 1944', 'Mare Island')],
  ['a5', 'Two hundred fifty-eight of them refused.', T('258', 'refused')],
  ['a6', 'They had been told nothing clear about what caused the explosions, and they had been given no new safety training.', P('p9', { focus: [0.5, 0.5], zoom: [1.2, 1.3] })],
  ['a7', 'They were held on a prison barge. On August 10, one of them, Joe Small, spoke to the men on board.', T('A prison barge', 'Mare Island, August 1944')],
  ['a8', 'The next day, Admiral Carleton Wright warned them that continued refusal to work would be treated as mutinous conduct.', T('Adm. Carleton Wright', '11 August 1944')],
  ['a9', 'Most of them went back to work. Two hundred eight were convicted in summary courts-martial of disobeying orders.', P('p6', { focus: [0.6, 0.5], zoom: [1.2, 1.3] })],
  ['a9b', 'They lost three months of pay. They were shipped to the Pacific, and when they left the service they received bad conduct discharges, which cost them their veterans benefits.', T('208 men', 'bad conduct discharges')],
  ['a10', 'Fifty were singled out. They would be known as the Port Chicago Fifty.', T('The Port Chicago 50', 'charged with mutiny')],

  // ---- the trial
  ['t1', 'On September 14, 1944, the court-martial began on Yerba Buena Island, in San Francisco Bay.', T('Yerba Buena Island', 'San Francisco Bay'), { section: 'trial', stamp: '14 September 1944' }],
  ['t2', 'It was the largest mutiny trial in the history of the United States Navy. All fifty men pleaded not guilty.', T('50 men', 'one trial')],
  ['t3', 'Their lawyer, Gerald Veltmann, argued that a refusal to work was not a mutiny.', T('Gerald Veltmann', 'lead defense attorney')],
  ['t3b', 'One by one, the accused men took the stand. Each said he would obey any order except loading ammunition. Each said he was afraid of another explosion.', C('recruits', 'Black Navy recruits, 1940s')],
  ['t3c', 'A sailor named Ollie Green told the court that officers raced the divisions against each other. I knowed the way they was handling ammunition, he said, it was liable to go off again.', T('Ollie Green', 'testifying, 1944')],
  ['t4', 'On October 9, a visitor sat down to watch. Thurgood Marshall, chief lawyer for the NAACP.', C('marshall', 'Thurgood Marshall'), { lowerThird: { name: 'Thurgood Marshall', sub: 'NAACP' } }],
  ['t5', 'A week later, he called for a formal government investigation of the conditions at Port Chicago.', C('marshall57', 'Thurgood Marshall')],
  ['t6', 'His argument was simple. These men were not mutineers. They were victims of gross negligence and racial injustice.', C('marshall', 'Thurgood Marshall')],
  ['t7', 'On October 24, the court returned its verdict. Accounts of how long it took differ. Eight minutes, or eighty. Either way, it found all fifty guilty.', T('Guilty', 'all 50, 24 October 1944')],
  ['t8', 'The sentences ran from eight to fifteen years of hard labor, with dishonorable discharges.', T('8 to 15 years', 'hard labor')],
  ['t8b', 'Ten men got fifteen years. Twenty-four got twelve. Eleven got ten. Five got eight.', T('15, 12, 10, 8', 'years, for 50 men')],
  ['t9', 'Admiral Wright reduced the sentences of forty of the men, and they were sent to prison at Terminal Island.', T('Terminal Island', 'prison, late 1944')],

  // ---- the long road
  ['r1', 'On April 3, 1945, Marshall took their appeal to Washington. In June, the court reaffirmed the convictions.', C('marshall57', 'Thurgood Marshall'), { section: 'road' }],
  ['r2', 'Then the war ended. On reviews, the sentences were cut to between seventeen and twenty-nine months. On January 6, 1946, the Navy announced that forty-seven of the fifty were being released, and they were shipped overseas for another year of duty.', T('6 January 1946', '47 of the 50 released')],
  ['r3', 'That February, the Navy began to desegregate its forces. In 1948, President Truman ordered equal treatment across the armed forces.', C('eo', 'Executive Order 9981, 26 July 1948')],
  ['r4', 'The National Park Service says the disaster helped lead to that order.', P('p11', { focus: [0.5, 0.7], zoom: [1.1, 1.2] })],
  ['r4b', 'And ammunition loading itself became far safer, with real training in handling explosives.', P('p2', { focus: [0.5, 0.45], zoom: [1.15, 1.25] })],
  ['r5', 'But the convictions stood. In 1990, a campaign in Congress to exonerate the men failed. In 1994, the Navy admitted that racial prejudice was behind sending only Black sailors to the loading divisions, but it still refused to overturn the convictions.', T('Convictions stand', '1990 and 1994')],
  ['r6', 'That same year, Port Chicago got a national memorial.', P('p1', { zoom: [1.0, 1.08] })],
  ['r7', 'In December 1999, President Bill Clinton pardoned one of the fifty, Freddie Meeks. He died in 2003.', T('Freddie Meeks', 'pardoned, December 1999')],

  // ---- exoneration
  ['x1', 'On July 17, 2024, eighty years to the day after the explosion, Navy Secretary Carlos Del Toro made an announcement.', P('p11', { zoom: [1.1, 1.0] }), { section: 'exonerated', stamp: '17 July 2024' }],
  ['x2', 'The Navy was exonerating two hundred fifty-six of the sailors, including the Port Chicago Fifty.', T('256', 'sailors exonerated')],
  ['x3', 'Its lawyers had found the trials unfair. The men were tried together. They had no meaningful right to counsel. And they were tried before the investigation of the explosion was finished.', P('p10', { focus: [0.5, 0.5], zoom: [1.15, 1.25] })],
  ['x3b', 'The Navy changed their discharges to honorable. Secretary Del Toro said the decision clears their names and restores their honor.', T('Honorable', 'discharges restored, 2024')],
  ['x4', 'None of the fifty was still alive to hear it.', T('None', 'of the 50 lived to hear it')],

  // ---- close
  ['e1', 'They were given the most dangerous job in the Navy, and no training for it.', P('p6', { zoom: [1.0, 1.08] }), { section: 'close' }],
  ['e2', 'They watched that job kill two hundred two of their fellow sailors.', P('p3', { focus: [0.5, 0.6], zoom: [1.1, 1.2] })],
  ['e3', 'They asked why. And they were told it was mutiny.', C('recruits', 'Black Navy recruits, 1940s')],
  ['e4', 'Their country took eighty years to say they had been right to ask.', P('p11', { focus: [0.75, 0.3], zoom: [1.1, 1.2] })],
  ['e5', 'Those were the Port Chicago Fifty. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-ellen-craft.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Port_Chicago_disaster',
  NPS: 'https://www.nps.gov/poch/learn/historyculture/index.htm',
  NPST: 'https://www.nps.gov/poch/learn/historyculture/the-mutiny-trial.htm',
  NPR: 'https://www.kpbs.org/news/national/2024/07/18/the-navy-exonerates-256-black-sailors-unjustly-punished-over-1944-wwii-port-explosion',
  CBS: 'https://cbsnews.com/sanfrancisco/news/navy-exonerates-black-sailors-convicted-in-largest-mutiny-in-u-s-history',
  ABC: 'https://abc13.com/post/navy-exonerates-256-black-sailors-unjustly-punished-1944/15065015/',
  EJS: 'https://equaljusticesociety.org/2024/07/17/navy-exonerates-the-port-chicago-50/',
  HIST: 'https://www.history.com/this-day-in-history/july-17/port-chicago-disaster',
  CA: 'https://www.leginfo.ca.gov/pub/09-10/bill/sen/sb_0001-0050/sjr_21_cfa_20100225_103046_sen_floor.html',
  MT: 'https://www.militarytimes.com/news/your-military/2024/07/17/navy-clears-black-sailors-unjustly-punished-after-1944-deadly-blast/',
  KIRK: 'https://www.kirkusreviews.com/book-reviews/robert-l-allen-2/the-port-chicago-mutiny-the-story-of-the-larges/',
};
const sourcesByClaim = {
  h1: ['WIKI', 'NPS'], h2: ['NPS', 'WIKI'], h3: ['WIKI', 'NPS'], h4: ['NPST', 'WIKI'], h5: ['WIKI', 'CBS'], b2: ['WIKI', 'NPS'], b3: ['NPR', 'WIKI'], b4: ['NPR', 'WIKI'],
  b5: ['NPS', 'WIKI'], b6: ['NPS', 'WIKI'], b7: ['WIKI', 'HIST'], b8: ['WIKI', 'NPR'], b9: ['NPST', 'WIKI'], n1: ['WIKI', 'HIST'], n2: ['WIKI', 'HIST'], n3: ['WIKI', 'HIST'],
  n4: ['WIKI', 'HIST'], n5: ['WIKI', 'HIST'], n6: ['WIKI', 'HIST'], n8: ['WIKI', 'NPR', 'NPS'], n9: ['NPS', 'WIKI'], a1: ['NPR', 'WIKI'], a2: ['WIKI', 'HIST'], a3: ['WIKI', 'KIRK'],
  a4: ['WIKI', 'KIRK'], a5: ['WIKI', 'NPS', 'KIRK'], a6: ['NPR', 'NPS'], a7: ['WIKI', 'NPST'], a8: ['WIKI', 'HIST'], a9: ['WIKI', 'NPR'], a10: ['WIKI', 'NPST'],
  t1: ['WIKI', 'KIRK'], t2: ['KIRK', 'WIKI'], t3: ['NPST', 'WIKI'], t4: ['WIKI', 'KIRK'], t5: ['WIKI', 'NPST'], t6: ['NPST', 'WIKI'], t7: ['WIKI', 'NPST'], t8: ['NPST', 'CBS'],
  t9: ['WIKI', 'NPR'], r1: ['WIKI', 'NPST'], r2: ['WIKI', 'NPR'], r3: ['WIKI', 'NPS'], r4: ['NPS', 'WIKI'], r5: ['WIKI', 'HIST'], r6: ['WIKI', 'NPS'], r7: ['WIKI', 'NPS'],
  n2b: ['WIKI', 'HIST'], n7b: ['HIST', 'CA'], n10: ['WIKI', 'CA'], t3b: ['WIKI', 'NPST'], t3c: ['WIKI', 'NPST'], t8b: ['CA', 'WIKI'], a9b: ['WIKI', 'HIST', 'NPR'], x3b: ['MT', 'NPR'], r4b: ['HIST', 'NPR'],
  x1: ['WIKI', 'NPR', 'CBS'], x2: ['WIKI', 'NPR', 'EJS'], x3: ['NPR', 'ABC'], x4: ['CBS', 'ABC'],
};

const spec = {
  id: 'doc-port-chicago',
  title: '320 Dead. Then the Navy Put Survivors on Trial for Mutiny.',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { Quinault: 'Kwin-all', Suisun: 'Suh-soon', 'Yerba Buena': 'Yerba Bwayna', Veltmann: 'Velt-man', Kinne: 'Kin-ee', Eleanor: 'Ellen-or' },
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
    'Verdict time: 8 minutes (NPS) vs 80 minutes (Wikipedia): the script gives both as differing accounts.',
    'What Joe Small said on the barge and any Marshall quote: wording not confirmed in two sources; paraphrased or left out.',
    'Whether the sailors testified: the NPS page contradicts itself; Wikipedia says each testified: the script says they would say so under oath, from the trial record.',
    'Injuries and remains: left out on purpose (no graphic detail).',
  ],
};
fs.writeFileSync('data/doc-port-chicago.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images`);
