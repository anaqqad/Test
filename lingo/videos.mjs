// Scripts for the four videos. Facts are kept conservative (ranges, "fewer than") where sources disagree.
// audio: {file, start?} one Commons recording (start "auto" = first stretch that is not English),
//        {ll: iso639-3, words?: [...], n?} Lingua Libre word recordings, {seq: [File names]} short clips in a row.
// flag: ISO 3166 code from flag-icons, or a custom key from FLAGS in render.mjs, or null.

export const CHANNEL = "LingoDude";

const F = (o) => ({ fem: true, ...o });

export const VIDEOS = {
  // ------------------------------------------------------------------ 1
  extinct2: {
    title: "Nearly Extinct Languages be like…",
    part: "Part 2",
    layout: "story",
    counterLabel: "speakers",
    items: [
      {
        name: "Wymysorys", flag: "pl", speakers: "~20", scene: "village", loc: [49.9, 19.15, "Wilamowice, Poland"],
        char: F({ skin: "pale", hair: "braids", hairColor: "blonde", hat: { type: "headscarf", color: "#b5302a", color2: "#f1d36b" }, outfit: { type: "dress", color: "#1f4e8c", color2: "#f2c94c", trim: "#c0392b", pattern: "stripes" }, expression: "smile" }),
        cards: [
          "Wymysorys is a Germanic language spoken in one small town in southern Poland, Wilamowice. It is thought to come from settlers who arrived in the Middle Ages.",
          "After World War II the communist authorities banned it. Speakers were punished, and families stopped passing it on to their children.",
          "Only around 20 elderly native speakers remain, but a revival led by young locals like Tymoteusz Król means kids are learning it again.",
        ],
        audio: { file: "Helka 20120104 Wym.webm", start: "auto" },
      },
      {
        name: "Kusunda", flag: "np", speakers: "~1", scene: "himalaya", loc: [28.2, 82.6, "Western Nepal"],
        char: F({ skin: "tan", hair: "long", hairColor: "black", hat: { type: "headscarf", color: "#9b2335", color2: "#f2c94c" }, outfit: { type: "wrap", color: "#7a2e2e", color2: "#c8553d", trim: "#f2c94c" }, earrings: "#e9c46a", expression: "neutral" }),
        cards: [
          "Kusunda is a language isolate from Nepal: it is not related to any other language on Earth. Its speakers were once forest hunter-gatherers.",
          "Gyani Maiya Sen is one of the very last people who speak it fluently. You are listening to her right now.",
          "In recent years she has helped teach classes so younger Kusunda people can learn the words of their ancestors.",
        ],
        audio: { file: "Gyani Maiya Sen Kusunda - how Mihaq (Kusunda) language should be brought to the next generation.webm", start: "auto", search: "Gyani Maiya Sen Kusunda" },
      },
      {
        name: "Dalmatian", flag: "hr", speakers: "0", scene: "adriatic", loc: [45.1, 14.6, "Krk island, Croatia"],
        char: { skin: "light", hair: "bald", hairColor: "white", beard: true, beardColor: "white", outfit: { type: "coat", color: "#4a3b32", inner: "#e8e0d0" }, hat: { type: "beret", color: "#2f2f2f" }, expression: "sad" },
        cards: [
          "Dalmatian was a Romance language, a cousin of Italian, spoken along the coast of Croatia. Its last dialect survived on the island of Krk.",
          "Its last speaker, Tuone Udaina, was interviewed by a linguist even though he was nearly deaf, had no teeth and hadn't spoken it in 20 years.",
          "He died in 1898 in an explosion during road works, and the language died with him.",
        ],
        audio: null,
      },
      {
        name: "Eyak", flag: "us", speakers: "0", scene: "alaska", loc: [60.5, -145.5, "Copper River, Alaska"],
        char: F({ skin: "olive", hair: "bob", hairColor: "grey", outfit: { type: "parka", color: "#5b3a29", fur: "#efe3cf", trim: "#2a9d8f" }, glasses: true, expression: "smile" }),
        cards: [
          "Eyak was spoken around the Copper River delta in southern Alaska. It is a distant relative of the Athabaskan languages and Navajo.",
          "Its last native speaker, Marie Smith Jones, died in 2008. She spent years working with linguist Michael Krauss to record it.",
          "Amazingly, a teenager in France, Guillaume Leduey, taught himself Eyak from those records and now helps teach it to others.",
        ],
        audio: null,
      },
      {
        name: "Nuxalk", flag: "ca", speakers: "<20", scene: "bella", loc: [52.37, -126.75, "Bella Coola, Canada"],
        char: { skin: "brown", hair: "long", hairColor: "black", hat: { type: "headband", color: "#b5302a", color2: "#1d1d1d" }, outfit: { type: "wrap", color: "#1d1d1d", color2: "#b5302a", trim: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "Nuxalk is a Salishan language from Bella Coola in British Columbia, Canada. Fewer than 20 fluent speakers are left.",
          "It is famous for very long words with no vowels at all, like xłp̓x̣ʷłtłpłłskʷc̓, which means 'he had had a bunchberry plant'. That's the word you just heard.",
          "A local school teaches Nuxalk to children, giving the language a real chance of survival.",
        ],
        audio: { seq: ["Xłp̓x̣ʷłtłpłłskʷc̓.ogg"], repeat: 3 },
      },
      {
        name: "Livonian", flag: "liv", speakers: "0 native", scene: "baltic", loc: [57.6, 22.0, "Livonian Coast, Latvia"],
        char: F({ skin: "pale", hair: "long", hairColor: "blonde", hat: { type: "bonnet", color: "#f4f1e8", color2: "#2a6fa5" }, outfit: { type: "dress", color: "#2e6b4f", color2: "#f4f1e8", trim: "#f4f1e8" }, expression: "sad" }),
        cards: [
          "Livonian is a Finnic language, related to Estonian and Finnish, from a strip of fishing villages on the coast of Latvia.",
          "Its last native speaker, Grizelda Kristiņa, died in 2013 in Canada at the age of 103.",
          "A small group of people have since learned it, and Latvia protects the Livonian Coast as a cultural area.",
        ],
        audio: null,
      },
      {
        name: "Ladino", flag: null, speakers: "<100,000", scene: "istanbul", loc: [41.0, 28.97, "Turkey, Israel, Balkans"],
        char: { skin: "light", hair: "short", hairColor: "grey", beard: true, beardColor: "grey", hat: { type: "fez", color: "#9b1c1c", color2: "#1d1d1d" }, outfit: { type: "coat", color: "#2b2f45", inner: "#f4f1e8" }, glasses: true, expression: "smile" },
        cards: [
          "Ladino, or Judeo-Spanish, is the language of the Sephardic Jews who were expelled from Spain in 1492 and settled across the Ottoman Empire.",
          "It is basically old Spanish mixed with Hebrew, Turkish and Greek, and was traditionally written in Hebrew letters.",
          "The Holocaust destroyed many Ladino-speaking communities. Today most speakers are elderly and live in Israel and Turkey.",
        ],
        audio: { file: "Isaac 20210219 Lad.webm", start: "auto" },
      },
      {
        name: "Yaghan", flag: "cl", speakers: "0 native", scene: "fuego", loc: [-55.0, -67.6, "Navarino Island, Chile"],
        char: F({ skin: "brown", hair: "short", hairColor: "white", outfit: { type: "wrap", color: "#5b4636", color2: "#8a6a4f", trim: "#d9c7a7" }, expression: "smile" }),
        cards: [
          "Yaghan was spoken at the very bottom of the world, in Tierra del Fuego. The Yaghan people paddled canoes around Cape Horn.",
          "It is known for 'mamihlapinatapai', once listed by Guinness as the most succinct word: a look shared by two people who each hope the other will do something.",
          "Its last native speaker, Cristina Calderón, died in 2022 aged 93. She left behind a dictionary written with her granddaughter.",
        ],
        audio: null,
      },
      {
        name: "Boruca", flag: "cr", speakers: "<10", scene: "amazon", loc: [9.0, -83.3, "Southern Costa Rica"],
        char: { skin: "brown", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#f4f1e8", vest: "#7a2e2e" }, hat: { type: "widehat", color: "#d9b26f", color2: "#7a2e2e" }, expression: "smile" },
        cards: [
          "Boruca is a Chibchan language of the Brunca people in southern Costa Rica. Only a handful of elders can still speak it.",
          "The Boruca are famous for the Fiesta de los Diablitos, where carved balsa-wood masks re-enact their ancestors' resistance to the Spanish.",
          "Community members are now working to teach the language, and its songs, to younger generations.",
        ],
        audio: { file: "Anonymous speaking Boruca.webm", start: "auto" },
      },
      {
        name: "Aka-Bo", flag: "in", speakers: "0", scene: "andaman", loc: [12.6, 92.8, "Andaman Islands, India"],
        char: F({ skin: "deep", hair: "curly", hairColor: "grey", outfit: { type: "wrap", color: "#c8553d", color2: "#e9c46a", trim: "#2a9d8f" }, necklace: "#f4f1e8", expression: "sad" }),
        cards: [
          "Aka-Bo was one of the Great Andamanese languages, spoken on the Andaman Islands in the Bay of Bengal.",
          "Its last speaker, Boa Sr, died in 2010. For decades she had no one left to talk to in her own language.",
          "She told linguist Anvita Abbi that she often spoke to the birds instead, because they were the only ones who seemed to understand.",
        ],
        audio: null,
      },
    ],
  },

  // ------------------------------------------------------------------ 2
  niche2: {
    title: "Insanely Niche Languages be like…",
    part: "Part 2",
    layout: "story",
    counterLabel: "speakers",
    items: [
      {
        name: "Romansh", flag: "ch", speakers: "~40,000", scene: "alps", loc: [46.7, 9.6, "Graubünden, Switzerland"],
        char: F({ skin: "pale", hair: "bun", hairColor: "brown", outfit: { type: "dress", color: "#1d1d1d", color2: "#c0392b", trim: "#c0392b" }, hat: { type: "flower", color: "#f4f1e8", color2: "#f2c94c" }, expression: "smile" }),
        cards: [
          "Romansh is Switzerland's fourth national language, after German, French and Italian. It descends from the Latin spoken by Roman soldiers in the Alps.",
          "It has five main written varieties, so in 1982 a common standard called Rumantsch Grischun was created.",
          "Around 40,000 people call it their main language, mostly in the canton of Graubünden.",
        ],
        audio: { file: "Romansh (Wikitongues).ogg", start: "auto" },
      },
      {
        name: "Faroese", flag: "fo", speakers: "~70,000", scene: "faroe", loc: [62.0, -6.8, "Faroe Islands"],
        char: { skin: "pale", hair: "short", hairColor: "red", beard: true, beardColor: "red", outfit: { type: "tunic", color: "#2c3e66", trim: "#c0392b", pattern: "diamonds", color2: "#3d5288" }, hat: { type: "beanie", color: "#8c2b2b", color2: "#f4f1e8" }, expression: "grin" },
        cards: [
          "Faroese is spoken on the Faroe Islands, between Scotland and Iceland. Like Icelandic, it comes from the Old Norse of the Vikings.",
          "For centuries Danish was the official language, and Faroese was not written down at all until the 1800s.",
          "Around 70,000 people speak it. In 2016 the islands even strapped cameras to sheep to get onto Google Street View: 'Sheep View 360'.",
        ],
        audio: { file: "Tú alfagra land mítt.ogg", start: 0 },
      },
      {
        name: "North Frisian", flag: "nfris", speakers: "~10,000", scene: "moorland", loc: [54.7, 8.6, "North Frisian islands, Germany"],
        char: F({ skin: "pale", hair: "long", hairColor: "blonde", hat: { type: "headscarf", color: "#1d1d1d", color2: "#c0a060" }, outfit: { type: "dress", color: "#7a1f1f", color2: "#e9c46a", trim: "#e9c46a" }, necklace: "#d9d9d9", expression: "smile" }),
        cards: [
          "North Frisian is spoken on the islands and coast of northern Germany, near Denmark. It is one of the closest relatives of English.",
          "Around 10,000 people speak it, yet it has about ten dialects, and speakers from different islands can struggle to understand each other.",
          "You are hearing a song in North Frisian. On islands like Föhr and Amrum, it is still taught in schools.",
        ],
        audio: { file: "Andreas singing in Northern Frisian.webm", start: "auto" },
      },
      {
        name: "Siwi", flag: "eg", speakers: "~30,000", scene: "arabia", loc: [29.2, 25.5, "Siwa Oasis, Egypt"],
        char: { skin: "olive", hair: "short", hairColor: "black", hat: { type: "turban", color: "#f4f1e8", color2: "#c0a060" }, outfit: { type: "robe", color: "#e8dcc4", trim: "#a0522d" }, mustache: true, expression: "smile" },
        cards: [
          "Siwi is a Berber language spoken in the Siwa Oasis in Egypt's Western Desert, close to the border with Libya.",
          "It is the easternmost Berber language in the world, an island of Berber surrounded by Arabic.",
          "Siwa is also home to the ancient oracle that Alexander the Great famously travelled across the desert to visit.",
        ],
        audio: { file: "A young man from Siwa offers his greetings in the Siwan language.webm", start: 0 },
      },
      {
        name: "Mingrelian", flag: "ge", speakers: "~340,000", scene: "caucasus", loc: [42.5, 41.9, "Samegrelo, Georgia"],
        char: { skin: "light", hair: "short", hairColor: "black", mustache: true, outfit: { type: "coat", color: "#2b2b2b", inner: "#1d1d1d" }, hat: { type: "furhat", fur: "#3a3a3a" }, expression: "smug" },
        cards: [
          "Mingrelian is a Kartvelian language from western Georgia. It is related to Georgian, but the two are not mutually intelligible.",
          "It has no official status and is mostly spoken at home. When written, it uses the Georgian alphabet.",
          "Most Mingrelians are bilingual: Mingrelian at home, Georgian at school and work, which is why the language is slowly losing ground.",
        ],
        audio: { file: "WIKITONGUES- Valerian speaking Mingrelian.webm", start: "auto" },
      },
      {
        name: "Tuvan", flag: "ru", speakers: "~280,000", scene: "steppe", loc: [51.7, 94.4, "Tuva, Siberia"],
        char: { skin: "tan", hair: "short", hairColor: "black", hat: { type: "furhat", fur: "#7a5a3a" }, outfit: { type: "robe", color: "#1f5aa6", trim: "#e9c46a" }, sash: "#e9c46a", expression: "smile" },
        cards: [
          "Tuvan is a Turkic language spoken in the Republic of Tuva, in southern Siberia on the border with Mongolia.",
          "Tuva is famous for throat singing, where one singer produces two or more notes at the same time.",
          "Unlike many Siberian languages, Tuvan is still spoken by most Tuvans, and it is written in the Cyrillic alphabet.",
        ],
        audio: { file: "WIKITONGUES- Aydyn speaking Tuvan.webm", start: "auto" },
      },
      {
        name: "Gagauz", flag: "gag", speakers: "~150,000", scene: "grassland", loc: [46.3, 28.65, "Gagauzia, Moldova"],
        char: F({ skin: "light", hair: "braids", hairColor: "black", hat: { type: "headscarf", color: "#f4f1e8", color2: "#c0392b" }, outfit: { type: "dress", color: "#f4f1e8", color2: "#c0392b", trim: "#c0392b" }, expression: "smile" }),
        cards: [
          "Gagauz is a Turkic language, close to Turkish, spoken in Gagauzia, an autonomous region in southern Moldova.",
          "Unusually for Turkic peoples, the Gagauz are Orthodox Christians. Their origins are still debated by historians.",
          "In the Soviet era it was written in Cyrillic, but since the 1990s it has used a Latin alphabet very similar to Turkish.",
        ],
        audio: { file: "Gagauzskaia pesnia 01.ogg", start: 0 },
      },
      {
        name: "Jèrriais", flag: "je", speakers: "<3,000", scene: "jersey", loc: [49.2, -2.13, "Jersey, Channel Islands"],
        char: { skin: "pale", hair: "short", hairColor: "brown", outfit: { type: "shirt", color: "#2c3e50", vest: "#7a5a3a" }, hat: { type: "flatcap", color: "#5a4a3a" }, expression: "smile" },
        cards: [
          "Jèrriais is the Norman language of Jersey, an island between England and France. It is related to French but is its own language.",
          "Many English words came over from Norman after 1066, so Jèrriais can feel familiar to both English and French speakers.",
          "Fewer than 3,000 people speak it, mostly older islanders, but it is taught in Jersey's schools.",
        ],
        audio: { file: "Ben Spink speaks Jèrriais and recites \"Man Bieau P'tit Jèrri\".ogg", start: 0 },
      },
      {
        name: "Mirandese", flag: "pt", speakers: "~15,000", scene: "grassland", loc: [41.5, -6.27, "Miranda do Douro, Portugal"],
        char: { skin: "light", hair: "short", hairColor: "black", outfit: { type: "coat", color: "#3a2a1f", inner: "#f4f1e8" }, hat: { type: "widehat", color: "#2b2b2b", color2: "#2b2b2b" }, expression: "smile" },
        cards: [
          "Mirandese is spoken in a corner of north-eastern Portugal. It is not a dialect of Portuguese but a separate Astur-Leonese language.",
          "In 1999 Portugal officially recognised it, yet most Portuguese people have never heard it spoken.",
          "Around 15,000 people use it, and the famous dance of the Pauliteiros, with sticks, comes from this region.",
        ],
        audio: { file: "Lhiçon de Giografie.wav", start: 0 },
      },
      {
        name: "Greenlandic", flag: "gl", speakers: "~57,000", scene: "greenland", loc: [64.2, -51.7, "Greenland"],
        char: F({ skin: "tan", hair: "bun", hairColor: "black", outfit: { type: "parka", color: "#c0392b", fur: "#f4f1e8", trim: "#1d1d1d" }, necklace: "#2a6fa5", expression: "grin" }),
        cards: [
          "Greenlandic is an Inuit language, and since 2009 the only official language of Greenland.",
          "It is polysynthetic: whole sentences can be packed into one enormous word by stacking suffixes.",
          "For example, 'Nalunaarasuartaatilioqateeraliorfinnialikkersaatiginngitsoq' was once cited as a single Greenlandic word.",
        ],
        audio: { file: "WIKITONGUES- Mark speaking Greenlandic.webm", start: "auto" },
      },
      {
        name: "Toki Pona", flag: null, speakers: "1,000s", scene: "abstract", loc: null,
        char: F({ skin: "light", hair: "bob", hairColor: "#6c5ce7", outfit: { type: "tunic", color: "#00b894", trim: "#fdcb6e" }, glasses: true, expression: "grin" }),
        cards: [
          "Toki Pona is a constructed language invented by Sonja Lang in 2001. Its name means 'good language' or 'simple language'.",
          "It has only around 120 core words. Everything else is built from them: a 'friend' is 'jan pona', literally 'good person'.",
          "Its tiny vocabulary makes it one of the fastest languages to learn, and its fans have written whole books in it.",
        ],
        audio: { file: "Tobiah - toki pona.mp3", start: "auto" },
      },
      {
        name: "Luxembourgish", flag: "lu", speakers: "~400,000", scene: "forest", loc: [49.6, 6.13, "Luxembourg"],
        char: { skin: "pale", hair: "short", hairColor: "brown", outfit: { type: "shirt", color: "#1f3a5f", tie: "#c0392b", vest: "#2b2b2b" }, glasses: true, expression: "smug" },
        cards: [
          "Luxembourgish is a Germanic language that only became Luxembourg's national language by law in 1984.",
          "Most Luxembourgers also speak German and French, and often switch between all three in the same day.",
          "It says 'Moien' for hello, and the national motto, 'Mir wëlle bleiwe wat mir sinn', means 'We want to remain what we are'.",
        ],
        audio: { file: "WIKITONGUES- Mark speaking Luxembourgish.webm", start: "auto" },
      },
    ],
  },

  // ------------------------------------------------------------------ 3
  hardest: {
    title: "Ranking languages by how hard they are",
    part: "for English speakers",
    layout: "ranking",
    scoreLabel: "difficulty",
    items: [
      { name: "Norwegian", flag: "no", score: 2, weeks: 24, char: { skin: "pale", hair: "short", hairColor: "blonde", beard: true, beardColor: "blonde", outfit: { type: "tunic", color: "#1f3a6b", pattern: "diamonds", color2: "#f4f1e8", trim: "#f4f1e8" }, hat: { type: "beanie", color: "#c0392b", color2: "#f4f1e8" }, expression: "grin" }, cards: ["Very close to English in grammar and word order. Verbs don't even change for 'I', 'you' or 'she'. The trickiest part is its sing-song pitch accent."], audio: { ll: "nor", n: 6 } },
      { name: "Spanish", flag: "es", score: 2.5, weeks: 24, char: F({ skin: "olive", hair: "bun", hairColor: "black", hat: { type: "flower", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#c0392b", color2: "#1d1d1d", trim: "#1d1d1d" }, earrings: "#e9c46a", expression: "smile" }), cards: ["Spelled almost exactly how it sounds, with thousands of words shared with English. Verb endings and the subjunctive take practice, but most learners get going quickly."], audio: { ll: "spa", n: 6 } },
      { name: "Dutch", flag: "nl", score: 3, weeks: 24, char: { skin: "pale", hair: "short", hairColor: "blonde", outfit: { type: "shirt", color: "#e67e22", vest: "#1f3a6b" }, glasses: true, expression: "smile" }, cards: ["Sits between English and German. Lots of words look familiar, but the throaty 'g' and word order in longer sentences trip people up."], audio: { ll: "nld", n: 6 } },
      { name: "Italian", flag: "it", score: 3, weeks: 24, char: { skin: "light", hair: "short", hairColor: "black", mustache: true, outfit: { type: "shirt", color: "#f4f1e8", vest: "#2c3e50", tie: "#27ae60" }, expression: "grin" }, cards: ["Phonetic spelling, lots of Latin vocabulary English already uses, and very clear vowels. Verb conjugations are the main hurdle."], audio: { ll: "ita", n: 6 } },
      { name: "French", flag: "fr", score: 3.5, weeks: 30, char: F({ skin: "pale", hair: "bob", hairColor: "brown", hat: { type: "beret", color: "#1d1d1d" }, outfit: { type: "tunic", color: "#f4f1e8", pattern: "stripes", color2: "#1f3a6b", trim: "#1f3a6b" }, expression: "smug" }), cards: ["A third of English vocabulary comes from French, but the spelling is full of silent letters and the pronunciation is famously hard to get right."], audio: { ll: "fra", n: 6 } },
      { name: "Swahili", flag: "tz", score: 4.5, weeks: 36, char: F({ skin: "dark", hair: "bun", hairColor: "black", hat: { type: "headscarf", color: "#f2a541", color2: "#2a9d8f" }, outfit: { type: "wrap", color: "#2a9d8f", color2: "#f2a541", trim: "#c0392b" }, earrings: "#e9c46a", expression: "grin" }), cards: ["Easy pronunciation and no tones, but nouns fall into many 'noun classes', and the prefixes on every word must agree with them."], audio: { file: "WIKITONGUES- Iddy speaking Swahili.webm", start: "auto" } },
      { name: "Indonesian", flag: "id", score: 4.5, weeks: 36, char: { skin: "tan", hair: "short", hairColor: "black", hat: { type: "fez", color: "#1d1d1d", color2: "#1d1d1d" }, outfit: { type: "shirt", color: "#8e5a2b", vest: "#5a3a1f" }, expression: "smile" }, cards: ["No verb tenses, no gender and no plurals (you just say the word twice). The hard part is the vocabulary and its many prefixes and suffixes."], audio: { ll: "ind", n: 6 } },
      { name: "German", flag: "de", score: 5, weeks: 36, char: { skin: "pale", hair: "short", hairColor: "blonde", mustache: true, hat: { type: "widehat", color: "#2f4a2f", color2: "#7a5a3a" }, outfit: { type: "shirt", color: "#f4f1e8", vest: "#3a5a2f" }, expression: "neutral" }, cards: ["English's close cousin, but with three genders, four cases, and verbs that jump to the end of the sentence. Spelling, at least, is very regular."], audio: { ll: "deu", n: 6 } },
      { name: "Russian", flag: "ru", score: 6.5, weeks: 44, char: F({ skin: "pale", hair: "braids", hairColor: "blonde", hat: { type: "kokoshnik", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#c0392b", color2: "#f2c94c", trim: "#f2c94c" }, expression: "neutral" }), cards: ["A new alphabet (easier than it looks), six grammatical cases, and verbs that come in pairs depending on whether an action is finished."], audio: { ll: "rus", n: 6 } },
      { name: "Hindi", flag: "in", score: 6.5, weeks: 44, char: F({ skin: "brown", hair: "long", hairColor: "black", outfit: { type: "wrap", color: "#d35400", color2: "#f1c40f", trim: "#8e44ad" }, earrings: "#e9c46a", necklace: "#e9c46a", expression: "smile" }), cards: ["Written in the Devanagari script, with sounds English doesn't separate, like four different kinds of 't'. Grammar is fairly regular once you're used to it."], audio: { ll: "hin", n: 6 } },
      { name: "Polish", flag: "pl", score: 7, weeks: 44, char: { skin: "pale", hair: "short", hairColor: "brown", mustache: true, outfit: { type: "coat", color: "#7a1f1f", inner: "#f4f1e8" }, hat: { type: "flatcap", color: "#3a3a3a" }, expression: "smug" }, cards: ["Seven cases, three genders and consonant clusters like 'szcz' in words like 'Szczebrzeszyn'. Thankfully, the spelling is consistent."], audio: { ll: "pol", n: 6 } },
      { name: "Finnish", flag: "fi", score: 7, weeks: 44, char: F({ skin: "pale", hair: "long", hairColor: "blonde", hat: { type: "beanie", color: "#1f4e8c", color2: "#f4f1e8" }, outfit: { type: "parka", color: "#1f4e8c", fur: "#f4f1e8", trim: "#f4f1e8" }, expression: "neutral" }), cards: ["Not related to English at all. It has around 15 cases and very long words, but it's spelled exactly as it's pronounced."], audio: { ll: "fin", n: 6 } },
      { name: "Hungarian", flag: "hu", score: 7.5, weeks: 44, char: { skin: "light", hair: "short", hairColor: "black", mustache: true, outfit: { type: "shirt", color: "#f4f1e8", vest: "#1d1d1d" }, hat: { type: "widehat", color: "#1d1d1d", color2: "#c0392b" }, expression: "neutral" }, cards: ["Another language with no link to English: around 18 cases, vowel harmony and verbs that change depending on whether the object is definite."], audio: { ll: "hun", n: 6 } },
      { name: "Vietnamese", flag: "vn", score: 7.5, weeks: 44, char: F({ skin: "light", hair: "long", hairColor: "black", hat: { type: "conical", color: "#e9d8a6" }, outfit: { type: "robe", color: "#f4f1e8", trim: "#e9c46a" }, expression: "smile" }), cards: ["Uses the Latin alphabet and has simple grammar, but six tones mean 'ma' can be 'ghost', 'mother', 'horse' or 'rice seedling'."], audio: { ll: "vie", n: 6 } },
      { name: "Korean", flag: "kr", score: 8.5, weeks: 88, char: F({ skin: "pale", hair: "bun", hairColor: "black", outfit: { type: "robe", color: "#e84393", trim: "#fdcb6e" }, expression: "smile" }), cards: ["Hangul can be learned in a day, but grammar is very different from English and speech levels change depending on who you're talking to."], audio: { ll: "kor", n: 6 } },
      { name: "Arabic", flag: "sa", score: 9, weeks: 88, char: { skin: "olive", hair: "short", hairColor: "black", beard: true, hat: { type: "headscarf", color: "#f4f1e8", color2: "#c0392b" }, outfit: { type: "robe", color: "#f4f1e8", trim: "#d9cbb0" }, expression: "neutral" }, cards: ["Right-to-left script, sounds made deep in the throat, and a big gap between Modern Standard Arabic and the dialects people actually speak at home."], audio: { ll: "ara", n: 6 } },
      { name: "Mandarin", flag: "cn", score: 9.5, weeks: 88, char: F({ skin: "light", hair: "bun", hairColor: "black", outfit: { type: "robe", color: "#c0392b", trim: "#f2c94c" }, earrings: "#e9c46a", expression: "neutral" }), cards: ["Grammar is surprisingly simple, but you need thousands of characters to read a newspaper, and four tones to be understood."], audio: { ll: "cmn", n: 6 } },
      { name: "Japanese", flag: "jp", score: 10, weeks: 88, char: { skin: "light", hair: "spiky", hairColor: "black", outfit: { type: "robe", color: "#1f2a44", trim: "#c0392b" }, hat: { type: "headband", color: "#f4f1e8", color2: "#c0392b" }, expression: "angry" }, cards: ["Three writing systems at once (hiragana, katakana and kanji), verbs at the end, and different politeness levels. The FSI marks it as usually harder than others in its group."], audio: { ll: "jpn", n: 6 } },
    ],
  },

  // ------------------------------------------------------------------ 4
  sounds: {
    title: "Languages with the weirdest sounds be like…",
    part: "",
    layout: "story",
    counterLabel: "speakers",
    items: [
      {
        name: "Xhosa", flag: "za", speakers: "~8M", scene: "savanna", loc: [-32.0, 27.5, "Eastern Cape, South Africa"],
        char: F({ skin: "dark", hair: "short", hairColor: "black", hat: { type: "headscarf", color: "#1d1d1d", color2: "#f4f1e8" }, outfit: { type: "wrap", color: "#f4f1e8", color2: "#1d1d1d", trim: "#c0392b" }, necklace: "#c0392b", earrings: "#f4f1e8", expression: "grin" }),
        cards: [
          "Xhosa is one of South Africa's official languages, with around 8 million native speakers. It was Nelson Mandela's mother tongue.",
          "It has 15 click consonants, written with the letters c, q and x. The 'X' in Xhosa itself is a click.",
          "Singer Miriam Makeba made Xhosa clicks world famous with her song known in English as 'The Click Song'.",
        ],
        audio: { file: "Sisters remember xhosa songs and games.ogg", start: "auto" },
      },
      {
        name: "Taa (!Xóõ)", flag: "bw", speakers: "~2,500", scene: "kalahari", loc: [-24.0, 21.5, "Kalahari, Botswana"],
        char: { skin: "brown", hair: "short", hairColor: "black", outfit: { type: "wrap", color: "#a0673f", color2: "#c8955a", trim: "#f4f1e8" }, necklace: "#f4f1e8", expression: "smile" },
        cards: [
          "Taa, also called !Xóõ, is spoken by around 2,500 people in the Kalahari Desert of Botswana and Namibia.",
          "It may have more distinct sounds than any other language. By some counts it has over 100 consonants, most of them clicks.",
          "Linguists still argue over exactly how many sounds it has, because many clicks can combine with other sounds.",
        ],
        audio: { file: "TWa040429-0101 2 (1).wav", start: "auto" },
      },
      {
        name: "Silbo Gomero", flag: "es", speakers: "1,000s", scene: "canary", loc: [28.1, -17.2, "La Gomera, Canary Islands"],
        char: { skin: "olive", hair: "short", hairColor: "grey", outfit: { type: "shirt", color: "#f4f1e8", vest: "#7a2e2e" }, hat: { type: "widehat", color: "#d9b26f", color2: "#7a2e2e" }, expression: "open" },
        cards: [
          "Silbo Gomero is Spanish, but whistled. Shepherds on La Gomera used it to talk across deep ravines.",
          "A strong whistle can carry for kilometres, much further than a shout. That's what you're hearing right now.",
          "It is a UNESCO Intangible Cultural Heritage, and since 1999 every child on the island learns it at school.",
        ],
        audio: { file: "Silbo.ogg", start: 0 },
      },
      {
        name: "Ubykh", flag: "tr", speakers: "0", scene: "caucasus", loc: [43.6, 39.7, "Caucasus → Turkey"],
        char: { skin: "light", hair: "bald", hairColor: "white", mustache: true, beardColor: "white", outfit: { type: "coat", color: "#3a3a3a", inner: "#f4f1e8" }, glasses: true, expression: "sad" },
        cards: [
          "Ubykh was spoken on the Black Sea coast of the Caucasus until the Ubykh people were forced into the Ottoman Empire in 1864.",
          "It had around 80 consonants but only two or three vowels, one of the most extreme sound systems ever recorded.",
          "Its last speaker, Tevfik Esenç, died in Turkey in 1992. He asked that his gravestone say he was the last person who could speak it.",
        ],
        audio: null,
      },
      {
        name: "Rotokas", flag: "pg", speakers: "~4,000", scene: "bougainville", loc: [-6.1, 155.2, "Bougainville, Papua New Guinea"],
        char: { skin: "dark", hair: "curly", hairColor: "black", outfit: { type: "bare", color: "#2a9d8f" }, necklace: "#f4f1e8", expression: "grin" },
        cards: [
          "Rotokas, from the island of Bougainville in Papua New Guinea, goes the other way: it has one of the smallest sound systems in the world.",
          "Its central dialect uses only 11 sounds: 6 consonants and 5 vowels. English has more than 40.",
          "Its alphabet has just 12 letters: A, E, G, I, K, O, P, R, S, T, U and V.",
        ],
        audio: null,
      },
      {
        name: "Pirahã", flag: "br", speakers: "~400", scene: "amazon", loc: [-7.3, -62.0, "Maici River, Brazil"],
        char: { skin: "brown", hair: "short", hairColor: "black", outfit: { type: "bare" }, necklace: "#c0392b", facepaint: "lines", paintColor: "#c0392b", expression: "smile" },
        cards: [
          "Pirahã is spoken by about 400 people along the Maici River in the Amazon. It has one of the smallest sets of sounds of any language.",
          "It can be hummed, sung or whistled instead of spoken, and it uses rare sounds like a trill made by vibrating the lips.",
          "Linguist Daniel Everett argued it has no words for exact numbers, a claim other researchers still debate.",
        ],
        audio: { seq: ["ʔíʙogi.wav"], repeat: 4 },
      },
      {
        name: "Cantonese", flag: "hk", speakers: "~85M", scene: "hongkong", loc: [22.3, 114.17, "Hong Kong, Guangdong"],
        char: F({ skin: "light", hair: "bob", hairColor: "black", outfit: { type: "robe", color: "#1f6f5a", trim: "#f2c94c" }, earrings: "#2a9d8f", expression: "smug" }),
        cards: [
          "Cantonese is spoken in Hong Kong, Macau and Guangdong, by around 85 million people.",
          "It has six tones (nine by the traditional count), so the syllable 'si' can mean poem, history, try, time, market or yes.",
          "You're hearing someone count from zero to ten in Cantonese. Listen to how much the pitch moves.",
        ],
        audio: { file: "Zero to ten in Cantonese Chinese.ogg", start: 0 },
      },
      {
        name: "Georgian", flag: "ge", speakers: "~3.7M", scene: "tbilisi", loc: [41.7, 44.8, "Georgia"],
        char: { skin: "light", hair: "short", hairColor: "black", beard: true, outfit: { type: "coat", color: "#1d1d1d", inner: "#7a1f1f" }, hat: { type: "furhat", fur: "#1d1d1d" }, expression: "smug" },
        cards: [
          "Georgian has its own unique alphabet with 33 letters and no capital letters at all.",
          "It loves stacking consonants: 'gvprtskvni', meaning 'you peel us', starts with eight consonants in a row.",
          "It also has 'ejective' sounds, popped out with a burst of air from the throat, which English doesn't have.",
        ],
        audio: { file: "WIKITONGUES- Mariam speaking Georgian.webm", start: "auto" },
      },
      {
        name: "Czech", flag: "cz", speakers: "~10M", scene: "prague", loc: [50.08, 14.43, "Czech Republic"],
        char: F({ skin: "pale", hair: "braids", hairColor: "brown", hat: { type: "flower", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#f4f1e8", color2: "#c0392b", trim: "#1f3a6b" }, expression: "smile" }),
        cards: [
          "Czech has the letter ř, a sound found in almost no other language: a rolled 'r' and a 'zh' at the same time.",
          "It is often one of the last sounds Czech children learn. You can hear it in the name of the composer Dvořák.",
          "Czech can also build sentences with no vowels at all, like 'Strč prst skrz krk', meaning 'stick your finger through your throat'.",
        ],
        audio: { ll: "ces", words: ["řeka", "tři", "moře", "řeč", "Dvořák", "keř", "dobře", "příroda", "krk", "prst"], n: 7 },
      },
      {
        name: "Danish", flag: "dk", speakers: "~6M", scene: "copenhagen", loc: [55.68, 12.57, "Denmark"],
        char: { skin: "pale", hair: "short", hairColor: "blonde", outfit: { type: "tunic", color: "#c0392b", pattern: "stripes", color2: "#f4f1e8", trim: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "Danish is famous for swallowing its consonants. Written words often look nothing like how they sound.",
          "It has the 'stød', a tiny catch in the throat that can change the meaning of a word.",
          "Its tongue-twister 'rødgrød med fløde' (red berry pudding with cream) is a classic test for foreigners.",
        ],
        audio: { ll: "dan", n: 7 },
      },
      {
        name: "Welsh", flag: "gb-wls", speakers: "~540,000", scene: "wales", loc: [52.4, -3.8, "Wales"],
        char: F({ skin: "pale", hair: "long", hairColor: "brown", hat: { type: "tophat", color: "#1d1d1d", color2: "#1d1d1d" }, outfit: { type: "coat", color: "#7a1f1f", inner: "#f4f1e8", pattern: "check", color2: "#5a1515" }, expression: "smile" }),
        cards: [
          "Welsh has the 'll' sound: put your tongue where you'd say 'l', then blow air around its sides.",
          "It is home to one of the longest place names in Europe: Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch.",
          "In Welsh, 'w' and 'y' are also vowels, which is why 'cwtch', a hug, is a perfectly normal word.",
        ],
        audio: { file: "WIKITONGUES- Sandra speaking Welsh.webm", start: "auto" },
      },
      {
        name: "Hawaiian", flag: "us", speakers: "~24,000", scene: "hawaii", loc: [20.8, -156.3, "Hawaiʻi"],
        char: F({ skin: "tan", hair: "long", hairColor: "black", hat: { type: "flower", color: "#ff7eb6", color2: "#f2c94c" }, outfit: { type: "dress", color: "#2a9d8f", color2: "#ff7eb6", trim: "#ff7eb6", pattern: "dots" }, necklace: "#ff7eb6", expression: "grin" }),
        cards: [
          "Hawaiian has one of the smallest alphabets in the world: just 13 letters, five vowels, seven consonants and the ʻokina, a glottal stop.",
          "That means lots of vowels and long words like humuhumunukunukuāpuaʻa, Hawaiʻi's state fish.",
          "After being banned in schools in 1896 it nearly vanished, but immersion schools since the 1980s have brought it back.",
        ],
        audio: { ll: "haw", n: 7 },
      },
    ],
  },
};
