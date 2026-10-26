// Builds data/doc-robert-smalls.json: the 8-minute long-form documentary (16:9) on Robert Smalls.
// Every fact comes from the sourced podcast fact sheet (data/podcast-ep02-robert-smalls-andrew.json, "sources")
// and the reel fact sheet (data/reel-robert-smalls.json, "facts"), each fact with two or more sources.
// Run: node data/build_doc_robert_smalls.mjs
import fs from 'node:fs';

const assets = {
  // already downloaded for the reel (copied from public/pd/reel-robert-smalls)
  portrait: 'File:Robert Smalls - Brady-Handy.jpg',
  mc: 'File:Robert Smalls, S.C. M.C. Born in Beaufort, SC, April 1839 Trim.jpg',
  heroes: 'File:Heroes in Ebony-The captors of the Rebel steamer Planter, Robert Small, W. Morrison, A. Gradine and John Small LCCN99403228.jpg',
  harpers: 'File:Robert Smalls, captain of the gun-boat "Planter" The gun-boat "Planter," run out of Charleston, S.C., by Robert Smalls, May 1862. LCCN97512451.jpg',
  gunboat: 'File:Gunboat Planter.png',
  planter: 'File:USS Planter 1860s.jpg',
  sumter: 'File:Fort Sumter - 1861.jpg',
  harbor1865: "File:Fort Sumter, in Charleston Harbor - Harper's weekly 1865.jpg",
  house: 'File:SOUTH (FRONT) ELEVATION - McKee-Smalls House, 511 Prince Street, Beaufort, Beaufort County, SC HABS SC,7-BEAUF,32-2.tif',
  // new for the documentary
  plantation: "File:Five generations on Smith's Plantation, Beaufort, South Carolina LCCN98504449.jpg",
  wharf: 'File:View of boats and ships at wharf, Charleston, South Carolina LCCN90713000.jpg',
  steamers: 'File:Charleston, South Carolina (vicinity).) Steamers at wharf LOC cwpb.03212.jpg',
  harbormap: 'File:Charleston Harbor and its approaches. 1863.jpg',
  bombard: 'File:Bombardment of Fort Sumter by the batteries of the Confederate states, April 13, 1861 LCCN2013646579.jpg',
  pinckney: 'File:Castle Pinckney - showing early light beacon.jpg',
  blockade: 'File:The blockade of Charleston LCCN00652823.jpg',
  saxton: 'File:Gen. Rufus Saxton - NARA - 528079.jpg',
  stanton: 'File:Edwin M. Stanton, Secretary of War - NARA - 528682 (page 2) (3x4a).jpg',
  keokuk: 'File:USS Keokuk h59546.jpg',
  keokukiln: 'File:The Civil War in America - The Federal Ironclad Keokuk as she appeared the morning after the fight - ILN 1863 (cropped).jpg',
  ruins: 'File:Ruins in Charleston, South Carolina by George N. Barnard - crop.jpg',
  radical: 'File:Radical members of the first legislature after the war, South Carolina LCCN97504690.jpg',
  tillman: 'File:Benjamin Tillman cph.3a02079.jpg',
  signature: 'File:Signature of Robert Smalls.png',
};

// [id, text, visual, overlays?, extra?]  visual shorthand: 'p:key' photo, 'c:key' card, 'm:step' map,
// 'ch:N|Title' chapter card, 't:Big|sub' title card, 'end'.
const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const M = (step) => ({ kind: 'map', step });
const CH = (num, title) => ({ kind: 'chapter', num, title });
const T = (title, sub) => ({ kind: 'title', title, sub });

const beats = [
  // ---- cold open (0:00-0:40)
  ['hook1', 'In the spring of 1862, an enslaved man stole a Confederate warship.', P('portrait', { focus: [0.45, 0.28], zoom: [1.05, 1.18] }), { hook: 'He stole a *Confederate warship.*' }],
  ['hook2', 'He did it in the dark, with his wife and children on board, right past the guns of Fort Sumter.', P('harbor1865', { motion: 'panRight', zoom: [1.0, 1.08] })],
  ['hook3', 'If they were caught, he had promised to sink the ship rather than surrender.', P('planter', { focus: [0.5, 0.55], zoom: [1.0, 1.12] })],
  ['hook4', 'His name was Robert Smalls. And the escape is not even the most surprising part of his story.', P('mc', { focus: [0.5, 0.3], zoom: [1.0, 1.1] }), { lowerThird: { name: 'Robert Smalls', sub: '1839 – 1915' } }],
  ['hook5', 'Because of what he did next, and what he bought when the war was over.', P('house', { zoom: [1.02, 1.1] })],

  // ---- chapter 1: the harbor
  ['c1', 'Chapter one. The harbor.', CH(1, 'The Harbor'), null, { section: 'harbor', captions: false }],
  ['born1', 'Robert Smalls was born into slavery on April the fifth, 1839, in Beaufort, South Carolina.', P('plantation', { zoom: [1.0, 1.1] }), { year: { from: 1839, to: 1839 }, pin: { label: 'Beaufort', sub: 'South Carolina' } }],
  ['born2', 'His mother, Lydia Polite, was enslaved too. Robert grew up in the shadow of their enslaver\'s house, a large house on Prince Street.', P('house', { motion: 'panLeft', zoom: [1.05, 1.12] })],
  ['born3', 'Remember that house. It comes back at the end of this story.', C('house', 'The house on Prince Street, Beaufort', { crop: [0.05, 0.1, 0.95, 0.9] })],
  ['chs1', 'When he was about twelve, he was sent to Charleston and hired out.', P('wharf', { zoom: [1.0, 1.1] }), { pin: { label: 'Charleston', sub: 'South Carolina' } }],
  ['chs2', 'He lit the city\'s street lamps. He worked on the docks, as a rigger and a sailor.', P('steamers', { motion: 'panRight' })],
  ['chs3', 'But the money he earned was not his. Most of his wages went to his owner.', T('His wages', 'went to his owner')],
  ['chs4', 'Year by year, he learned the water. The tides, the channels, the sandbars of Charleston harbor.', C('harbormap', 'Charleston Harbor and its approaches, 1863', { crop: [0.2, 0.15, 0.85, 0.85] })],
  ['chs5', 'He became so skilled that he was steering ships, doing the work of a pilot. The law would never give him that title.', P('steamers', { focus: [0.4, 0.5], zoom: [1.1, 1.2] })],

  // ---- chapter 2: the price of a family
  ['c2', 'Chapter two. The price of a family.', CH(2, 'The Price of a Family'), null, { section: 'family', captions: false }],
  ['fam1', 'In 1856, he married Hannah Jones, an enslaved woman who worked in Charleston hotels. They started a family.', P('wharf', { focus: [0.6, 0.5], zoom: [1.15, 1.25] }), { year: { from: 1856, to: 1856 } }],
  ['fam2', 'And Robert tried to do it the legal way. He asked what it would cost to buy his wife and their little daughter.', P('wharf', { focus: [0.35, 0.5], zoom: [1.2, 1.3] })],
  ['fam3', 'The answer was about eight hundred dollars.', T('$800', 'the price of his wife and daughter')],
  ['fam4', 'He had saved about one hundred.', T('$100', 'what he had saved')],
  ['fam4b', 'A man who did the work of a pilot could not afford to buy his own wife and child.', P('portrait', { focus: [0.47, 0.3], zoom: [1.1, 1.18] })],
  ['fam5', 'At that rate, it could take him most of his life. And at any moment, his family could be sold away from him.', P('plantation', { motion: 'panLeft', zoom: [1.05, 1.12] })],
  ['fam6', 'So he started to think about another way out. It would mean risking everything.', P('portrait', { focus: [0.47, 0.3], zoom: [1.2, 1.3] })],
  ['fam7', 'If the plan failed, the men could lose their lives, and their wives and children could be sold. He would need the right ship, the right night, and nerves of steel.', P('harbor1865', { focus: [0.3, 0.5], zoom: [1.1, 1.2] })],

  // ---- chapter 3: the night of May 12
  ['c3', 'Chapter three. The night of May the twelfth.', CH(3, 'The Night of May 12'), null, { section: 'night', captions: false }],
  ['war1', 'In April 1861, Confederate guns opened fire on Fort Sumter. The Civil War had begun.', P('bombard', { zoom: [1.0, 1.12] }), { year: { from: 1861, to: 1861 } }],
  ['war2', 'Smalls was working aboard a Confederate steamer called the Planter. It carried guns, ammunition and supplies around Charleston harbor.', P('planter', { motion: 'panLeft' })],
  ['war3', 'Smalls was its wheelman. He knew the ship, the harbor, and every signal the captain gave to pass the forts.', C('gunboat', 'The Planter, from Harper\'s Weekly, 14 June 1862')],
  ['war4', 'On May the twelfth, 1862, the Planter took on four big guns from a dismantled fort, along with ammunition.', P('gunboat', { zoom: [1.05, 1.15] }), { stamp: '12 May 1862' }],
  ['war5', 'That evening, the three white officers went ashore for the night, as they often did, leaving the ship to the enslaved crew.', P('steamers', { focus: [0.55, 0.5], zoom: [1.05, 1.15] })],
  ['war6', 'It was the chance Smalls had been waiting for.', T('3 a.m.', 'the boilers are lit')],
  ['esc1', 'Around three in the morning, the crew fired up the boilers and slipped away from the wharf.', M('wharf')],
  ['esc2', 'They stopped at another wharf to pick up their families, including Hannah and the children. Sixteen people were now aboard.', T('16', 'people on board')],
  ['esc3', 'Then they headed for the harbor mouth, past fort after fort. Castle Pinckney. Fort Johnson. Fort Moultrie.', M('forts')],
  ['esc3b', 'Every one of those forts had guns that could sink the Planter in minutes. One wrong signal, and it was over.', P('bombard', { focus: [0.6, 0.5], zoom: [1.15, 1.25] })],
  ['esc4', 'Smalls put on the captain\'s straw hat, folded his arms, and stood the way the captain stood, so that from a distance, in the dark, he would look like him.', P('heroes', { focus: [0.5, 0.25], zoom: [1.1, 1.2] })],
  ['esc5', 'At each fort, he gave the right whistle signals. And one after another, the forts let them pass.', P('pinckney', { zoom: [1.0, 1.1] })],
  ['esc6', 'At about half past four in the morning, they steamed past Fort Sumter itself.', M('sumter')],
  ['esc6b', 'Fort Sumter. Where the war had begun, thirteen months earlier. They were sailing right under its walls.', P('harbor1865', { focus: [0.6, 0.5], zoom: [1.2, 1.3] })],
  ['esc7', 'Once they were out of range, the crew pulled down the Confederate flag and raised a white bedsheet.', P('sumter', { motion: 'panRight' })],
  ['esc8', 'As the sun came up, they steered for the Union ships blockading the harbor.', M('fleet')],
  ['esc9', 'In the morning fog, the crew of the U.S.S. Onward saw a Confederate steamer coming straight at them. They swung a gun toward it.', P('blockade', { zoom: [1.0, 1.12] })],
  ['esc10', 'They were about to fire, when someone shouted that he could see a white flag.', T('Hold fire', 'a white flag')],
  ['esc11', 'Robert Smalls handed over the Planter, its guns, and its cargo to the United States Navy.', P('harpers', { focus: [0.5, 0.35], zoom: [1.0, 1.1] })],
  ['esc12', 'Sixteen people had gone to sleep enslaved. By sunrise, they were free.', P('heroes', { motion: 'panLeft', zoom: [1.0, 1.08] })],

  // ---- chapter 4: worth more than the ship
  ['c4', 'Chapter four. Worth more than the ship.', CH(4, 'Worth More Than the Ship'), null, { section: 'worth', captions: false }],
  ['wo1', 'The news spread across the North. Harper\'s Weekly put Smalls\'s face in its pages.', C('harpers', 'Harper\'s Weekly, 1862')],
  ['wo2', 'Congress passed a bill to reward him and his crew. Smalls received fifteen hundred dollars.', T('$1,500', 'his share of the prize')],
  ['wo3', 'But what Smalls carried in his head was worth as much as the ship. He knew the channels, the forts, and where the mines were laid.', C('harbormap', 'Charleston Harbor, 1863', { crop: [0.3, 0.3, 0.8, 0.8] })],
  ['wo4', 'Within days, Union forces used what he told them to take positions near Charleston that the Confederates had abandoned.', P('harbormap', { motion: 'panRight', zoom: [1.1, 1.2] })],
  ['wo5', 'And he did more than escape. The Union command in the region sent Smalls to Washington.', P('portrait', { focus: [0.47, 0.3], zoom: [1.1, 1.2] })],
  ['wo6', 'He carried a message for President Lincoln and the Secretary of War, Edwin Stanton. Let Black men fight.', P('stanton', { focus: [0.5, 0.3], zoom: [1.0, 1.08] }), { lowerThird: { name: 'Edwin M. Stanton', sub: 'Secretary of War' } }],
  ['wo7', 'Soon after, the Secretary of War authorized up to five thousand Black soldiers to be raised in the area.', P('saxton', { focus: [0.5, 0.3], zoom: [1.0, 1.08] }), { stamp: '5,000 soldiers' }],

  // ---- chapter 5: captain Smalls
  ['c5', 'Chapter five. Captain Smalls.', CH(5, 'Captain Smalls'), null, { section: 'captain', captions: false }],
  ['cap1', 'Smalls went back to the war, this time on the Union side.', P('planter', { focus: [0.45, 0.5], zoom: [1.1, 1.2] })],
  ['cap2', 'He piloted the Planter and the ironclad Keokuk in at least twelve engagements.', P('keokuk', { zoom: [1.0, 1.12] })],
  ['cap3', 'In April 1863 the Keokuk was hit again and again off Charleston.', C('keokukiln', 'The Keokuk the morning after the fight, Illustrated London News, 1863')],
  ['cap4', 'In one battle aboard the Planter, under heavy fire, the white captain lost his nerve. Smalls took command and brought the ship to safety.', P('gunboat', { motion: 'panRight', zoom: [1.05, 1.15] })],
  ['cap5', 'Afterward, he was made the Planter\'s captain. The man who had once steered the Planter for the Confederacy now commanded it for the United States.', T('Captain', 'of the Planter')],
  ['cap6', 'Even as a war hero, he was not treated as an equal. In December 1864, in Philadelphia, he was thrown off a streetcar reserved for white passengers.', P('portrait', { focus: [0.47, 0.32], zoom: [1.15, 1.22] }), { year: { from: 1864, to: 1864 } }],
  ['cap7', 'He joined a mass boycott. And in 1867, a new law opened Philadelphia\'s streetcars to Black passengers.', T('1867', 'Philadelphia\'s streetcars open to all')],

  // ---- chapter 6: the house on Prince Street
  ['c6', 'Chapter six. The house on Prince Street.', CH(6, 'The House on Prince Street'), null, { section: 'house', captions: false }],
  ['ho1', 'The war ended in 1865. Charleston lay in ruins.', P('ruins', { zoom: [1.0, 1.1] }), { year: { from: 1865, to: 1865 } }],
  ['ho2', 'Robert Smalls went home to Beaufort, to a house he now owned. It was the house where he had been enslaved. He had bought it at a tax sale.', P('house', { zoom: [1.0, 1.15] })],
  ['ho3', 'The boy who grew up in the shadow of that house now owned it.', C('house', '511 Prince Street, Beaufort', { crop: [0.0, 0.05, 1.0, 0.95] })],
  ['ho4', 'Imagine walking through the front door of a house you were once only allowed to serve in.', P('house', { focus: [0.5, 0.6], zoom: [1.2, 1.35] })],
  ['ho5', 'He opened a store, and a school for Black children. In 1868, he helped write a new constitution for South Carolina.', P('radical', { zoom: [1.0, 1.1] }), { year: { from: 1868, to: 1868 } }],
  ['ho6', 'He served in the state house, then the state senate.', P('radical', { focus: [0.5, 0.4], zoom: [1.15, 1.3] })],
  ['ho7', 'And in 1875, he took his seat in the United States House of Representatives. Over the years, he served five terms in Congress.', P('mc', { focus: [0.5, 0.3], zoom: [1.0, 1.12] }), { lowerThird: { name: 'Rep. Robert Smalls', sub: 'South Carolina · 5 terms' } }],

  // ---- chapter 7: the last stand
  ['c7', 'Chapter seven. The last stand.', CH(7, 'The Last Stand'), null, { section: 'stand', captions: false }],
  ['st1', 'But Reconstruction did not last. White supremacists took back power in South Carolina, and set out to take the vote away from Black citizens.', P('ruins', { motion: 'panLeft', zoom: [1.05, 1.12] })],
  ['st1b', 'In 1877, as Reconstruction collapsed, the new Democratic state government charged Smalls with taking a five-thousand-dollar bribe years earlier. He was convicted and sentenced to three years in prison.', T('1877', 'convicted')],
  ['st1c', 'He called the case political. In 1879 the governor pardoned him, and voters later sent him back to Congress.', P('mc', { focus: [0.5, 0.35], zoom: [1.05, 1.15] })],
  ['st2', 'In 1895, South Carolina held a convention to write a new constitution, designed to strip Black men of the right to vote.', P('tillman', { focus: [0.5, 0.3], zoom: [1.0, 1.1] }), { year: { from: 1895, to: 1895 }, lowerThird: { name: 'Benjamin Tillman', sub: 'Force behind the 1895 constitution' } }],
  ['st3', 'Robert Smalls was one of only six Black delegates. He stood up and spoke against it.', T('6', 'Black delegates')],
  ['st4', 'He said of his people: all they need is an equal chance in the battle of life.', { kind: 'quote', quote: 'All they need is an equal chance in the battle of life.', by: 'Robert Smalls, 1895' }],
  ['st5', 'He lost that vote. But he did not stay silent.', P('mc', { focus: [0.5, 0.3], zoom: [1.15, 1.25] })],
  ['st6', 'He served for years as the collector of customs at the port of Beaufort, until 1913.', P('wharf', { motion: 'panRight' })],
  ['st7', 'On February the twenty-third, 1915, Robert Smalls died, in the house where he had once been enslaved. He was seventy-five years old.', P('house', { zoom: [1.1, 1.0] }), { year: { from: 1915, to: 1915 } }],

  // ---- close
  ['end1', 'A boy whose wages belonged to someone else.', P('steamers', { focus: [0.5, 0.5], zoom: [1.1, 1.18] }), null, { section: 'close' }],
  ['end2', 'A father who could not afford to buy his own family.', P('plantation', { focus: [0.5, 0.5], zoom: [1.1, 1.18] })],
  ['end3', 'A man who took a warship, sailed past Fort Sumter, and came home to own the house where he had been enslaved.', P('portrait', { focus: [0.47, 0.3], zoom: [1.0, 1.12] })],
  ['end4', 'That was Robert Smalls. Every fact in this video is sourced at the black history room dot com. If you want the next story, subscribe, because tomorrow we tell another one history tried to forget.', { kind: 'endcard' }, null, { captions: false }],
];

// Images too small to fill a 1920x1080 frame without visible upscaling are shown as captioned cards.
const CARD_CAPTIONS = {
  harbor1865: "Fort Sumter in Charleston harbor, Harper's Weekly, 1865",
  tillman: 'Benjamin Tillman',
  stanton: 'Edwin M. Stanton, Secretary of War',
  keokuk: 'The ironclad USS Keokuk',
  pinckney: 'Castle Pinckney, Charleston harbor',
  harbormap: 'Charleston Harbor and its approaches, 1863',
};
for (const b of beats) {
  const v = b[2];
  if (v.kind === 'photo' && CARD_CAPTIONS[v.image]) b[2] = { kind: 'card', image: v.image, caption: CARD_CAPTIONS[v.image] };
}

// facts from the existing, sourced fact sheets
const pod = JSON.parse(fs.readFileSync('data/podcast-ep02-robert-smalls-andrew.json', 'utf8'));
const reel = JSON.parse(fs.readFileSync('data/reel-robert-smalls.json', 'utf8'));

const spec = {
  id: 'doc-robert-smalls',
  title: 'He Stole a Confederate Warship. Then He Bought His Master\'s House.',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { ...reel.voice, speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1.0 },
  music: reel.music,
  mix: { ...(reel.mix || {}), hookBoostDb: 0 },
  brand: { page: 'The Black History Room', cta: 'Subscribe', ctaLine: 'One story history tried to forget, every day.', theme: 'bhr' },
  assets: Object.fromEntries(Object.entries(assets).map(([k, v]) => [k, { commons: v }])),
  beats: beats.map(([id, text, visual, overlays, extra]) => ({ id, text, visual, ...(overlays ? { overlays } : {}), ...(extra || {}) })),
  facts: reel.facts,
  sourcesByClaim: pod.sources,
  sources: reel.sources,
};
fs.writeFileSync('data/doc-robert-smalls.json', JSON.stringify(spec, null, 1) + '\n');
const words = beats.map((b) => b[1]).join(' ').split(/\s+/).length;
console.log(`${beats.length} beats, ${words} words, ~${(words / 174).toFixed(1)} min at the podcast pace, ${Object.keys(assets).length} images`);
