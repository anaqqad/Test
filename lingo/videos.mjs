// Scripts for the four videos. Facts are kept conservative (ranges, "fewer than") where sources disagree.
// audio: {file, start?} one Commons recording (start "auto" = first stretch that is not English),
//        {ll: iso639-3, words?: [...], n?} Lingua Libre word recordings, {seq: [File names]} short clips in a row.
// flag: ISO 3166 code from flag-icons, or a custom key from FLAGS in render.mjs, or null.

export const CHANNEL = "LingoDude";

const F = (o) => ({ fem: true, ...o });

export const VIDEOS = {
  // ------------------------------------------------------------------ 1
  extinct: {
    title: "Nearly Extinct Languages be like…",
    part: "",
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
        name: "Cherokee", flag: "us", speakers: "~2,000", scene: "forest", loc: [35.9, -94.97, "Oklahoma & North Carolina"],
        char: { skin: "tan", hair: "short", hairColor: "grey", outfit: { type: "shirt", color: "#8c2b2b", vest: "#2b2b2b" }, hat: { type: "widehat", color: "#2b2b2b", color2: "#c0392b" }, expression: "smile" },
        cards: [
          "Cherokee is an Iroquoian language of the Cherokee people, spoken today mainly in Oklahoma and North Carolina.",
          "In the 1820s a Cherokee man named Sequoyah, who couldn't read any language, invented a complete writing system for it on his own.",
          "Only around 2,000 fluent speakers remain, most of them elderly, and the Cherokee Nation has declared a language emergency.",
        ],
        audio: { file: "Wikitongues Jerry speaking Cherokee.mp3", start: "auto" },
      },
      {
        name: "Vepsian", flag: "ru", speakers: "~1,600", scene: "dalarna", loc: [61.0, 35.5, "Lake Onega, Russia"],
        char: F({ skin: "pale", hair: "braids", hairColor: "blonde", hat: { type: "headscarf", color: "#c0392b", color2: "#f4f1e8" }, outfit: { type: "dress", color: "#f4f1e8", color2: "#c0392b", trim: "#c0392b" }, expression: "smile" }),
        cards: [
          "Vepsian is a Finnic language, a relative of Finnish and Estonian, spoken in villages between Lake Ladoga and Lake Onega in Russia.",
          "In the Soviet era Vepsian schools were closed and families switched to Russian. Today only around 1,600 people speak it.",
          "In the 1990s Vepsian got a new Latin alphabet, schoolbooks and even a newspaper, as activists fought to keep it alive.",
        ],
        audio: { file: "Eniisi Lisika Vep.webm", start: "auto", avoid: ["en", "ru"] },
      },
      {
        name: "Lakota", flag: "us", speakers: "~2,000", scene: "oklahoma", loc: [43.5, -101.5, "South & North Dakota"],
        char: { skin: "brown", hair: "braids", hairColor: "black", hat: { type: "headband", color: "#1f4e8c", color2: "#f4f1e8" }, outfit: { type: "shirt", color: "#f4f1e8", vest: "#7a4a2a" }, expression: "neutral" },
        cards: [
          "Lakota is a Siouan language of the Great Plains. It was the language of famous leaders like Sitting Bull and Crazy Horse.",
          "The English word 'tipi' comes from Lakota, where 'thípi' means a house or dwelling.",
          "Only around 2,000 fluent speakers are left, but immersion schools on the reservations are raising a new generation of speakers.",
        ],
        audio: { file: "WIKITONGUES- Junior speaking Lakota.webm", start: "auto" },
      },
      {
        name: "Yugambeh", flag: "au", speakers: "revival", scene: "hawaii", loc: [-28.0, 153.2, "Gold Coast, Australia"],
        char: { skin: "deep", hair: "curly", hairColor: "black", beard: true, outfit: { type: "tunic", color: "#c8553d", trim: "#f2c94c" }, facepaint: "lines", paintColor: "#f4f1e8", expression: "smile" },
        cards: [
          "Yugambeh is an Aboriginal language from the area around today's Gold Coast and Logan in Queensland, Australia.",
          "After colonisation it was nearly wiped out, and for decades almost no one spoke it fluently.",
          "Today the Yugambeh community is bringing it back with classes, songs and dictionaries, and many local place names still come from it.",
        ],
        audio: { file: "Wikitongues - Shaun speaking Yugambeh Aboriginal Australians and Torres Strait Islanders .webm", ranges: [[0, 6.6], [10.8, 20.1], [26.2, 36.0]] },
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
        name: "Boruca", flag: "cr", speakers: "<10", scene: "amazon", loc: [9.0, -83.3, "Southern Costa Rica"],
        char: { skin: "brown", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#f4f1e8", vest: "#7a2e2e" }, hat: { type: "widehat", color: "#d9b26f", color2: "#7a2e2e" }, expression: "smile" },
        cards: [
          "Boruca is a Chibchan language of the Brunca people in southern Costa Rica. Only a handful of elders can still speak it.",
          "The Boruca are famous for the Fiesta de los Diablitos, where carved balsa-wood masks re-enact their ancestors' resistance to the Spanish.",
          "Community members are now working to teach the language, and its songs, to younger generations.",
        ],
        audio: { file: "Anonymous speaking Boruca.webm", start: "auto" },
      },
    ],
  },

  // ------------------------------------------------------------------ 2
  niche: {
    title: "Insanely Niche Languages be like…",
    part: "",
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
        audio: { seq: ["Fo-Foroyar.ogg", "Fo-Torshavn.ogg", "Fo-Eiði.oga"], repeat: 2 },
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
        audio: { file: "Gagauzskaia pesnia 01.ogg", start: 42 },
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
      { name: "Norwegian", flag: "no", score: 2, weeks: 24, char: { skin: "pale", hair: "short", hairColor: "blonde", beard: true, beardColor: "blonde", outfit: { type: "tunic", color: "#1f3a6b", pattern: "diamonds", color2: "#f4f1e8", trim: "#f4f1e8" }, hat: { type: "beanie", color: "#c0392b", color2: "#f4f1e8" }, expression: "grin" }, cards: ["Very close to English in grammar and word order. Verbs don't even change for 'I', 'you' or 'she'. The trickiest part is its sing-song pitch accent."], audio: { ll: "nor", n: 3 } },
      { name: "Spanish", flag: "es", score: 2.5, weeks: 24, char: F({ skin: "olive", hair: "bun", hairColor: "black", hat: { type: "flower", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#c0392b", color2: "#1d1d1d", trim: "#1d1d1d" }, earrings: "#e9c46a", expression: "smile" }), cards: ["Spelled almost exactly how it sounds, with thousands of words shared with English. Verb endings and the subjunctive take practice, but most learners get going quickly."], audio: { ll: "spa", n: 3 } },
      { name: "Dutch", flag: "nl", score: 3, weeks: 24, char: { skin: "pale", hair: "short", hairColor: "blonde", outfit: { type: "shirt", color: "#e67e22", vest: "#1f3a6b" }, glasses: true, expression: "smile" }, cards: ["Sits between English and German. Lots of words look familiar, but the throaty 'g' and word order in longer sentences trip people up."], audio: { ll: "nld", n: 3 } },
      { name: "Italian", flag: "it", score: 3, weeks: 24, char: { skin: "light", hair: "short", hairColor: "black", mustache: true, outfit: { type: "shirt", color: "#f4f1e8", vest: "#2c3e50", tie: "#27ae60" }, expression: "grin" }, cards: ["Phonetic spelling, lots of Latin vocabulary English already uses, and very clear vowels. Verb conjugations are the main hurdle."], audio: { ll: "ita", n: 3 } },
      { name: "French", flag: "fr", score: 3.5, weeks: 30, char: F({ skin: "pale", hair: "bob", hairColor: "brown", hat: { type: "beret", color: "#1d1d1d" }, outfit: { type: "tunic", color: "#f4f1e8", pattern: "stripes", color2: "#1f3a6b", trim: "#1f3a6b" }, expression: "smug" }), cards: ["A third of English vocabulary comes from French, but the spelling is full of silent letters and the pronunciation is famously hard to get right."], audio: { ll: "fra", n: 3 } },
      { name: "Swahili", flag: "tz", score: 4.5, weeks: 36, char: F({ skin: "dark", hair: "bun", hairColor: "black", hat: { type: "headscarf", color: "#f2a541", color2: "#2a9d8f" }, outfit: { type: "wrap", color: "#2a9d8f", color2: "#f2a541", trim: "#c0392b" }, earrings: "#e9c46a", expression: "grin" }), cards: ["Easy pronunciation and no tones, but nouns fall into many 'noun classes', and the prefixes on every word must agree with them."], audio: { file: "WIKITONGUES- Iddy speaking Swahili.webm", start: "auto" } },
      { name: "Indonesian", flag: "id", score: 4.5, weeks: 36, char: { skin: "tan", hair: "short", hairColor: "black", hat: { type: "fez", color: "#1d1d1d", color2: "#1d1d1d" }, outfit: { type: "shirt", color: "#8e5a2b", vest: "#5a3a1f" }, expression: "smile" }, cards: ["No verb tenses, no gender and no plurals (you just say the word twice). The hard part is the vocabulary and its many prefixes and suffixes."], audio: { ll: "ind", n: 3 } },
      { name: "German", flag: "de", score: 5, weeks: 36, char: { skin: "pale", hair: "short", hairColor: "blonde", mustache: true, hat: { type: "widehat", color: "#2f4a2f", color2: "#7a5a3a" }, outfit: { type: "shirt", color: "#f4f1e8", vest: "#3a5a2f" }, expression: "neutral" }, cards: ["English's close cousin, but with three genders, four cases, and verbs that jump to the end of the sentence. Spelling, at least, is very regular."], audio: { ll: "deu", n: 3 } },
      { name: "Russian", flag: "ru", score: 6.5, weeks: 44, char: F({ skin: "pale", hair: "braids", hairColor: "blonde", hat: { type: "kokoshnik", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#c0392b", color2: "#f2c94c", trim: "#f2c94c" }, expression: "neutral" }), cards: ["A new alphabet (easier than it looks), six grammatical cases, and verbs that come in pairs depending on whether an action is finished."], audio: { ll: "rus", n: 3 } },
      { name: "Hindi", flag: "in", score: 6.5, weeks: 44, char: F({ skin: "brown", hair: "long", hairColor: "black", outfit: { type: "wrap", color: "#d35400", color2: "#f1c40f", trim: "#8e44ad" }, earrings: "#e9c46a", necklace: "#e9c46a", expression: "smile" }), cards: ["Written in the Devanagari script, with sounds English doesn't separate, like four different kinds of 't'. Grammar is fairly regular once you're used to it."], audio: { ll: "hin", n: 3 } },
      { name: "Polish", flag: "pl", score: 7, weeks: 44, char: { skin: "pale", hair: "short", hairColor: "brown", mustache: true, outfit: { type: "coat", color: "#7a1f1f", inner: "#f4f1e8" }, hat: { type: "flatcap", color: "#3a3a3a" }, expression: "smug" }, cards: ["Seven cases, three genders and consonant clusters like 'szcz' in words like 'Szczebrzeszyn'. Thankfully, the spelling is consistent."], audio: { ll: "pol", n: 3 } },
      { name: "Finnish", flag: "fi", score: 7, weeks: 44, char: F({ skin: "pale", hair: "long", hairColor: "blonde", hat: { type: "beanie", color: "#1f4e8c", color2: "#f4f1e8" }, outfit: { type: "parka", color: "#1f4e8c", fur: "#f4f1e8", trim: "#f4f1e8" }, expression: "neutral" }), cards: ["Not related to English at all. It has around 15 cases and very long words, but it's spelled exactly as it's pronounced."], audio: { ll: "fin", n: 3 } },
      { name: "Hungarian", flag: "hu", score: 7.5, weeks: 44, char: { skin: "light", hair: "short", hairColor: "black", mustache: true, outfit: { type: "shirt", color: "#f4f1e8", vest: "#1d1d1d" }, hat: { type: "widehat", color: "#1d1d1d", color2: "#c0392b" }, expression: "neutral" }, cards: ["Another language with no link to English: around 18 cases, vowel harmony and verbs that change depending on whether the object is definite."], audio: { ll: "hun", n: 3 } },
      { name: "Vietnamese", flag: "vn", score: 7.5, weeks: 44, char: F({ skin: "light", hair: "long", hairColor: "black", hat: { type: "conical", color: "#e9d8a6" }, outfit: { type: "robe", color: "#f4f1e8", trim: "#e9c46a" }, expression: "smile" }), cards: ["Uses the Latin alphabet and has simple grammar, but six tones mean 'ma' can be 'ghost', 'mother', 'horse' or 'rice seedling'."], audio: { ll: "vie", n: 3 } },
      { name: "Korean", flag: "kr", score: 8.5, weeks: 88, char: F({ skin: "pale", hair: "bun", hairColor: "black", outfit: { type: "robe", color: "#e84393", trim: "#fdcb6e" }, expression: "smile" }), cards: ["Hangul can be learned in a day, but grammar is very different from English and speech levels change depending on who you're talking to."], audio: { ll: "kor", n: 3 } },
      { name: "Arabic", flag: "sa", score: 9, weeks: 88, char: { skin: "olive", hair: "short", hairColor: "black", beard: true, hat: { type: "headscarf", color: "#f4f1e8", color2: "#c0392b" }, outfit: { type: "robe", color: "#f4f1e8", trim: "#d9cbb0" }, expression: "neutral" }, cards: ["Right-to-left script, sounds made deep in the throat, and a big gap between Modern Standard Arabic and the dialects people actually speak at home."], audio: { ll: "ara", n: 3 } },
      { name: "Mandarin", flag: "cn", score: 9.5, weeks: 88, char: F({ skin: "light", hair: "bun", hairColor: "black", outfit: { type: "robe", color: "#c0392b", trim: "#f2c94c" }, earrings: "#e9c46a", expression: "neutral" }), cards: ["Grammar is surprisingly simple, but you need thousands of characters to read a newspaper, and four tones to be understood."], audio: { ll: "cmn", n: 3 } },
      { name: "Japanese", flag: "jp", score: 10, weeks: 88, char: { skin: "light", hair: "spiky", hairColor: "black", outfit: { type: "robe", color: "#1f2a44", trim: "#c0392b" }, hat: { type: "headband", color: "#f4f1e8", color2: "#c0392b" }, expression: "angry" }, cards: ["Three writing systems at once (hiragana, katakana and kanji), verbs at the end, and different politeness levels. The FSI marks it as usually harder than others in its group."], audio: { ll: "jpn", n: 3 } },
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
        audio: { file: "TWa040429-0101 2 (1).wav", start: 170 },
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
        name: "Hmong", flag: "la", speakers: "millions", scene: "himalaya", loc: [20.0, 103.0, "Laos, Vietnam, China"],
        char: F({ skin: "light", hair: "long", hairColor: "black", hat: { type: "headband", color: "#1d1d1d", color2: "#e84393" }, outfit: { type: "dress", color: "#1d1d1d", color2: "#e84393", trim: "#e84393", pattern: "zigzag" }, necklace: "#d9d9d9", expression: "smile" }),
        cards: [
          "Hmong is spoken in the mountains of southern China, Laos, Vietnam and Thailand, and by large communities in the USA.",
          "It has around seven or eight tones. In its Latin alphabet, the last letter of a word shows the tone, so 'Hmoob' ends in 'b' for a high tone.",
          "Its tones are so important that the qeej, a bamboo pipe instrument, can 'speak' Hmong phrases by playing their tone melodies.",
        ],
        audio: { file: "May speaking Hmong Don.webm", start: "auto" },
      },
      {
        name: "Yoruba", flag: "ng", speakers: "~45M", scene: "savanna", loc: [7.4, 3.9, "Nigeria & Benin"],
        char: { skin: "dark", hair: "short", hairColor: "black", hat: { type: "fez", color: "#2a6fa5", color2: "#2a6fa5" }, outfit: { type: "robe", color: "#2a6fa5", trim: "#f2c94c" }, expression: "grin" },
        cards: [
          "Yoruba is spoken by tens of millions of people in Nigeria and Benin. It has three tones: high, mid and low.",
          "Tone changes meaning completely: 'ọkọ' can mean husband, hoe or vehicle depending on the pitch of each syllable.",
          "Because words have melodies, the 'talking drum' (dùndún) can imitate speech, and listeners can understand the messages.",
        ],
        audio: { file: "Dorcas speaking Yoruba.webm", start: "auto" },
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
        audio: { ll: "ces", words: ["řeka", "tři", "moře", "řeč", "Dvořák", "keř", "dobře", "příroda", "krk", "prst"], n: 4 },
      },
      {
        name: "Danish", flag: "dk", speakers: "~6M", scene: "copenhagen", loc: [55.68, 12.57, "Denmark"],
        char: { skin: "pale", hair: "short", hairColor: "blonde", outfit: { type: "tunic", color: "#c0392b", pattern: "stripes", color2: "#f4f1e8", trim: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "Danish is famous for swallowing its consonants. Written words often look nothing like how they sound.",
          "It has the 'stød', a tiny catch in the throat that can change the meaning of a word.",
          "Its tongue-twister 'rødgrød med fløde' (red berry pudding with cream) is a classic test for foreigners.",
        ],
        audio: { ll: "dan", n: 4 },
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
        audio: { ll: "haw", n: 4 },
      },
    ],
  },

  // ------------------------------------------------------------------ 5
  conlangs: {
    title: "Constructed Languages be like…",
    part: "",
    layout: "story",
    counterLabel: "speakers",
    accent: "#6c5ce7",
    items: [
      {
        name: "Esperanto", flag: "eo", speakers: "100k–2M?", scene: "village", loc: null,
        char: { skin: "pale", hair: "short", hairColor: "grey", beard: true, beardColor: "grey", glasses: true, outfit: { type: "coat", color: "#2b2b2b", inner: "#f4f1e8" }, expression: "smile" },
        cards: [
          "Esperanto was published in 1887 by L. L. Zamenhof, an eye doctor in Warsaw who dreamed of one easy second language for the whole world.",
          "Its grammar has almost no exceptions: every noun ends in -o and every adjective in -a. 'Esperanto' itself means 'one who hopes'.",
          "Estimates of speakers range from 100,000 to 2 million, and around a thousand people grew up speaking it, including billionaire George Soros.",
        ],
        audio: { file: "Stela Speaks Esperanto.webm", start: "auto" },
      },
      {
        name: "Toki Pona", flag: null, speakers: "1,000s", scene: "abstract", loc: null,
        char: F({ skin: "light", hair: "bob", hairColor: "#6c5ce7", outfit: { type: "tunic", color: "#00b894", trim: "#fdcb6e" }, glasses: true, expression: "grin" }),
        cards: [
          "Toki Pona was invented by Sonja Lang in 2001. Its name means 'good language' or 'simple language'.",
          "It has only around 120 core words. Everything else is built from them: a 'friend' is 'jan pona', literally 'good person'.",
          "Its tiny vocabulary makes it one of the fastest languages to learn, and fans have written whole books in it.",
        ],
        audio: { file: "WIKITONGUES- Koishi speaking Toki Pona.webm", start: "auto" },
      },
      {
        name: "Klingon", flag: null, speakers: "a few dozen", scene: "abstract", loc: null,
        char: { skin: "olive", hair: "long", hairColor: "black", beard: true, outfit: { type: "coat", color: "#3a2a22", inner: "#7a1f1f" }, expression: "angry" },
        cards: [
          "Klingon was created by linguist Marc Okrand for the Star Trek films, and it has a full grammar and dictionary.",
          "It puts the object first and the subject last, a word order that almost no natural language uses. 'Qapla'' means 'success!'.",
          "Fans have translated Shakespeare's Hamlet into Klingon, but only a few dozen people are thought to speak it fluently.",
        ],
        audio: { seq: ["Tlh-Qapla'.oga", "Tlh-Qu'vatlh.oga", "NukneH 01.ogg"], repeat: 2 },
      },
      {
        name: "Volapük", flag: null, speakers: "a handful", scene: "forest", loc: null,
        char: { skin: "pale", hair: "bald", hairColor: "white", beard: true, beardColor: "white", outfit: { type: "robe", color: "#1d1d1d", trim: "#1d1d1d" }, glasses: true, expression: "smug" },
        cards: [
          "Volapük was created around 1880 by Johann Martin Schleyer, a German Catholic priest who said the idea came to him in a dream.",
          "Its name means 'world speech', from English 'world' and 'speak', squeezed until they're barely recognisable.",
          "It briefly had hundreds of thousands of learners, then collapsed when Schleyer refused any changes. In Dutch, 'Volapük' now means gibberish.",
        ],
        audio: { seq: ["Vo-Volapük.ogg", "Vo-binön.ogg", "Vo-falajelöm.ogg", "Vo-gudükumön.ogg", "Vo-dilamamalül.ogg"], repeat: 2 },
      },
      {
        name: "Lojban", flag: null, speakers: "a few dozen", scene: "abstract", loc: null,
        char: { skin: "light", hair: "spiky", hairColor: "brown", glasses: true, outfit: { type: "shirt", color: "#2d3436", tie: "#00b894" }, expression: "smug" },
        cards: [
          "Lojban, launched in 1987, is built on formal logic, and its grammar is designed so that a sentence can only be parsed one way.",
          "Its root words were blended from six big languages: Mandarin, English, Hindi, Spanish, Russian and Arabic.",
          "It's used for experiments in logic and computing, and only a few dozen people speak it conversationally.",
        ],
        audio: { file: "WIKITONGUES- John speaking Lojban.webm", start: 346 },
      },
      {
        name: "Ido", flag: null, speakers: "a few hundred", scene: "grassland", loc: null,
        char: { skin: "pale", hair: "short", hairColor: "brown", mustache: true, outfit: { type: "shirt", color: "#f4f1e8", vest: "#1d1d1d", tie: "#1d1d1d" }, hat: { type: "tophat", color: "#1d1d1d", color2: "#1d1d1d" }, expression: "neutral" },
        cards: [
          "Ido is a reformed Esperanto from 1907. Its name means 'offspring' in Esperanto.",
          "It dropped Esperanto's accented letters like ĉ and ĝ, and tried to look more familiar to speakers of European languages.",
          "The split caused a bitter feud between the two movements. Ido is still spoken today, by a few hundred enthusiasts.",
        ],
        audio: { file: "Ido pronunciation Beaufront Jespersen La maxim bona.wav", start: 0 },
      },
    ],
  },

  // ------------------------------------------------------------------ 6
  revived: {
    title: "Revived Languages be like…",
    part: "Back from the dead",
    layout: "story",
    counterLabel: "speakers",
    accent: "#2a9d8f",
    items: [
      {
        name: "Hebrew", flag: "il", speakers: "~9M", scene: "arabia", loc: [31.8, 35.2, "Israel"],
        char: { skin: "light", hair: "short", hairColor: "brown", beard: true, outfit: { type: "shirt", color: "#f4f1e8", vest: "#1f3a6b" }, glasses: true, expression: "smile" },
        cards: [
          "For around 1,700 years, Hebrew was used for prayer and writing, but nobody spoke it as their everyday mother tongue.",
          "In the late 1800s Eliezer Ben-Yehuda insisted on speaking only Hebrew at home, and his son became the first native speaker in modern times.",
          "Today around 9 million people speak it, the only known case of a language revived all the way to a national language.",
        ],
        audio: { ll: "heb", n: 4 },
      },
      {
        name: "Cornish", flag: "kernow", speakers: "~600", scene: "jersey", loc: [50.3, -5.0, "Cornwall, England"],
        char: F({ skin: "pale", hair: "long", hairColor: "auburn", outfit: { type: "dress", color: "#1d1d1d", color2: "#f4f1e8", trim: "#f2c94c" }, expression: "smile" }),
        cards: [
          "Cornish, a Celtic cousin of Welsh and Breton, stopped being spoken as a community language around 1800.",
          "In 1904 Henry Jenner published a handbook to bring it back, and enthusiasts slowly started speaking it again.",
          "In 2010 UNESCO changed its status from 'extinct' to 'critically endangered', and today there are even children raised in Cornish.",
        ],
        audio: { file: "WIKITONGUES- Elizabeth speaking Cornish.webm", start: "auto" },
      },
      {
        name: "Manx", flag: "im", speakers: "~2,000", scene: "faroe", loc: [54.2, -4.5, "Isle of Man"],
        char: { skin: "pale", hair: "short", hairColor: "red", beard: true, beardColor: "red", outfit: { type: "tunic", color: "#2e6b4f", trim: "#f2c94c" }, hat: { type: "flatcap", color: "#3a3a3a" }, expression: "grin" },
        cards: [
          "Manx is the Gaelic language of the Isle of Man. Its last native speaker, Ned Maddrell, died in 1974.",
          "Luckily he and other elders had been recorded, and learners used those tapes to rebuild the language.",
          "Today there is a Manx-medium primary school, and a new generation of children speaks Manx again.",
        ],
        audio: { file: "WIKITONGUES- Owen speaking Manx.webm", start: "auto" },
      },
      {
        name: "Māori", flag: "nz", speakers: "~185,000", scene: "bougainville", loc: [-38.5, 176.0, "Aotearoa New Zealand"],
        char: { skin: "tan", hair: "bun", hairColor: "black", tattoo: true, outfit: { type: "wrap", color: "#7a4a2a", color2: "#c8955a", trim: "#1d1d1d" }, necklace: "#2a9d8f", expression: "smile" },
        cards: [
          "By the 1970s Māori was in serious trouble: children had been punished for speaking it at school, and few young people could.",
          "In 1982 the first 'kōhanga reo' (language nests) opened, preschools where elders spoke only Māori with the children.",
          "Māori became an official language in 1987, and today it's heard everywhere, from the news to the national anthem.",
        ],
        audio: { file: "Māori waiata from Waiheke Island.ogg", start: "auto" },
      },
      {
        name: "Latin", flag: "va", speakers: "0 native", scene: "tuscany", loc: [41.9, 12.45, "Vatican City"],
        char: { skin: "light", hair: "short", hairColor: "grey", outfit: { type: "wrap", color: "#f4f1e8", color2: "#8c2b2b", trim: "#e9c46a" }, hat: { type: "crown", color: "#2e6b4f", color2: "#7a9a3a" }, expression: "smug" },
        cards: [
          "Latin has had no native speakers for over a thousand years, but it never fully went away.",
          "It's still an official language of the Vatican, which even had cash machines with instructions in Latin.",
          "A 'living Latin' movement now holds courses and summer camps where people speak it fluently, like the speaker you're hearing.",
        ],
        audio: { file: "WIKITONGUES- Titus speaking Latin.webm", start: "auto" },
      },
      {
        name: "Sanskrit", flag: "in", speakers: "~25,000", scene: "himalaya", loc: [13.9, 75.6, "Mattur, India"],
        char: { skin: "brown", hair: "bald", hairColor: "black", outfit: { type: "wrap", color: "#f4f1e8", color2: "#e67e22", trim: "#c0392b" }, facepaint: "brow", paintColor: "#c0392b", expression: "smile" },
        cards: [
          "Sanskrit is over 3,000 years old, the classical language of Hinduism, Buddhism and Jainism and a cousin of Latin and Greek.",
          "For centuries it was mostly used for scripture and scholarship, not for chatting at home.",
          "In India's 2011 census about 25,000 people listed it as their mother tongue, and in villages like Mattur it's used in everyday life.",
        ],
        audio: { ll: "san", n: 4 },
      },
    ],
  },
};
