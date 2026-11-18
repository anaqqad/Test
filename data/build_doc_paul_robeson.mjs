// Builds data/doc-paul-robeson.json: 8-minute long-form documentary (16:9) on Paul Robeson (1898-1976).
// Built on public-domain film of him: Body and Soul (1925), The Emperor Jones (1933) and the U.S. Army film
// Easy to Get (1940s), where he speaks to camera as himself. Plus public-domain photos.
// Free local voice (Kokoro). Every fact has two or more sources (sourcesByClaim).
// Ending follows the owner's rule: only "subscribe for more". Run: node data/build_doc_paul_robeson.mjs
import fs from 'node:fs';

const assets = {
  p1942: 'File:Paul Robeson 1942 crop.jpg',
  ulmann: 'File:Paul Robeson by Doris Ulmann, c. 1924, platinum print, from the National Portrait Gallery - NPG-NPG 78 2Robeson-000001 (adjusted).jpg',
  vanvechten: 'File:Portrait of Paul Robeson LCCN2004663510.jpg',
  karsh: 'File:Paul Robeson by Karsh, 1941.jpg',
  senior: 'File:Paul Robeson, senior photo from the Scarlet Letter yearbook.jpg',
  prob1919: 'File:PRobeson.jpg',
  capskull: 'File:Photograph of Paul Robeson with fellow Cap and Skull inductees.jpg',
  pollard: 'File:Pollard and Robeson.jpg',
  bsposter: 'File:Body and Soul (1925 film poster).jpg',
  ejposter: 'File:Emperor Jones (film poster, 1933).jpg',
  othello: 'File:Scene from Othello with Paul Robeson as Othello 8e07912v.jpg',
  othello2: 'File:Scene from Othello with Paul Robeson 8e07911v.jpg',
  othello3: 'File:Scene from Othello with Paul Robeson 8e07913v (retouched).jpg',
  alston: 'File:PAUL ROBESON - ACTOR, ARTIST, ATHLETE - NARA - 535624.jpg',
  teruel: 'File:Paul Robeson at Teruel.jpg',
  ballad: 'File:Earl Robinson Paul Robeson Ballad for Americans 1939.JPG',
  shipyard: 'File:"Paul Robeson, world famous Negro baritone, leading Moore Shipyard (Oakland, CA) workers in singing the Star Spangled Ba - NARA - 535874.jpg',
  einstein: 'File:Actor Paul Robeson with Albert Einstein.jpg',
  truman: 'File:TRUMAN 58-766-06 (cropped).jpg',
  jackie: 'File:Jackie Robinson, Brooklyn Dodgers, 1954.jpg',
  dubois: 'File:Vito Marcantonio (right) with W. E. B. Du Bois (center) and Paul Robeson (left).jpg',
  welcome: 'File:WELCOME RETURN.jpg',
  nara: 'File:Paul Robeson - NARA - 559205.jpg',
  p1930s: 'File:Paul Robeson - 1930s.JPG',
  bham: 'File:Paul Robeson - Birmingham Town Hall - 1939-03-07.jpg',
  ejstill: 'File:Paul Robeson in The Emperor Jones.jpg',
};

const EJ = 'File:The Emperor Jones (1933) by Dudley Murphy and William Churchill de Mille.webm';
const BS = 'File:Body and Soul (1925).webm';
const BSD = 'File:BODY AND SOUL-Paul Robeson-silent.webm';
const ETG = 'File:Easy to get.webm';
const ej = (start, dur, o = {}) => ({ file: 'emperor_jones.webm', commons: EJ, start, dur, ...o });
const clips = {
  pulpit: { file: 'body_and_soul.webm', commons: BS, start: 511.5, dur: 4.5 },
  pulpit2: { file: 'body_and_soul.webm', commons: BS, start: 482, dur: 3.5 },
  suit: { file: 'body_and_soul.webm', commons: BS, start: 846, dur: 3.2 },
  bssit: { file: 'body_and_soul_sd.webm', commons: BSD, start: 1060, dur: 2.2, speed: 0.5 },
  church: { file: 'body_and_soul_sd.webm', commons: BSD, start: 3774, dur: 5 },
  shoes: ej(514, 4),
  hug: ej(763.5, 3, { speed: 0.7 }),
  sofa: ej(914, 10),
  tux: ej(980, 8),
  club: ej(1054, 8),
  quarry: ej(1448, 6),
  helmet: ej(2190.5, 5),
  boss: ej(2534, 10),
  close: ej(2632, 10),
  throne: ej(3114, 8),
  uniclose: ej(3174, 6),
  smile: ej(3265, 5),
  dark: ej(3615, 8),
  jungle: ej(3717, 7),
  smile2: ej(3955, 8),
  desk: { file: 'easy_to_get.webm', commons: ETG, start: 1292, dur: 8 },
  talk: { file: 'easy_to_get.webm', commons: ETG, start: 1310, dur: 12 },
  talk2: { file: 'easy_to_get.webm', commons: ETG, start: 1325, dur: 12 },
};

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const V = (clip, focus = [0.5, 0.35], o = {}) => ({ kind: 'video', clip, focus, anchor: [0.5, focus[1]], zoom: [1.0, 1.06], ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const Q = (quote, by) => ({ kind: 'quote', quote, by });

const beats = [
  // ---- cold open
  ['o1', 'He was one of the most famous men in the world. Then his own government took away his passport, and tried to erase him.', P('vanvechten', { focus: [0.66, 0.58], zoom: [1.0, 1.08], anchor: [0.72, 0.5] }), { hook: 'One of the most famous men alive. *Then America took his passport.*' }, { captions: false }],
  ['o2', 'On June 12th, 1956, he sat in front of a committee of the United States Congress.', V('talk', [0.5, 0.35]), { stamp: '12 June 1956', lowerThird: { name: 'Paul Robeson', sub: 'U.S. Army film, 1940s' } }],
  ['o3', 'They asked about his politics, and about his travels. Then one of them asked why he did not just go and live in Russia.', V('desk', [0.5, 0.4])],
  ['o4', 'He answered: Because my father was a slave, and my people died to build this country. And I am going to stay here, and have a part of it, just like you.', Q('Because my father was a slave, and my people died to build this country, and I am going to stay here, and have a part of it just like you.', 'Paul Robeson, 1956')],
  ['o5', 'His name was Paul Robeson. This is his story.', T('Paul Robeson', 'athlete, singer, actor, activist')],

  // ---- Princeton
  ['e1', 'Paul Robeson was born on April 9th, 1898, in Princeton, New Jersey.', P('ulmann', { focus: [0.5, 0.3], zoom: [1.05, 1.15], anchor: [0.6, 0.4] }), { section: 'early', pin: { label: 'Princeton, New Jersey' } }],
  ['e2', 'His father, William Drew Robeson, had been born into slavery in North Carolina. As a teenager, he escaped.', T('He escaped slavery', 'William Drew Robeson, Paul\'s father')],
  ['e3', 'He went to school, and became the minister of a Black Presbyterian church in Princeton. After a dispute with the church\'s white backers, he lost that pulpit.', V('church', [0.5, 0.4])],
  ['e4', 'Then, when Paul was six years old, his mother died in a fire at home.', T('Six years old', 'his mother died in a fire')],
  ['e5', 'His father raised him alone, and expected the very best from him.', V('pulpit2', [0.5, 0.32])],

  // ---- Rutgers
  ['r1', 'In 1915, Paul won a statewide exam, and a scholarship to Rutgers College.', P('prob1919', { focus: [0.5, 0.3], zoom: [1.05, 1.15] }), { section: 'rutgers', stamp: '1915' }],
  ['r2', 'He was only the third Black student ever to enroll there, and the only one at the time.', C('capskull', 'Robeson with Cap and Skull inductees, Rutgers, 1919')],
  ['r3', 'He tried out for the football team. His own teammates did not want him. In the first scrimmages, they broke his nose, and dislocated his shoulder.', T('A broken nose', 'and a dislocated shoulder')],
  ['r4', 'He came back anyway. And he became the best player on the field.', C('pollard', 'Fritz Pollard and Paul Robeson, 1918')],
  ['r5', 'He was named an All-American twice. He earned varsity letters in four sports. He was elected to Phi Beta Kappa.', C('senior', 'Robeson\'s senior photo, Rutgers, 1919')],
  ['r6', 'And in 1919, his classmates chose him as valedictorian. In his speech, he called for equality for every American.', T('Valedictorian', 'Rutgers, class of 1919'), { stamp: '1919' }],

  // ---- the law
  ['l1', 'Next came law school, at Columbia. To pay for it, he played professional football on weekends, for the Akron Pros, and the Milwaukee Badgers.', V('suit', [0.5, 0.3]), { section: 'law' }],
  ['l2', 'He was one of the first Black players in what became the N F L.', T('Akron Pros, 1921', 'Milwaukee Badgers, 1922')],
  ['l3', 'In 1921 he married Eslanda Goode, a chemist, who would later manage his career.', V('hug', [0.4, 0.3]), { stamp: '1921' }],
  ['l4', 'He graduated in 1923, and joined a law firm in New York.', V('shoes', [0.5, 0.3])],
  ['l5', 'But a white secretary there refused to take dictation from him, because he was Black.', T('She refused', 'to take dictation from a Black man')],
  ['l6', 'He walked out. Not just out of that job, but out of the law, for good.', V('boss', [0.6, 0.3])],

  // ---- stage
  ['s1', 'So he turned to the stage. In 1924 he starred in two plays by Eugene O\'Neill in New York, All God\'s Chillun Got Wings, and The Emperor Jones.', P('ulmann', { focus: [0.5, 0.3], zoom: [1.05, 1.15], anchor: [0.6, 0.4] }), { section: 'stage' }],
  ['s2', 'In 1925 he made his first film, Body and Soul, for the Black director Oscar Micheaux. He played two brothers: a crooked preacher, and an honest man.', V('pulpit', [0.5, 0.3]), { lowerThird: { name: 'Body and Soul', sub: '1925' } }],
  ['s3', 'That same year, with the pianist Lawrence Brown, he gave a concert of nothing but Black spirituals.', P('vanvechten', { focus: [0.66, 0.6], zoom: [1.05, 1.12] })],
  ['s4', 'It was a sensation. His deep bass voice made him a star.', V('pulpit2', [0.5, 0.32])],

  // ---- London
  ['w1', 'In 1928, he sang Ol\' Man River in Show Boat, in London. It became his song for the rest of his life.', V('sofa', [0.33, 0.32]), { section: 'london', pin: { label: 'London' } }],
  ['w2', 'In 1930 he played Othello in London. A Black actor in that role was rare, and it made headlines.', C('othello3', 'Robeson as Othello')],
  ['w3', 'The Robesons stayed in Britain for most of the next decade. He was rich, and famous across the world.', V('tux', [0.7, 0.3])],
  ['w4', 'In 1933 he starred in the film of The Emperor Jones, a rare film of its time with a Black actor in the lead role.', V('throne', [0.55, 0.35]), { lowerThird: { name: 'The Emperor Jones', sub: '1933' } }],
  ['w5', 'In Britain, he got to know Welsh coal miners, and men fighting colonial rule in Africa and India. He began to see his own people\'s struggle as part of a bigger one.', V('smile', [0.5, 0.3])],
  ['w6', 'In 1934 he visited the Soviet Union. He said that there, for the first time in his life, he felt like a full human being.', Q('Here I am not a Negro but a human being for the first time in my life.', 'Paul Robeson, Moscow, 1934')],
  ['w7', 'In 1938 he went to Spain, in the middle of its civil war, to sing for the soldiers fighting fascism.', C('teruel', 'Robeson in Spain, 1938'), { stamp: '1938' }],

  // ---- home
  ['h1', 'In 1939 he came home. On national radio, he sang Ballad for Americans, a song about what America could be. It was a hit.', C('ballad', 'Ballad for Americans, CBS radio, 1939'), { section: 'home' }],
  ['h2', 'During the war, he sang for workers in the shipyards.', C('shipyard', 'Robeson leads shipyard workers in song, Oakland, 1942')],
  ['h3', 'In 1943 he played Othello on Broadway. It ran 296 performances, still a record for Shakespeare on Broadway.', P('othello', { focus: [0.5, 0.3], zoom: [1.05, 1.15] }), { stamp: '1943' }],
  ['h4', 'The N A A C P gave him its highest honor, the Spingarn Medal.', P('alston', { focus: [0.5, 0.35], zoom: [1.05, 1.15] })],
  ['h5', 'He was one of the most famous Black men in the world.', P('p1942', { focus: [0.5, 0.3], zoom: [1.05, 1.15] })],

  // ---- turning
  ['t1', 'And he refused to stay quiet. In 1946, after a wave of lynchings, he led a delegation to the White House.', C('truman', 'President Harry Truman'), { section: 'turn', stamp: '1946' }],
  ['t2', 'He asked President Truman to speak out against lynching. Truman said the time was not right.', P('truman', { focus: [0.5, 0.3], zoom: [1.1, 1.2] })],
  ['t3', 'Robeson warned that if the government would not protect Black Americans, they would defend themselves. The meeting was over.', V('uniclose', [0.5, 0.3])],
  ['t4', 'He also kept praising the Soviet Union. In Cold War America, that made him a target.', C('einstein', 'Robeson with Albert Einstein, 1947')],
  ['t5', 'In April 1949, he spoke at a peace congress in Paris. American newspapers reported that he had said Black Americans would never fight a war against Russia.', V('dark', [0.5, 0.32]), { stamp: 'April 1949' }],
  ['t6', 'His words had been twisted. But the damage was done.', V('jungle', [0.5, 0.32])],
  ['t7', 'Congress even called in Jackie Robinson, the man who broke baseball\'s color line, to answer him.', C('jackie', 'Jackie Robinson')],
  ['t8', 'Robinson said Robeson\'s statement, if it was reported right, sounded silly. And he used his time to attack racism at home.', P('jackie', { focus: [0.45, 0.42], zoom: [1.0, 1.08] })],

  // ---- Peekskill
  ['k1', 'That summer, Robeson was due to sing at a concert near Peekskill, New York.', P('bham', { focus: [0.5, 0.4], zoom: [1.05, 1.15] }), { section: 'peekskill', pin: { label: 'Peekskill, New York' } }],
  ['k2', 'Before he even got there, a mob attacked the crowd with rocks and clubs. A cross was burned on a hill nearby. The police did almost nothing.', T('Peekskill', '27 August 1949')],
  ['k3', 'A week later, he came back and sang to some twenty thousand people.', V('club', [0.5, 0.3])],
  ['k4', 'As they drove home, rioters stoned their cars and buses. More than a hundred and forty people were hurt.', T('140 injured', 'Peekskill, 4 September 1949')],

  // ---- passport
  ['p1', 'In 1950, the State Department cancelled his passport. He could no longer travel, or perform, abroad.', T('Passport cancelled', 'U.S. State Department, 1950'), { section: 'passport', stamp: '1950' }],
  ['p2', 'To get it back, he was told to sign a statement promising not to make speeches overseas. He refused.', P('nara', { focus: [0.5, 0.3], zoom: [1.1, 1.2] })],
  ['p3', 'At home, he was blacklisted. Concert halls shut their doors. His records were pulled from stores. His films disappeared.', V('close', [0.5, 0.3])],
  ['p4', 'His income fell from over a hundred thousand dollars a year to almost nothing.', T('Almost nothing', 'his income after the blacklist')],
  ['p5', 'He kept speaking out anyway, beside friends like W. E. B. Du Bois.', C('dubois', 'Robeson, W. E. B. Du Bois and Vito Marcantonio, 1951')],

  // ---- border
  ['b1', 'In January 1952, a miners\' union in Canada invited him to sing in Vancouver. No passport was needed to enter Canada back then.', V('helmet', [0.5, 0.3]), { section: 'border' }],
  ['b2', 'He was stopped at the border anyway, and turned back.', T('Turned back', 'U.S.-Canada border, 1952')],
  ['b3', 'So the union brought the concert to him. On May 18th, 1952, at the Peace Arch on the border, he stood on a flatbed truck on the American side.', P('p1930s', { focus: [0.5, 0.3], zoom: [1.05, 1.15] }), { stamp: '18 May 1952', pin: { label: 'Peace Arch, U.S.-Canada border' } }],
  ['b4', 'And he sang across the line, to tens of thousands of people on both sides.', V('sofa', [0.33, 0.32])],
  ['b5', 'In 1957, he did it again, across an ocean. Over the new transatlantic telephone cable, he sang from New York to a hall full of Welsh miners.', V('smile2', [0.5, 0.3]), { stamp: '1957' }],

  // ---- hearing
  ['q1', 'And in 1956, Congress called him in. The House Un-American Activities Committee.', V('talk2', [0.5, 0.35]), { section: 'hearing', lowerThird: { name: 'Paul Robeson', sub: 'U.S. Army film, 1940s' } }],
  ['q2', 'He refused to say whether he was a Communist. He told them his father was a slave, and that he would stay.', V('talk', [0.5, 0.35])],
  ['q3', 'Then, before it was over, he told the committee: You are the un-Americans, and you ought to be ashamed of yourselves.', Q('You are the un-Americans, and you ought to be ashamed of yourselves.', 'Paul Robeson to Congress, 1956')],

  // ---- return
  ['x1', 'In 1958 he published a book, Here I Stand. That June, the Supreme Court ruled that the government could not deny a passport over a person\'s beliefs.', C('welcome', 'The Afro-American, 1955'), { section: 'return', stamp: '1958' }],
  ['x2', 'After eight years, Paul Robeson got his passport back. He left for Europe almost at once.', C('ejstill', 'Paul Robeson in The Emperor Jones, 1933')],
  ['x3', 'In London he became the first Black performer to sing at Saint Paul\'s Cathedral. In 1959 he played Othello one more time, at Stratford-upon-Avon.', P('othello2', { focus: [0.5, 0.3], zoom: [1.05, 1.15] })],
  ['x4', 'But the years of pressure had taken their toll. In 1961, in Moscow, he suffered a breakdown.', V('quarry', [0.5, 0.35])],
  ['x5', 'He spent much of the next two years in hospitals.', P('p1942', { focus: [0.5, 0.3], zoom: [1.3, 1.4] })],

  // ---- end
  ['d1', 'In 1963 he came home to America, and lived quietly, out of public view. His wife Eslanda died two years later.', V('bssit', [0.5, 0.3]), { section: 'end' }],
  ['d2', 'Paul Robeson died in Philadelphia, on January 23rd, 1976. He was 77.', P('ulmann', { focus: [0.5, 0.3], zoom: [1.15, 1.25] }), { stamp: '23 January 1976' }],
  ['d3', 'Years later, Jackie Robinson wrote that he had come to respect him deeply, as a man who gave up his career, his wealth and his comfort to help his people.', P('jackie', { focus: [0.45, 0.42], zoom: [1.05, 1.12] })],
  ['d4', 'In 1995, Paul Robeson was finally named to the College Football Hall of Fame.', T('1995', 'College Football Hall of Fame')],
  ['d5', 'In 2004, he appeared on a United States postage stamp.', C('karsh', 'Paul Robeson, 1941')],

  // ---- close
  ['z1', 'His father escaped slavery. His teammates broke his nose. His country took his passport, his concerts and his income.', V('desk', [0.5, 0.4]), { section: 'close' }],
  ['z2', 'And still, he told Congress that this was his country too, and that he was going to stay.', V('talk2', [0.5, 0.35])],
  ['z3', 'That was Paul Robeson. Subscribe for more.', { kind: 'endcard' }, null, { captions: false }],
];

const base = JSON.parse(fs.readFileSync('data/doc-hattie-mcdaniel.json', 'utf8'));
const sources = {
  WIKI: 'https://en.wikipedia.org/wiki/Paul_Robeson',
  ENC: 'https://www.encyclopedia.com/education/news-wires-white-papers-and-books/robeson-paul',
  BRIT: 'https://www.britannica.com/biography/Paul-Robeson',
  RU: 'https://www.rutgers.edu/news/paul-robeson-launched-career-singer-and-stage-actor-after-rutgers-graduation',
  RU2: 'https://www.rutgers.edu/news/paul-robesons-journey-activism',
  COL: 'https://www.law.columbia.edu/news/archive/activist-global-stage-paul-robeson-1923',
  SWAN: 'https://collections.swansea.ac.uk/s/paul-robeson-wales/page/passport-withdrawal',
  SWAN2: 'https://collections.swansea.ac.uk/s/paul-robeson-wales/page/transatlantic-exchange',
  DWB: 'https://biography.wales/article/s14-ROBE-LER-1898',
  PAN: 'https://www.peacearchnews.com/community/look-back-at-political-statement-at-peace-arch-border/',
  MNW: 'https://mynorthwest.com/local/washingtons-forgotten-woodstock-of-the-mccarthy-era/294843',
  HUAC: 'https://www.marxists.org/archive/robeson/1956/06/12.htm',
  GMU: 'https://historymatters.gmu.edu/d/6440',
  PEEK: 'https://en.wikipedia.org/wiki/Peekskill_riots',
  ACAL: 'https://en.wikipedia.org/wiki/American_Crusade_Against_Lynching',
  TRU: 'https://www.trumanlibraryinstitute.org/civil-rights-symposium-history-6/',
  AND: 'https://andscape.com/features/jackie-robinson-was-asked-to-denounce-paul-robeson-before-huac-instead-he-went-after-jim-crow/',
  NATION: 'https://www.thenation.com/article/archive/huac-jackie-robinson-paul-robeson/',
  SABR: 'https://sabr.org/journal/article/cold-warrior-the-jackie-robinson-story/',
  CFHOF: 'https://cfbhall.com/inductees/paul-robeson-1995',
  NARA: 'https://commons.wikimedia.org/wiki/File:%22Paul_Robeson,_world_famous_Negro_baritone,_leading_Moore_Shipyard_(Oakland,_CA)_workers_in_singing_the_Star_Spangled_Ba_-_NARA_-_535874.jpg',
  FILMS: 'https://commons.wikimedia.org/wiki/File:Easy_to_get.webm',
};
const sourcesByClaim = {
  o2: ['HUAC', 'GMU', 'WIKI'], o3: ['HUAC', 'GMU'], o4: ['HUAC', 'GMU', 'RU2'],
  e1: ['WIKI', 'ENC', 'BRIT'], e2: ['WIKI', 'ENC'], e3: ['WIKI', 'ENC'], e4: ['WIKI', 'ENC'], e5: ['WIKI', 'ENC'],
  r1: ['WIKI', 'RU'], r2: ['WIKI', 'RU'], r3: ['WIKI', 'RU', 'ENC'], r4: ['WIKI', 'RU'], r5: ['WIKI', 'ENC', 'CFHOF'], r6: ['WIKI', 'RU', 'RU2'],
  l1: ['WIKI', 'COL', 'CFHOF'], l2: ['WIKI', 'CFHOF'], l3: ['WIKI', 'ENC'], l4: ['COL', 'WIKI'], l5: ['WIKI', 'COL', 'ENC'], l6: ['WIKI', 'COL'],
  s1: ['WIKI', 'ENC', 'RU'], s2: ['WIKI', 'FILMS', 'ENC'], s3: ['WIKI', 'RU', 'ENC'], s4: ['RU', 'ENC'],
  w1: ['WIKI', 'ENC'], w2: ['WIKI', 'ENC', 'BRIT'], w3: ['WIKI', 'RU2'], w4: ['WIKI', 'BRIT'], w5: ['RU2', 'DWB', 'WIKI'], w6: ['WIKI', 'ENC'], w7: ['WIKI', 'ENC'],
  h1: ['WIKI', 'ENC'], h2: ['NARA', 'WIKI'], h3: ['WIKI', 'ENC', 'BRIT'], h4: ['WIKI', 'ENC'], h5: ['WIKI', 'BRIT'],
  t1: ['WIKI', 'ACAL', 'TRU'], t2: ['ACAL', 'RU2', 'WIKI'], t3: ['WIKI', 'RU2'], t4: ['WIKI', 'ENC'], t5: ['WIKI', 'ENC', 'RU2'], t6: ['WIKI', 'ENC'],
  t7: ['WIKI', 'AND', 'NATION'], t8: ['WIKI', 'AND', 'SABR'],
  k1: ['PEEK', 'WIKI'], k2: ['PEEK', 'WIKI'], k3: ['PEEK', 'WIKI'], k4: ['PEEK', 'ENC'],
  p1: ['WIKI', 'SWAN', 'RU2'], p2: ['SWAN', 'WIKI', 'ENC'], p3: ['WIKI', 'ENC', 'SWAN'], p4: ['WIKI', 'ENC'], p5: ['WIKI', 'ENC'],
  b1: ['PAN', 'MNW', 'WIKI'], b2: ['PAN', 'MNW'], b3: ['PAN', 'MNW', 'WIKI'], b4: ['PAN', 'MNW'], b5: ['WIKI', 'DWB', 'SWAN2'],
  q1: ['HUAC', 'GMU'], q2: ['HUAC', 'GMU'], q3: ['HUAC', 'GMU', 'WIKI'],
  x1: ['WIKI', 'ENC', 'SWAN'], x2: ['WIKI', 'RU2'], x3: ['WIKI', 'ENC'], x4: ['WIKI', 'ENC'], x5: ['WIKI', 'ENC'],
  d1: ['WIKI', 'ENC'], d2: ['WIKI', 'ENC', 'BRIT'], d3: ['AND', 'NATION', 'SABR'], d4: ['CFHOF', 'WIKI'], d5: ['WIKI', 'BRIT'],
};

const spec = {
  id: 'doc-paul-robeson',
  title: 'America Took His Passport: The Paul Robeson Story',
  format: 'doc',
  fps: 30,
  width: 1920,
  height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.0, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: { Robeson: 'Robe-son', "Ol' Man River": 'Old Man River', Eslanda: 'Es-lahn-da', Micheaux: 'Mee-show', Teruel: 'Teh-roo-el', 'Du Bois': 'Doo Boyss', Peekskill: 'Peek-skill', Chillun: 'Chill-un' },
  music: base.music,
  mix: base.mix,
  brand: { page: 'The Black History Room', cta: 'Subscribe', ctaLine: '', theme: 'bhr' },
  assets: Object.fromEntries(Object.entries(assets).map(([k, v]) => [k, { commons: v }])),
  clips,
  beats: beats.map(([id, text, visual, overlays, extra]) => {
    const { section, ...ov } = overlays || {};
    return { id, text, visual, ...(Object.keys(ov).length ? { overlays: ov } : {}), ...(section ? { section } : {}), ...(extra || {}) };
  }),
  sourcesByClaim,
  sources: Object.fromEntries(Object.entries(sources).map(([k, url]) => [k, { url }])),
  notUsed: [
    'Mother\'s death: house fire (Wikipedia) vs stove-fire accident (Encyclopedia.com): said as "a fire at home".',
    'Income: $150,000 to under $3,000 (Wikipedia) vs $104,000 to $6,000 (other accounts): said as "over a hundred thousand ... almost nothing".',
    'Peace Arch crowd: 25,000-40,000 depending on source: said as "tens of thousands".',
    'Truman "abruptly ended the meeting": weaker sources; said as "The meeting was over".',
    'Jackie Robinson\'s later respect: wording from his 1972 autobiography as quoted by Andscape, The Nation and SABR; paraphrased, not quoted.',
    'Easy to Get: Commons dates it 1947, other catalogues 1944: labelled "1940s". It is footage of Robeson speaking to soldiers, not of the 1956 hearing; the hearing beats use it as illustration only.',
    '1961 suicide attempt and electroconvulsive therapy: true (Wikipedia) but left out; script says "breakdown" and "hospitals".',
    'Stalin Prize 1952: left out for time.',
  ],
};
fs.writeFileSync('data/doc-paul-robeson.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images, ${Object.keys(clips).length} clips`);
