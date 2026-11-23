// Builds data/doc-erased-towns.json: long-form countdown (16:9), "15 Forgotten Black Towns America Erased".
// Long-form queue video 1 (docs/long-form-queue.md). Research and sources: docs/long-form-erased-towns-research.md.
// Every fact has two or more sources (sourcesByClaim); disputed numbers are avoided or given as ranges.
// Images: public domain / CC0 only. Tulsa photos are reused from public/pd/doc-black-wall-street (copy them in with
// their credits before rendering). Voice: free Kokoro. Ending: only "subscribe for more".
// Run: node data/build_doc_erased_towns.mjs
import fs from 'node:fs';

const P = (key, o = {}) => ({ kind: 'photo', image: key, ...o });
const C = (key, caption, o = {}) => ({ kind: 'card', image: key, caption, ...o });
const T = (title, sub) => ({ kind: 'title', title, sub });
const CH = (num, title) => ({ kind: 'chapter', num, title });
const S = (to, label, image, o = {}) => ({ kind: 'stat', image, stat: { to, label, ...o } });
const PZ = (key, fy = 0.3) => P(key, { focus: [0.5, fy], zoom: [1.04, 1.12], anchor: [0.5, 0.42] });
const NC = { captions: false };

const assets = {
  atlfront: 'File:Front Page of Atlanta Georgian Newspaper Sep 10 1912.jpg',
  jaildoor: 'File:Mob batters down jail door at Cumming, Atlanta Georgian Newspaper Sep 10 1912.jpg',
  defendants: 'File:Defendants in 1912 Forsyth County Trials.jpg',
  lanier: 'File:Island in Lake Lanier, July 2018.jpg',
  buford: 'File:Buford Dam March 2017 1.jpg',
  jjbenson: 'File:John Jackson Benson.png',
  wbenson: 'File:William E. Benson of Kowaliga, Alabama.png',
  kinst: 'File:General View of Kowaliga Academic and Industrial Institute.png',
  kcampus: 'File:Kowaliga Academic and Industrial Institute campus view east.png',
  vanport: 'File:1948 Vanport flood.jpg',
  deltapark: 'File:AT DELTA PARK ON THE COLUMBIA RIVER - NARA - 548116.jpg',
  julyperry: 'File:July Perry Ocoee Massacre victim.jpg',
  ocoeefront: 'File:Front-page-Evening-Reporter-Star-November-3-1920-Ocoee-Massacre-Florida.jpg',
  ros2: 'File:Rosewood Florida rc12409.jpg',
  rosmap: 'File:Rosewood 1923 map from Tropic Magazine.jpg',
  sarah: 'File:Sara Carrier.jpg',
  roshead: 'File:Rosewood Florida Headline.jpg',
  hattie: 'File:Studio publicity Hattie McDaniel.jpg',
  hattie41: 'File:1941hattie.jpg',
  wilkins: 'File:Portrait of Roy Wilkins LCCN2004663739.jpg',
  wilkins68: 'File:Roy Wilkins at the White House, 30 April, 1968.jpg',
  joelouis: 'File:Joe Louis, Underwood & Underwood, active 1880 - c. 1950, from the National Portrait Gallery, Smithsonian Institution.tif',
  holiday: 'File:Billie Holiday, Downbeat, New York, N.Y., ca. Feb. 1947 (William P. Gottlieb 04251).jpg',
  ella: 'File:Ella Fitzgerald (Gottlieb 02871) (cropped).jpg',
  claiborne: 'File:ClaiborneFrenchmen1938B.jpg',
  merrick: 'File:John Merrick at the Age of 40.jpg',
  armstrong: 'File:Louis Armstrong restored.jpg',
  waters: 'File:Maxine Waters Official.jpg',
};

const beats = [
  // ---- open
  ['o1', 'They didn\'t fade away. They were burned, flooded, bulldozed, and paved over.', P('smoke', { focus: [0.45, 0.4], zoom: [1.0, 1.1] }), { hook: 'They didn\'t fade away. *They were erased.*' }, NC],
  ['o2', 'Today, people swim, drive and park on top of them, and most have never heard their names.', P('lanier', { motion: 'panRight', zoom: [1.0, 1.05] })],
  ['o3', 'These are fifteen Black towns and neighborhoods that America erased. We\'ll count down to the one you think you know.', T('15 Towns', 'that America erased')],

  // ---- 15 Oscarville
  ['a0', 'Number fifteen. Oscarville, Georgia.', CH(15, 'Oscarville, Georgia'), { section: 'oscarville' }, NC],
  ['a1', 'In 1912, Forsyth County, Georgia, had about eleven hundred Black residents. Many of them farmed around a small place called Oscarville.', C('atlfront', 'Atlanta Georgian, September 10, 1912'), { pin: { label: 'Oscarville', sub: 'Forsyth County, Georgia' } }],
  ['a2', 'That fall, after a young white woman was killed, a mob lynched one Black man. Two Black teenagers were hanged after rushed trials.', C('jaildoor', 'The mob at the Cumming jail, 1912')],
  ['a3', 'Night riders burned homes and churches, and ordered every Black person out of the county. Within weeks, almost all of them were gone. Their land passed into white hands.', C('defendants', 'Defendants in the 1912 trials')],
  ['a4', 'Forty years later, the government built Buford Dam, and the water rose. Today, Oscarville lies under Lake Lanier, where people boat and swim every summer.', P('buford', { motion: 'panLeft', zoom: [1.0, 1.05] }), { stamp: 'Lake Lanier' }],

  // ---- 14 Kowaliga
  ['b0', 'Number fourteen. Kowaliga, Alabama.', CH(14, 'Kowaliga, Alabama'), { section: 'kowaliga' }, NC],
  ['b1', 'John Jackson Benson was born enslaved. After freedom, he bought land in Alabama, and a Black community grew around it, called Kowaliga.', C('jjbenson', 'John Jackson Benson, 1911')],
  ['b2', 'His son William opened a school there. Then the family\'s company built its own railroad, sixteen miles long, to Alexander City.', C('kinst', 'Kowaliga Academic and Industrial Institute')],
  ['b3', 'But William died in 1915, and the town began to decline. Then Alabama Power built Martin Dam.', C('wbenson', 'William E. Benson')],
  ['b4', 'When the new lake filled, Kowaliga went under. Today, lake houses line the water above it.', P('kcampus', { motion: 'panRight', zoom: [1.0, 1.06] }), { stamp: 'Lake Martin' }],

  // ---- 13 Vanport
  ['c0', 'Number thirteen. Vanport, Oregon.', CH(13, 'Vanport, Oregon'), { section: 'vanport' }, NC],
  ['c1', 'In 1942, to house shipyard workers, the Kaiser company built a whole city outside Portland. Vanport became the second largest city in Oregon.', T('Vanport', 'Oregon, 1942')],
  ['c2', 'Thousands of Black workers came for the war jobs. By 1948, about a third of the people still living there were Black.', P('vanport', { focus: [0.5, 0.45], zoom: [1.0, 1.06] })],
  ['c3', 'On May 30th, 1948, residents were told the dikes were safe. That afternoon, a railroad embankment gave way.', T('May 30, 1948', 'Memorial Day')],
  ['c4', 'By nightfall, the city was gone. Fifteen people died, and about eighteen thousand lost their homes. Vanport was never rebuilt. Today the land holds a park, a racetrack and a golf course.', C('deltapark', 'Delta Park, on the site of Vanport')],

  // ---- 12 Bruce's Beach
  ['d0', 'Number twelve. Bruce\'s Beach, California.', CH(12, 'Bruce\'s Beach, California'), { section: 'bruces' }, NC],
  ['d1', 'In 1912, Willa and Charles Bruce bought beachfront land in Manhattan Beach, and opened a resort for Black families, who were shut out of other beaches.', T('Bruce\'s Beach', 'Manhattan Beach, California')],
  ['d2', 'They were harassed for years. In 1924, the city took their land by eminent domain, saying it needed a park.', T('1924', 'the city takes the land')],
  ['d3', 'The Bruces asked for a hundred and twenty thousand dollars. They got fourteen thousand five hundred.', S(14500, 'paid to the Bruces, 1929', null, { prefix: '$' })],
  ['d4', 'In 2022, Los Angeles County gave the land back to their great-grandsons. The family then sold it to the county, for twenty million dollars.', S(20, 'paid to the Bruce family, 2023', null, { prefix: '$', suffix: ' million' })],

  // ---- 11 Ocoee
  ['e0', 'Number eleven. Ocoee, Florida.', CH(11, 'Ocoee, Florida'), { section: 'ocoee' }, NC],
  ['e1', 'On Election Day, 1920, a Black landowner in Ocoee named Mose Norman went to vote, and was turned away.', C('ocoeefront', 'Evening Reporter-Star, November 3, 1920')],
  ['e2', 'That night, a white mob went to the home of another Black landowner, July Perry, who had helped register Black voters. Perry was lynched.', C('julyperry', 'July Perry')],
  ['e3', 'The mob burned Black homes, two churches and a lodge. Nobody knows how many people died. Estimates run from about thirty to more than fifty.', P('ocoeefront', { focus: [0.5, 0.3], zoom: [1.1, 1.2], anchor: [0.5, 0.35] })],
  ['e4', 'Every Black family was driven out. In 1930, the census counted two Black residents in Ocoee.', S(2, 'Black residents in Ocoee, 1930 census', 'julyperry')],

  // ---- 10 Rosewood
  ['f0', 'Number ten. Rosewood, Florida.', CH(10, 'Rosewood, Florida'), { section: 'rosewood' }, NC],
  ['f1', 'Rosewood was a small town in the Florida woods. Most of its families were Black, and worked in timber and turpentine.', C('rosmap', 'Rosewood, Florida, January 1923')],
  ['f2', 'On New Year\'s Day, 1923, a white woman in a nearby town said a Black man had attacked her. White mobs poured into Rosewood.', C('roshead', 'The news, January 1923')],
  ['f3', 'Sarah Carrier was killed in her home. Over the next week, the mobs burned almost every building in town.', C('sarah', 'Sarah Carrier')],
  ['f4', 'The official count was eight dead. Survivors said there were many more. No one was ever charged, and Rosewood was never rebuilt.', C('ros2', 'A house burns in Rosewood, 1923')],
  ['f5', 'Seventy years later, in 1994, Florida became the first state to pay compensation for racial violence, to the survivors of Rosewood.', T('1994', 'Florida pays the survivors')],

  // ---- 9 Sugar Hill
  ['g0', 'Number nine. Sugar Hill, Los Angeles.', CH(9, 'Sugar Hill, Los Angeles'), { section: 'sugarhill' }, NC],
  ['g1', 'In the 1940s, Black stars bought mansions on a hill in Los Angeles that came to be called Sugar Hill. Hattie McDaniel, the first Black Oscar winner, was one of them.', C('hattie', 'Hattie McDaniel')],
  ['g2', 'White neighbors sued to force them out, using racial covenants in the deeds. In December 1945, a judge threw the case out.', PZ('hattie41', 0.25)],
  ['g3', 'They had won in court. Then the state built the Santa Monica Freeway, right through the neighborhood.', T('Interstate 10', 'through Sugar Hill')],

  // ---- 8 Rondo
  ['h0', 'Number eight. Rondo, St. Paul.', CH(8, 'Rondo, St. Paul'), { section: 'rondo' }, NC],
  ['h1', 'Rondo was the heart of Black St. Paul, Minnesota. By the 1930s, about half of the city\'s Black residents lived there. Roy Wilkins, later the head of the NAACP, grew up there.', C('wilkins', 'Roy Wilkins')],
  ['h2', 'Then planners sent Interstate 94 straight through it. Hundreds of homes and businesses were torn down.', T('Interstate 94', 'St. Paul, Minnesota')],
  ['h3', 'In 2015, the mayor of St. Paul apologized.', PZ('wilkins68', 0.3)],

  // ---- 7 Black Bottom
  ['i0', 'Number seven. Black Bottom, Detroit.', CH(7, 'Black Bottom, Detroit'), { section: 'blackbottom' }, NC],
  ['i1', 'In Detroit, Black Bottom and Paradise Valley were full of homes, churches, clubs and Black-owned businesses. Joe Louis grew up there.', C('joelouis', 'Joe Louis')],
  ['i2', 'Duke Ellington and Billie Holiday played its clubs.', C('holiday', 'Billie Holiday, 1947')],
  ['i3', 'From the 1950s, the city cleared it for urban renewal, and laid a freeway, Interstate 375, over Hastings Street.', T('Interstate 375', 'over Hastings Street')],
  ['i4', 'Today that freeway is being torn out, with a hundred and four million dollars in federal money. The neighborhood is not coming back.', S(104, 'federal grant to remove I-375, 2022', 'joelouis', { prefix: '$', suffix: ' million' })],

  // ---- 6 Overtown
  ['j0', 'Number six. Overtown, Miami.', CH(6, 'Overtown, Miami'), { section: 'overtown' }, NC],
  ['j1', 'Overtown was the Black heart of Miami. Its main street was called the Little Broadway.', T('Overtown', 'Miami, Florida')],
  ['j2', 'When stars like Ella Fitzgerald and Billie Holiday played Miami Beach, they could not stay there. They stayed in Overtown.', C('ella', 'Ella Fitzgerald, 1946')],
  ['j3', 'In the 1960s, Interstate 95 and its interchange were driven through its center. Most of its people were pushed out.', T('Interstate 95', 'through Overtown')],

  // ---- 5 Claiborne Avenue
  ['k0', 'Number five. Claiborne Avenue, New Orleans.', CH(5, 'Claiborne Avenue, New Orleans'), { section: 'claiborne' }, NC],
  ['k1', 'Claiborne Avenue was the main street of Black business in New Orleans, with a wide row of oak trees down the middle, where families gathered at Mardi Gras.', C('claiborne', 'Claiborne Avenue, 1938')],
  ['k2', 'In 1966, the oaks were bulldozed. An elevated interstate was built right on top of the avenue.', P('claiborne', { focus: [0.5, 0.45], zoom: [1.1, 1.2] }), { stamp: '1966' }],
  ['k3', 'Today, artists have painted oak trees on the concrete pillars.', T('Interstate 10', 'over Claiborne Avenue')],

  // ---- 4 Hayti
  ['l0', 'Number four. Hayti, Durham.', CH(4, 'Hayti, Durham'), { section: 'hayti' }, NC],
  ['l1', 'Freed people built Hayti, in Durham, North Carolina, right after the Civil War. Its businessmen, like John Merrick, helped make Durham famous as a Black Wall Street.', C('merrick', 'John Merrick')],
  ['l2', 'In 1958, urban renewal began. Then came the Durham Freeway. About four thousand families and five hundred businesses were displaced.', S(4000, 'families displaced', 'merrick')],
  ['l3', 'Out of the whole neighborhood, one church was left standing.', T('One church', 'left standing')],

  // ---- 3 Fillmore
  ['m0', 'Number three. The Fillmore, San Francisco.', CH(3, 'The Fillmore, San Francisco'), { section: 'fillmore' }, NC],
  ['m1', 'San Francisco\'s Fillmore district was called the Harlem of the West. Jazz played all night, and Louis Armstrong played there.', C('armstrong', 'Louis Armstrong')],
  ['m2', 'From 1956, the city\'s redevelopment agency cleared it, block by block. Residents had a name for it: Negro removal.', T('Redevelopment', 'block by block')],
  ['m3', 'Thousands of families were given certificates, promising them a way back. Only four percent were ever used.', S(4, 'of the promises to return were ever used', 'armstrong', { suffix: '%' })],

  // ---- 2 Kinloch
  ['n0', 'Number two. Kinloch, Missouri.', CH(2, 'Kinloch, Missouri'), { section: 'kinloch' }, NC],
  ['n1', 'Kinloch was founded in 1890, and became the oldest Black city in Missouri. Congresswoman Maxine Waters grew up there.', C('waters', 'Maxine Waters')],
  ['n2', 'From the 1980s, the airport next door bought out its homes, to clear land for noise. In 1960, Kinloch had about sixty-five hundred people. In 2020, it had two hundred and sixty-three.', S(263, 'people left in Kinloch, 2020', 'waters', { from: 6501 })],

  // ---- 1 Greenwood
  ['p0', 'Number one. Greenwood, Tulsa.', CH(1, 'Greenwood, Tulsa'), { section: 'greenwood' }, NC],
  ['p1', 'Greenwood was the Black district of Tulsa, Oklahoma. It was so prosperous, people called it Black Wall Street.', P('panorama', { motion: 'panRight', zoom: [1.0, 1.05] })],
  ['p2', 'On May 31st and June 1st, 1921, a white mob burned more than thirty-five blocks. The Red Cross counted twelve hundred and fifty-six homes burned.', P('smoke', { focus: [0.45, 0.4], zoom: [1.05, 1.15] }), { stamp: '1921' }],
  ['p3', 'About ten thousand people were left homeless. The official death toll was thirty-six. Historians now believe it may have been as high as three hundred.', P('ruins', { zoom: [1.0, 1.08] })],
  ['p4', 'And then Greenwood did something remarkable. It rebuilt.', C('rebuild', 'Greenwood rebuilding')],
  ['p5', 'Decades later, urban renewal and a new interstate, I-244, cut straight through it. Greenwood was destroyed twice.', T('Destroyed twice', '1921 and the 1960s')],

  // ---- close
  ['x1', 'Fifteen places. Some burned, some flooded, some paved over. You can still drive across most of them today, without ever knowing their names.', P('lanier', { motion: 'panLeft', zoom: [1.05, 1.1] }), { section: 'close' }],
  ['x2', 'Subscribe for more.', { kind: 'endcard' }, null, NC],
];

const sources = {
  NPRFORSYTH: 'https://www.npr.org/2016/09/15/494063372/the-racial-cleansing-that-drove-1-100-black-residents-out-of-forsyth-county-ga',
  AHC: 'https://www.atlantahistorycenter.com/blog/forsyth-1912-examining-the-displacement-of-the-countys-black-residents/',
  WPOSCAR: 'https://en.wikipedia.org/wiki/Oscarville,_Georgia',
  WPKOW: 'https://en.wikipedia.org/wiki/Kowaliga,_Alabama',
  ACO: 'https://www.alexcityoutlook.com/news/two-amateur-historians-are-putting-the-drowned-town-of-benson-back-on-the-map/article_3afaeb42-a820-11eb-a63e-5b09d47736a2.html',
  EOA: 'https://encyclopediaofalabama.org/?p=14926',
  WPVAN: 'https://en.wikipedia.org/wiki/Vanport,_Oregon',
  OREENC: 'https://www.oregonencyclopedia.org/articles/vanport/',
  NPRVAN: 'https://www.npr.org/sections/codeswitch/2015/03/02/389482158/the-time-nature-and-racism-teamed-up-to-wipe-out-a-whole-town',
  WPBRUCE: 'https://en.wikipedia.org/wiki/Bruce%27s_Beach',
  ABC7: 'https://abc7.com/bruces-beach-manhattan-la-county-coastal-property/12647127/',
  DB: 'https://www.dailybreeze.com/2022/06/28/la-county-returns-land-to-black-family-90-plus-years-after-manhattan-beach-took-it',
  WPOCOEE: 'https://en.wikipedia.org/wiki/Ocoee_massacre',
  OPPAGA: 'https://oppaga.fl.gov/Documents/Reports/19-15.pdf',
  WAPO: 'https://www.washingtonpost.com/history/2020/11/02/ocoee-florida-election-day-massacre/',
  WPROSE: 'https://en.wikipedia.org/wiki/Rosewood_massacre',
  BRITROSE: 'https://www.britannica.com/topic/Rosewood-riot-of-1923',
  SCROSE: 'https://southernchanges.digitalscholarship.emory.edu/sc16-1_001/sc16-1_005',
  NPRSUGAR: 'https://www.npr.org/2021/05/04/993605428/beneath-the-santa-monica-freeway-lies-the-erasure-of-sugar-hill',
  WPSUGAR: 'https://en.wikipedia.org/wiki/West_Adams_Heights,_Los_Angeles',
  FOX11: 'https://www.foxla.com/news/sugar-hill-the-dark-history-the-10-freeway-has-to-a-historic-black-community',
  MNOPEDIA: 'https://www.mnhs.org/mnopedia/search/index/place/rondo-neighborhood-st-paul',
  KARE: 'https://kare11.com/article/news/local/rondo-neighborhood-gets-apologies-for-i-94/105454642',
  PBSRONDO: 'https://www.pbs.org/newshour/show/could-a-land-bridge-project-help-minority-communities-recover-from-displacement',
  DHS: 'https://detroithistorical.org/learn/encyclopedia-of-detroit/black-bottom-neighborhood',
  WPBB: 'https://en.wikipedia.org/wiki/Black_Bottom,_Detroit',
  DET375: 'https://detroitmi.gov/departments/planning-and-development-department/neighborhood-plans/central-design-region/i-375-reconnecting-communities-project',
  UMOVER: 'https://library.miami.edu/ohp-communities-overtown.html',
  NPROVER: 'https://www.npr.org/2010/08/28/129475747/paying-a-local-price-for-i-95s-global-promise',
  WPOVER: 'https://en.wikipedia.org/wiki/Overtown_(Miami)',
  TRIPOD: 'https://tripodnola.hnoc.org/episodes/the-monster-claiborne-avenue-before-and-after-the-interstate/',
  SMITHCLAI: 'https://www.smithsonianmag.com/smart-news/documenting-history-iconic-new-orleans-street-and-looking-its-future-180977854/',
  WPCLAI: 'https://en.wikipedia.org/wiki/Claiborne_Avenue',
  BC150: 'https://www.bullcity150.org/uneven_ground/dismantling_hayti/',
  ABC11: 'https://abc11.com/post/durham-hayti-community-freeway-history-black/10362504/',
  WPHAYTI: 'https://en.wikipedia.org/wiki/Hayti,_Durham,_North_Carolina',
  KQED: 'https://www.kqed.org/news/11825401/how-urban-renewal-decimated-the-fillmore-district-and-took-jazz-with-it',
  PBSFILL: 'https://www.pbs.org/kqed/fillmore/',
  WPFILL: 'https://en.wikipedia.org/wiki/Fillmore_District,_San_Francisco',
  WPKIN: 'https://en.wikipedia.org/wiki/Kinloch,_Missouri',
  RFT: 'https://www.riverfronttimes.com/?p=42185',
  STLPR: 'https://www.stlpr.org/other/2006-06-07/lambert-considers-selling-back-land-to-kinloch',
  OHS: 'https://www.okhistory.org/publications/enc/entry?entry=TU013',
  WPTULSA: 'https://en.wikipedia.org/wiki/Tulsa_race_massacre',
  SMITHTULSA: 'https://www.smithsonianmag.com/history/black-wall-streets-second-destruction-180977871/',
};
const sourcesByClaim = {
  o1: ['WPTULSA', 'NPRSUGAR', 'WPOSCAR'], o2: ['WPOSCAR', 'WPVAN'], o3: ['WPOSCAR', 'WPTULSA'],
  a1: ['NPRFORSYTH', 'AHC', 'WPOSCAR'], a2: ['NPRFORSYTH', 'AHC'], a3: ['NPRFORSYTH', 'AHC', 'WPOSCAR'], a4: ['AHC', 'WPOSCAR'],
  b1: ['WPKOW', 'ACO'], b2: ['WPKOW', 'ACO'], b3: ['WPKOW', 'EOA'], b4: ['WPKOW', 'ACO', 'EOA'],
  c1: ['WPVAN', 'OREENC'], c2: ['WPVAN', 'OREENC', 'NPRVAN'], c3: ['NPRVAN', 'WPVAN'], c4: ['WPVAN', 'OREENC', 'NPRVAN'],
  d1: ['WPBRUCE', 'DB'], d2: ['WPBRUCE', 'DB'], d3: ['WPBRUCE', 'DB'], d4: ['WPBRUCE', 'ABC7', 'DB'],
  e1: ['WPOCOEE', 'OPPAGA', 'WAPO'], e2: ['WPOCOEE', 'OPPAGA', 'WAPO'], e3: ['WPOCOEE', 'OPPAGA'], e4: ['WPOCOEE', 'OPPAGA'],
  f1: ['WPROSE', 'BRITROSE'], f2: ['WPROSE', 'BRITROSE'], f3: ['WPROSE', 'SCROSE'], f4: ['WPROSE', 'BRITROSE'], f5: ['WPROSE', 'BRITROSE', 'SCROSE'],
  g1: ['NPRSUGAR', 'WPSUGAR', 'FOX11'], g2: ['NPRSUGAR', 'WPSUGAR'], g3: ['NPRSUGAR', 'WPSUGAR', 'FOX11'],
  h1: ['MNOPEDIA', 'PBSRONDO'], h2: ['MNOPEDIA', 'KARE', 'PBSRONDO'], h3: ['KARE', 'PBSRONDO'],
  i1: ['DHS', 'WPBB'], i2: ['DHS', 'WPBB'], i3: ['DHS', 'WPBB'], i4: ['DET375', 'WPBB'],
  j1: ['UMOVER', 'WPOVER'], j2: ['UMOVER', 'WPOVER'], j3: ['UMOVER', 'NPROVER', 'WPOVER'],
  k1: ['TRIPOD', 'SMITHCLAI', 'WPCLAI'], k2: ['TRIPOD', 'WPCLAI'], k3: ['TRIPOD', 'SMITHCLAI'],
  l1: ['BC150', 'WPHAYTI'], l2: ['BC150', 'ABC11', 'WPHAYTI'], l3: ['ABC11', 'WPHAYTI'],
  m1: ['KQED', 'PBSFILL', 'WPFILL'], m2: ['KQED', 'WPFILL'], m3: ['KQED', 'WPFILL'],
  n1: ['WPKIN', 'RFT'], n2: ['WPKIN', 'RFT', 'STLPR'],
  p1: ['OHS', 'WPTULSA'], p2: ['OHS', 'WPTULSA'], p3: ['OHS', 'WPTULSA'], p4: ['SMITHTULSA', 'OHS'], p5: ['SMITHTULSA', 'WPTULSA'],
  x1: ['WPOSCAR', 'WPTULSA'],
};

const base = JSON.parse(fs.readFileSync('data/doc-black-wall-street.json', 'utf8'));
const spec = {
  id: 'doc-erased-towns',
  title: '15 Forgotten Black Towns America Erased',
  format: 'doc', fps: 30, width: 1920, height: 1080,
  voice: { engine: 'kokoro', voice: 'am_michael', speed: 1.05, leadInSeconds: 0.4, sectionGapSeconds: 1 },
  pronounce: {
    Oscarville: 'Oscar-ville', Kowaliga: 'Koh-wah-LIE-guh', Ocoee: 'Oh-KOH-ee', Vanport: 'Van-port', Hayti: 'Hay-tie',
    Claiborne: 'Clay-born', Kinloch: 'Kin-lock', Rondo: 'Ron-doh', Overtown: 'Over-town', Greenwood: 'Green-wood', 'Mose Norman': 'Mohz Norman',
  },
  music: base.music, mix: base.mix,
  brand: { page: 'The Black History Room', cta: 'Subscribe', ctaLine: '', theme: 'bhr' },
  assets: Object.fromEntries(Object.entries(assets).map(([k, v]) => [k, { commons: v }])),
  keywords: ['Oscarville', 'Kowaliga', 'Vanport', 'Bruce', 'Ocoee', 'Rosewood', 'Sugar Hill', 'Rondo', 'Black Bottom', 'Paradise Valley',
    'Overtown', 'Claiborne', 'Hayti', 'Fillmore', 'Kinloch', 'Greenwood', 'Black Wall Street', 'Interstate', 'freeway', 'destroyed twice'],
  chapters: Object.fromEntries(beats.filter((b) => b[2].kind === 'chapter').map((b) => [b[3].section, b[2].title])),
  chapterLabel: 'No.',
  chapterCountdown: true,
  grain: true,
  beats: beats.map(([id, text, visual, overlays, extra]) => {
    const { section, ...ov } = overlays || {};
    const v = Object.fromEntries(Object.entries(visual).filter(([, x]) => x !== null && x !== undefined));
    return { id, text, visual: v, ...(Object.keys(ov).length ? { overlays: ov } : {}), ...(section ? { section } : {}), ...(extra || {}) };
  }),
  sourcesByClaim,
  sources: Object.fromEntries(Object.entries(sources).map(([k, url]) => [k, { url }])),
  notUsed: [
    'Oscarville "flooded on purpose to erase a Black town": called mostly myth by the Atlanta History Center. Told as expelled in 1912, under the lake decades later.',
    'Forsyth crowd sizes (2,000 / 8,000): one source: not said.',
    'Kowaliga\'s "first Black-owned railroad": one source: not said.',
    'Vanport peak population (40,000 / 42,000) and peak Black share: disputed: not said.',
    'Ocoee buildings burned (25+ vs 20) and deaths (30-56): given as a range.',
    'Rosewood deaths beyond the official 8 (27 / 150): "many more". Compensation amount ($2M / $2.1M): not said.',
    'Rondo homes (600 / 700): "hundreds".',
    'Overtown population drop (40,000 to 10,000 / 50% / 40%): "most of its people".',
    'Claiborne oaks (200 / 400) and homes (155 / 500): not said.',
    'Hayti 5,000+ families / 1,000+ businesses (one paper): the 4,000 / 500 figures used.',
    'Kinloch buyout cost and "meant to dissolve the town": one source / disputed: not said.',
    'Tulsa deaths: official 36; historians up to about 300 (OHS "fifty to three hundred").',
    'I-244 construction years disputed: "decades later".',
  ],
};
fs.writeFileSync('data/doc-erased-towns.json', JSON.stringify(spec, null, 1) + '\n');
const text = beats.map((b) => b[1]).join(' ');
const missing = beats.filter((b) => !sourcesByClaim[b[0]] && !['chapter', 'endcard'].includes(b[2].kind)).map((b) => b[0]);
console.log(`${beats.length} beats, ${text.split(/\s+/).length} words, ${text.length} characters, ${Object.keys(assets).length} images, missing sources: ${missing.join(',') || 'none'}`);
