// Builds data/doc-tuskegee-airmen.json: 8-minute long-form documentary (16:9) on the Tuskegee Airmen.
// Free local voice (Kokoro), owner's request 2026-11-08. Every fact has two or more sources (sourcesByClaim).
// Ending follows the owner's rule: only "subscribe for more". Run: node data/build_doc_tuskegee_airmen.mjs
import fs from 'node:fs';

const assets = {
  pilots: 'File:Tuskegee Airmen 332nd Fighter Group pilots ppmsca13245u.jpg',
  airman2: 'File:Tuskegee airman2.jpg',
  airmen2: 'File:Tuskegee airmen 2.jpg',
  mustangs: 'File:P-51Cs 332nd FG with goats Ramitelli 1945.jpg',
  briefing: 'File:Tuskegee airmen attending a briefing in Ramitelli, Italy.jpg',
  parachute: 'File:Tuskegee airmen exiting the parachute room.jpg',
  cards: "File:Tuskegee airmen playing cards in the officers' club.jpg",
  davis41: 'File:"(Army Air Corps) cadets reporting to Captain B(enjamin) O. Davis, Jr. commandant of cadets.", 09-1941 - NARA - 531133.jpg',
  welcome: 'File:"Address of welcome to (Army Air Corps) cadets in front of Booker T. Washington Monument on the grounds of Tuskegee Inst - NARA - 531132.jpg',
  review: 'File:"Officer returns salute as he passes the cadets lined up during review.", ca. 1941 - ca. 1945 - NARA - 535831.jpg',
  sq99: 'File:"Members of the 99th Fighter Squadron of the Army Air Forces, famous all-Negro outfit, who are rapidly making themselves - NARA - 520624.jpg',
  map: 'File:"With an officer giving them pointers from a giant map, pilots of an American P-51 Mustang fighter-bomber group learn th - NARA - 535766.jpg',
  selfridge: 'File:"Pilots at Selfridge Field (MI) learn to carry out bombing missions as they would carry them out under actual combat con - NARA - 535963.jpg',
  hunting: 'File:"GOOD HUNTING, SON,- YOU\'RE ON YOUR OWN NOW^^" - NARA - 535667.jpg',
  firstclass: 'File:First Tuskeegee Class.jpg',
  stearman: 'File:Boeing Stearman at Tuskegee Airfield c1942.jpg',
  eleanor: 'File:First Lady Eleanor Roosevelt and C. Alfred “Chief” Anderson.jpg',
  coldavis: 'File:Col Benjamin O. Davis Jr.jpg',
  davisfsa: 'File:Benjamin O. Davis fsa 8e00217.jpg',
  freeman: 'File:Freeman Field Mutiny.jpg',
  bush: 'File:President George W. Bush Presents the Congressional Gold Medal to Dr. Roscoe Brown Jr., During Ceremonies Honoring the Tuskegee Airmen at the U.S. Capitol.jpg',
  medal: 'File:2006 Tuskegee Airmen Congressional Gold Medal front.jpg',
  eo: 'File:Executive Order 9981.jpg',
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });

const PILOTS = 'Pilots of the 332nd Fighter Group, Ramitelli, Italy, March 1945';
const beats = [
  // ---- cold open
  ['h1', 'In 1925, a study at the Army War College claimed that Black men did not have what it takes to serve as leaders in the military, or to fly aircraft of any kind.', C('pilots', PILOTS), { hook: 'They said Black men *could not fly.*' }],
  ['h2', 'Twenty years later, Black American pilots in red-tailed fighters were escorting bombers all the way to Berlin.', P('mustangs', { focus: [0.5, 0.2], zoom: [1.3, 1.4] })],
  ['h3', 'They flew more than fifteen thousand combat sorties. They shot down German jets.', P('map', { zoom: [1.0, 1.08] })],
  ['h4', 'And back home in the same spring, more than a hundred of their fellow Black officers were arrested, over an officers club.', C('freeman', 'Freeman Field, Indiana, April 1945')],
  ['h5', 'They had two wars to fight. One overseas, and one in their own country. They were the Tuskegee Airmen.', C('airmen2', 'Tuskegee Airmen, Ramitelli, Italy, 1945'), { lowerThird: { name: 'The Tuskegee Airmen', sub: '1941 – 1946' } }],

  // ---- origins
  ['o1', 'In the nineteen thirties, the Army Air Corps did not accept Black pilots.', T('No Black pilots', 'Army Air Corps, 1930s'), { section: 'origins' }],
  ['o2', 'But Black Americans were already flying. Charles Alfred Anderson, known as Chief, earned his pilot license in 1929.', C('eleanor', 'C. Alfred "Chief" Anderson, with Eleanor Roosevelt, 1941'), { lowerThird: { name: 'C. Alfred "Chief" Anderson', sub: 'chief flight instructor' } }],
  ['o3', 'In 1932, he became the first African American to hold a commercial pilot certificate.', T('1932', 'first Black commercial pilot certificate')],
  ['o4', 'In 1939, with war coming closer, Congress paid for a program to train civilian pilots, and it included Black students.', P('stearman', { zoom: [1.0, 1.08] }), { year: { from: 1939, to: 1939 } }],
  ['o5', 'One of the places it reached was Tuskegee Institute in Alabama, the school built by Booker T. Washington.', P('welcome', { focus: [0.5, 0.4], zoom: [1.0, 1.1] }), { pin: { label: 'Tuskegee', sub: 'Alabama' } }],
  ['o6', 'In January 1941, the War Department announced the first all-Black flying unit in American history, the 99th Pursuit Squadron.', T('The 99th', 'first all-Black flying unit, January 1941')],
  ['o7', 'It was a test. Could Black Americans lead, fly military aircraft, and fight? The men would have to prove it inside a segregated Army.', P('review', { zoom: [1.0, 1.08] })],
  ['o8', 'That spring, First Lady Eleanor Roosevelt visited Tuskegee, and she went up in a plane with Chief Anderson.', C('eleanor', 'Eleanor Roosevelt and Chief Anderson, Tuskegee, 1941'), { stamp: '1941' }],
  ['o9', 'The photograph of the two of them, smiling in the cockpit, is still one of the most famous pictures of the program.', P('eleanor', { focus: [0.5, 0.45], zoom: [1.0, 1.1] })],
  ['o10', 'Anderson is credited with persuading her to encourage the President to back flight training at Tuskegee.', T('Eleanor Roosevelt', 'backed the Tuskegee program')],

  // ---- training
  ['t1', 'On July 19, 1941, the first class of cadets began training.', P('welcome', { focus: [0.5, 0.6], zoom: [1.2, 1.3] }), { section: 'training', stamp: '19 July 1941' }],
  ['t2', 'Thirteen men started. Five finished, in March 1942.', P('firstclass', { zoom: [1.0, 1.08] })],
  ['t3', 'One of the five was already known to the Army. Captain Benjamin O. Davis Junior.', P('davis41', { focus: [0.7, 0.45], zoom: [1.1, 1.2] }), { lowerThird: { name: 'Capt. Benjamin O. Davis Jr.', sub: 'first class at Tuskegee' } }],
  ['t4', 'His father was the first Black general in the United States Army. And he had already been through something few men could stand.', C('coldavis', 'Benjamin O. Davis Jr.')],
  ['t5', 'He entered West Point in 1932. For four years, the other cadets would not speak to him. He had no roommate. He ate his meals alone.', T('Four years', 'of silence at West Point')],
  ['t6', 'He wrote later that he was silenced because cadets did not want Black men at West Point.', C('coldavis', 'Benjamin O. Davis Jr.')],
  ['t7', 'He graduated in 1936, thirty-fifth in a class of two hundred seventy-six.', T('35th of 276', 'West Point, 1936')],
  ['t8', 'Now he would lead the first Black fighter pilots.', P('davisfsa', { zoom: [1.0, 1.08] })],
  ['t9', 'From 1941 to 1946, nearly a thousand Black pilots trained at Tuskegee.', P('review', { focus: [0.5, 0.6], zoom: [1.2, 1.3] })],
  ['t10', 'And the Airmen were not only pilots. They were navigators, technicians, mechanics, parachute riggers, men and women.', C('parachute', 'Pilots leaving the parachute room, Ramitelli, 1945')],

  // ---- combat
  ['c1', 'In April 1943, the 99th shipped out for North Africa.', P('sq99', { zoom: [1.0, 1.08] }), { section: 'combat', pin: { label: 'North Africa', sub: 'April 1943' } }],
  ['c2', 'On June 2, it flew its first combat mission, over the Italian island of Pantelleria.', C('hunting', 'U.S. war cartoon on Pantelleria, 1943')],
  ['c3', 'Then came the attack from their own side. In September 1943, their group commander, Colonel William Momyer, reported that the 99th lacked discipline, teamwork and aggressiveness.', T('Col. William Momyer', 'September 1943 report')],
  ['c4', 'The criticism threatened the whole program.', P('sq99', { focus: [0.5, 0.35], zoom: [1.2, 1.3] })],
  ['c5', 'So the War Department ran a formal comparison. On March 30, 1944, the report came out. The 99th had performed as well as the white squadrons it flew with.', T('As well as', 'the white squadrons, March 1944')],
  ['c6', 'That May, the 99th earned a Distinguished Unit Citation for its strikes at Monte Cassino. It was the squadron\'s second.', C('selfridge', 'Black pilots in training, Selfridge Field, Michigan, about 1943')],
  ['c7', 'In June 1944, the 99th joined the 332nd Fighter Group, at Ramitelli, on the Italian coast. Davis, now a colonel, was in command.', P('mustangs', { focus: [0.5, 0.2], zoom: [1.2, 1.3] }), { pin: { label: 'Ramitelli', sub: 'Italy' } }],
  ['c8', 'Their job now was to protect American bombers over Germany and across Europe. And they painted the tails of their planes red.', C('briefing', 'A briefing at Ramitelli, Italy, March 1945')],
  ['c9', 'The bomber crews noticed. People came to call them the Red Tails.', P('mustangs', { focus: [0.35, 0.2], zoom: [1.4, 1.5] })],
  ['c10', 'You may have heard that they never lost a bomber. That is a legend, and it is not true.', C('airman2', 'A Tuskegee Airman, Ramitelli, Italy, 1945')],
  ['c11', 'Here is the real record. They flew one hundred seventy-nine bomber escort missions. They lost bombers on seven of them, twenty-seven bombers in all.', T('27', 'bombers lost in 179 missions')],
  ['c12', 'The other P-51 groups in the same air force lost an average of forty-six. The truth is impressive enough.', T('46', 'average, other P-51 groups')],
  ['c13', 'On March 24, 1945, they flew one of the longest escort missions of the war, about sixteen hundred miles there and back, to Berlin.', P('map', { focus: [0.45, 0.4], zoom: [1.2, 1.3] }), { stamp: '24 March 1945', pin: { label: 'Berlin', sub: '1945' } }],
  ['c14', 'Colonel Davis led them. Over the city, they met German jets, the fastest fighters in the sky. They shot down three.', C('pilots', PILOTS)],
  ['c15', 'The group won a Distinguished Unit Citation for that day.', T('Berlin', 'three German jets shot down')],
  ['c16', 'By the end of the war, they had flown fifteen hundred seventy-eight missions and fifteen thousand five hundred thirty-three combat sorties.', T('15,533', 'combat sorties')],
  ['c17', 'They destroyed one hundred twelve enemy aircraft in the air, and one hundred fifty on the ground.', T('262', 'enemy aircraft destroyed')],
  ['c18', 'It cost them. More than sixty pilots were killed in action or in accidents, and thirty-two became prisoners of war.', C('cards', 'The officers club at Ramitelli, March 1945')],

  // ---- Freeman Field
  ['f1', 'And while they fought in Europe, the other war was still going on at home.', T('The other war', 'United States, 1945'), { section: 'freeman' }],
  ['f2', 'In the spring of 1945, the 477th Bombardment Group, another Black unit, was training at Freeman Field, in Indiana. It never saw combat.', C('freeman', 'Freeman Field, Indiana, 1945'), { pin: { label: 'Freeman Field', sub: 'Indiana' } }],
  ['f3', 'The base commander, Colonel Robert Selway, set up two officers clubs. One for white officers, whom he called instructors. One for Black officers, whom he called trainees.', T('Two clubs', 'one white, one Black')],
  ['f4', 'A year earlier, the War Department had ordered recreational facilities on bases to be integrated.', T('1944', 'War Department order')],
  ['f5', 'On April 5, Black officers began walking into the white club, in small groups. Over two nights, sixty-one were arrested.', P('freeman', { zoom: [1.0, 1.08] }), { stamp: '5 April 1945' }],
  ['f6', 'Then the Army wrote a new base regulation, and ordered every officer to sign it. One hundred one Black officers refused.', T('101', 'refused to sign')],
  ['f7', 'They were arrested and flown to Godman Field, in Kentucky.', P('freeman', { focus: [0.5, 0.5], zoom: [1.2, 1.3] })],
  ['f8', 'The NAACP, the National Urban League and the Black press pushed back, hard. Late that April, the one hundred one were released, with reprimands in their files.', C('airmen2', 'Tuskegee Airmen, 1945')],
  ['f9', 'Three more officers faced court-martial. Only one, Roger Terry, was convicted, and he got a dishonorable discharge.', T('Roger Terry', 'convicted, November 1945')],
  ['f10', 'In 1995, fifty years later, he was pardoned, and his rank was restored.', T('1995', 'pardoned')],
  ['f11', 'People remember Freeman Field as an early, nonviolent sit-in for civil rights, by men in uniform, years before the famous ones.', C('pilots', PILOTS)],

  // ---- legacy
  ['z1', 'On July 26, 1948, President Harry Truman signed Executive Order 9981, ordering equal treatment in the armed forces.', C('eo', 'Executive Order 9981, 26 July 1948'), { section: 'legacy', stamp: '26 July 1948' }],
  ['z2', 'Benjamin O. Davis Junior went on to become the first Black general in the United States Air Force.', C('coldavis', 'Benjamin O. Davis Jr.')],
  ['z3', 'And on March 29, 2007, in the Rotunda of the United States Capitol, about three hundred fifty Tuskegee Airmen and their widows received the Congressional Gold Medal.', C('bush', 'The Congressional Gold Medal ceremony, U.S. Capitol, 29 March 2007'), { stamp: '29 March 2007' }],
  ['z4', 'It came sixty-two years after the war ended.', C('medal', 'The Tuskegee Airmen Congressional Gold Medal')],

  // ---- close
  ['e1', 'They were told they did not have the intelligence, or the courage.', C('airman2', 'A Tuskegee Airman, 1945'), { section: 'close' }],
  ['e2', 'They were tested in a way no white unit was.', P('firstclass', { focus: [0.6, 0.5], zoom: [1.1, 1.2] })],
  ['e3', 'They fought for a country that would arrest them for walking into a club.', C('freeman', 'Freeman Field, 1945')],
  ['e4', 'And they flew anyway.', C('pilots', PILOTS)],
  ['e5', 'Those were the Tuskegee Airmen. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-ellen-craft.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Tuskegee_Airmen',
  AFHRA: 'https://www.afhra.af.mil/Portals/16/documents/Timelines/World%20War%20II/Misconceptions_About_the_Tuskegee_Airmen.pdf',
  CENT: 'https://webarchive.library.unt.edu/eot2008/20080916072426/http://centennialofflight.gov/essay/Air_Power/tuskegee/AP26.htm',
  CAF: 'https://cafriseabove.org/the-tuskegee-airmen/tuskegee-airmen-history/war-service/',
  FRIENDS: 'https://www.friendsoftuskegeeairmennhs.org/the-tuskegee-airmen',
  NPS: 'https://www.nps.gov/tuai/learn/historyculture/index.htm',
  SI: 'https://si.edu/newsdesk/snapshot/eleanor-roosevelt-tuskegee',
  ANDERSON: 'https://en.wikipedia.org/wiki/C._Alfred_%22Chief%22_Anderson',
  DAVIS: 'https://en.wikipedia.org/wiki/Benjamin_O._Davis_Jr.',
  AF: 'https://www.af.mil/News/Article-Display/Article/111740/tuskegee-airman-goes-on-to-become-first-air-force-african-american-general',
  CNN: 'https://abc17news.com/?p=1289409',
  HIST: 'https://www.history.com/articles/tuskegee-airmen-impact-civil-rights-movement',
  FF: 'https://en.wikipedia.org/wiki/Freeman_Field_mutiny',
  TAI: 'https://www.tuskegeeairmen.org/legacy/the-people/',
};
const sourcesByClaim = {
  h1: ['CNN', 'DAVIS'], h2: ['WIKI', 'FRIENDS'], h3: ['CAF', 'FRIENDS'], h4: ['HIST', 'FF'], o2: ['FRIENDS', 'ANDERSON'], o3: ['FRIENDS', 'ANDERSON'],
  o4: ['WIKI', 'NPS'], o5: ['NPS', 'FRIENDS'], o6: ['WIKI', 'CENT'], o7: ['NPS', 'FRIENDS'], o8: ['SI', 'ANDERSON', 'WIKI'], o10: ['FRIENDS', 'ANDERSON'],
  t1: ['WIKI', 'CAF'], t2: ['CENT', 'TAI'], t3: ['CENT', 'DAVIS'], t4: ['CNN', 'DAVIS'], t5: ['DAVIS', 'AF', 'CNN'], t6: ['DAVIS', 'CNN'], t7: ['DAVIS', 'AF'],
  t9: ['WIKI', 'FRIENDS'], t10: ['NPS', 'WIKI'], c1: ['WIKI', 'CAF'], c2: ['WIKI', 'CENT'], c3: ['CENT', 'AFHRA'], c5: ['CENT', 'AFHRA'], c6: ['WIKI', 'FRIENDS'],
  c7: ['WIKI', 'CAF'], c8: ['AFHRA', 'WIKI'], c9: ['AFHRA', 'WIKI'], c10: ['AFHRA', 'WIKI'], c11: ['CAF', 'WIKI', 'FRIENDS', 'AFHRA'], c12: ['CAF', 'AFHRA'],
  c13: ['WIKI', 'FRIENDS'], c14: ['WIKI', 'FRIENDS'], c15: ['WIKI', 'FRIENDS'], c16: ['CAF', 'FRIENDS'], c17: ['CAF', 'WIKI'], c18: ['CAF', 'WIKI'],
  f2: ['FF', 'CAF'], f3: ['FF', 'HIST'], f4: ['HIST', 'FF'], f5: ['HIST', 'FF'], f6: ['HIST', 'FF'], f7: ['HIST', 'FF'], f8: ['HIST', 'FF'], f9: ['HIST', 'FF'],
  f10: ['HIST', 'FF'], z1: ['WIKI', 'FRIENDS', 'HIST'], z2: ['AF', 'DAVIS'], z3: ['WIKI', 'TAI'],
};

const spec = {
  id: 'doc-tuskegee-airmen',
  title: 'They Said Black Men Could Not Fly. Then They Escorted Bombers to Berlin.',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { Tuskegee: 'Tuss-kee-ghee', Pantelleria: 'Pan-tell-uh-ree-uh', Ramitelli: 'Rah-mee-tell-ee', Momyer: 'Mo-my-er', Eleanor: 'Ellen-or', 'Monte Cassino': 'Mon-tay Cah-see-no', Selway: 'Sell-way', Godman: 'God-man' },
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
    'Date of the Eleanor Roosevelt flight: 29 March, 11 April and 19 April 1941 appear in different sources; script says "that spring".',
    'Her reported remark on the flight: wording differs and is not firmly documented.',
    'Pilots graduated: 992, 994, 996 by source: script says "nearly a thousand".',
    'Deaths: 150 (CAF, all causes) vs 84 (Wikipedia): script gives only "more than sixty pilots killed in action or accidents" (66 and 68).',
    'Distinguished Flying Crosses: 96 vs 150: left out.',
    'German destroyer at Trieste: identification disputed: left out.',
    'Bush saluting the Airmen in 2007: not confirmed in two sources: left out.',
  ],
};
fs.writeFileSync('data/doc-tuskegee-airmen.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ~${(text.split(/\s+/).length / 165).toFixed(1)} min at 165 wpm, ${Object.keys(assets).length} images`);
