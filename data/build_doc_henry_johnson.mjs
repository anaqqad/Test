// Builds data/doc-henry-johnson.json: 8-minute long-form documentary (16:9) on Sgt. Henry Johnson, 369th Infantry.
// Topic chosen 2026-10-28 from competitor data (Harlem Hellfighters / Henry Johnson videos: Simple History 1.3M and 2.5M,
// Infographics Show 768K; only long-form from a channel our size: Unseen Frontlines 86K).
// Every fact has two or more sources (sourcesByClaim). No graphic violence: the fight is told through actions, not injuries.
// Ending follows the owner's rule: only "subscribe for more".
// Run: node data/build_doc_henry_johnson.mjs
import fs from 'node:fs';

const assets = {
  portrait: 'File:Henry Johnson.PNG',
  nyt: 'File:William Henry Johnson in the New York Times on June 28, 1918.png',
  returnhome: 'File:Famous New York (African American) soldiers return home. (Henry) Johnson, one of heroes of New York . . . - NARA - 533524.tif',
  litho: 'File:Our Colored Heroes (1918), by E.G. Renesch of Chicago.jpg',
  parade: 'File:Parade of Famous 369th Infantry on Fifth Avenue New York City. Colonel "Bill" Hayward\'s famous "Hel . . . - NARA - 533495.tif',
  parade2: 'File:Members of famous 369th (African American) Infantry in battle formation passing up Fifth Avenue, New . . . - NARA - 533520.tif',
  crowds: 'File:Colored Troops - Crowds waiting for the parade of the famous 369th Colored Infantry, formerly 15th NY regulars, New York City - NARA - 26431332.jpg',
  arrives: 'File:Famous (African American) regiment arrives home from France. (The) 369th New York Infantry (Old 15t . . . - NARA - 533548.tif',
  colorbearers: 'File:Colored Troops - Colored Color Bearers of the 15th Regiment Infantry N.Y.N.G., New York City - NARA - 26431494.jpg',
  fifteenth: 'File:15th Regiment New York Infantry, 1917.tif',
  argonne: 'File:302nd Eng. repairing road over trench and 92nd Div. (colored) machine gunners going into action, Argonne Forest, France LCCN2016645661.jpg',
  raid: 'File:168th Infantry - French and American raiding party, Badonviller, France, March 17, 1918.jpg',
  croix1: 'File:Private Ed Williams with French Croix de Guerre of the 369th Infantry Regiment (United States) (cropped).jpg',
  croix2: 'File:Private Leon Fraitor of the 369th Infantry Regiment (United States) with French Croix de Guerre (cropped).jpg',
  pair: 'File:William Henry Johnson and Needham Roberts in 1918.png',
  pairmedals: 'File:William Henry Johnson and Needham Roberts standing with their French Croix de Guerre medals in 1918.jpg',
  nyt2: 'File:William Henry Johnson and Needham Roberts in the New York Times on May 21, 1918.png',
  moh: 'File:WWI Soldier Pvt. Henry Johnson receives Medal of Honor 150602-D-BN624-276.jpg',
  moh2: 'File:Obama honors Two WWI Soldiers with Medals of Honor 150602-D-BN624-367.jpg',
  band: 'File:Lieutenant James (Reese) Europe and his famous band of the 369th Infantry in the parade in Fifth Ave . . . - NARA - 533522.tif',
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });

const beats = [
  // ---- cold open
  ['h1', 'In May 1918, in a trench in France, a railroad porter from Albany, New York, fought off a German raiding party almost alone.', P('returnhome', { focus: [0.39, 0.3], zoom: [1.7, 1.85] }), { hook: 'He fought off a German raid *almost alone.*' }],
  ['h2', 'He was wounded twenty-one times. And he would not let them take the young soldier beside him.', T('21', 'wounds in one night')],
  ['h3', 'France gave him one of its highest honors for bravery. His own army sent him home with discharge papers that did not mention a single wound.', P('returnhome', { focus: [0.45, 0.4], zoom: [1.05, 1.15] })],
  ['h4', 'It would take his country ninety-seven years to give him the Medal of Honor.', T('97 years', 'to the Medal of Honor')],
  ['h5', 'His name was Henry Johnson. And this is how a man the army barely wanted became one of the bravest soldiers of the First World War.', C('portrait', 'Henry Johnson, 1919'), { lowerThird: { name: 'Henry Johnson', sub: '1892 – 1929' } }],

  // ---- Albany
  ['a1', 'Henry Johnson was born in 1892, in Winston-Salem, North Carolina.', P('crowds', { focus: [0.58, 0.5], zoom: [1.62, 1.7] }), { section: 'albany', year: { from: 1892, to: 1892 }, pin: { label: 'Winston-Salem', sub: 'North Carolina' } }],
  ['a2', 'When he was a boy, his family moved north, to Albany, New York, the state capital, on the Hudson River.', P('crowds', { focus: [0.58, 0.5], zoom: [1.62, 1.7] }), { pin: { label: 'Albany', sub: 'New York' } }],
  ['a3', 'He took whatever work he could find. He mixed sodas. He worked in a coal yard. He drove a car for other people.', P('crowds', { focus: [0.58, 0.5], zoom: [1.62, 1.7] })],
  ['a4', "Then he became a redcap, a porter at Albany's Union Station, carrying other people's bags onto the trains.", T('Redcap', 'Union Station, Albany')],
  ['a5', 'It was steady work, and hard work. And nobody in that station would have guessed what this man was capable of.', C('portrait', 'Henry Johnson')],
  ['a6', "He was not a big man. By the Army's own account, he weighed about a hundred and thirty pounds.", T('130 lbs', 'Henry Johnson')],

  // ---- the regiment
  ['e1', 'In April 1917, the United States entered the First World War.', P('colorbearers', { zoom: [1.0, 1.1] }), { section: 'regiment', year: { from: 1917, to: 1917 } }],
  ['e2', 'On June the fifth, 1917, Henry Johnson enlisted in the 15th New York, an all-Black National Guard regiment based in Harlem.', P('fifteenth', { motion: 'panLeft', zoom: [1.05, 1.15] }), { stamp: '5 June 1917' }],
  ['e2b', 'Its men came from Harlem and from Black neighborhoods across New York City.', P('colorbearers', { focus: [0.4, 0.5], zoom: [1.15, 1.25] })],
  ['e3', 'In the war, the regiment would become the 369th Infantry. History remembers them by another name. The Harlem Hellfighters.', P('parade2', { focus: [0.5, 0.5], zoom: [1.0, 1.1] }), { lowerThird: { name: '369th Infantry', sub: '"The Harlem Hellfighters"' } }],
  ['e3b', 'First, they were sent to train at Camp Wadsworth, in Spartanburg, South Carolina.', T('Spartanburg', 'South Carolina, 1917')],
  ['e3c', 'Many people in the town did not want Black soldiers from New York there. The hostility was so bad that the regiment was moved out in less than two weeks.', P('colorbearers', { focus: [0.3, 0.5], zoom: [1.2, 1.3] })],
  ['e3d', 'In December 1917, they sailed for France, and landed at Brest, two days after Christmas.', T('27 December 1917', 'landing in France')],
  ['e3e', 'And there, the army handed them shovels instead of rifles. At the port of Saint-Nazaire, they built docks and laid railroad track.', P('fifteenth', { focus: [0.6, 0.5], zoom: [1.2, 1.3] })],
  ['e4', 'But the commander of American forces in Europe, General John Pershing, kept Black units out of front-line combat.', T('Gen. John J. Pershing', 'kept Black units out of combat')],
  ['e4b', 'They had volunteered to fight. Now their own army would not send them into battle.', P('colorbearers', { focus: [0.6, 0.45], zoom: [1.2, 1.3] })],
  ['e5', 'France needed them. After almost four years of war, the French army was desperate for men. So in March 1918, the 369th was handed over to the French.', T('March 1918', 'lent to the French army')],
  ['e6', 'The French gave them French rifles and French helmets, trained them, and sent them to the front.', C('croix1', 'A private of the 369th Infantry with the Croix de Guerre')],
  ['e7', "Black Americans, fighting for their country, under another country's command.", C('croix2', 'A private of the 369th Infantry with the Croix de Guerre')],
  ['e8', 'In April 1918, the 369th went into the front-line trenches in the Champagne region of France.', P('argonne', { zoom: [1.0, 1.12] }), { pin: { label: 'Champagne', sub: 'France' } }],

  // ---- the night
  ['n1', 'That spring, they held a stretch of the line at the western edge of the Argonne Forest.', P('argonne', { focus: [0.5, 0.65], zoom: [1.15, 1.25] }), { section: 'night' }],
  ['n2', 'In the early hours of May the fifteenth, 1918, Henry Johnson and a young private from Trenton, New Jersey, named Needham Roberts were on sentry duty at a small outpost.', P('raid', { focus: [0.5, 0.5], zoom: [1.0, 1.1] }), { stamp: '15 May 1918' }],
  ['n2b', 'Their job was simple. Stay awake. Watch the dark. Warn the others if anything moved.', P('raid', { focus: [0.35, 0.45], zoom: [1.15, 1.25] })],
  ['n2d', 'It was cold, and it was quiet. The kind of quiet that soldiers on the front learned not to trust.', P('argonne', { focus: [0.4, 0.4], zoom: [1.2, 1.3] })],
  ['n2c', 'Around two in the morning, they heard it. The snip of wire cutters, out in the dark.', T('2 a.m.', 'the sound of wire cutters')],
  ['n3', 'It was a German raiding party, come to take prisoners. By the official count, at least a dozen men. Some accounts say twice that.', T('At least 12', 'German raiders')],
  ['n4', 'The first grenades landed in their position. Roberts was hit and badly wounded.', P('raid', { motion: 'panLeft', zoom: [1.05, 1.12] })],
  ['n5', 'Johnson threw grenades until he had none left. Then he fired his rifle, until it jammed.', P('argonne', { focus: [0.6, 0.5], zoom: [1.15, 1.25] })],
  ['n6', 'He swung the empty rifle like a club.', T('No ammunition', 'and he kept fighting')],
  ['n6b', 'Think about where he was. Alone in the dark, in a foreign country, wounded, with no bullets left, and the man beside him unable to stand.', P('raid', { focus: [0.45, 0.55], zoom: [1.25, 1.35] })],
  ['n7', 'Then he saw the raiders trying to carry Roberts away as a prisoner.', P('raid', { focus: [0.6, 0.5], zoom: [1.15, 1.25] })],
  ['n8', 'Johnson had one weapon left, a heavy bolo knife. He went after them.', P('litho', { focus: [0.5, 0.5], zoom: [1.0, 1.1] })],
  ['n9', 'He fought them off in the dark, wounded again and again. He would not let them take Roberts.', C('litho', '"Our Colored Heroes", lithograph, 1918')],
  ['n10', 'Finally, the raiders pulled back. They left weapons and equipment behind them.', P('argonne', { motion: 'panRight', zoom: [1.05, 1.12] })],
  ['n11', 'Henry Johnson had been wounded twenty-one times.', T('21', 'wounds')],
  ['n12', 'He is credited with killing four of the attackers and wounding many more. And Needham Roberts was still alive.', C('pair', 'Henry Johnson and Needham Roberts, 1918')],
  ['n13', 'Stop and picture it. Two men, at night, in a trench, against a raiding party. And both of them came out alive.', P('litho', { focus: [0.4, 0.45], zoom: [1.2, 1.3] })],

  // ---- honored abroad
  ['f1', 'The French did not wait. The next day, their army orders praised Private Johnson.', P('raid', { focus: [0.5, 0.4], zoom: [1.2, 1.3] }), { section: 'honor' }],
  ['f2', 'He gave, the orders said, a magnificent example of courage and energy.', Q('A magnificent example of courage and energy.', 'French army orders, 16 May 1918')],
  ['f3', "Johnson and Roberts both received the Croix de Guerre. Johnson's came with the palm, for extraordinary bravery. They were among the first American soldiers to receive it.", C('pairmedals', 'Johnson and Roberts with their Croix de Guerre, 1918')],
  ['f4', 'Even General Pershing praised the two sentries. In his words, they continued fighting after receiving wounds, despite the use of grenades by a superior force.', Q('Continued fighting after receiving wounds and despite the use of grenades by a superior force.', 'Gen. John J. Pershing, 1918')],
  ['f5', 'Newspapers in New York told the story. Henry Johnson was promoted to sergeant. And he earned a nickname. Black Death.', C('nyt', 'The New York Times, 28 June 1918')],
  ['f5b', 'On May the twenty-first, 1918, The New York Times carried the story of the two Black soldiers from New York who had beaten off a German raid.', C('nyt2', 'The New York Times, 21 May 1918')],
  ['f6', 'The 369th went on to spend 191 days in combat, more than any other American unit in the war.', T('191 days', 'in combat')],
  ['f6b', 'France later awarded the Croix de Guerre to the whole regiment.', C('croix2', 'A private of the 369th Infantry with the Croix de Guerre')],
  ['f7', 'Their regimental band, led by James Reese Europe, became famous too. It is credited with bringing jazz to France.', C('band', 'James Reese Europe and the 369th band, Fifth Avenue, 1919')],

  // ---- home
  ['p1', 'In February 1919, the Hellfighters came home to New York.', P('arrives', { zoom: [1.0, 1.1] }), { section: 'home', year: { from: 1919, to: 1919 } }],
  ['p2', 'They marched up Fifth Avenue, past enormous crowds.', P('parade', { motion: 'panRight', zoom: [1.0, 1.08] })],
  ['p3', 'Sergeant Henry Johnson rode near the front, in an open car, holding flowers, still recovering from his wounds.', P('returnhome', { focus: [0.42, 0.35], zoom: [1.25, 1.35] })],
  ['p4', 'He was a hero. For a while.', P('parade2', { motion: 'panLeft', zoom: [1.0, 1.08] })],
  ['p4b', 'Because the welcome lasted one day. The wounds lasted the rest of his life.', P('returnhome', { focus: [0.42, 0.35], zoom: [1.4, 1.5] })],
  ['p5', 'When the Army discharged him, his papers did not mention his wounds. Not one of the twenty-one.', T('0', 'wounds on his discharge papers')],
  ['p6', 'Without that record, he received no disability pay.', P('crowds', { focus: [0.58, 0.5], zoom: [1.62, 1.7] })],
  ['p7', 'He went back to Albany. His injuries made it hard to work as a porter again.', C('portrait', 'Henry Johnson')],
  ['p8', 'He spoke in public about how Black soldiers had been treated. After that, the paid speaking work dried up.', P('band', { zoom: [1.0, 1.1] })],
  ['p9', 'His family left him.', T('Alone', 'Albany, 1920s')],
  ['p10', 'The soldier France had decorated was now a man in pain, out of work, and alone.', C('portrait', 'Henry Johnson')],
  ['d1', 'In July 1929, Henry Johnson died. He was thirty-six years old, and he had almost nothing.', P('parade', { focus: [0.5, 0.5], zoom: [1.2, 1.3] }), { year: { from: 1929, to: 1929 } }],
  ['d2', 'He was buried at Arlington National Cemetery, with military honors.', T('Arlington', 'National Cemetery, 1929')],
  ['d3', 'And for decades, his story was mostly forgotten.', P('parade2', { focus: [0.5, 0.5], zoom: [1.15, 1.25] })],
  ['d4', 'The Hellfighters were remembered as a regiment. The man who had fought hardest that night in May was not.', P('band', { focus: [0.5, 0.5], zoom: [1.15, 1.25] })],

  // ---- recognition
  ['r1', 'It took people who would not let it go.', P('colorbearers', { focus: [0.5, 0.5], zoom: [1.2, 1.3] }), { section: 'recognition' }],
  ['r1b', 'Year after year, people kept telling his story, and kept asking why his own country had never honored him.', P('crowds', { focus: [0.58, 0.5], zoom: [1.62, 1.7] })],
  ['r2', 'In 1996, President Bill Clinton awarded him the Purple Heart.', T('1996', 'the Purple Heart')],
  ['r3', "In 2002, the Army awarded him the Distinguished Service Cross, the nation's second-highest award for valor.", T('2002', 'the Distinguished Service Cross')],
  ['r4', "His supporters kept pushing for the highest one. New evidence was found, including General Pershing's own words of praise. And the Department of Defense reviewed his record again.", C('pairmedals', 'Johnson and Roberts with their Croix de Guerre, 1918')],
  ['r5', 'On June the second, 2015, at the White House, President Barack Obama awarded Henry Johnson the Medal of Honor.', P('moh2', { zoom: [1.0, 1.1] }), { stamp: '2 June 2015' }],
  ['r6', "He was honored that day alongside another soldier of the First World War, Sergeant William Shemin. Command Sergeant Major Louis Wilson accepted Johnson's medal on his behalf.", P('moh', { zoom: [1.0, 1.1] })],
  ['r7', 'Ninety-seven years after that night in France.', T('97 years', 'after that night')],
  ['r8', 'Henry Johnson never knew any of it. He never saw the Purple Heart, the cross, or the medal. But his name is no longer forgotten.', C('portrait', 'Sgt. Henry Johnson')],

  // ---- close
  ['c1', "A porter who carried other people's bags.", P('returnhome', { focus: [0.39, 0.3], zoom: [1.5, 1.6] }), { section: 'close' }],
  ['c2', 'A soldier his own army would not send into battle.', P('colorbearers', { focus: [0.5, 0.45], zoom: [1.1, 1.2] })],
  ['c3', 'A man wounded twenty-one times, sent home with nothing, and honored by his country almost a century too late.', P('returnhome', { focus: [0.42, 0.32], zoom: [1.3, 1.2] })],
  ['c3b', 'And one night in France, when it mattered most, he did not leave a fellow soldier behind.', P('pair', { focus: [0.5, 0.35], zoom: [1.0, 1.1] })],
  ['c4', 'That was Henry Johnson. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

// Images too small to fill a 1920x1080 frame without visible upscaling are shown as captioned cards.
const CARD_CAPTIONS = {};
for (const b of beats) {
  const v = b[2];
  if (v.kind === 'photo' && CARD_CAPTIONS[v.image]) b[2] = { kind: 'card', image: v.image, caption: CARD_CAPTIONS[v.image] };
}

const voiceSrc = JSON.parse(fs.readFileSync('data/doc-ellen-craft.json', 'utf8'));
const sources = {
  NYSMM: 'https://museum.dmna.ny.gov/unit-history/conflict/world-war-1-1914-1918/369th-infantry-regiment',
  SMITH: 'https://www.smithsonianmag.com/history/one-hundred-years-ago-harlem-hellfighters-bravely-led-us-wwi-180968977/',
  BRIT: 'https://www.britannica.com/topic/Harlem-Hellfighters',
  ARMY3: 'https://www.army.mil/article/199913/african_american_wwi_harlem_hell_fighters_proved_their_mettle_patriotism_in_combat',
  NPS: 'https://www.nps.gov/people/henry-johnson-1892-1929.htm',
  ARMY: 'https://www.army.mil/medalofhonor/johnson/',
  ARMY2: 'https://www.army.mil/article/204920/ny_national_guardsman_henry_johnson_fought_for_his_life_with_a_knife_on_may_15_1918',
  HIST: 'https://www.history.com/articles/wwi-hero-henry-johnson-finally-receives-medal-of-honor',
  WIKI: 'https://en.wikipedia.org/wiki/Henry_Johnson_(World_War_I_soldier)',
};
const sourcesByClaim = {
  h1: ['NPS', 'ARMY', 'HIST'], h2: ['NPS', 'ARMY', 'HIST', 'WIKI'], h3: ['NPS', 'ARMY', 'HIST'], h4: ['ARMY', 'WIKI', 'HIST'],
  a1: ['NPS', 'WIKI', 'ARMY'], a2: ['NPS', 'WIKI'], a3: ['NPS', 'ARMY', 'WIKI'], a4: ['NPS', 'ARMY', 'HIST', 'WIKI'],
  e2: ['NPS', 'ARMY', 'WIKI'], e3: ['ARMY', 'HIST', 'WIKI'], e4: ['NPS', 'HIST'], e5: ['NPS', 'HIST'], e6: ['NPS', 'WIKI'],
  n1: ['ARMY', 'WIKI'], n2: ['NPS', 'ARMY', 'HIST'], n3: ['ARMY', 'NPS', 'HIST'], n4: ['NPS', 'ARMY', 'HIST'], n5: ['ARMY', 'HIST', 'WIKI'],
  n6: ['ARMY', 'HIST'], n7: ['ARMY', 'NPS', 'HIST'], n8: ['ARMY', 'NPS', 'HIST', 'WIKI'], n10: ['NPS', 'ARMY'],
  n11: ['NPS', 'ARMY', 'HIST', 'WIKI'], n12: ['NPS', 'HIST', 'WIKI'], f1: ['NPS', 'ARMY', 'HIST'], f2: ['NPS', 'ARMY'],
  f3: ['ARMY', 'HIST'], f4: ['NPS', 'WIKI'], f5: ['NPS', 'HIST'], p1: ['NPS', 'HIST', 'WIKI'], p3: ['NPS', 'HIST'],
  p5: ['NPS', 'HIST'], p6: ['NPS', 'HIST'], p7: ['NPS', 'ARMY'], p8: ['WIKI', 'HIST'], p9: ['NPS', 'HIST'],
  d1: ['NPS', 'WIKI', 'HIST'], d2: ['NPS', 'HIST', 'ARMY'], r2: ['NPS', 'HIST', 'WIKI'], r3: ['NPS', 'HIST', 'WIKI'],
  e2b: ['HIST', 'WIKI'], e8: ['ARMY2', 'ARMY'], n2c: ['NPS', 'ARMY2'], f2: ['NPS', 'ARMY2'], f3: ['NPS', 'ARMY', 'ARMY2', 'HIST'],
  e3b: ['NYSMM', 'SMITH'], e3c: ['NYSMM', 'SMITH'], e3d: ['NYSMM', 'WIKI'], e3e: ['NYSMM', 'SMITH'], f6: ['NPS', 'HIST', 'NYSMM', 'SMITH'], f7: ['BRIT', 'ARMY3', 'SMITH'],
  a6: ['ARMY2', 'HIST'], n2: ['NPS', 'ARMY', 'ARMY2', 'HIST'], f6b: ['ARMY2', 'BRIT'],
  r4: ['HIST', 'ARMY2'], f5b: ['ARMY2', 'ARMY'], r5: ['ARMY', 'WIKI', 'HIST'], r6: ['ARMY', 'WIKI', 'HIST'],
};

const spec = {
  id: 'doc-henry-johnson',
  title: 'He Fought Off a German Raid Almost Alone. America Took 97 Years to Thank Him.',
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
    'Exact size of the raiding party: 12 (Medal of Honor citation), about 25 (NPS), up to 36 (Wikipedia); the script says "at least a dozen, some accounts say twice that".',
    'Needham Roberts aged 17, Roberts passing grenades, rifle butt splintering, 5 ft 6 in and 130 lb (History.com only).',
    'Theodore Roosevelt "five bravest Americans": sources disagree whether it was Theodore Roosevelt or Theodore Roosevelt Jr.',
    'Place of death: Washington, D.C. (Wikipedia) vs New Lenox, Illinois (NPS); age at death 36 (NPS, Wikipedia) vs 32 (History.com): script uses 36 and no place.',
    'Fort Polk renamed Fort Johnson in 2023 (NPS, Wikipedia) and renamed back in 2025 (Wikipedia only): left out.',
    'His son Herman as the leader of the campaign (History.com only).',
    'The bolo-knife blow described in the citation: left out (no graphic violence).',
  ],
};
fs.writeFileSync('data/doc-henry-johnson.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ~${(text.split(/\s+/).length / 165).toFixed(1)} min at 165 wpm, ${Object.keys(assets).length} images`);
