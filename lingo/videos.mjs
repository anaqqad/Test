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
        audio: { file: "Helka 20120104 Wym.webm", start: "auto", voice: "f" },
      },
      {
        name: "Kusunda", flag: "np", speakers: "~1", scene: "himalaya", loc: [28.2, 82.6, "Western Nepal"],
        char: F({ skin: "tan", hair: "long", hairColor: "black", hat: { type: "headscarf", color: "#9b2335", color2: "#f2c94c" }, outfit: { type: "wrap", color: "#7a2e2e", color2: "#c8553d", trim: "#f2c94c" }, earrings: "#e9c46a", expression: "neutral" }),
        cards: [
          "Kusunda is a language isolate from Nepal: it is not related to any other language on Earth. Its speakers were once forest hunter-gatherers.",
          "Gyani Maiya Sen is one of the very last people who speak it fluently. You are listening to her right now.",
          "In recent years she has helped teach classes so younger Kusunda people can learn the words of their ancestors.",
        ],
        audio: { file: "Gyani Maiya Sen Kusunda - how Mihaq (Kusunda) language should be brought to the next generation.webm", start: "auto", search: "Gyani Maiya Sen Kusunda", voice: "f" },
      },
      {
        name: "Nuxalk", flag: "ca", speakers: "<20", scene: "bella", loc: [52.37, -126.75, "Bella Coola, Canada"],
        char: { skin: "brown", hair: "long", hairColor: "black", hat: { type: "headband", color: "#b5302a", color2: "#1d1d1d" }, outfit: { type: "wrap", color: "#1d1d1d", color2: "#b5302a", trim: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "Nuxalk is a Salishan language from Bella Coola in British Columbia, Canada. Fewer than 20 fluent speakers are left.",
          "It is famous for very long words with no vowels at all, like xłp̓x̣ʷłtłpłłskʷc̓, which means 'he had had a bunchberry plant'. That's the word you just heard.",
          "A local school teaches Nuxalk to children, giving the language a real chance of survival.",
        ],
        audio: { seq: ["Xłp̓x̣ʷłtłpłłskʷc̓.ogg"], repeat: 3, voice: "keep" },
      },
      {
        name: "Cherokee", flag: "us", speakers: "~2,000", scene: "forest", loc: [35.9, -94.97, "Oklahoma & North Carolina"],
        char: { skin: "tan", hair: "short", hairColor: "grey", outfit: { type: "shirt", color: "#8c2b2b", vest: "#2b2b2b" }, hat: { type: "widehat", color: "#2b2b2b", color2: "#c0392b" }, expression: "smile" },
        cards: [
          "Cherokee is an Iroquoian language of the Cherokee people, spoken today mainly in Oklahoma and North Carolina.",
          "In the 1820s a Cherokee man named Sequoyah, who couldn't read any language, invented a complete writing system for it on his own.",
          "Only around 2,000 fluent speakers remain, most of them elderly, and the Cherokee Nation has declared a language emergency.",
        ],
        audio: { file: "Wikitongues Jerry speaking Cherokee.mp3", start: "auto", voice: "m" },
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
        audio: { file: "WIKITONGUES- Junior speaking Lakota.webm", start: "auto", voice: "m" },
      },
      {
        name: "Yugambeh", flag: "au", speakers: "revival", scene: "hawaii", loc: [-28.0, 153.2, "Gold Coast, Australia"],
        char: { skin: "deep", hair: "curly", hairColor: "black", beard: true, outfit: { type: "tunic", color: "#c8553d", trim: "#f2c94c" }, facepaint: "lines", paintColor: "#f4f1e8", expression: "smile" },
        cards: [
          "Yugambeh is an Aboriginal language from the area around today's Gold Coast and Logan in Queensland, Australia.",
          "After colonisation it was nearly wiped out, and for decades almost no one spoke it fluently.",
          "Today the Yugambeh community is bringing it back with classes, songs and dictionaries, and many local place names still come from it.",
        ],
        audio: { file: "Wikitongues - Shaun speaking Yugambeh Aboriginal Australians and Torres Strait Islanders .webm", ranges: [[0, 6.6], [10.8, 20.1], [26.2, 36.0]], voice: "m" },
      },
      {
        name: "Ladino", flag: null, speakers: "<100,000", scene: "istanbul", loc: [41.0, 28.97, "Turkey, Israel, Balkans"],
        char: { skin: "light", hair: "short", hairColor: "grey", beard: true, beardColor: "grey", hat: { type: "fez", color: "#9b1c1c", color2: "#1d1d1d" }, outfit: { type: "coat", color: "#2b2f45", inner: "#f4f1e8" }, glasses: true, expression: "smile" },
        cards: [
          "Ladino, or Judeo-Spanish, is the language of the Sephardic Jews who were expelled from Spain in 1492 and settled across the Ottoman Empire.",
          "It is basically old Spanish mixed with Hebrew, Turkish and Greek, and was traditionally written in Hebrew letters.",
          "The Holocaust destroyed many Ladino-speaking communities. Today most speakers are elderly and live in Israel and Turkey.",
        ],
        audio: { file: "Isaac 20210219 Lad.webm", start: "auto", voice: "m" },
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
        audio: { file: "Andreas singing in Northern Frisian.webm", start: "auto", voice: "m" },
      },
      {
        name: "Siwi", flag: "eg", speakers: "~30,000", scene: "arabia", loc: [29.2, 25.5, "Siwa Oasis, Egypt"],
        char: { skin: "olive", hair: "short", hairColor: "black", hat: { type: "turban", color: "#f4f1e8", color2: "#c0a060" }, outfit: { type: "robe", color: "#e8dcc4", trim: "#a0522d" }, mustache: true, expression: "smile" },
        cards: [
          "Siwi is a Berber language spoken in the Siwa Oasis in Egypt's Western Desert, close to the border with Libya.",
          "It is the easternmost Berber language in the world, an island of Berber surrounded by Arabic.",
          "Siwa is also home to the ancient oracle that Alexander the Great famously travelled across the desert to visit.",
        ],
        audio: { file: "A young man from Siwa offers his greetings in the Siwan language.webm", start: 0, voice: "m" },
      },
      {
        name: "Mingrelian", flag: "ge", speakers: "~340,000", scene: "caucasus", loc: [42.5, 41.9, "Samegrelo, Georgia"],
        char: { skin: "light", hair: "short", hairColor: "black", mustache: true, outfit: { type: "coat", color: "#2b2b2b", inner: "#1d1d1d" }, hat: { type: "furhat", fur: "#3a3a3a" }, expression: "smug" },
        cards: [
          "Mingrelian is a Kartvelian language from western Georgia. It is related to Georgian, but the two are not mutually intelligible.",
          "It has no official status and is mostly spoken at home. When written, it uses the Georgian alphabet.",
          "Most Mingrelians are bilingual: Mingrelian at home, Georgian at school and work, which is why the language is slowly losing ground.",
        ],
        audio: { file: "WIKITONGUES- Valerian speaking Mingrelian.webm", start: "auto", voice: "m" },
      },
      {
        name: "Tuvan", flag: "ru", speakers: "~280,000", scene: "steppe", loc: [51.7, 94.4, "Tuva, Siberia"],
        char: { skin: "tan", hair: "short", hairColor: "black", hat: { type: "furhat", fur: "#7a5a3a" }, outfit: { type: "robe", color: "#1f5aa6", trim: "#e9c46a" }, sash: "#e9c46a", expression: "smile" },
        cards: [
          "Tuvan is a Turkic language spoken in the Republic of Tuva, in southern Siberia on the border with Mongolia.",
          "Tuva is famous for throat singing, where one singer produces two or more notes at the same time.",
          "Unlike many Siberian languages, Tuvan is still spoken by most Tuvans, and it is written in the Cyrillic alphabet.",
        ],
        audio: { file: "WIKITONGUES- Aydyn speaking Tuvan.webm", start: "auto", voice: "m" },
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
        audio: { file: "Ben Spink speaks Jèrriais and recites \"Man Bieau P'tit Jèrri\".ogg", start: 0, voice: "m" },
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
        audio: { file: "WIKITONGUES- Mark speaking Greenlandic.webm", start: "auto", voice: "m" },
      },
      {
        name: "Luxembourgish", flag: "lu", speakers: "~400,000", scene: "forest", loc: [49.6, 6.13, "Luxembourg"],
        char: { skin: "pale", hair: "short", hairColor: "brown", outfit: { type: "shirt", color: "#1f3a5f", tie: "#c0392b", vest: "#2b2b2b" }, glasses: true, expression: "smug" },
        cards: [
          "Luxembourgish is a Germanic language that only became Luxembourg's national language by law in 1984.",
          "Most Luxembourgers also speak German and French, and often switch between all three in the same day.",
          "It says 'Moien' for hello, and the national motto, 'Mir wëlle bleiwe wat mir sinn', means 'We want to remain what we are'.",
        ],
        audio: { file: "WIKITONGUES- Mark speaking Luxembourgish.webm", start: "auto", voice: "m" },
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
      { name: "Norwegian", flag: "no", score: 2, weeks: 24, char: { skin: "pale", hair: "short", hairColor: "blonde", beard: true, beardColor: "blonde", outfit: { type: "tunic", color: "#1f3a6b", pattern: "diamonds", color2: "#f4f1e8", trim: "#f4f1e8" }, hat: { type: "beanie", color: "#c0392b", color2: "#f4f1e8" }, expression: "grin" }, cards: ["Very close to English in grammar and word order. Verbs don't even change for 'I', 'you' or 'she'. The trickiest part is its sing-song pitch accent."], audio: { seq: ["LL-Q9043 (nor)-Telaneo-takk.wav", "LL-Q9043 (nor)-EdoAug-vann.wav", "LL-Q9043 (nor)-EdoAug-venn.wav"] } },
      { name: "Spanish", flag: "es", score: 2.5, weeks: 24, char: F({ skin: "olive", hair: "bun", hairColor: "black", hat: { type: "flower", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#c0392b", color2: "#1d1d1d", trim: "#1d1d1d" }, earrings: "#e9c46a", expression: "smile" }), cards: ["Spelled almost exactly how it sounds, with thousands of words shared with English. Verb endings and the subjunctive take practice, but most learners get going quickly."], audio: { seq: ["LL-Q1321 (spa)-CaroEspinoza-HOLA.wav", "LL-Q1321 (spa)-Rdrg109-gracias.wav", "LL-Q1321 (spa)-Precision27-agua.wav"] } },
      { name: "Dutch", flag: "nl", score: 3, weeks: 24, char: { skin: "pale", hair: "short", hairColor: "blonde", outfit: { type: "shirt", color: "#e67e22", vest: "#1f3a6b" }, glasses: true, expression: "smile" }, cards: ["Sits between English and German. Lots of words look familiar, but the throaty 'g' and word order in longer sentences trip people up."], audio: { seq: ["LL-Q7411 (nld)-Mélody Xu YANG WMFr-dank je.wav", "LL-Q7411 (nld)-Robin van der Vliet-hallo.wav", "LL-Q7411 (nld)-Robin van der Vliet-water.wav"] } },
      { name: "Italian", flag: "it", score: 3, weeks: 24, char: { skin: "light", hair: "short", hairColor: "black", mustache: true, outfit: { type: "shirt", color: "#f4f1e8", vest: "#2c3e50", tie: "#27ae60" }, expression: "grin" }, cards: ["Phonetic spelling, lots of Latin vocabulary English already uses, and very clear vowels. Verb conjugations are the main hurdle."], audio: { seq: ["LL-Q652 (ita)-XANA000-ciao.wav", "LL-Q652 (ita)-XANA000-grazie.wav", "LL-Q652 (ita)-XANA000-acqua.wav"] } },
      { name: "French", flag: "fr", score: 3.5, weeks: 30, char: F({ skin: "pale", hair: "bob", hairColor: "brown", hat: { type: "beret", color: "#1d1d1d" }, outfit: { type: "tunic", color: "#f4f1e8", pattern: "stripes", color2: "#1f3a6b", trim: "#1f3a6b" }, expression: "smug" }), cards: ["A third of English vocabulary comes from French, but the spelling is full of silent letters and the pronunciation is famously hard to get right."], audio: { seq: ["LL-Q150 (fra)-Poslovitch-bonjour.wav", "LL-Q150 (fra)-XANA000-merci.wav", "LL-Q150 (fra)-Mecanautes-eau.wav"] } },
      { name: "Swahili", flag: "tz", score: 4.5, weeks: 36, char: F({ skin: "dark", hair: "bun", hairColor: "black", hat: { type: "headscarf", color: "#f2a541", color2: "#2a9d8f" }, outfit: { type: "wrap", color: "#2a9d8f", color2: "#f2a541", trim: "#c0392b" }, earrings: "#e9c46a", expression: "grin" }), cards: ["Easy pronunciation and no tones, but nouns fall into many 'noun classes', and the prefixes on every word must agree with them."], audio: { file: "WIKITONGUES- Iddy speaking Swahili.webm", start: "auto" } },
      { name: "Indonesian", flag: "id", score: 4.5, weeks: 36, char: { skin: "tan", hair: "short", hairColor: "black", hat: { type: "fez", color: "#1d1d1d", color2: "#1d1d1d" }, outfit: { type: "shirt", color: "#8e5a2b", vest: "#5a3a1f" }, expression: "smile" }, cards: ["No verb tenses, no gender and no plurals (you just say the word twice). The hard part is the vocabulary and its many prefixes and suffixes."], audio: { seq: ["LL-Q9240 (ind)-Xbypass-terima kasih.wav", "LL-Q9240 (ind)-Akbar Soepadhi-halo.wav", "LL-Q9240 (ind)-Xbypass-air.wav"] } },
      { name: "German", flag: "de", score: 5, weeks: 36, char: { skin: "pale", hair: "short", hairColor: "blonde", mustache: true, hat: { type: "widehat", color: "#2f4a2f", color2: "#7a5a3a" }, outfit: { type: "shirt", color: "#f4f1e8", vest: "#3a5a2f" }, expression: "neutral" }, cards: ["English's close cousin, but with three genders, four cases, and verbs that jump to the end of the sentence. Spelling, at least, is very regular."], audio: { seq: ["LL-Q188 (deu)-Sebastian Wallroth-Danke.wav", "LL-Q188 (deu)-Natschoba-hallo.wav", "LL-Q188 (deu)-Ionenlaser-Wasser.wav"] } },
      { name: "Russian", flag: "ru", score: 6.5, weeks: 44, char: F({ skin: "pale", hair: "braids", hairColor: "blonde", hat: { type: "kokoshnik", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#c0392b", color2: "#f2c94c", trim: "#f2c94c" }, expression: "neutral" }), cards: ["A new alphabet (easier than it looks), six grammatical cases, and verbs that come in pairs depending on whether an action is finished."], audio: { seq: ["LL-Q7737 (rus)-Butko-спасибо.wav", "LL-Q7737 (rus)-Tatiana Kerbush-привет.wav", "LL-Q7737 (rus)-Lvova-вода.wav"] } },
      { name: "Hindi", flag: "in", score: 6.5, weeks: 44, char: F({ skin: "brown", hair: "long", hairColor: "black", outfit: { type: "wrap", color: "#d35400", color2: "#f1c40f", trim: "#8e44ad" }, earrings: "#e9c46a", necklace: "#e9c46a", expression: "smile" }), cards: ["Written in the Devanagari script, with sounds English doesn't separate, like four different kinds of 't'. Grammar is fairly regular once you're used to it."], audio: { seq: ["LL-Q1568 (hin)-QueerEcofeminist-नमस्ते.wav", "LL-Q1568 (hin)-Sriveenkat-धन्यवाद.wav", "LL-Q1568 (hin)-EditorFX-पानी.wav"] } },
      { name: "Polish", flag: "pl", score: 7, weeks: 44, char: { skin: "pale", hair: "short", hairColor: "brown", mustache: true, outfit: { type: "coat", color: "#7a1f1f", inner: "#f4f1e8" }, hat: { type: "flatcap", color: "#3a3a3a" }, expression: "smug" }, cards: ["Seven cases, three genders and consonant clusters like 'szcz' in words like 'Szczebrzeszyn'. Thankfully, the spelling is consistent."], audio: { seq: ["LL-Q809 (pol)-Olaf-dziękuję.wav", "LL-Q809 (pol)-Olaf-przyjaciel.wav", "LL-Q809 (pol)-Olaf-chrząszcz.wav"] } },
      { name: "Finnish", flag: "fi", score: 7, weeks: 44, char: F({ skin: "pale", hair: "long", hairColor: "blonde", hat: { type: "beanie", color: "#1f4e8c", color2: "#f4f1e8" }, outfit: { type: "parka", color: "#1f4e8c", fur: "#f4f1e8", trim: "#f4f1e8" }, expression: "neutral" }), cards: ["Not related to English at all. It has around 15 cases and very long words, but it's spelled exactly as it's pronounced."], audio: { seq: ["LL-Q1412 (fin)-Uranus123451-vesi.ogg", "LL-Q1412 (fin)-Nurtsio-sauna.wav", "LL-Q1412 (fin)-Seqv-kuin.wav"] } },
      { name: "Hungarian", flag: "hu", score: 7.5, weeks: 44, char: { skin: "light", hair: "short", hairColor: "black", mustache: true, outfit: { type: "shirt", color: "#f4f1e8", vest: "#1d1d1d" }, hat: { type: "widehat", color: "#1d1d1d", color2: "#c0392b" }, expression: "neutral" }, cards: ["Another language with no link to English: around 18 cases, vowel harmony and verbs that change depending on whether the object is definite."], audio: { seq: ["LL-Q9067 (hun)-Procrastineur49-ötödik.wav", "LL-Q9067 (hun)-Beaudine Wilson-citrom.wav", "LL-Q9067 (hun)-Beaudine Wilson-születésnap.wav"] } },
      { name: "Vietnamese", flag: "vn", score: 7.5, weeks: 44, char: F({ skin: "light", hair: "long", hairColor: "black", hat: { type: "conical", color: "#e9d8a6" }, outfit: { type: "robe", color: "#f4f1e8", trim: "#e9c46a" }, expression: "smile" }), cards: ["Uses the Latin alphabet and has simple grammar, but six tones mean 'ma' can be 'ghost', 'mother', 'horse' or 'rice seedling'."], audio: { seq: ["LL-Q9199 (vie)-Jessica Nguyen (Pamputt)-cảm ơn.wav", "LL-Q9199 (vie)-Jessica Nguyen (Pamputt)-nước.wav", "LL-Q9199 (vie)-Penn Zero MSSJ-phở.wav"] } },
      { name: "Korean", flag: "kr", score: 8.5, weeks: 88, char: F({ skin: "pale", hair: "bun", hairColor: "black", outfit: { type: "robe", color: "#e84393", trim: "#fdcb6e" }, expression: "smile" }), cards: ["Hangul can be learned in a day, but grammar is very different from English and speech levels change depending on who you're talking to."], audio: { seq: ["LL-Q9176 (kor)-Gaillon27-안녕하세요.wav", "LL-Q9176 (kor)-CHK2605-감사합니다.wav", "LL-Q9176 (kor)-HappyMidnight-사랑.wav"] } },
      { name: "Arabic", flag: "sa", score: 9, weeks: 88, char: { skin: "olive", hair: "short", hairColor: "black", beard: true, hat: { type: "headscarf", color: "#f4f1e8", color2: "#c0392b" }, outfit: { type: "robe", color: "#f4f1e8", trim: "#d9cbb0" }, expression: "neutral" }, cards: ["Right-to-left script, sounds made deep in the throat, and a big gap between Modern Standard Arabic and the dialects people actually speak at home."], audio: { seq: ["LL-Q13955 (ara)-Zinou2go-مرحبا.wav", "LL-Q13955 (ara)-Zinou2go-شكرا.wav", "LL-Q13955 (ara)-Annisa Tiara Ramadhani-ماء.wav"] } },
      { name: "Mandarin", flag: "cn", score: 9.5, weeks: 88, char: F({ skin: "light", hair: "bun", hairColor: "black", outfit: { type: "robe", color: "#c0392b", trim: "#f2c94c" }, earrings: "#e9c46a", expression: "neutral" }), cards: ["Grammar is surprisingly simple, but you need thousands of characters to read a newspaper, and four tones to be understood."], audio: { seq: ["LL-Q9192 (cmn)-Bakerkobe-你好.wav", "LL-Q9192 (cmn)-Luilui6666-谢谢.wav", "LL-Q9192 (cmn)-雲角-水.wav"] } },
      { name: "Japanese", flag: "jp", score: 10, weeks: 88, char: { skin: "light", hair: "spiky", hairColor: "black", outfit: { type: "robe", color: "#1f2a44", trim: "#c0392b" }, hat: { type: "headband", color: "#f4f1e8", color2: "#c0392b" }, expression: "angry" }, cards: ["Three writing systems at once (hiragana, katakana and kanji), verbs at the end, and different politeness levels. The FSI marks it as usually harder than others in its group."], audio: { seq: ["LL-Q5287 (jpn)-葵心-友達.wav", "LL-Q5287 (jpn)-葵心-猫.wav", "LL-Q5287 (jpn)-Zsrtrgh-言う.wav"] } },
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
        audio: { file: "Sisters remember xhosa songs and games.ogg", start: "auto", voice: "f" },
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
        audio: { file: "Silbo.ogg", start: 0, voice: "keep" },
      },
      {
        name: "Hmong", flag: "la", speakers: "millions", scene: "himalaya", loc: [20.0, 103.0, "Laos, Vietnam, China"],
        char: F({ skin: "light", hair: "long", hairColor: "black", hat: { type: "headband", color: "#1d1d1d", color2: "#e84393" }, outfit: { type: "dress", color: "#1d1d1d", color2: "#e84393", trim: "#e84393", pattern: "zigzag" }, necklace: "#d9d9d9", expression: "smile" }),
        cards: [
          "Hmong is spoken in the mountains of southern China, Laos, Vietnam and Thailand, and by large communities in the USA.",
          "It has around seven or eight tones. In its Latin alphabet, the last letter of a word shows the tone, so 'Hmoob' ends in 'b' for a high tone.",
          "Its tones are so important that the qeej, a bamboo pipe instrument, can 'speak' Hmong phrases by playing their tone melodies.",
        ],
        audio: { file: "May speaking Hmong Don.webm", start: "auto", voice: "f" },
      },
      {
        name: "Yoruba", flag: "ng", speakers: "~45M", scene: "savanna", loc: [7.4, 3.9, "Nigeria & Benin"],
        char: { skin: "dark", hair: "short", hairColor: "black", hat: { type: "fez", color: "#2a6fa5", color2: "#2a6fa5" }, outfit: { type: "robe", color: "#2a6fa5", trim: "#f2c94c" }, expression: "grin" },
        cards: [
          "Yoruba is spoken by tens of millions of people in Nigeria and Benin. It has three tones: high, mid and low.",
          "Tone changes meaning completely: 'ọkọ' can mean husband, hoe or vehicle depending on the pitch of each syllable.",
          "Because words have melodies, the 'talking drum' (dùndún) can imitate speech, and listeners can understand the messages.",
        ],
        audio: { file: "Dorcas speaking Yoruba.webm", start: "auto", voice: "f" },
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
        audio: { file: "WIKITONGUES- Mariam speaking Georgian.webm", start: "auto", voice: "f" },
      },
      {
        name: "Czech", flag: "cz", speakers: "~10M", scene: "prague", loc: [50.08, 14.43, "Czech Republic"],
        char: F({ skin: "pale", hair: "braids", hairColor: "brown", hat: { type: "flower", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#f4f1e8", color2: "#c0392b", trim: "#1f3a6b" }, expression: "smile" }),
        cards: [
          "Czech has the letter ř, a sound found in almost no other language: a rolled 'r' and a 'zh' at the same time.",
          "It is often one of the last sounds Czech children learn. You can hear it in the name of the composer Dvořák.",
          "Czech can also build sentences with no vowels at all, like 'Strč prst skrz krk', meaning 'stick your finger through your throat'.",
        ],
        audio: { ll: "ces", words: ["řeka", "tři", "moře", "řeč", "Dvořák", "keř", "dobře", "příroda", "krk", "prst"], n: 4, voice: "m" },
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
        audio: { file: "WIKITONGUES- Sandra speaking Welsh.webm", start: "auto", voice: "f" },
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
  isolates: {
    title: "Language Isolates be like…", // YouTube: "... (Part 1)"; languages with no known relatives, none in an earlier video
    part: "Part 1",
    layout: "story",
    counterLabel: "speakers",
    accent: "#00a8a8",
    items: [
      {
        name: "Burushaski", wojak: "i_bsk", flag: "pk", speakers: "~100,000", scene: "himalaya", loc: null,
        char: { skin: "tan", hair: "short", hairColor: "black", beard: true, outfit: { type: "coat", color: "#6b4a2b", inner: "#f4f1e8" }, expression: "smile" },
        cards: [
          "Burushaski is spoken by around 100,000 people in the Hunza, Nagar and Yasin valleys of northern Pakistan, among the highest mountains on Earth.",
          "Linguists have tried to link it to the languages of the Caucasus, to Siberia's Yeniseian languages, even to Indo-European. Nothing has been proven.",
          "It sorts every noun into four classes: men, women, animals and countable things, and everything else. The voice is Izhar Hunzai, telling how he survived COVID-19.",
        ],
        audio: { file: "cache/isolates/src/burushaski.m4a", start: 112.0 }, // built by build_isolates.py
      },
      {
        name: "Mapudungun", wojak: "i_arn", flag: "cl", speakers: "100,000s", scene: "patagonia", loc: null,
        char: { skin: "tan", hair: "long", hairColor: "black", outfit: { type: "coat", color: "#3a2a2a", inner: "#b22222" }, expression: "smile" },
        cards: [
          "Mapudungun is the language of the Mapuche people of Chile and Argentina. Its name means 'the speech of the land'.",
          "The Mapuche held off both the Inca and the Spanish Empire for centuries, and their language has no proven relative anywhere.",
          "Its verbs can stack many endings into one long word to say who did what, how and when. The voice is Victor, recorded by Wikitongues.",
        ],
        audio: { file: "cache/isolates/src/mapudungun.m4a", start: 12.0 },
      },
      {
        name: "Sandawe", wojak: "i_sad", flag: "tz", speakers: "~60,000", scene: "savanna", loc: null,
        char: { skin: "dark", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#7fb2d9", vest: "#7fb2d9" }, expression: "smile" },
        cards: [
          "Sandawe is spoken by about 60,000 people in central Tanzania.",
          "It uses click sounds, like the languages of the Kalahari more than 2,000 km away. For a long time they were grouped together, but no family link has ever been proven.",
          "It is also a tonal language, so the pitch of a syllable changes its meaning. These are real recordings of Sandawe words, made in 1991.",
        ],
        audio: { file: "cache/isolates/src/sandawe.m4a", start: 194.0 },
      },
      {
        name: "Warao", wojak: "i_wba", flag: "ve", speakers: "~30,000", scene: "tropical", loc: null,
        char: { skin: "tan", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#f4f1e8", vest: "#f4f1e8" }, expression: "smile" },
        cards: [
          "Warao is spoken by about 30,000 people in the Orinoco river delta of Venezuela, and in Guyana and Suriname. Its name is often translated as 'the canoe people'.",
          "It is one of the very few languages whose usual word order is object, subject, verb: 'the fish the man caught'.",
          "No relative has ever been found for it. What you are hearing is a reading of the Book of Genesis in Warao.",
        ],
        audio: { file: "cache/isolates/src/warao.m4a", start: 36.0 },
      },
      {
        name: "Tiwi", wojak: "i_tiw", flag: "au", speakers: "~2,000", scene: "andaman", loc: null,
        char: { skin: "dark", hair: "short", hairColor: "grey", beard: true, outfit: { type: "shirt", color: "#2f5d3a", vest: "#2f5d3a" }, expression: "smile" },
        cards: [
          "Tiwi is spoken on the Tiwi Islands, off the coast of northern Australia, by about 2,000 people. It is not related to any language on the Australian mainland.",
          "Its verbs can pack a whole sentence into one word. Young people today speak 'New Tiwi', a simpler form mixed with English.",
          "The voice is Marius Puruntatameri, reading Tiwi words in 1976.",
        ],
        audio: { file: "cache/isolates/src/tiwi.webm", start: 29.0 },
      },
    ],
  },
  conlangs3: {
    title: "People Actually Speak These Made-Up Languages", // YouTube: "... (Part 3)"
    part: "Part 3",
    layout: "story",
    counterLabel: "speakers",
    accent: "#6c5ce7",
    items: [
      {
        name: "Kunyotóri'an", wojak: "c_kun_f", flag: null, speakers: "a handful", scene: "village", loc: null,
        char: { skin: "light", hair: "long", hairColor: "brown", outfit: { type: "shirt", color: "#c97b4a", vest: "#c97b4a" }, expression: "smile" },
        cards: [
          "Modern Latin Kunyotóri’an, in its own words Kunyotóri’an Laónn Motóryo, was sent to us by one of our subscribers. Thank you, catlover82!",
          "What you are hearing is a local song about eight cats: 'Tenyo ítho navos ne me caal' means 'I have eight cats in my house'.",
          "The cats are black, white, orange, striped, non-striped and grey-striped. 'Who knows where they came from, but they are mine!'",
        ],
        audio: { file: "cache/conlangs3/src/kunyotorian_catlover82.mp3", start: 0.8 }, // catlover82 (@orion_cat823), used with permission; built by build_conlangs3.py
      },
      {
        name: "Occidental", wojak: "c_ile_f", flag: null, speakers: "100s", scene: "abstract", loc: null,
        char: { skin: "light", hair: "bob", hairColor: "brown", outfit: { type: "shirt", color: "#1f8a8a", vest: "#1f8a8a" }, expression: "smile" },
        cards: [
          "Occidental was published in 1922 by Edgar de Wahl, a teacher in Tallinn, Estonia. In 1949 it was renamed Interlingue.",
          "It was built to look natural, so Europeans can often read it at first sight: 'Salute, mi nómine es…' means 'Hello, my name is…'.",
          "The voice you are hearing is Dorlota, an avatar in the virtual world Second Life, introducing herself in Occidental.",
        ],
        audio: { file: "cache/conlangs3/src/occidental_paulineauster.weba", start: 1.6 },
      },
      {
        name: "Interslavic", wojak: "c_isv", flag: null, speakers: "1,000s", scene: "forest", loc: null,
        char: { skin: "light", hair: "short", hairColor: "brown", outfit: { type: "shirt", color: "#2f5d3a", vest: "#2f5d3a" }, expression: "smile" },
        cards: [
          "Interslavic is built from what Russian, Polish, Czech, Serbian and the other Slavic languages share, so Slavs can understand it without studying it.",
          "The man you are hearing had discovered it only the day before. He reads it using the Slavic languages he already speaks.",
          "It is written in both Latin and Cyrillic letters, so every Slav can read it in their own alphabet.",
        ],
        audio: { file: "cache/conlangs3/src/interslavic_thecandle.m4a", start: 87.0 },
      },
      {
        name: "Kotava", wojak: "c_avk_f", flag: null, speakers: "dozens", scene: "hills", loc: null,
        char: { skin: "pale", hair: "short", hairColor: "grey", glasses: true, outfit: { type: "coat", color: "#5b3a7a", inner: "#f4f1e8" }, expression: "smile" },
        cards: [
          "Kotava was created in 1978 by Staren Fetcey in France, as a language that belongs to no people at all.",
          "Its words are not borrowed from any existing language, so nobody gets a head start when learning it.",
          "The voice you are hearing is Luce Vergneaux, who has also recorded thousands of Kotava words for Wikimedia Commons.",
        ],
        audio: { file: "cache/conlangs3/src/kotava_lucekotavusik.m4a", start: 8.0 },
      },
      {
        name: "Pandunia", wojak: "c_pan", flag: null, speakers: "a handful", scene: "grassland", loc: null,
        char: { skin: "pale", hair: "short", hairColor: "blond", beard: true, outfit: { type: "coat", color: "#2b4a8a", inner: "#f4f1e8" }, expression: "smile" },
        cards: [
          "Pandunia was created by Risto Kupsala from Finland, as a world language that takes its words from every continent.",
          "Its name says it: 'pan' means all and 'dunia' means world, a word shared by Arabic, Persian, Hindi, Malay and Swahili.",
          "The voice you are hearing is Risto Kupsala himself, saying hello in his own language: 'Salam!'",
        ],
        audio: { file: "cache/conlangs3/src/pandunia_ristokupsala.m4a", start: 2.3 },
      },
      {
        name: "Solresol", wojak: "c_sol_f", flag: null, speakers: "a handful", scene: "dusk", loc: null,
        char: { skin: "pale", hair: "short", hairColor: "grey", glasses: true, outfit: { type: "coat", color: "#8a2b2b", inner: "#f4f1e8" }, expression: "smile" },
        cards: [
          "Solresol was invented by the French musician François Sudre, starting in 1817. Every word is built from the seven notes do, re, mi, fa, sol, la, si.",
          "So it can be spoken, sung, played on an instrument, or even written with seven colours.",
          "Turn a word around and you get its opposite: fala means good, lafa means bad. The voice is Luce Vergneaux, the same speaker as in Kotava.",
        ],
        audio: { file: "cache/conlangs3/src/solresol.wav", start: 0.0 },
      },
    ],
  },
  conlangs2: {
    title: "People Actually Speak These Made-Up Languages", // Part 1's YouTube title (owner); YouTube: "... (Part 2)"
    part: "Part 2",
    layout: "story",
    counterLabel: "speakers",
    accent: "#6c5ce7",
    items: [
      {
        name: "Interlingua", wojak: "c_ina", flag: null, speakers: "1,000s", scene: "village", loc: null,
        char: { skin: "light", hair: "short", hairColor: "brown", outfit: { type: "shirt", color: "#4a6fa5", vest: "#4a6fa5" }, expression: "smile" },
        cards: [
          "Interlingua was published in 1951 in New York by the International Auxiliary Language Association, after more than 25 years of work.",
          "Its words were not invented. They were taken from what English, French, Italian, Spanish and Portuguese already share, so millions can read it without a lesson.",
          "Medical journals once printed their summaries in Interlingua, because doctors across Europe could understand it at first sight.",
        ],
        audio: { file: "cache/conlangs2/src/interlingua_yt.m4a", start: 8.0 }, // mithradates (YouTube), used with permission; built by build_conlangs2.py
      },
      {
        name: "Lingua Franca Nova", wojak: "c_lfn", flag: null, speakers: "100s", scene: "forest", loc: null,
        char: { skin: "pale", hair: "short", hairColor: "grey", beard: true, beardColor: "grey", outfit: { type: "coat", color: "#7a5a3a", inner: "#9bc4e2" }, expression: "smile" },
        cards: [
          "Lingua Franca Nova was created in 1998 by C. George Boeree, an American psychology professor. Its fans call it Elefen, after the letters L, F, N.",
          "Its words come from French, Italian, Spanish, Portuguese and Catalan, but its grammar copies creole languages: verbs never change, whoever does the action.",
          "What you are hearing is Lingua Franca Nova describing itself: a simple, regular language that sounds like Italian or Spanish. It even has its own Wikipedia.",
        ],
        audio: { file: "cache/conlangs2/src/lfn2.mp3", start: 0.0 },
      },
      {
        name: "Uropi", wojak: "c_uro", flag: null, speakers: "a handful", scene: "tuscany", loc: null,
        char: { skin: "pale", hair: "short", hairColor: "white", glasses: true, outfit: { type: "coat", color: "#1f2a44", inner: "#f4f1e8" }, expression: "smile" },
        cards: [
          "Uropi was started in 1986 by Joël Landais, a teacher in France, who wanted one language that every European would find familiar.",
          "He rebuilt its words from the ancient roots that most European languages grew from, so a Uropi word often looks like a distant cousin of the one you know.",
          "The voice you are hearing is Landais himself, reciting the French poem Le Pont Mirabeau translated into Uropi.",
        ],
        audio: { file: "cache/conlangs2/src/uropi.mp3", start: 0.0 },
      },
      {
        name: "Láadan", wojak: "c_ldn", flag: null, speakers: "a handful", scene: "grassland", loc: null,
        char: { skin: "light", hair: "short", hairColor: "brown", beard: true, outfit: { type: "coat", color: "#5b2a6e", inner: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "Láadan was invented in 1982 by linguist Suzette Haden Elgin for her science-fiction novel Native Tongue, to give women words other languages lack.",
          "Every sentence opens with a word saying what it is, a statement, question or command, and closes with one saying how you know it: you saw it, dreamed it or were told.",
          "It has separate verbs for menstruating in pain, with joy and for the first time. Only a handful of people speak it, and these are real recordings of its words.",
        ],
        audio: { file: "cache/conlangs2/src/laadan.wav", start: 0.0 },
      },
    ],
  },
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
        audio: { file: "Stela Speaks Esperanto.webm", start: "auto", voice: "f" },
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
        audio: { file: "WIKITONGUES- John speaking Lojban.webm", start: 346, voice: "m" },
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
        audio: { ll: "heb", n: 4, voice: "m" },
      },
      {
        name: "Cornish", flag: "kernow", speakers: "~600", scene: "jersey", loc: [50.3, -5.0, "Cornwall, England"],
        char: F({ skin: "pale", hair: "long", hairColor: "auburn", outfit: { type: "dress", color: "#1d1d1d", color2: "#f4f1e8", trim: "#f2c94c" }, expression: "smile" }),
        cards: [
          "Cornish, a Celtic cousin of Welsh and Breton, stopped being spoken as a community language around 1800.",
          "In 1904 Henry Jenner published a handbook to bring it back, and enthusiasts slowly started speaking it again.",
          "In 2010 UNESCO changed its status from 'extinct' to 'critically endangered', and today there are even children raised in Cornish.",
        ],
        audio: { file: "WIKITONGUES- Elizabeth speaking Cornish.webm", start: "auto", voice: "f" },
      },
      {
        name: "Manx", flag: "im", speakers: "~2,000", scene: "faroe", loc: [54.2, -4.5, "Isle of Man"],
        char: { skin: "pale", hair: "short", hairColor: "red", beard: true, beardColor: "red", outfit: { type: "tunic", color: "#2e6b4f", trim: "#f2c94c" }, hat: { type: "flatcap", color: "#3a3a3a" }, expression: "grin" },
        cards: [
          "Manx is the Gaelic language of the Isle of Man. Its last native speaker, Ned Maddrell, died in 1974.",
          "Luckily he and other elders had been recorded, and learners used those tapes to rebuild the language.",
          "Today there is a Manx-medium primary school, and a new generation of children speaks Manx again.",
        ],
        audio: { file: "WIKITONGUES- Owen speaking Manx.webm", start: "auto", voice: "m" },
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
        audio: { file: "WIKITONGUES- Titus speaking Latin.webm", start: "auto", voice: "m" },
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
  // ------------------------------------------------------------------ 7
  soundlike: {
    title: "Languages That Sound Like a Different Language",
    part: "Part 1",
    layout: "story",
    counterLabel: "speakers",
    items: [
      {
        name: "Maltese", flag: "mt", speakers: "~520,000", like: "Arabic", verdict: ["SORT OF", "#ff9500"], scene: "adriatic", loc: [35.9, 14.51, "Valletta, Malta"],
        char: { skin: "olive", hair: "short", hairColor: "black", beard: true, outfit: { type: "shirt", color: "#c0392b", vest: "#f4f1e8" }, expression: "grin" },
        cards: [
          "Maltese grew out of Arabic, but it's the only Semitic language written in the Latin alphabet, and an official EU language.",
          "Centuries of Sicilian, Italian and English mixed in, so 'grazzi' means thank you and 'karozza' means car.",
        ],
        audio: { file: "WIKITONGUES- Keith speaking Maltese.webm", start: "auto", voice: "m" },
      },
      {
        name: "European Portuguese", flag: "pt", speakers: "~10M", like: "Russian", verdict: ["NOPE", "#ff3b30"], scene: "adriatic", loc: [38.72, -9.14, "Portugal"],
        char: F({ skin: "light", hair: "long", hairColor: "brown", outfit: { type: "dress", color: "#1f4e8c", color2: "#f4f1e8", trim: "#c0392b" }, earrings: "#e9c46a", expression: "smile" }),
        cards: [
          "In Portugal, Portuguese swallows its unstressed vowels and turns many s sounds into a 'sh', so it can sound Slavic to outsiders.",
          "It is a Romance language from Latin, like Spanish. Many Brazilians say the Portugal accent is the hard one to follow.",
        ],
        audio: { file: "WIKITONGUES- Sara speaking Portuguese.webm", start: "auto", voice: "f" },
      },
      {
        name: "Romanian", flag: "ro", speakers: "~24M", like: "Italian on shuffle", verdict: ["SAME FAMILY", "#34c759"], scene: "hills", loc: [46.77, 23.6, "Cluj-Napoca, Romania"],
        char: F({ skin: "light", hair: "braids", hairColor: "brown", hat: { type: "headscarf", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#f4f1e8", color2: "#c0392b", trim: "#1f4e8c" }, expression: "smile" }),
        cards: [
          "Romanian comes from Latin, just like Italian, but it grew up surrounded by Slavic languages and Hungarian and borrowed many of their words.",
          "It's the only major Romance language that still has noun cases, a leftover from Latin.",
        ],
        audio: { file: "WIKITONGUES- Raluca speaking Romanian.webm", start: "auto", voice: "f" },
      },
      {
        name: "Dutch", flag: "nl", speakers: "~24M", like: "English after 3 drinks", verdict: ["CLOSE COUSIN", "#34c759"], scene: "copenhagen", loc: [52.37, 4.9, "Netherlands"],
        char: F({ skin: "pale", hair: "ponytail", hairColor: "blonde", outfit: { type: "tunic", color: "#e67e22", trim: "#f4f1e8" }, expression: "grin" }),
        cards: [
          "Dutch and English are close Germanic cousins: 'appel', 'water', 'boek' and 'huis' are apple, water, book and house.",
          "The throaty Dutch g sound comes from the back of the mouth, so 'Gouda' starts a bit like clearing your throat.",
        ],
        audio: { file: "WIKITONGUES- Eva speaking Dutch.webm", start: "auto", voice: "f" },
      },
      {
        name: "West Frisian", flag: "nl", speakers: "~470,000", like: "Old English", verdict: ["CLOSEST COUSIN", "#34c759"], scene: "baltic", loc: [53.2, 5.8, "Friesland, Netherlands"],
        char: F({ skin: "pale", hair: "bob", hairColor: "blonde", outfit: { type: "shirt", color: "#1f4e8c", vest: "#f4f1e8" }, glasses: true, expression: "smile" }),
        cards: [
          "The Frisian languages are usually called English's closest relatives on the mainland of Europe.",
          "An old rhyme says bread, butter and green cheese is good English and good Frisian. In Frisian: 'Brea, bûter en griene tsiis'.",
        ],
        audio: { file: "WIKITONGUES- Sjoukje speaking West Frisian.webm", start: "auto", voice: "f" },
      },
      {
        name: "Afrikaans", flag: "za", speakers: "~7M", like: "Dutch", verdict: ["ITS CHILD", "#34c759"], scene: "kalahari", loc: [-33.92, 18.42, "Cape Town, South Africa"],
        char: { skin: "light", hair: "short", hairColor: "brown", beard: true, beardColor: "brown", outfit: { type: "shirt", color: "#2e6b4f", vest: "#c8a165" }, hat: { type: "widehat", color: "#8a6a3b", color2: "#3b2a16" }, expression: "grin" },
        cards: [
          "Afrikaans grew out of the Dutch brought to the Cape in the 1600s. Dutch and Afrikaans speakers can mostly understand each other.",
          "Its grammar got simpler: 'ek is, jy is, hy is' means I am, you are, he is. One verb form for everyone.",
        ],
        audio: { file: "WIKITONGUES- Roussow speaking Afrikaans.webm", start: "auto", voice: "m" },
      },
      {
        name: "Luxembourgish", flag: "lu", speakers: "~400,000", like: "German, but in France", verdict: ["ACCURATE", "#34c759"], scene: "forest", loc: [49.6, 6.13, "Luxembourg"],
        char: { skin: "light", hair: "short", hairColor: "brown", outfit: { type: "coat", color: "#1f3a5f", inner: "#f4f1e8" }, glasses: true, expression: "smile" },
        cards: [
          "Luxembourgish is a Germanic language, close to German, but it is full of French: thank you is simply 'merci'.",
          "Most Luxembourgers also speak German and French, and many switch between all three in a single day.",
        ],
        audio: { file: "WIKITONGUES- Mark speaking Luxembourgish.webm", start: "auto", voice: "m" },
      },
      {
        name: "Esperanto", flag: "eo", speakers: "100k–2M?", like: "Spanish? Italian? Polish?", verdict: ["ALL OF THEM", "#ff9500"], scene: "village", loc: null,
        char: F({ skin: "light", hair: "long", hairColor: "auburn", outfit: { type: "tunic", color: "#2e8b57", trim: "#f2c94c" }, expression: "grin" }),
        cards: [
          "Esperanto was invented in 1887 from mostly Romance, Germanic and Slavic roots, so it sounds a little like all of them at once.",
          "Every noun ends in -o and every adjective in -a: 'bela knabo' is a handsome boy.",
        ],
        audio: { file: "Stela Speaks Esperanto.webm", start: "auto", voice: "f" },
      },
      {
        name: "Hungarian", flag: "hu", speakers: "~13M", like: "Finnish", verdict: ["DISTANT COUSIN", "#ff9500"], scene: "grassland", loc: [47.5, 19.04, "Hungary"],
        char: F({ skin: "light", hair: "long", hairColor: "brown", outfit: { type: "dress", color: "#c0392b", color2: "#f4f1e8", trim: "#2e6b4f", pattern: "stripes" }, expression: "smile" }),
        cards: [
          "Hungarian really is a distant relative of Finnish and Estonian, but they split thousands of years ago and can't understand each other.",
          "Every word is stressed on its first syllable, which gives Hungarian its rolling rhythm.",
        ],
        audio: { file: "WIKITONGUES- Orsolya speaking Hungarian.webm", start: "auto", voice: "f" },
      },
      {
        name: "Persian", flag: "ir", speakers: "~110M", like: "Arabic", verdict: ["NOPE", "#ff3b30"], scene: "zagros", loc: [35.7, 51.4, "Iran"],
        char: { skin: "olive", hair: "short", hairColor: "black", beard: true, outfit: { type: "shirt", color: "#1d1d1d", vest: "#3a3a3a" }, expression: "neutral" },
        cards: [
          "Persian is written in an Arabic-based script and borrowed many Arabic words, but it's Indo-European: closer to English than to Arabic.",
          "'Mâdar' (mother) and 'barâdar' (brother) are distant cousins of the English words.",
        ],
        audio: { file: "WIKITONGUES- Daniel speaking Farsi.webm", start: "auto", voice: "m" },
      },
      {
        name: "Korean", flag: "kr", speakers: "~80M", like: "Japanese", verdict: ["NOPE", "#ff3b30"], scene: "hongkong", loc: [37.56, 126.98, "South Korea"],
        char: { skin: "light", hair: "short", hairColor: "black", outfit: { type: "coat", color: "#2b2b2b", inner: "#f4f1e8" }, expression: "smile" },
        cards: [
          "Korean and Japanese have similar grammar, with the verb at the end, but most linguists treat them as unrelated.",
          "Korean has its own alphabet, Hangul, created in the 1440s under King Sejong so ordinary people could learn to read.",
        ],
        audio: { file: "WIKITONGUES- Hanbid speaking Korean.webm", start: "auto" },
      },
      {
        name: "Welsh", flag: "gb-wls", speakers: "~540,000", like: "Elvish", verdict: ["KINDA!", "#34c759"], scene: "wales", loc: [52.4, -3.8, "Wales"],
        char: F({ skin: "pale", hair: "long", hairColor: "brown", hat: { type: "tophat", color: "#1d1d1d", color2: "#1d1d1d" }, outfit: { type: "coat", color: "#7a1f1f", inner: "#f4f1e8", pattern: "check", color2: "#5a1515" }, expression: "smile" }),
        cards: [
          "Tolkien loved Welsh, and it inspired the sound of Sindarin, one of the Elvish languages in The Lord of the Rings.",
          "Its famous 'll' sound: put your tongue up as for an L, then blow air out the sides, as in 'Llanelli'.",
        ],
        audio: { file: "WIKITONGUES- Sandra speaking Welsh.webm", start: "auto", voice: "f" },
      },
    ],
  },
  // ------------------------------------------------------------------ 7b
  soundlike2: {
    title: "Languages That Sound Like a Different Language",
    part: "Part 2",
    layout: "story",
    counterLabel: "speakers",
    items: [
      {
        name: "Finnish", wojak: "sl2_fin", flag: "fi", speakers: "~5.5M", like: "Japanese", verdict: ["NOPE", "#ff3b30"], scene: "dalarna", loc: [60.17, 24.94, "Helsinki, Finland"],
        char: F({ skin: "pale", hair: "long", hairColor: "blonde", outfit: { type: "coat", color: "#1f4e8c", inner: "#f4f1e8" }, expression: "smile" }),
        cards: [
          "Both love vowels and care about length: Finnish 'tuli' is fire but 'tuuli' is wind, like Japanese 'obasan' (aunt) and 'obaasan' (grandma).",
          "Finnish is Uralic, related to Estonian and distantly to Hungarian. Tolkien used it to build Quenya, the High-Elvish language.",
        ],
        audio: { file: "WIKITONGUES- Jenni speaking Finnish.webm", start: "auto", voice: "f" },
      },
      {
        name: "Sardinian", wojak: "sl2_srd", flag: "it", speakers: "~1M", like: "Latin", verdict: ["CLOSEST THING", "#34c759"], scene: "canary", loc: [40.32, 9.33, "Sardinia, Italy"],
        char: { skin: "olive", hair: "short", hairColor: "black", beard: true, outfit: { type: "shirt", color: "#f4f1e8", vest: "#1d1d1d" }, hat: { type: "flatcap", color: "#1d1d1d" }, expression: "grin" },
        cards: [
          "Sardinian is often called the living Romance language closest to Latin: 'domo' is house, from Latin 'domus'.",
          "It isn't an Italian dialect but a language of its own, officially recognised by Italy in 1999.",
        ],
        audio: { file: "WIKITONGUES- Ricardo speaking Sardinian.webm", start: "auto", voice: "m" },
      },
      {
        name: "Tagalog", wojak: "sl2_tgl", flag: "ph", speakers: "~28M", like: "Spanish", verdict: ["BORROWED A LOT", "#ff9500"], scene: "andaman", loc: [14.6, 120.98, "Manila, Philippines"],
        char: { skin: "tan", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#f4f1e8", vest: "#e9dcc4" }, expression: "grin" },
        cards: [
          "After 300+ years of Spanish rule, Tagalog took thousands of Spanish words: 'kumusta' (how are you), 'mesa' (table), 'sapatos' (shoes).",
          "But it is Austronesian, related to Malay, Hawaiian and Malagasy. Two o'clock is often 'alas dos', straight from Spanish.",
        ],
        audio: { file: "WIKITONGUES- Josh speaking Tagalog.webm", start: "auto", voice: "m" },
      },
      {
        name: "Greek", wojak: "sl2_ell", flag: "gr", speakers: "~13M", like: "Spanish", verdict: ["NOPE", "#ff3b30"], scene: "adriatic", loc: [37.97, 23.72, "Athens, Greece"],
        char: F({ skin: "olive", hair: "long", hairColor: "black", outfit: { type: "dress", color: "#1f6fb5", color2: "#f4f1e8", trim: "#f4f1e8" }, earrings: "#e9c46a", expression: "smile" }),
        cards: [
          "Greek and Spanish both have just five vowels, a, e, i, o, u, and a similar rhythm, so to outsiders they can sound alike.",
          "Greek is its own branch of Indo-European and the oldest one still spoken, with texts from about 1400 BC.",
        ],
        audio: { file: "WIKITONGUES- Ioanna speaking Greek.webm", start: "auto", voice: "f" },
      },
      {
        name: "Scottish Gaelic", wojak: "sl2_gla", flag: "gb-sct", speakers: "~60,000", like: "Russian", verdict: ["NOPE", "#ff3b30"], scene: "moorland", loc: [57.3, -6.2, "Isle of Skye, Scotland"],
        char: F({ skin: "pale", hair: "bob", hairColor: "auburn", outfit: { type: "coat", color: "#2e6b4f", inner: "#f4f1e8", pattern: "check", color2: "#7a1f1f" }, expression: "smile" }),
        cards: [
          "Gaelic consonants come in 'broad' and 'slender' pairs, a bit like the hard and soft consonants of Russian, so it can sound Slavic.",
          "It came over from Ireland about 1,500 years ago. 'Whisky' comes from Gaelic 'uisge beatha', water of life.",
        ],
        audio: { file: "WIKITONGUES- Rosemary speaking Scottish Gaelic.webm", start: "auto", voice: "f" },
      },
      {
        name: "Kazakh", wojak: "sl2_kaz", flag: "kz", speakers: "~13M", like: "Russian", verdict: ["NOPE", "#ff3b30"], scene: "steppe", loc: [43.24, 76.89, "Almaty, Kazakhstan"],
        char: { skin: "light", hair: "short", hairColor: "black", outfit: { type: "coat", color: "#1f5f8b", inner: "#f2c94c" }, expression: "smile" },
        cards: [
          "Kazakh is written in Cyrillic and full of Russian loanwords, but it is a Turkic language, a cousin of Turkish and Uzbek.",
          "Kazakhstan is moving Kazakh to the Latin alphabet, with the switch planned to finish by 2031.",
        ],
        audio: { file: "WIKITONGUES- Yernur speaking Kazakh.webm", start: "auto", voice: "m" },
      },
      {
        name: "Lithuanian", wojak: "sl2_lit", flag: "lt", speakers: "~3M", like: "Sanskrit", verdict: ["DISTANT COUSIN", "#ff9500"], scene: "baltic", loc: [54.69, 25.28, "Vilnius, Lithuania"],
        char: F({ skin: "pale", hair: "braids", hairColor: "blonde", outfit: { type: "dress", color: "#2e6b4f", color2: "#f4f1e8", trim: "#c0392b" }, expression: "smile" }),
        cards: [
          "Lithuanian kept many very old Indo-European features, so linguists love comparing it with Sanskrit: 'sūnus' (son) is Sanskrit 'sūnu'.",
          "It still has seven noun cases and a pitch accent, which very few European languages keep today.",
        ],
        audio: { file: "WIKITONGUES- Erika speaking Lithuanian.webm", start: "auto", voice: "f" },
      },
      {
        name: "Icelandic", wojak: "sl2_isl", flag: "is", speakers: "~350,000", like: "Vikings", verdict: ["PRETTY MUCH", "#34c759"], scene: "faroe", loc: [64.15, -21.94, "Reykjavík, Iceland"],
        char: { skin: "pale", hair: "short", hairColor: "blonde", beard: true, beardColor: "#9a6b2f", outfit: { type: "coat", color: "#3a3a3a", inner: "#f4f1e8" }, hat: { type: "beanie", color: "#1f4e8c", color2: "#f4f1e8" }, expression: "grin" },
        cards: [
          "Icelandic changed so little that Icelanders can still read sagas written down over 700 years ago.",
          "Instead of borrowing words it builds them: computer is 'tölva', from 'tala' (number) and 'völva' (prophetess).",
        ],
        audio: { file: "WIKITONGUES- Ljóni speaking Icelandic.webm", start: "auto" },
      },
      {
        name: "Estonian", wojak: "sl2_est", flag: "ee", speakers: "~1.1M", like: "Finnish", verdict: ["CLOSE COUSIN", "#34c759"], scene: "forest", loc: [59.44, 24.75, "Tallinn, Estonia"],
        char: F({ skin: "pale", hair: "ponytail", hairColor: "brown", outfit: { type: "tunic", color: "#1f5f8b", trim: "#f4f1e8" }, glasses: true, expression: "smile" }),
        cards: [
          "Estonian and Finnish are close Finnic relatives and share many basic words: fish is 'kala' in both.",
          "It has 14 noun cases, and vowel pileups like 'jäääär', the edge of the ice, with four ä in a row.",
        ],
        audio: { file: "WIKITONGUES- Liisi speaking Estonian.webm", start: "auto", voice: "f" },
      },
      {
        name: "Georgian", wojak: "sl2_kat", flag: "ge", speakers: "~4M", like: "an alien language", verdict: ["VERY REAL", "#34c759"], scene: "tbilisi", loc: [41.72, 44.79, "Tbilisi, Georgia"],
        char: F({ skin: "light", hair: "long", hairColor: "black", outfit: { type: "dress", color: "#7a1f1f", color2: "#f4f1e8", trim: "#e9c46a" }, expression: "grin" }),
        cards: [
          "Georgian loves consonant pileups: 'gvprtskvni' means 'you peel us', with eight consonant sounds in a row.",
          "It isn't related to Russian, Turkish or Armenian, and has its own alphabet. The oldest Georgian inscriptions are from the 400s AD.",
        ],
        audio: { file: "WIKITONGUES- Mariam speaking Georgian.webm", start: "auto", voice: "f" },
      },
      {
        name: "Neapolitan", wojak: "sl2_nap", flag: "it", speakers: "~5M", like: "Italian", verdict: ["OWN LANGUAGE", "#ff9500"], scene: "adriatic", loc: [40.85, 14.27, "Naples, Italy"],
        char: { skin: "olive", hair: "curly", hairColor: "black", beard: true, outfit: { type: "shirt", color: "#1f4e8c", vest: "#f4f1e8" }, expression: "grin" },
        cards: [
          "Neapolitan grew out of Latin alongside Italian, so it isn't just Italian with an accent. It blurs final vowels into a soft 'uh'.",
          "Many famous songs are in Neapolitan, like ’O sole mio and Funiculì, Funiculà.",
        ],
        audio: { file: "WIKITONGUES- Foffo speaking Neapolitan.webm", start: "auto", voice: "m" },
      },
      {
        name: "Polish", wojak: "sl2_pol", flag: "pl", speakers: "~40M", like: "Russian", verdict: ["SAME FAMILY", "#34c759"], scene: "prague", loc: [52.23, 21.01, "Warsaw, Poland"],
        char: F({ skin: "pale", hair: "long", hairColor: "brown", outfit: { type: "coat", color: "#c0392b", inner: "#f4f1e8" }, expression: "smile" }),
        cards: [
          "Polish and Russian are both Slavic, but Polish uses the Latin alphabet, and its sz, cz and rz give it a shushing sound.",
          "Famous tongue twister: 'W Szczebrzeszynie chrząszcz brzmi w trzcinie', a beetle buzzes in the reeds in Szczebrzeszyn.",
        ],
        audio: { file: "WIKITONGUES- Marta speaking Polish.webm", start: "auto", voice: "f" },
      },
    ],
  },
  // ------------------------------------------------------------------ US audience
  native: {
    title: "Native American Languages be like…",
    part: "",
    layout: "story",
    counterLabel: "speakers",
    accent: "#b5452f",
    items: [
      {
        name: "Navajo", wojak: "n_nav", flag: "us", speakers: "~170,000", scene: "sierra", loc: [35.67, -109.05, "Navajo Nation, Arizona"],
        char: F({ skin: "brown", hair: "bun", hairColor: "black", outfit: { type: "shirt", color: "#1f4e8c", vest: "#f4f1e8" }, earrings: "#3fb8af", expression: "smile" }),
        cards: [
          "Navajo has more speakers than any other Native language in the US, and it’s tonal: a high or low pitch can change a word’s meaning.",
          "In World War II, Navajo Code Talkers sent US Marine messages in a code built on Navajo. The enemy never broke it.",
        ],
        audio: { file: "US Department of Labor - A message in Navajo about workers' compensation benefits (2023).opus", start: 7.5, voice: "f" },
      },
      {
        name: "Cherokee", wojak: "n_chr", flag: "us", speakers: "~2,000", scene: "forest", loc: [35.9, -94.97, "Oklahoma & North Carolina"],
        char: { skin: "tan", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#7a1f1f", vest: "#f4f1e8" }, expression: "smile" },
        cards: [
          "Speakers call the language Tsalagi, and 'osiyo' means hello.",
          "Cherokee is Iroquoian, a cousin of Mohawk and Seneca far to the north. It is the only Iroquoian language of the South still spoken.",
        ],
        audio: { file: "WIKITONGUES- Hassan speaking Cherokee.webm", start: "auto", voice: "m" },
      },
      {
        name: "Ojibwe", wojak: "n_oji", flag: "us", speakers: "~20,000", scene: "dalarna", loc: [47.5, -92.5, "Great Lakes, US & Canada"],
        char: { skin: "tan", hair: "short", hairColor: "black", outfit: { type: "coat", color: "#2e6b4f", inner: "#f4f1e8" }, expression: "smile" },
        cards: [
          "English got words from Ojibwe: 'Mississippi' is 'misi-ziibi', great river, and 'Michigan' comes from 'mishigami', great water.",
          "Every Ojibwe noun is either animate or inanimate, and some things you might not expect count as 'alive', like a rock: 'asin'.",
        ],
        audio: { file: "Casey speaking Ojibwe.webm", start: 18, voice: "m" },
      },
      {
        name: "Lakota", wojak: "n_lkt", flag: "us", speakers: "~2,000", scene: "grassland", loc: [43.5, -101.5, "South & North Dakota"],
        char: F({ skin: "tan", hair: "long", hairColor: "black", outfit: { type: "shirt", color: "#c0392b", vest: "#f4f1e8" }, expression: "smile" }),
        cards: [
          "Lakota, Dakota and Nakota are close varieties of one Sioux language. 'Dakota' is usually said to mean friends or allies.",
          "Lakota has sounds English lacks, like k’, said with a little pop of air from the throat.",
        ],
        audio: { file: "Kimberly speaking Lakota.webm", start: "auto", voice: "f" },
      },
      {
        name: "Crow", wojak: "n_cro", flag: "us", speakers: "~3,000", scene: "patagonia", loc: [45.6, -107.5, "Crow Reservation, Montana"],
        char: F({ skin: "tan", hair: "long", hairColor: "black", outfit: { type: "coat", color: "#1f5f8b", inner: "#f4f1e8" }, expression: "smile" }),
        cards: [
          "The Crow call themselves Apsáalooke, 'children of the large-beaked bird'. English speakers turned that into 'Crow'.",
          "Crow is a Siouan language, and its closest relative is Hidatsa, spoken in North Dakota.",
        ],
        audio: { file: "WIKITONGUES- Roanne speaking Crow.webm", start: "auto", voice: "f" },
      },
      {
        name: "Gwich’in", wojak: "n_gwi", flag: "us", speakers: "a few hundred", scene: "alaska", loc: [66.56, -145.27, "Alaska & northern Canada"],
        char: { skin: "light", hair: "short", hairColor: "grey", outfit: { type: "coat", color: "#3a3a3a", inner: "#c0392b" }, expression: "smile" },
        cards: [
          "Gwich’in is spoken around the Arctic Circle in Alaska and northern Canada, where caribou have fed its people for thousands of years.",
          "It is Athabaskan, a relative of Navajo, even though the two are thousands of kilometres apart.",
        ],
        audio: { file: "WIKITONGUES- Allan speaking Gwich'in.webm", start: "auto", voice: "m" },
      },
    ],
  },
  // ------------------------------------------------------------------ 8
  // Simulated: the owner asked for AI voices here. Each phrase is a published scholarly reconstruction, written in IPA
  // and read by a Piper voice (ipa_say.py / sim_audio.py). The video labels every clip as an AI simulation.
  ancient: {
    title: "Extinct Languages Simulated by AI (Part 1)",
    simVoices: "Arabic for Egyptian, Hebrew for Akkadian, Icelandic for Old Norse and Gothic, Italian for Latin, Greek for Ancient Greek, Turkish for Hittite, Dutch for Old English, Persian for Sumerian, German for Proto-Indo-European",
    simLimits: "Ancient Greek's musical pitch accent is not reproduced, and some details (Egyptian vowels, the laryngeal sounds of Proto-Indo-European) are educated guesses even among experts",
    simTexts: "Hávamál 76, Beowulf 1-2, Gothic Bible (Matthew 6:9), Caesar, Homer's Iliad 1.1, Hrozný's Hittite sentence, Code of Hammurabi law 1, the Egyptian royal formula ankh wedja seneb, the Sumerian King List, and Schleicher's fable in the version by Andrew Byrd",
    part: "",
    layout: "story",
    counterLabel: "spoken around",
    sim: true,
    items: [
      {
        name: "Old Norse", flag: null, speakers: "~1000 AD", scene: "faroe", loc: [62.0, 8.0, "Scandinavia & Iceland"],
        script: "Deyr fé, deyja frændr, deyr sjalfr it sama",
        char: { skin: "pale", hair: "short", hairColor: "auburn", beard: true, beardColor: "#7a3b1c", outfit: { type: "tunic", color: "#5b3a29", trim: "#c8a165" }, hat: { type: "beanie", color: "#4a4a4a", color2: "#4a4a4a" }, expression: "grin" },
        cards: [
          "The language of the Vikings. 'Cattle die, kinsmen die, you yourself will die the same' is from the Hávamál, poems written down in Iceland around 1270.",
          "Icelandic changed so little that Icelanders today can still read the old sagas.",
        ],
        audio: { sim: { model: "is_IS-steinn-medium", scale: 1.1, words: [["Deyr", "dœyr"], ["fé,", "feː,"], ["deyja", "ˈdœyjɑ"], ["frændr,", "ˈfrɛːndr,"], ["deyr", "dœyr"], ["sjalfr", "ˈsjɑlvr"], ["it", "it"], ["sama.", "ˈsɑmɑ."]] } },
      },
      {
        name: "Old English", flag: null, speakers: "~1000 AD", scene: "moorland", loc: [52.5, -1.5, "England"],
        script: "Hwæt! Wē Gār-Dena in ġēar-dagum, þēod-cyninga þrym ġefrūnon",
        char: { skin: "pale", hair: "short", hairColor: "brown", beard: true, beardColor: "brown", outfit: { type: "tunic", color: "#2f5d3a", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "The first line of Beowulf: 'Listen! We have heard of the glory of the kings of the Spear-Danes in days of old.'",
          "This is the ancestor of English, yet today it has to be studied like a foreign language.",
        ],
        audio: { sim: { model: "nl_NL-ronnie-medium", scale: 1.1, words: [["Hwæt!", "ʍæt!"], ["Wē", "weː"], ["Gār-Dena", "ˈɡɑːrdenɑ"], ["in", "in"], ["ġēar-dagum,", "ˈjæːɑrdɑɣum,"], ["þēod-cyninga", "ˈθeːodkyniŋɡɑ"], ["þrym", "θrym"], ["ġefrūnon.", "jeˈfruːnon."]] } },
      },
      {
        name: "Gothic", flag: null, speakers: "~350 AD", scene: "steppe", loc: [44.5, 27.0, "Lower Danube"],
        script: "𐌰𐍄𐍄𐌰 𐌿𐌽𐍃𐌰𐍂 𐌸𐌿 𐌹𐌽 𐌷𐌹𐌼𐌹𐌽𐌰𐌼",
        scriptFont: "Noto Sans Gothic",
        char: { skin: "light", hair: "short", hairColor: "blonde", beard: true, beardColor: "#9a6b2f", outfit: { type: "coat", color: "#3a2f5b", inner: "#f4f1e8" }, expression: "grin" },
        cards: [
          "Around 350 AD bishop Wulfila invented the Gothic alphabet to translate the Bible. This is the Lord's Prayer: Our Father in heaven, holy be your name.",
          "The last known Gothic speakers lived in Crimea. A Flemish diplomat wrote down a list of their words in the 1560s.",
        ],
        audio: { sim: { model: "is_IS-bui-medium", scale: 1.1, words: [["Atta", "ˈatta"], ["unsar", "ˈunsar"], ["þu", "θuː"], ["in", "in"], ["himinam,", "ˈhiminam,"], ["weihnai", "ˈwiːhnɛː"], ["namo", "ˈnamoː"], ["þein.", "θiːn."]] } },
      },
      {
        name: "Classical Latin", flag: null, speakers: "~50 BC", scene: "tuscany", loc: [41.9, 12.5, "Rome"],
        script: "VENI · VIDI · VICI",
        char: F({ skin: "olive", hair: "bun", hairColor: "black", outfit: { type: "dress", color: "#f4f1e8", color2: "#7a1f1f", trim: "#c8a165" }, earrings: "#e9c46a", expression: "smile" }),
        cards: [
          "Romans said v like w and c always like k. So Caesar said 'weenee, weedee, weekee', and his own name sounded like 'Kaisar'.",
          "The second line is from Caesar's Gallic War: all Gaul is divided into three parts.",
        ],
        audio: { sim: { model: "it_IT-paola-medium", scale: 1.05, words: [["Vēnī,", "ˈweːniː,"], ["vīdī,", "ˈwiːdiː,"], ["vīcī.", "ˈwiːkiː."], ["Gallia", "ˈɡallia"], ["est", "ɛst"], ["omnis", "ˈɔmnɪs"], ["dīvīsa", "diːˈwiːsa"], ["in", "ɪn"], ["partēs", "ˈparteːs"], ["trēs.", "treːs."]] } },
      },
      {
        name: "Ancient Greek", flag: null, speakers: "~700 BC", scene: "adriatic", loc: [37.97, 23.72, "Greece"],
        script: "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος",
        scriptFont: "Noto Serif",
        char: F({ skin: "olive", hair: "long", hairColor: "black", outfit: { type: "dress", color: "#f4f1e8", color2: "#1f4e8c", trim: "#c8a165" }, expression: "neutral" }),
        cards: [
          "The first line of the Iliad by Homer: 'Sing, goddess, the rage of Achilles, son of Peleus.'",
          "Ancient Greek had a pitch accent: the little marks over the letters showed where the voice went up and down, almost like singing.",
        ],
        audio: { sim: { model: "el_GR-rapunzelina-medium", scale: 1.1, words: [["mênin", "ˈmɛːnin"], ["áeide", "aˈeːde"], ["theà", "tʰeˈa"], ["Pēlēïádeō", "pɛːlɛːiˈadeɔː"], ["Akhilêos.", "akʰiˈlɛːos."]] } },
      },
      {
        name: "Hittite", flag: null, speakers: "~1600 BC", scene: "steppe", loc: [40.02, 34.61, "Hattusa, Turkey"],
        script: "nu NINDA-an ezzateni, wātar-ma ekutteni", scriptLabel: "CUNEIFORM, IN LATIN LETTERS",
        char: { skin: "tan", hair: "long", hairColor: "black", beard: true, outfit: { type: "wrap", color: "#8c2b2b", color2: "#c8a165", trim: "#f2c94c" }, expression: "neutral" },
        cards: [
          "Hittite was the language of an empire in today's Turkey, written in cuneiform on clay tablets. This sentence means: now you will eat bread and drink water.",
          "In 1915 Bedřich Hrozný spotted 'wātar' (water) and 'ezza' (eat) here and realised Hittite was a distant relative of English.",
        ],
        audio: { sim: { model: "tr_TR-dfki-medium", scale: 1.1, words: [["nu", "nu"], ["NINDA-an", "ˈnindaan"], ["ezzateni,", "edzˈzateni,"], ["wātar-ma", "ˈwaːtarma"], ["ekutteni.", "eˈkutteni."]] } },
      },
      {
        name: "Akkadian", flag: null, speakers: "~1750 BC", scene: "arabia", loc: [32.54, 44.42, "Babylon, Iraq"],
        scriptLabel: "CUNEIFORM, IN LATIN LETTERS", script: "šumma awīlum awīlam ubbirma nērtam elīšu iddīma lā uktīnšu, mubbiršu iddâk",
        char: { skin: "tan", hair: "long", hairColor: "black", beard: true, outfit: { type: "wrap", color: "#1f3a5f", color2: "#c8a165", trim: "#f2c94c" }, hat: { type: "headband", color: "#c8a165", color2: "#1f3a5f" }, expression: "neutral" },
        cards: [
          "Akkadian was the language of Babylon. This is law number 1 of the Code of Hammurabi: whoever accuses a man of murder without proof shall be put to death.",
          "It is the oldest known Semitic language, a distant relative of Arabic and Hebrew.",
        ],
        audio: { sim: { model: "he_IL-saspeech-medium", scale: 1.0, words: [["šumma", "ˈʃumma"], ["awīlum", "aˈwiːlum"], ["awīlam", "aˈwiːlam"], ["ubbirma", "ubˈbirma"], ["nērtam", "ˈneːrtam"], ["elīšu", "eˈliːʃu"], ["iddīma", "idˈdiːma"], ["lā", "laː"], ["uktīnšu,", "ukˈtiːnʃu,"], ["mubbiršu", "mubˈbirʃu"], ["iddâk.", "idˈdaːk."]] } },
      },
      {
        name: "Ancient Egyptian", flag: null, speakers: "~2000 BC", scene: "arabia", loc: [25.7, 32.6, "Thebes, Egypt"],
        script: "𓋹𓍑𓋴",
        scriptFont: "Noto Sans Egyptian Hieroglyphs", scriptSize: 110,
        char: { skin: "brown", hair: "short", hairColor: "black", outfit: { type: "wrap", color: "#f4f1e8", color2: "#c8a165", trim: "#1f6fb0" }, necklace: "#c8a165", expression: "neutral" },
        cards: [
          "'Life, prosperity, health!' Egyptians wrote these three signs after the name of the pharaoh.",
          "Hieroglyphs wrote no vowels. Scholars rebuild them from Coptic, the last stage of Egyptian, and from foreign spellings of Egyptian names.",
        ],
        audio: { sim: { model: "ar_JO-kareem-medium", scale: 1.15, words: [["ꜥnḫ", "ˈʕaːnax,"], ["wḏꜣ", "ˈwaːdʒaʔ,"], ["snb!", "ˈsaːnib!"]] } },
      },
      {
        name: "Sumerian", flag: null, speakers: "~2100 BC", scene: "arabia", loc: [31.32, 45.64, "Uruk, Iraq"],
        scriptLabel: "CUNEIFORM, IN LATIN LETTERS", script: "nam-lugal an-ta e₁₁-de₃-a-ba, nam-lugal eriduᵏⁱ-ga",
        char: { skin: "tan", hair: "bald", hairColor: "black", outfit: { type: "wrap", color: "#f4f1e8", color2: "#8a6a3b", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "Sumerian is one of the two oldest written languages, in cuneiform from about 3200 BC. This is the start of the Sumerian King List: when kingship came down from heaven, the kingship was in Eridu.",
          "It has no known relatives. Babylonian scribes kept copying it for centuries after people stopped speaking it, like Latin in Europe.",
        ],
        audio: { sim: { model: "fa_IR-amir-medium", scale: 1.15, words: [["nam-lugal", "namˈluɡal"], ["an-ta", "ˈanta"], ["e-de-a-ba,", "edeˈaba,"], ["nam-lugal", "namˈluɡal"], ["eridu-ga", "eriˈduɡa."]] } },
      },
      {
        name: "Proto-Indo-European", flag: null, speakers: "~4000 BC", scene: "steppe", loc: [48.0, 40.0, "Pontic steppe (one theory)"],
        script: "h₂áwis h₁éḱwōs-kʷe", scriptLabel: "NEVER WRITTEN · MODERN RECONSTRUCTION",
        char: { skin: "light", hair: "short", hairColor: "brown", beard: true, beardColor: "#3b2a16", outfit: { type: "wrap", color: "#6b4a2b", color2: "#3b2a16", trim: "#c8a165" }, expression: "smile" },
        cards: [
          "Never written down. Linguists rebuilt it by comparing its descendants: English, Hindi, Persian, Russian, Greek, Latin and hundreds more.",
          "This is 'The Sheep and the Horses', a short story linguists write in it: a sheep that had no wool saw horses.",
        ],
        audio: { sim: { model: "de_DE-thorsten-medium", scale: 1.1, words: [["h₂áwis", "ˈxawis"], ["h₁éḱwōs-kʷe.", "ˈʔekʷoːskʷe."], ["h₂áwis,", "ˈxawis,"], ["yésmin", "ˈjesmin"], ["h₂wl̥h₁néh₂", "xʷl̩ˈneːx"], ["ne", "ne"], ["h₁ést,", "ˈʔest,"], ["dédorḱe", "ˈdedorke"], ["h₁éḱwons.", "ˈʔekʷons."]] } },
      },
    ],
  },
  // ------------------------------------------------------------------ 9
  ancient2: {
    title: "Extinct Languages Simulated by AI (Part 2)",
    simVoices: "Mexican Spanish for Maya, Russian for Tocharian, Swahili for Meroitic, Welsh for Gaulish, Persian for Old Persian, Hebrew for Aramaic, Romanian for Etruscan, Mandarin for Old Chinese, Arabic for Phoenician, Greek for Mycenaean Greek",
    simLimits: "some details are educated guesses even among experts: the vowels of Phoenician and Old Chinese, and the sounds of Etruscan and Meroitic, two languages we can read aloud but still barely understand",
    simTexts: "the royal title of Pakal of Palenque, Tocharian B kinship words, the Meroitic words for king and queen, the Gaulish dedication from Vaison-la-Romaine, Darius's Behistun inscription, Daniel 5:25, the numbers on Etruscan dice, the first poem of the Shijing (Old Chinese after Baxter and Sagart), the Ahiram sarcophagus, and Linear B words from Pylos",
    part: "",
    layout: "story",
    counterLabel: "spoken around",
    sim: true,
    items: [
      {
        name: "Classical Maya", flag: null, speakers: "~700 AD", scene: "amazon", loc: [17.48, -92.05, "Palenque, Mexico"],
        script: "k'uhul baakal ajaw, K'inich Janaab Pakal", scriptLabel: "MAYA GLYPHS, IN LATIN LETTERS",
        char: { skin: "brown", hair: "long", hairColor: "black", hat: { type: "feathers", color: "#1f8a5b", color2: "#f2c94c" }, outfit: { type: "wrap", color: "#f4f1e8", color2: "#1f8a5b", trim: "#c0392b" }, necklace: "#1f8a5b", expression: "neutral" },
        cards: [
          "The royal title of Pakal the Great, who ruled the city of Palenque for 68 years: holy lord of Baakal, K'inich Janaab Pakal.",
          "Maya glyphs were only cracked in the late 1900s, after Yuri Knorozov showed in the 1950s that many signs stand for syllables. Mayan languages are still spoken by millions today.",
        ],
        audio: { sim: { model: "es_MX-ald-medium", scale: 1.1, words: [["k'uhul", "kuˈhul"], ["baakal", "baːˈkal"], ["ajaw,", "aˈxaw,"], ["K'inich", "kiˈnitʃ"], ["Janaab", "xaˈnaːb"], ["Pakal.", "paˈkal."]] } },
      },
      {
        name: "Tocharian", flag: null, speakers: "~600 AD", scene: "arabia", loc: [41.72, 82.94, "Kucha, western China"],
        script: "pācer · mācer · procer · kante", scriptLabel: "TOCHARIAN B, IN LATIN LETTERS",
        char: { skin: "light", hair: "long", hairColor: "auburn", outfit: { type: "coat", color: "#7a2e2e", inner: "#f2c94c" }, expression: "neutral" },
        cards: [
          "Found in 1,000-year-old manuscripts in the deserts of western China, yet it's Indo-European like English: pācer, mācer, procer mean father, mother, brother.",
          "Its word for hundred, kante, starts with k like Latin centum, not with s like its Indian and Persian neighbours, Sanskrit śata and Persian sad.",
        ],
        audio: { sim: { model: "ru_RU-denis-medium", scale: 1.15, words: [["pācer,", "ˈpaːtɕer,"], ["mācer,", "ˈmaːtɕer,"], ["procer,", "ˈprotɕer,"], ["kante.", "ˈkante."]] } },
      },
      {
        name: "Meroitic", flag: null, speakers: "~100 BC", scene: "savanna", loc: [16.94, 33.75, "Meroë, Sudan"],
        script: "qore · kdke", scriptLabel: "MEROITIC, IN LATIN LETTERS",
        char: F({ skin: "dark", hair: "short", hairColor: "black", hat: { type: "crown", color: "#d9b13b", color2: "#c0392b" }, outfit: { type: "dress", color: "#f4f1e8", color2: "#d9b13b", trim: "#c0392b" }, necklace: "#d9b13b", earrings: "#d9b13b", expression: "neutral" }),
        cards: [
          "The language of the Kingdom of Kush in today's Sudan, land of more pyramids than Egypt. We can read its letters aloud, but we understand only a small part of it.",
          "Two words we do know: qore, king, and kdke, queen. Through Greek and the Bible, kdke became the name Candace.",
        ],
        audio: { sim: { model: "sw_CD-lanfrica-medium", scale: 1.15, words: [["qore,", "ˈkore,"], ["kdke.", "kanˈdake."]] } },
      },
      {
        name: "Gaulish", flag: null, speakers: "~50 BC", scene: "forest", loc: [44.24, 5.07, "Vaison-la-Romaine, France"],
        script: "ΣΕΓΟΜΑΡΟΣ ΟΥΙΛΛΟΝΕΟΣ ΤΟΟΥΤΙΟΥΣ ΝΑΜΑΥΣΑΤΙΣ ΕΙΩΡΟΥ ΒΗΛΗΣΑΜΙ ΣΟΣΙΝ ΝΕΜΗΤΟΝ", scriptLabel: "GAULISH, WRITTEN IN GREEK LETTERS",
        char: { skin: "pale", hair: "long", hairColor: "blonde", mustache: true, beardColor: "#9a6b2f", outfit: { type: "tunic", color: "#2e6b4f", trim: "#c0392b", pattern: "check", color2: "#1f4e3a" }, expression: "grin" },
        cards: [
          "Asterix's language! A Gaul named Segomaros, citizen of Nîmes, dedicated a sacred grove, a nemeton, to the goddess Belesama, writing Gaulish in Greek letters.",
          "Gaulish died out under Roman rule, but French kept around 150 of its words, like chêne (oak) and mouton (sheep).",
        ],
        audio: { sim: { model: "cy_GB-gwryw_gogleddol-medium", scale: 1.1, words: [["Segomaros", "seɡoˈmaros"], ["Uilloneos", "wilˈloneos"], ["toutius", "ˈtoutius"], ["Namausatis", "namauˈsatis"], ["eiōrū", "ˈejoːruː"], ["Bēlēsami", "beːleːˈsami"], ["sosin", "ˈsosin"], ["nemeton.", "ˈnemeton."]] } },
      },
      {
        name: "Old Persian", flag: null, speakers: "~520 BC", scene: "zagros", loc: [34.39, 47.44, "Behistun, Iran"],
        script: "𐎠𐎭𐎶𐏐𐎭𐎠𐎼𐎹𐎺𐎢𐏁𐏐𐎧𐏁𐎠𐎹𐎰𐎡𐎹", scriptFont: "Noto Sans Old Persian", scriptSize: 64,
        char: { skin: "olive", hair: "long", hairColor: "black", beard: true, hat: { type: "crown", color: "#d9b13b", color2: "#1f4e8c" }, outfit: { type: "coat", color: "#5b2a6b", inner: "#d9b13b" }, expression: "neutral" },
        cards: [
          "King Darius carved this on a cliff at Behistun: I am Darius, the great king, king of kings. The same text in three languages later helped scholars crack cuneiform.",
          "His word for king, xšāyaθiya, slowly turned into the Persian word shah.",
        ],
        audio: { sim: { model: "fa_IR-amir-medium", scale: 1.1, words: [["adam", "aˈdam"], ["Dārayavauš,", "daːraˈjavauʃ,"], ["xšāyaθiya", "xʃaːˈjaθija"], ["vazraka,", "vazˈraka,"], ["xšāyaθiya", "xʃaːˈjaθija"], ["xšāyaθiyānām.", "xʃaːjaθiˈjaːnaːm."]] } },
      },
      {
        name: "Ancient Aramaic", flag: null, speakers: "~500 BC", scene: "arabia", loc: [32.5, 44.4, "Babylon, Iraq"],
        script: "מנא מנא תקל ופרסין", scriptFont: "Noto Serif Hebrew", scriptSize: 60, scriptLabel: "ARAMAIC, IN THE SQUARE SCRIPT",
        char: { skin: "tan", hair: "short", hairColor: "black", beard: true, hat: { type: "turban", color: "#f4f1e8", color2: "#1f4e8c" }, outfit: { type: "wrap", color: "#8a6a3b", color2: "#f4f1e8", trim: "#1f4e8c" }, expression: "neutral" },
        cards: [
          "Mene, mene, tekel, upharsin: the writing on the wall in the Book of Daniel, in Aramaic. Counted, counted, weighed, divided.",
          "Aramaic was the shared language of the Persian Empire and the everyday language of Jesus. Small communities still speak modern forms of it.",
        ],
        audio: { sim: { model: "he_IL-saspeech-medium", scale: 1.15, words: [["mənē", "məˈneː"], ["mənē", "məˈneː"], ["təqēl", "təˈkeːl"], ["ūp̄arsīn.", "ufarˈsiːn."]] } },
      },
      {
        name: "Etruscan", flag: null, speakers: "~500 BC", scene: "tuscany", loc: [42.5, 11.8, "Etruria, Italy"],
        script: "θu · zal · ci · huθ · maχ · śa", scriptLabel: "THE NUMBERS ON ETRUSCAN DICE",
        char: F({ skin: "olive", hair: "braids", hairColor: "black", outfit: { type: "dress", color: "#b5452f", color2: "#f4f1e8", trim: "#1d1d1d" }, earrings: "#d9b13b", expression: "smile" }),
        cards: [
          "The language of Italy before Rome. We can read every letter, since the Romans took their alphabet from the Etruscans, but we barely understand it.",
          "Even the numbers one to six on Etruscan dice, θu, zal, ci, huθ, maχ, śa, are still argued over.",
        ],
        audio: { sim: { model: "ro_RO-mihai-medium", scale: 1.2, words: [["θu,", "tʰu,"], ["zal,", "tsal,"], ["ci,", "ki,"], ["huθ,", "hutʰ,"], ["maχ,", "makʰ,"], ["śa.", "ʃa."]] } },
      },
      {
        name: "Old Chinese", flag: null, speakers: "~800 BC", scene: "hills", loc: [34.6, 112.4, "Yellow River, China"],
        script: "關關雎鳩 在河之洲", scriptFont: "Noto Serif TC", scriptSize: 60,
        char: F({ skin: "light", hair: "bun", hairColor: "black", outfit: { type: "coat", color: "#9b1d1d", inner: "#f2c94c" }, expression: "smile" }),
        cards: [
          "The first poem in the Book of Songs, about 3,000 years old: guan guan cry the ospreys, on the island in the river.",
          "Characters don't show sound, so linguists rebuild it from ancient rhymes and old Chinese words in Vietnamese, Korean and Japanese. Many think it had no tones yet.",
        ],
        audio: { sim: { model: "zh_CN-huayan-medium", scale: 1.15, words: [["kʷˤra[n]", "kʷraːn"], ["kʷˤra[n]", "kʷraːn"], ["tsʰa", "tsʰa"], ["ku,", "ku,"], ["dzˤəʔ", "dzəʔ"], ["ɡˤaj", "ɡaj"], ["tə", "tə"], ["tu.", "tu."]] } },
      },
      {
        name: "Phoenician", flag: null, speakers: "~1000 BC", scene: "adriatic", loc: [34.12, 35.65, "Byblos, Lebanon"],
        script: "𐤀𐤓𐤍 𐤆 𐤐𐤏𐤋 𐤀𐤕𐤁𐤏𐤋 𐤁𐤍 𐤀𐤇𐤓𐤌 𐤌𐤋𐤊 𐤂𐤁𐤋", scriptFont: "Noto Sans Phoenician", scriptSize: 56,
        char: { skin: "olive", hair: "short", hairColor: "black", beard: true, outfit: { type: "tunic", color: "#6b1f5b", trim: "#d9b13b" }, expression: "neutral" },
        cards: [
          "From King Ahiram's coffin in Byblos: this coffin Ittobaal, son of Ahiram, king of Byblos, made for his father.",
          "Phoenician sailors spread this 22-letter alphabet around the Mediterranean. It is the ancestor of the Greek, Latin, Hebrew and Arabic alphabets.",
        ],
        audio: { sim: { model: "ar_JO-kareem-medium", scale: 1.1, words: [["ʾrn", "ʔaˈroːn"], ["z", "zeː"], ["pʿl", "paˈʕal"], ["ʾtbʿl", "ʔittobaˈʕal"], ["bn", "bin"], ["ʾḥrm,", "ʔaħiːˈrom,"], ["mlk", "milk"], ["gbl.", "ˈɡubl."]] } },
      },
      {
        name: "Mycenaean Greek", flag: null, speakers: "~1400 BC", scene: "adriatic", loc: [37.03, 21.7, "Pylos, Greece"],
        script: "wa-na-ka · po-ti-ni-ja · ti-ri-po · di-pa", scriptLabel: "LINEAR B, IN LATIN LETTERS",
        char: F({ skin: "olive", hair: "long", hairColor: "black", outfit: { type: "dress", color: "#1f4e8c", color2: "#f4f1e8", trim: "#d9b13b", pattern: "stripes" }, expression: "neutral" }),
        cards: [
          "Written in Linear B on clay tablets around 1400 BC, the oldest Greek we have: wanax (king), potnia (lady), tripod, cup.",
          "In 1952 architect Michael Ventris cracked Linear B. A tablet that spelled ti-ri-po next to a drawing of a tripod soon proved him right.",
        ],
        audio: { sim: { model: "el_GR-rapunzelina-medium", scale: 1.15, words: [["wanaks,", "ˈwanaks,"], ["potnija,", "ˈpotnija,"], ["tripos,", "ˈtripos,"], ["dipas.", "ˈdipas."]] } },
      },
    ],
  },
  // ------------------------------------------------------------------ 10
  // One voice (Piper en_GB-alan) reads English through the centuries from reconstructed pronunciations.
  english: {
    title: "How English Sounded Through Time (AI Simulation)",
    part: "",
    layout: "story",
    counterLabel: "year",
    sim: true,
    simVoices: "one British English voice for every era, so only the language changes",
    simMethod: [
      "Nobody alive has heard English before the age of recordings, so the voice in this video is an AI simulation, not a recording. The method:",
      "1. Real texts: every line is a real text from its time, and the Lord's Prayer appears in several eras so you can compare the same words.",
      "2. Reconstructed pronunciation: linguists rebuild older English from spelling (Old and Middle English were written much closer to how they sounded), from rhymes and poetic meter, from spelling mistakes, from descriptions by early grammarians, and from how English is spoken in different places today.",
      "3. One AI voice for every era: an open-source Piper text-to-speech voice was fed the reconstructed sounds directly, written in the International Phonetic Alphabet (IPA), so it says exactly what the reconstruction says. Using the same voice throughout means only the language changes, not the speaker.",
      "Limits: the voice is a modern British speaker, so his accent comes through. Older stages are less certain: Old English vowels and Chaucer's final e are rebuilt from spelling, rhyme and meter, and the 1600s accent follows David Crystal's Original Pronunciation work. Think of it as a best guess built on real scholarship.",
    ],
    simLimits: "older stages are more uncertain: Old English vowels and Chaucer's final e are rebuilt from spelling, rhyme and meter, and the 1600s accent follows David Crystal's Original Pronunciation work",
    simTexts: "Cædmon's Hymn, the Lord's Prayer from the West Saxon Gospels, Chaucer's General Prologue, the Wycliffe Bible, Tyndale's New Testament, Hamlet, the King James Bible, the Declaration of Independence, and a modern translation of the Lord's Prayer",
    items: [
      {
        name: "Earliest English", flag: null, speakers: "~670 AD", scene: "moorland", loc: [54.49, -0.61, "Whitby, England"],
        script: "Nū sculon heriġean heofonrīċes weard, meotodes meahte ond his mōdġeþanc", scriptLabel: "OLD ENGLISH · CÆDMON'S HYMN",
        char: { skin: "pale", hair: "short", hairColor: "brown", outfit: { type: "wrap", color: "#6b4a2b", color2: "#3b2a16", trim: "#c8a165" }, expression: "smile" },
        cards: [
          "The oldest English poem we know. A cowherd named Cædmon is said to have sung it after a dream: now we must praise the guardian of heaven's kingdom.",
          "Old English had sounds we lost, like the throaty x in meahte (might), still heard in Scottish loch and German Nacht.",
        ],
        audio: { sim: { model: "en_GB-alan-medium", scale: 1.05, words: [["Nū", "nuː"], ["sculon", "ˈʃulon"], ["heriġean", "ˈherijən"], ["heofonrīċes", "ˈheovonriːtʃəs"], ["weard,", "wæɑrd,"], ["meotodes", "ˈmeotodəs"], ["meahte", "ˈmæɑxte"], ["ond", "ond"], ["his", "his"], ["mōdġeþanc.", "ˈmoːdjəθɑnk."]] } },
      },
      {
        name: "Old English", flag: null, speakers: "~1000 AD", scene: "village", loc: [51.06, -1.31, "Winchester, England"],
        script: "Fæder ūre þū þe eart on heofonum, sī þīn nama ġehālgod", scriptLabel: "THE LORD'S PRAYER · WEST SAXON GOSPELS",
        char: { skin: "pale", hair: "short", hairColor: "auburn", beard: true, beardColor: "#7a3b1c", outfit: { type: "tunic", color: "#2f5d3a", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "The Lord's Prayer around 1000 AD. Word for word: father our, thou that art in heavens, be thy name hallowed.",
          "Nouns had case endings like German today, so word order was freer. Fæder (father) and nama (name) are still easy to spot.",
        ],
        audio: { sim: { model: "en_GB-alan-medium", scale: 1.05, words: [["Fæder", "ˈfæder"], ["ūre", "ˈuːre"], ["þū", "θuː"], ["þe", "θe"], ["eart", "æɑrt"], ["on", "on"], ["heofonum,", "ˈheovonum,"], ["sī", "siː"], ["þīn", "θiːn"], ["nama", "ˈnɑmɑ"], ["ġehālgod.", "jeˈhɑːlɣod."]] } },
      },
      {
        name: "Chaucer's English", flag: null, speakers: "~1390", scene: "village", loc: [51.28, 1.08, "Canterbury, England"],
        script: "Whan that Aprille with his shoures soote / The droghte of March hath perced to the roote", scriptLabel: "MIDDLE ENGLISH · THE CANTERBURY TALES",
        char: { skin: "pale", hair: "short", hairColor: "grey", beard: true, beardColor: "#8a8a8a", hat: { type: "beret", color: "#7a1f1f" }, outfit: { type: "coat", color: "#7a1f1f", inner: "#f4f1e8" }, expression: "smile" },
        cards: [
          "The opening of Chaucer's Canterbury Tales: when April with its sweet showers has pierced the drought of March to the root.",
          "Letters we now ignore were spoken: the k in knight, the gh in night (like loch), and often the final e, as in soote.",
        ],
        audio: { sim: { model: "en_GB-alan-medium", scale: 1.05, words: [["Whan", "ʍan"], ["that", "θat"], ["Aprille", "ˈaːpril"], ["with", "wiθ"], ["his", "his"], ["shoures", "ˈʃuːrəs"], ["soote,", "ˈsoːtə,"], ["the", "θə"], ["droghte", "druxt"], ["of", "ɔf"], ["March", "martʃ"], ["hath", "haθ"], ["perced", "ˈpeːrsəd"], ["to", "toː"], ["the", "θə"], ["roote.", "ˈroːtə."]] } },
      },
      {
        name: "Middle English", flag: null, speakers: "~1390", scene: "moorland", loc: [52.48, -1.2, "Lutterworth, England"],
        script: "Oure fadir that art in heuenes, halewid be thi name", scriptLabel: "THE LORD'S PRAYER · WYCLIFFE BIBLE",
        char: { skin: "pale", hair: "bald", hairColor: "brown", beard: true, beardColor: "#5a3b22", outfit: { type: "wrap", color: "#3a3a3a", color2: "#1d1d1d", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "The same prayer in the Wycliffe Bible, the first complete Bible in English. Suddenly it's almost readable!",
          "But the vowels were still old: name sounded like nah-muh and thi like thee. The big vowel changes hadn't happened yet.",
        ],
        audio: { sim: { model: "en_GB-alan-medium", scale: 1.05, words: [["Oure", "ˈuːrə"], ["fadir", "ˈfaːdir"], ["that", "θat"], ["art", "art"], ["in", "in"], ["heuenes,", "ˈhɛvənəs,"], ["halewid", "ˈhaːləwid"], ["be", "beː"], ["thi", "θiː"], ["name.", "ˈnaːmə."]] } },
      },
      {
        name: "Tyndale's English", flag: null, speakers: "1526", scene: "village", loc: [50.94, 6.96, "printed in Germany"],
        script: "O oure father which arte in heven, halowed be thy name", scriptLabel: "THE LORD'S PRAYER · TYNDALE'S NEW TESTAMENT",
        char: { skin: "pale", hair: "short", hairColor: "brown", beard: true, beardColor: "#4a3020", hat: { type: "flatcap", color: "#1d1d1d" }, outfit: { type: "coat", color: "#1d1d1d", inner: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "William Tyndale translated the New Testament from Greek in 1526. It was printed in Germany and smuggled into England, and he was later executed for it.",
          "English was in the middle of the Great Vowel Shift: long vowels were moving, so name was heading from nah-muh towards naym.",
        ],
        audio: { sim: { model: "en_GB-alan-medium", scale: 1.05, words: [["O", "oː"], ["oure", "uːr"], ["father", "ˈfaːðər"], ["which", "hwɪtʃ"], ["arte", "art"], ["in", "ɪn"], ["heven,", "ˈhɛvən,"], ["halowed", "ˈhaloːd"], ["be", "beː"], ["thy", "ðəi"], ["name.", "neːm."]] } },
      },
      {
        name: "Shakespeare's English", flag: null, speakers: "~1600", scene: "village", loc: [51.5, -0.1, "London, England"],
        script: "To be, or not to be, that is the question", scriptLabel: "HAMLET",
        char: { skin: "pale", hair: "bald", hairColor: "brown", mustache: true, beard: true, beardColor: "#5a3b22", earrings: "#d9b13b", outfit: { type: "coat", color: "#1d1d1d", inner: "#f4f1e8" }, expression: "smile" },
        cards: [
          "Hamlet, around 1600, in Original Pronunciation, the accent linguists like David Crystal have rebuilt for Shakespeare's plays.",
          "Every r was pronounced, and some of his rhymes only work in this accent, like love and prove.",
        ],
        audio: { sim: { model: "en_GB-alan-medium", scale: 1.05, words: [["To", "tə"], ["be,", "biː,"], ["or", "ɔɹ"], ["not", "nɔt"], ["to", "tə"], ["be,", "biː,"], ["that", "ðat"], ["is", "ɪz"], ["the", "ðə"], ["question.", "ˈkwɛsjən."]] } },
      },
      {
        name: "King James English", flag: null, speakers: "1611", scene: "village", loc: [51.5, -0.1, "London, England"],
        script: "Our Father which art in heaven, Hallowed be thy name", scriptLabel: "THE LORD'S PRAYER · KING JAMES BIBLE",
        char: { skin: "pale", hair: "long", hairColor: "brown", mustache: true, beardColor: "#4a3020", hat: { type: "tophat", color: "#1d1d1d" }, outfit: { type: "coat", color: "#2b2b4a", inner: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "The King James Bible of 1611, the version most English speakers still recognise today.",
          "Thou, thee and thy were already going out of everyday speech, but the Bible kept them, which is partly why they sound holy to us.",
        ],
        audio: { sim: { model: "en_GB-alan-medium", scale: 1.05, words: [["Our", "ɐʊɹ"], ["Father", "ˈfaːðəɹ"], ["which", "ʍɪtʃ"], ["art", "aɹt"], ["in", "ɪn"], ["heaven,", "ˈhɛvən,"], ["Hallowed", "ˈhaləd"], ["be", "biː"], ["thy", "ðəɪ"], ["name.", "neːm."]] } },
      },
      {
        name: "1776 American English", flag: null, speakers: "1776", scene: "forest", loc: [39.95, -75.15, "Philadelphia, USA"],
        script: "When in the Course of human events, it becomes necessary for one people to dissolve the political bands", scriptLabel: "DECLARATION OF INDEPENDENCE",
        char: { skin: "pale", hair: "short", hairColor: "grey", hat: { type: "tophat", color: "#1d1d1d" }, outfit: { type: "coat", color: "#1f3a5f", inner: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "The Declaration of Independence, 1776. American and British English still sounded very close: most English people pronounced their r's too.",
          "Dropping the r after vowels spread in southern England after this time, a big reason Americans and Brits sound different today.",
        ],
        audio: { sim: { model: "en_GB-alan-medium", scale: 1.05, words: [["When", "ʍɛn"], ["in", "ɪn"], ["the", "ðə"], ["Course", "koːɹs"], ["of", "əv"], ["human", "ˈhjuːmən"], ["events,", "ɪˈvɛnts,"], ["it", "ɪt"], ["becomes", "bɪˈkʌmz"], ["necessary", "ˈnɛsəsɛɹi"], ["for", "fɔɹ"], ["one", "wʌn"], ["people", "ˈpiːpəl"], ["to", "tə"], ["dissolve", "dɪˈzɑlv"], ["the", "ðə"], ["political", "pəˈlɪtɪkəl"], ["bands.", "bændz."]] } },
      },
      {
        name: "Modern English", flag: null, speakers: "today", scene: "hongkong", loc: null,
        script: "Our Father in heaven, hallowed be your name", scriptLabel: "THE LORD'S PRAYER · TODAY",
        char: { skin: "light", hair: "short", hairColor: "brown", outfit: { type: "tunic", color: "#2f6fb0", trim: "#f2c94c" }, glasses: true, expression: "grin" },
        cards: [
          "The same prayer today. In about 1,000 years, every word has changed its sound, and most changed their spelling too.",
          "English now has around 1.5 billion speakers, and most of them learned it as a second language.",
        ],
        audio: { sim: { model: "en_GB-alan-medium", scale: 1.05, words: [["Our", "ˈaʊə"], ["Father", "ˈfɑːðə"], ["in", "ɪn"], ["heaven,", "ˈhɛvən,"], ["hallowed", "ˈhæləʊd"], ["be", "biː"], ["your", "jɔː"], ["name.", "neɪm."]] } },
      },
    ],
  },
  // ------------------------------------------------------------------ 11
  ancient3: {
    title: "Extinct Languages Simulated by AI (Part 3)",
    part: "",
    layout: "story",
    counterLabel: "spoken around",
    sim: true,
    simVoices: "Latvian for Old Prussian, Catalan for Old Occitan, French for Old French, Spanish for Mozarabic, Italian for Early Japanese, Russian for Old Church Slavonic, German for Old High German, Welsh for Old Irish, Mandarin for Middle Chinese, Arabic for Coptic",
    simLimits: "some details are educated guesses even among experts: the exact vowels of Middle Chinese, the stress of Old Prussian, and how the Arabic-script Mozarabic verses were really pronounced",
    simTexts: "the Lord's Prayer from the 1561 Old Prussian Enchiridion, Bernart de Ventadorn's Can vei la lauzeta mover, the Song of Roland, a Mozarabic kharja, the Iroha poem, the Lord's Prayer in Old Church Slavonic, the Hildebrandslied, Pangur Bán, Li Bai's Quiet Night Thought (Middle Chinese after Baxter), and the Lord's Prayer in Bohairic Coptic",
    items: [
      {
        name: "Old Prussian", wojak: "p3_prussian", flag: null, speakers: "1561", scene: "baltic", loc: [54.7, 20.5, "Prussia (today Poland & Russia)"],
        script: "Tawe nūson kas tu essei en dangon", scriptLabel: "THE LORD'S PRAYER · 1561 CATECHISM",
        char: { skin: "pale", hair: "short", hairColor: "blonde", beard: true, beardColor: "#9a6b2f", outfit: { type: "coat", color: "#3a4a2a", inner: "#f4f1e8" }, hat: { type: "furhat", color: "#5b3a29" }, expression: "neutral" },
        cards: [
          "The Lord's Prayer from a Lutheran catechism of 1561, one of the very few texts in Old Prussian. Tawe, father, is related to Lithuanian tėvas.",
          "A Baltic language, cousin of Lithuanian and Latvian. It died out around 1700, but the name Prussia lived on for centuries.",
        ],
        audio: { sim: { model: "lv_LV-aivars-medium", scale: 1.1, words: [["Tawe", "ˈtaːwe"], ["nūson", "ˈnuːson"], ["kas", "kas"], ["tu", "tu"], ["essei", "ˈesej"], ["en", "en"], ["dangon,", "ˈdaŋɡon,"], ["swintints", "ˈswintints"], ["wirst", "wirst"], ["twais", "twajs"], ["emmens.", "ˈemmens."]] } },
      },
      {
        name: "Old Occitan", wojak: "p3_occitan", flag: null, speakers: "~1170", scene: "tuscany", loc: [44.0, 2.0, "Southern France"],
        script: "Can vei la lauzeta mover de joi sas alas contra·l rai", scriptLabel: "TROUBADOUR SONG · BERNART DE VENTADORN",
        char: F({ skin: "light", hair: "long", hairColor: "auburn", hat: { type: "flower", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#2e6b4f", color2: "#f2c94c", trim: "#c0392b" }, expression: "smile" }),
        cards: [
          "Troubadours sang love songs in Old Occitan across southern France. Bernart de Ventadorn: when I see the lark beat its wings for joy against the sun's rays.",
          "European love poetry as we know it started with them. Occitan is still spoken in southern France, but by far fewer people.",
        ],
        audio: { sim: { model: "ca_ES-upc_ona-medium", scale: 1.1, words: [["Can", "kan"], ["vei", "vej"], ["la", "la"], ["lauzeta", "lawˈzeta"], ["mover", "muˈver"], ["de", "de"], ["joi", "dʒɔj"], ["sas", "sas"], ["alas", "ˈalas"], ["contra·l", "ˈkontral"], ["rai.", "raj."]] } },
      },
      {
        name: "Old French", wojak: "p3_french", flag: null, speakers: "~1100", scene: "village", loc: [48.85, 2.35, "Northern France"],
        script: "Carles li reis, nostre emperere magnes, set anz tuz pleins ad estet en Espaigne", scriptLabel: "THE SONG OF ROLAND",
        char: { skin: "pale", hair: "short", hairColor: "brown", beard: true, beardColor: "#4a3020", hat: { type: "crown", color: "#d9b13b", color2: "#1f4e8c" }, outfit: { type: "coat", color: "#1f3a7a", inner: "#d9b13b" }, expression: "neutral" },
        cards: [
          "The Song of Roland, around 1100: Charles the king, our great emperor, has been in Spain for seven full years.",
          "French still sounded its final consonants: tuz was said like 'toots'. English borrowed thousands of words from this French after 1066.",
        ],
        audio: { sim: { model: "fr_FR-tom-medium", scale: 1.1, words: [["Carles", "ˈtʃarləs"], ["li", "li"], ["reis,", "rejs,"], ["nostre", "ˈnɔstrə"], ["emperere", "empəˈrɛrə"], ["magnes,", "ˈmaɲəs,"], ["set", "sɛt"], ["anz", "ants"], ["tuz", "tuts"], ["pleins", "plejns"], ["ad", "að"], ["estet", "esˈteθ"], ["en", "en"], ["Espaigne.", "esˈpaɲə."]] } },
      },
      {
        name: "Mozarabic", wojak: "p3_mozarabic", flag: null, speakers: "~1050", scene: "arabia", loc: [37.88, -4.78, "Al-Andalus, Spain"],
        script: "Garid boš, ay yermanellaš, kom kontenir a meu male", scriptLabel: "A KHARJA, WRITTEN IN ARABIC LETTERS",
        char: F({ skin: "olive", hair: "long", hairColor: "black", hat: { type: "headscarf", color: "#1f6f8b", color2: "#f2c94c" }, outfit: { type: "dress", color: "#1f6f8b", color2: "#f2c94c", trim: "#c0392b" }, earrings: "#d9b13b", expression: "neutral" }),
        cards: [
          "A Romance language spoken by Christians in Muslim Spain and written in Arabic letters. This verse ends a love poem: tell me, little sisters, how can I hold back my pain?",
          "These verses, called kharjas, are some of the oldest lines in any Spanish-like language.",
        ],
        audio: { sim: { model: "es_ES-davefx-medium", scale: 1.1, words: [["Garid", "ɡaˈrid"], ["boš,", "boʃ,"], ["ay", "aj"], ["yermanellaš,", "jermaˈneʎaʃ,"], ["kom", "kom"], ["kontenir", "konteˈnir"], ["a", "a"], ["meu", "mew"], ["male?", "ˈmale?"]] } },
      },
      {
        name: "Early Japanese", wojak: "p3_japanese", flag: null, speakers: "~1000 AD", scene: "hills", loc: [35.0, 135.77, "Kyoto, Japan"],
        script: "いろはにほへと ちりぬるを", scriptFont: "IPAPGothic", scriptSize: 54,
        char: F({ skin: "light", hair: "long", hairColor: "black", outfit: { type: "coat", color: "#9b1d4a", inner: "#f2c94c" }, expression: "neutral" }),
        cards: [
          "The Iroha, a poem from around 1000 AD that uses every kana sign exactly once: even the brightest blossoms scatter in the end.",
          "Back then h was said like a soft f, and even earlier like p. That is why the sign for pa is just ha with a little circle.",
        ],
        audio: { sim: { model: "it_IT-paola-medium", scale: 1.6, words: [["iro", "ˈiro"], ["fa", "ɸa"], ["nifofeto", "niɸoˈɸeto"], ["tirinuru", "tiriˈnuru"], ["wo.", "wo."]] } },
      },
      {
        name: "Old Church Slavonic", wojak: "p3_slavonic", flag: null, speakers: "~863", scene: "caucasus", loc: [41.1, 23.0, "Thessaloniki & Moravia"],
        script: "Отьче нашь, иже ѥси на небесехъ", scriptLabel: "THE LORD'S PRAYER",
        char: { skin: "light", hair: "bald", hairColor: "grey", beard: true, beardColor: "#8a8a8a", outfit: { type: "wrap", color: "#1d1d1d", color2: "#3a3a3a", trim: "#d9b13b" }, expression: "neutral" },
        cards: [
          "Written down in the 860s by the brothers Cyril and Methodius, missionaries to the Slavs. Our Father, who art in heaven.",
          "Their followers created the Cyrillic alphabet, named after Cyril, now used for Russian, Ukrainian, Bulgarian, Serbian and more.",
        ],
        audio: { sim: { model: "ru_RU-denis-medium", scale: 1.1, words: [["Otĭče", "ˈotʲtʃe"], ["našĭ,", "naʃʲ,"], ["iže", "ˈiʒe"], ["jesi", "ˈjesi"], ["na", "na"], ["nebesechŭ.", "nebeˈsexu."]] } },
      },
      {
        name: "Old High German", wojak: "p3_german", flag: null, speakers: "~830", scene: "forest", loc: [50.55, 9.68, "Fulda, Germany"],
        script: "Ik gihorta ðat seggen, ðat sih urhettun ænon muotin", scriptLabel: "THE HILDEBRANDSLIED",
        char: { skin: "pale", hair: "long", hairColor: "brown", beard: true, beardColor: "#5a3b22", outfit: { type: "tunic", color: "#5b3a29", trim: "#9a9a9a" }, expression: "neutral" },
        cards: [
          "The Hildebrandslied, the oldest heroic poem in German: I heard it told that two warriors met in single combat.",
          "German was splitting from English through a sound shift: English water, that and pipe became German Wasser, das and Pfeife.",
        ],
        audio: { sim: { model: "de_DE-thorsten-medium", scale: 1.1, words: [["Ik", "ik"], ["gihorta", "ɡiˈhoːrta"], ["ðat", "θat"], ["seggen,", "ˈseɡɡen,"], ["ðat", "θat"], ["sih", "sih"], ["urhettun", "urˈhettun"], ["ænon", "ˈeːnon"], ["muotin.", "ˈmuotin."]] } },
      },
      {
        name: "Old Irish", wojak: "ancient3", flag: null, speakers: "~800", scene: "moorland", loc: [53.3, -7.5, "Ireland"],
        script: "Messe ocus Pangur Bán, cechtar nathar fria shaindán", scriptLabel: "PANGUR BÁN",
        char: { skin: "pale", hair: "short", hairColor: "auburn", outfit: { type: "wrap", color: "#6b4a2b", color2: "#3b2a16", trim: "#c8a165" }, expression: "smile" },
        cards: [
          "Pangur Bán, written by an Irish monk in the 800s about his cat: I and Pangur Bán, each of us two at his special task.",
          "Old Irish is the ancestor of Irish, Scottish Gaelic and Manx, and the Celtic language with the oldest large written literature.",
        ],
        audio: { sim: { model: "cy_GB-gwryw_gogleddol-medium", scale: 1.1, words: [["Messe", "ˈmʲesʲe"], ["ocus", "ˈoɡus"], ["Pangur", "ˈpaŋɡur"], ["Bán,", "baːn,"], ["cechtar", "ˈkʲeχtar"], ["nathar", "ˈnaθar"], ["fria", "ˈfʲrʲiə"], ["shaindán.", "ˈhanʲdaːn."]] } },
      },
      {
        name: "Middle Chinese", wojak: "p3_chinese", flag: null, speakers: "~750", scene: "hills", loc: [34.27, 108.95, "Chang'an, China"],
        script: "床前明月光 疑是地上霜", scriptFont: "Noto Serif TC", scriptSize: 60,
        char: F({ skin: "light", hair: "bun", hairColor: "black", outfit: { type: "coat", color: "#f4f1e8", inner: "#1f4e8c" }, expression: "smile" }),
        cards: [
          "Li Bai's Quiet Night Thought, about 750 AD, the poem every Chinese child learns: before my bed, bright moonlight, like frost upon the ground.",
          "Cantonese kept old sounds Mandarin lost, like the t at the end of 月 (moon): Cantonese jyut, Mandarin yuè.",
        ],
        audio: { sim: { model: "zh_CN-huayan-medium", scale: 1.7, words: [["dʐjaŋ", "dʐjaŋ"], ["dzen", "dzen"], ["mjæŋ", "mjæŋ"], ["ŋjwɔt", "ŋjwɔt"], ["kwaŋ,", "kwaŋ,"], ["ŋi", "ŋi"], ["dʑje", "dʑje"], ["di", "di"], ["dʑjaŋ", "dʑjaŋ"], ["ʂjaŋ.", "ʂjaŋ."]] } },
      },
      {
        name: "Coptic", wojak: "p3_coptic", flag: null, speakers: "~400 AD", scene: "arabia", loc: [30.05, 31.23, "Egypt"],
        script: "Ⲡⲉⲛⲓⲱⲧ ⲉⲧϧⲉⲛ ⲛⲓⲫⲏⲟⲩⲓ", scriptFont: "Noto Sans Coptic", scriptSize: 54,
        char: { skin: "brown", hair: "short", hairColor: "black", beard: true, outfit: { type: "wrap", color: "#f4f1e8", color2: "#8a6a3b", trim: "#1f4e8c" }, expression: "neutral" },
        cards: [
          "The last stage of the language of the pharaohs, written with Greek letters plus a few from Egyptian. The Lord's Prayer: our Father who art in heaven.",
          "It stopped being spoken day to day around the 1600s, but Egyptian Christians still use it in church, and it helped Champollion read hieroglyphs.",
        ],
        audio: { sim: { model: "ar_JO-kareem-medium", scale: 1.1, words: [["Peniōt", "peniˈoːt"], ["etḫen", "etˈxen"], ["niphēoui.", "nipʰeˈwi."]] } },
      },
    ],
  },
  // ------------------------------------------------------------------ 12
  ancient4: {
    title: "Extinct Languages Simulated by AI (Part 4)",
    part: "",
    layout: "story",
    counterLabel: "last heard",
    sim: true,
    simVoices: "Finnish for Livonian, Romanian for Dalmatian, Icelandic for Norn, English for Cornish and Massachusett, Welsh for Cumbric, Brazilian Portuguese for Old Tupi, German for Crimean Gothic, Spanish for Taíno",
    simLimits: "some details are educated guesses even among experts: Taíno and Crimean Gothic survive only as words written down by Europeans, Massachusett is known from 1600s spellings, and the Cumbric link to the sheep-counting numbers is a popular theory, not a certainty",
    simTexts: "the Livonian anthem, the Lord's Prayer in Dalmatian as recorded from Tuone Udaina, the Orkney Norn Lord's Prayer (about 1700), Dolly Pentreath's famous words, the Lord's Prayer in John Eliot's 1663 Massachusett Bible, the Lord's Prayer in Old Tupi by José de Anchieta, Busbecq's Crimean Gothic word list, Taíno words borrowed into English, and the northern English sheep-counting numbers",
    items: [
      {
        name: "Livonian", wojak: "p4_livonian", flag: null, speakers: "2013", scene: "baltic", loc: [57.6, 22.0, "Courland coast, Latvia"],
        script: "Min izāmō, min sindimō", scriptLabel: "THE LIVONIAN ANTHEM",
        char: F({ skin: "pale", hair: "braids", hairColor: "blonde", hat: { type: "headscarf", color: "#1f4e8c", color2: "#f4f1e8" }, outfit: { type: "dress", color: "#f4f1e8", color2: "#1f4e8c", trim: "#1f6f3f" }, expression: "neutral" }),
        cards: [
          "A Finnic language of Latvia's coast, cousin of Finnish and Estonian. Its last native speaker, Grizelda Kristiņa, died in 2013 aged 103.",
          "This line is from the Livonian anthem: my fatherland, my birthplace. A few hundred people are learning it again today.",
        ],
        audio: { sim: { model: "fi_FI-harri-medium", scale: 1.2, words: [["Min", "min"], ["izāmō,", "ˈizaːmoː,"], ["min", "min"], ["sindimō.", "ˈsindimoː."]] } },
      },
      {
        name: "Dalmatian", wojak: "p4_dalmatian", flag: null, speakers: "1898", scene: "adriatic", loc: [45.03, 14.57, "Krk, Croatia"],
        script: "Tuota nuester, che te sante intel cil, sait santificuot el naun tuo", scriptLabel: "THE LORD'S PRAYER",
        char: { skin: "olive", hair: "short", hairColor: "grey", mustache: true, beardColor: "#9a9a9a", outfit: { type: "coat", color: "#3a3a3a", inner: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "A Romance language of Croatia's coast, somewhere between Latin and Italian. Our Father, who art in heaven, hallowed be thy name.",
          "Its last speaker, Tuone Udaina, died in 1898 in a road-building explosion. A linguist had written down his words just in time.",
        ],
        audio: { sim: { model: "ro_RO-mihai-medium", scale: 1.1, words: [["Tuota", "ˈtwɔta"], ["nuester,", "ˈnwɛster,"], ["che", "ke"], ["te", "te"], ["sante", "ˈsante"], ["intel", "ˈintel"], ["cil,", "tʃil,"], ["sait", "sajt"], ["santificuot", "santifiˈkwɔt"], ["el", "el"], ["naun", "nawn"], ["tuo.", "ˈtuo."]] } },
      },
      {
        name: "Norn", wojak: "p4_norn", flag: null, speakers: "~1800", scene: "faroe", loc: [60.3, -1.3, "Shetland & Orkney"],
        script: "Favor i ir i chimrie, Helleur ir i nam thite", scriptLabel: "THE LORD'S PRAYER · ORKNEY, ABOUT 1700",
        char: { skin: "pale", hair: "short", hairColor: "auburn", beard: true, beardColor: "#7a3b1c", outfit: { type: "tunic", color: "#3a4a6b", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "The Norse language of Orkney and Shetland, left by the Vikings. Written down around 1700: Father ours who art in heaven, hallowed be thy name.",
          "It faded out by about 1850, but Shetland dialect still keeps hundreds of Norn words, like peerie, small.",
        ],
        audio: { sim: { model: "is_IS-bui-medium", scale: 1.1, words: [["Favor", "ˈfavor"], ["i", "i"], ["ir", "ir"], ["i", "i"], ["chimrie,", "ˈçimri,"], ["Helleur", "ˈhɛlør"], ["ir", "ir"], ["i", "i"], ["nam", "nam"], ["thite.", "ˈtite."]] } },
      },
      {
        name: "Cornish", wojak: "p4_cornish", flag: null, speakers: "1777", scene: "wales", loc: [50.1, -5.53, "Mousehole, Cornwall"],
        script: "Me ne vidn cewsel Sawznek!", scriptLabel: "DOLLY PENTREATH",
        char: F({ skin: "pale", hair: "bun", hairColor: "grey", hat: { type: "bonnet", color: "#f4f1e8" }, outfit: { type: "dress", color: "#3a3a3a", color2: "#f4f1e8", trim: "#7a1f1f" }, expression: "neutral" }),
        cards: [
          "Dolly Pentreath, often called the last native speaker of Cornish, died in 1777. Her famous words: I will not speak English!",
          "She probably wasn't truly the last, and Cornish has since been revived: a few thousand people speak it again.",
        ],
        audio: { sim: { model: "en_US-amy-medium", scale: 1.15, words: [["Me", "meː"], ["ne", "nə"], ["vidn", "vɪdn"], ["cewsel", "ˈkɛʊzəl"], ["Sawznek!", "ˈsawznek!"]] } },
      },
      {
        name: "Massachusett", wojak: "p4_massachusett", flag: null, speakers: "~1800", scene: "forest", loc: [42.3, -71.1, "Massachusetts, USA"],
        script: "Nooshun kesukqut, quttianatamunach koowesuonk", scriptLabel: "THE LORD'S PRAYER · ELIOT BIBLE, 1663",
        char: { skin: "brown", hair: "long", hairColor: "black", outfit: { type: "wrap", color: "#8a5a2b", color2: "#3b2a16", trim: "#c0392b" }, expression: "neutral" },
        cards: [
          "In 1663 the first Bible printed in the Americas was in Massachusett, an Algonquian language. Our Father in heaven, hallowed be thy name.",
          "It stopped being spoken in the 1800s, but the Wampanoag people reawakened it in the 1990s, and children speak it again.",
        ],
        audio: { sim: { model: "en_US-lessac-high", scale: 1.1, words: [["Nooshun", "ˈnuːʃən"], ["kesukqut,", "kəˈsəkʷət,"], ["quttianatamunach", "kʷətiˌanataˈmənatʃ"], ["koowesuonk.", "kuːˈwesuənk."]] } },
      },
      {
        name: "Old Tupi", wojak: "p4_tupi", flag: null, speakers: "~1700", scene: "amazon", loc: [-23.0, -45.0, "Coast of Brazil"],
        script: "Oré rub, ybakype tekoar, imoeté pyramo nde rera toikó", scriptLabel: "THE LORD'S PRAYER · ANCHIETA",
        char: { skin: "tan", hair: "long", hairColor: "black", hat: { type: "feathers", color: "#c0392b", color2: "#f2c94c" }, outfit: { type: "bare" }, necklace: "#f4f1e8", expression: "neutral" },
        cards: [
          "Old Tupi was spoken along the coast of Brazil. Jesuits wrote its grammar and this Lord's Prayer in the 1500s: our Father in heaven, hallowed be thy name.",
          "English got jaguar, piranha and tapioca from it, through Portuguese. A descendant, Nheengatu, is still spoken in the Amazon.",
        ],
        audio: { sim: { model: "pt_BR-faber-medium", scale: 1.1, words: [["Oré", "oˈɾe"], ["rub,", "ɾub,"], ["ybakype", "ɨβaˈkɨpe"], ["tekoar,", "tekoˈaɾ,"], ["imoeté", "imoeˈte"], ["pyramo", "pɨˈɾamo"], ["nde", "ne"], ["rera", "ˈɾeɾa"], ["toikó.", "tojˈko."]] } },
      },
      {
        name: "Crimean Gothic", wojak: "p4_crimean", flag: null, speakers: "~1560", scene: "caucasus", loc: [44.6, 34.0, "Crimea"],
        script: "broe · plut · schuuester · stul · hus · brunna", scriptLabel: "WRITTEN DOWN BY BUSBECQ",
        char: { skin: "light", hair: "long", hairColor: "blonde", beard: true, beardColor: "#9a6b2f", outfit: { type: "tunic", color: "#6b3a2a", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "In the 1560s the diplomat Ogier de Busbecq met two men from Crimea and wrote down about 80 words of their Germanic language.",
          "Bread, blood, sister, seat, house, spring: broe, plut, schuuester, stul, hus, brunna. Sound familiar?",
        ],
        audio: { sim: { model: "de_DE-thorsten-medium", scale: 1.15, words: [["broe,", "broː,"], ["plut,", "plut,"], ["schuuester,", "ˈʃwester,"], ["stul,", "stuːl,"], ["hus,", "huːs,"], ["brunna.", "ˈbruna."]] } },
      },
      {
        name: "Taíno", wojak: "p4_taino", flag: null, speakers: "~1550", scene: "hawaii", loc: [18.7, -70.2, "Hispaniola"],
        script: "hurakán · kanoa · hamaka · barbakoa · tabako", scriptLabel: "TAÍNO WORDS",
        char: { skin: "brown", hair: "long", hairColor: "black", outfit: { type: "bare" }, necklace: "#f2c94c", facepaint: "lines", paintColor: "#c0392b", expression: "neutral" },
        cards: [
          "Taíno was spoken across the Caribbean when Columbus arrived in 1492. Within a few generations it was gone.",
          "But you speak it every day: hurricane, canoe, hammock, barbecue and probably tobacco all come from Taíno.",
        ],
        audio: { sim: { model: "es_ES-davefx-medium", scale: 1.15, words: [["hurakán,", "uɾaˈkan,"], ["kanoa,", "kaˈnoa,"], ["hamaka,", "aˈmaka,"], ["barbakoa,", "baɾbaˈkoa,"], ["tabako.", "taˈbako."]] } },
      },
      {
        name: "Cumbric", wojak: "p4_cumbric", flag: null, speakers: "~1100", scene: "moorland", loc: [54.6, -3.0, "Cumbria, England"],
        script: "yan · tan · tethera · methera · pimp", scriptLabel: "SHEEP-COUNTING NUMBERS",
        char: { skin: "pale", hair: "short", hairColor: "brown", beard: true, beardColor: "#5a3b22", outfit: { type: "wrap", color: "#6b6b4a", color2: "#3b3b2a", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "A Celtic language of northern England and southern Scotland, close to Welsh. It died out around 1100.",
          "Shepherds there kept counting sheep with yan, tan, tethera, methera, pimp: one to five. Many think these are its last echo.",
        ],
        audio: { sim: { model: "cy_GB-gwryw_gogleddol-medium", scale: 1.15, words: [["yan,", "jan,"], ["tan,", "tan,"], ["tethera,", "ˈtɛθəra,"], ["methera,", "ˈmɛθəra,"], ["pimp.", "pɪmp."]] } },
      },
    ],
  },
  ancient5: {
    title: "Extinct Languages Simulated by AI (Part 5)",
    part: "",
    layout: "story",
    counterLabel: "dated to",
    sim: true,
    simVoices: "Spanish for Charrúa, American English for Beothuk, German for Polabian, Indonesian for Kenaboi, Icelandic for Old English, Dutch for Old Saxon, Persian for Avestan, Hindi for Vedic Sanskrit, Arabic for Ugaritic, Turkish for Sumerian",
    simLimits: "Beothuk, Charrúa and Kenaboi survive only as word lists written down by outsiders, with no full sentences, so even experts can only guess how they sounded; Polabian is read from its German-style spelling; Khitan and Xianbei, also requested, are left out because nobody can read Khitan aloud yet and almost nothing of Xianbei survives",
    simTexts: "Charrúa numbers recorded by Teodoro Vilardebó, Beothuk numbers from W. E. Cormack's list (from Shanawdithit), the Polabian Lord's Prayer as written down by Christian Hennig von Jessen, two Kenaboi words from the word lists published by Skeat and Blagden in 1906, the opening of King Alfred's preface to Pastoral Care, the opening of the Heliand, the Ashem Vohu prayer, the first verse of the Rigveda, a line from the Baal Cycle, and the opening of the Instructions of Shuruppak",
    items: [
      {
        name: "Charrúa", wojak: "p5_charrua", flag: null, speakers: "1800s", scene: "grassland", loc: [-32.5, -56.0, "Uruguay"],
        script: "yú · sam · detí · bétum · guaroj", scriptLabel: "ONE, TWO, THREE, FOUR … TEN",
        char: { skin: "brown", hair: "long", hairColor: "black", hat: { type: "headband", color: "#c0392b" }, outfit: { type: "wrap", color: "#8a5a2b", color2: "#3b2a16", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "You asked for it! The Charrúa people lived on the plains of Uruguay. Only a few word lists of their language were ever written down.",
          "One, two, three, four: yú, sam, detí, bétum. Ten is guaroj, from guar, hand. It died out in the 1800s, with scattered reports of speakers much later.",
        ],
        audio: { sim: { model: "es_ES-davefx-medium", scale: 1.15, words: [["yú,", "ˈʝu,"], ["sam,", "sam,"], ["detí,", "deˈti,"], ["bétum,", "ˈbetum,"], ["guaroj.", "ɡwaˈɾox."]] } },
      },
      {
        name: "Beothuk", wojak: "p5_beothuk", flag: null, speakers: "1829", scene: "forest", loc: [49.0, -56.0, "Newfoundland, Canada"],
        script: "yaseek · adzeich · shendeek · dabseek · ninezeek", scriptLabel: "ONE TO FIVE · CORMACK'S LIST",
        char: F({ skin: "tan", hair: "long", hairColor: "black", facepaint: "lines", paintColor: "#b5432a", outfit: { type: "wrap", color: "#b5432a", color2: "#7a2a1a", trim: "#f4f1e8" }, expression: "neutral" }),
        cards: [
          "The Beothuk of Newfoundland painted themselves with red ochre. Shanawdithit, the last known Beothuk, died in 1829.",
          "About 400 words were written down, but not one full sentence. One to five: yaseek, adzeich, shendeek, dabseek, ninezeek.",
        ],
        audio: { sim: { model: "en_US-amy-medium", scale: 1.15, words: [["yaseek,", "jəˈsiːk,"], ["adzeich,", "ˈadzeɪtʃ,"], ["shendeek,", "ʃɛnˈdiːk,"], ["dabseek,", "dabˈsiːk,"], ["ninezeek.", "ˈnɪnəziːk."]] } },
      },
      {
        name: "Polabian", wojak: "p5_polabian", flag: null, speakers: "~1700", scene: "village", loc: [52.97, 11.15, "Wendland, Germany"],
        script: "Nôße Wader, ta toy giß wa Nebisgáy, Sjungta woarda Tügí Geima", scriptLabel: "THE LORD'S PRAYER · HENNIG",
        char: { skin: "pale", hair: "short", hairColor: "brown", hat: { type: "flatcap", color: "#3a3a3a" }, outfit: { type: "coat", color: "#4a3a2a", inner: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "A Slavic language spoken in northern Germany, cousin of Polish. Around 1700 a pastor wrote down its Lord's Prayer: our Father in heaven, holy be thy name.",
          "Its last native speaker, Emerentz Schultze, died in 1756. Only a few hundred words and a few short texts survive.",
        ],
        audio: { sim: { model: "de_DE-thorsten-medium", scale: 1.1, words: [["Nôße", "ˈnoːsə"], ["Wader,", "ˈvadɐ,"], ["ta", "ta"], ["toy", "tɔɪ"], ["giß", "jɪs"], ["wa", "va"], ["Nebisgáy,", "ˈneːbɪsjaɪ,"], ["Sjungta", "ˈsjʊŋta"], ["woarda", "ˈvoːarda"], ["Tügí", "ˈtyːji"], ["Geima.", "ˈjaɪma."]] } },
      },
      {
        name: "Kenaboi", wojak: "p5_kenaboi", flag: null, speakers: "1800s", scene: "andaman", loc: [2.6, 102.1, "Negeri Sembilan, Malaysia"],
        script: "mambu · par", scriptLabel: "WHITE · WATER",
        char: { skin: "brown", hair: "curly", hairColor: "black", outfit: { type: "wrap", color: "#2f6b3a", color2: "#1d4426", trim: "#f2c94c" }, expression: "neutral" },
        cards: [
          "A mystery language of the Malaysian jungle. All we have are about 250 words in three short lists, two of them collected by a British official in the 1800s.",
          "White was mambu and water was par. Nobody knows where these words came from, or what family the language belonged to.",
        ],
        audio: { sim: { model: "id_ID-news_tts-medium", scale: 1.2, words: [["mambu,", "ˈmambu,"], ["par.", "par."]] } },
      },
      {
        name: "Old English", wojak: "p5_oldenglish", flag: null, speakers: "~890", scene: "moorland", loc: [51.06, -1.31, "Winchester, England"],
        script: "Ælfred kyning hāteð grētan Wǣrferð biscep his wordum luflīce ond frēondlīce", scriptLabel: "KING ALFRED'S LETTER",
        char: { skin: "pale", hair: "long", hairColor: "auburn", mustache: true, beardColor: "#7a3b1c", hat: { type: "crown", color: "#d9b13b", color2: "#7a1f1f" }, outfit: { type: "tunic", color: "#7a1f1f", trim: "#d9b13b" }, expression: "neutral" },
        cards: [
          "King Alfred the Great opens a letter to his bishops: King Alfred sends greetings to Bishop Wærferth, with loving and friendly words.",
          "In the same letter he complains that hardly anyone in England can still read Latin, so he has books translated into English.",
        ],
        audio: { sim: { model: "is_IS-steinn-medium", scale: 1.1, words: [["Ælfred", "ˈælfred"], ["kyning", "ˈkyniŋɡ"], ["hāteð", "ˈhaːteθ"], ["grētan", "ˈɡreːtan"], ["Wǣrferð", "ˈwæːrferθ"], ["biscep", "ˈbiʃop"], ["his", "his"], ["wordum", "ˈwordum"], ["luflīce", "ˈluvliːtʃe"], ["ond", "ond"], ["frēondlīce.", "ˈfreːondliːtʃe."]] } },
      },
      {
        name: "Old Saxon", wojak: "p5_oldsaxon", flag: null, speakers: "~830", scene: "hills", loc: [52.0, 8.5, "Saxony, Germany"],
        script: "Manega uuârun, thea sia iro môd gespuon, that sia bigunnun uuord godes", scriptLabel: "THE HELIAND",
        char: { skin: "light", hair: "long", hairColor: "blonde", mustache: true, beardColor: "#9a6b2f", outfit: { type: "tunic", color: "#2f5a35", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "The Heliand is a 6,000-line poem telling the life of Jesus as if he were a Saxon warlord. There were many whose minds urged them to begin telling the word of God.",
          "Old Saxon is the ancestor of Low German, still spoken in northern Germany, but this form of it has been gone for nearly a thousand years.",
        ],
        audio: { sim: { model: "nl_NL-ronnie-medium", scale: 1.1, words: [["Manega", "ˈmaneɣa"], ["uuârun,", "ˈwaːrun,"], ["thea", "θea"], ["sia", "sia"], ["iro", "iro"], ["môd", "moːd"], ["gespuon,", "ɣeˈspuon,"], ["that", "θat"], ["sia", "sia"], ["bigunnun", "biˈɣunnun"], ["uuord", "word"], ["godes.", "ˈɣodes."]] } },
      },
      {
        name: "Avestan", wojak: "p5_avestan", flag: null, speakers: "~1000 BC", scene: "zagros", loc: [36.0, 62.0, "Greater Iran"],
        script: "ašəm vohū vahištəm astī, uštā astī, uštā ahmāi, hyat ašāi vahištāi ašəm", scriptLabel: "THE ASHEM VOHU PRAYER",
        char: { skin: "olive", hair: "long", hairColor: "black", beard: true, beardColor: "#2a2a2a", hat: { type: "turban", color: "#f4f1e8", color2: "#e8e2d0" }, outfit: { type: "robe", color: "#f4f1e8", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "The language of the Zoroastrian scriptures, passed down by memory for centuries before it was written. Truth is the best good. It is happiness.",
          "Nobody has spoken it for well over two thousand years, but Zoroastrian priests in Iran and India still recite this prayer every day.",
        ],
        audio: { sim: { model: "fa_IR-amir-medium", scale: 1.1, words: [["ašəm", "ˈaʃəm"], ["vohū", "voˈhuː"], ["vahištəm", "vaˈhiʃtəm"], ["astī,", "ˈastiː,"], ["uštā", "ˈuʃtaː"], ["astī,", "ˈastiː,"], ["uštā", "ˈuʃtaː"], ["ahmāi,", "ahˈmaːi,"], ["hyat", "hjat"], ["ašāi", "aˈʃaːi"], ["vahištāi", "vaˈhiʃtaːi"], ["ašəm.", "ˈaʃəm."]] } },
      },
      {
        name: "Vedic Sanskrit", wojak: "p5_vedic", flag: null, speakers: "~1200 BC", scene: "himalaya", loc: [31.0, 75.0, "Punjab"],
        script: "अग्निमीळे पुरोहितं यज्ञस्य देवमृत्विजम्", scriptFont: "Noto Serif Devanagari", scriptSize: 54, scriptLabel: "THE RIGVEDA, VERSE ONE",
        char: { skin: "brown", hair: "bun", hairColor: "black", beard: true, beardColor: "#2a2a2a", outfit: { type: "wrap", color: "#e8892b", color2: "#f4f1e8", trim: "#d9b13b" }, expression: "neutral" },
        cards: [
          "The first line of the Rigveda, more than 3,000 years old: I praise Agni, the household priest, the god of the sacrifice.",
          "Its 10,000 verses were passed down by memory, sound by sound. It is older than Classical Sanskrit, which grew out of it.",
        ],
        audio: { sim: { model: "hi_IN-rohan-medium", scale: 1.15, words: [["agnim", "ˈaɡnim"], ["īḷe", "ˈiːɭeː"], ["purohitaṃ", "puroːˈhitam"], ["yajñasya", "jadʒˈɲasja"], ["devam", "ˈdeːvam"], ["ṛtvijam.", "ˈritvidʒam."]] } },
      },
      {
        name: "Ugaritic", wojak: "p5_ugaritic", flag: null, speakers: "~1300 BC", scene: "arabia", loc: [35.6, 35.78, "Ugarit, Syria"],
        script: "𐎚𐎈𐎎𐎟𐎀𐎍𐎛𐎊𐎐𐎟𐎁𐎓𐎍", scriptFont: "Noto Sans Ugaritic", scriptSize: 64, scriptLabel: "THE BAAL CYCLE",
        char: { skin: "tan", hair: "long", hairColor: "black", beard: true, beardColor: "#1d1d1d", hat: { type: "headband", color: "#7a1f1f" }, outfit: { type: "robe", color: "#1f4e8c", trim: "#d9b13b" }, expression: "neutral" },
        cards: [
          "The port city of Ugarit wrote with an alphabet of just 30 letters, pressed into clay. Its myths tell of the storm god Baal.",
          "Message of mightiest Baal, word of the mightiest of heroes. The city was destroyed around 1185 BC, and its tablets were found in 1928.",
        ],
        audio: { sim: { model: "ar_JO-kareem-medium", scale: 1.15, words: [["taḥmu", "ˈtaħmu"], ["ʾalʾiyāni", "ʔalʔiˈjaːni"], ["baʿli,", "ˈbaʕli,"], ["hawatu", "ˈhawatu"], ["ʾaliyi", "ʔaˈlijji"], ["qarradīma.", "qarraˈdiːma."]] } },
      },
      {
        name: "Sumerian", wojak: "p5_sumerian", flag: null, speakers: "~2500 BC", scene: "arabia", loc: [31.78, 45.5, "Shuruppak, Iraq"],
        script: "ud re-a ud sud-ra re-a, gi re-a gi bad-ra re-a, mu re-a mu sud-ra re-a", scriptLabel: "INSTRUCTIONS OF SHURUPPAK",
        char: { skin: "tan", hair: "bald", hairColor: "black", beard: true, beardColor: "#1d1d1d", outfit: { type: "wrap", color: "#f4f1e8", color2: "#8a6a3b", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "One of the oldest pieces of literature in the world: a father giving advice to his son. In those days, in those far-off days.",
          "In those nights, in those distant nights, in those years, in those far-off years. Sumerian was written for 3,000 years but has no known relatives at all.",
        ],
        audio: { sim: { model: "tr_TR-dfki-medium", scale: 1.15, words: [["ud", "ud"], ["re-a", "ˈrea"], ["ud", "ud"], ["sud-ra", "ˈsudra"], ["re-a,", "ˈrea,"], ["gi", "ɡi"], ["re-a", "ˈrea"], ["gi", "ɡi"], ["bad-ra", "ˈbadra"], ["re-a,", "ˈrea,"], ["mu", "mu"], ["re-a", "ˈrea"], ["mu", "mu"], ["sud-ra", "ˈsudra"], ["re-a.", "ˈrea."]] } },
      },
    ],
  },
  ancient6: {
    title: "Extinct Languages Simulated by AI (Part 6)",
    part: "",
    layout: "story",
    counterLabel: "written around",
    sim: true,
    simVoices: "Mexican Spanish for Classical Nahuatl, Indonesian for Old Javanese, European Portuguese for Galician-Portuguese, Kazakh for Middle Mongolian, German for Middle High German, Spanish for Old Spanish, Hungarian for Old Hungarian, Ukrainian for Old East Slavic, Georgian for Classical Armenian, Hindi for Pali",
    simLimits: "these are older forms of languages that are still alive today in a changed form, so nobody speaks them like this anymore; details such as the vowels of Middle Mongolian and the old Slavic short vowels are educated guesses",
    simTexts: "the opening of the Nican Mopohua (1649), the motto line from Mpu Tantular's Sutasoma, Martin Codax's Ondas do mar de Vigo, the opening of the Secret History of the Mongols, the opening of the Nibelungenlied, a line from the Cantar de mio Cid, the Funeral Sermon and Prayer, the opening of the Primary Chronicle, the first sentence written in the Armenian alphabet (Proverbs 1:2), and the first verse of the Dhammapada",
    items: [
      {
        name: "Classical Nahuatl", wojak: "p6_nahuatl", flag: null, speakers: "1649", scene: "sierra", loc: [19.43, -99.13, "Mexico City"],
        script: "Nican mopohua, motecpana, in quenin yancuican huey tlamahuiçoltica monexiti", scriptLabel: "NICAN MOPOHUA, 1649",
        char: { skin: "brown", hair: "long", hairColor: "black", hat: { type: "feathers", color: "#1f8a5a", color2: "#d9b13b" }, outfit: { type: "wrap", color: "#f4f1e8", color2: "#c0392b", trim: "#1f8a5a" }, expression: "neutral" },
        cards: [
          "The language of the Aztec capital. After the Spanish conquest it was written in Latin letters, and thousands of documents survive. Here it is told and set in order how, by a great miracle, she appeared.",
          "About 1.7 million people speak Nahuatl today. English got chocolate, tomato and avocado from it.",
        ],
        audio: { sim: { model: "es_MX-ald-medium", scale: 1.1, words: [["Nican", "ˈnikan"], ["mopohua,", "moˈpowa,"], ["motecpana,", "moˈtekpana,"], ["in", "in"], ["quenin", "ˈkenin"], ["yancuican", "jaŋˈkwikan"], ["huey", "wej"], ["tlamahuiçoltica", "tlamawisolˈtika"], ["monexiti.", "moˈneʃiti."]] } },
      },
      {
        name: "Old Javanese", wojak: "p6_javanese", flag: null, speakers: "~1365", scene: "bougainville", loc: [-7.55, 112.38, "Majapahit, Java"],
        script: "Bhinnêka tunggal ika, tan hana dharma mangrwa", scriptLabel: "SUTASOMA · MPU TANTULAR",
        char: { skin: "tan", hair: "bun", hairColor: "black", mustache: true, beardColor: "#1d1d1d", hat: { type: "headband", color: "#d9b13b" }, outfit: { type: "wrap", color: "#7a1f1f", color2: "#3b1a1a", trim: "#d9b13b" }, expression: "neutral" },
        cards: [
          "The literary language of the Majapahit empire, full of Sanskrit words. Written by the poet Mpu Tantular: different, yet one. There is no duality in truth.",
          "Those first words, Bhinneka Tunggal Ika, are the national motto of Indonesia, printed on its coat of arms.",
        ],
        audio: { sim: { model: "id_ID-news_tts-medium", scale: 1.15, words: [["Bhinnêka", "binˈneka"], ["tunggal", "ˈtuŋɡal"], ["ika,", "ˈika,"], ["tan", "tan"], ["hana", "ˈhana"], ["dharma", "ˈdarma"], ["mangrwa.", "ˈmaŋrwa."]] } },
      },
      {
        name: "Galician-Portuguese", wojak: "p6_galician", flag: null, speakers: "~1250", scene: "adriatic", loc: [42.24, -8.72, "Vigo, Galicia"],
        script: "Ondas do mar de Vigo, se vistes meu amigo! E ai Deus, se verrá cedo!", scriptLabel: "MARTIN CODAX",
        char: F({ skin: "light", hair: "long", hairColor: "brown", outfit: { type: "dress", color: "#1f4e8c", color2: "#f4f1e8", trim: "#d9b13b" }, expression: "neutral" }),
        cards: [
          "The language of medieval love songs, sung even at the court of Castile. Waves of the sea of Vigo, have you seen my love? Oh God, will he come soon?",
          "It later split into two languages that are still alive: Galician and Portuguese.",
        ],
        audio: { sim: { model: "pt_PT-tugão-medium", scale: 1.1, words: [["Ondas", "ˈondas"], ["do", "du"], ["mar", "maɾ"], ["de", "de"], ["Vigo,", "ˈviɡo,"], ["se", "se"], ["vistes", "ˈvistes"], ["meu", "mew"], ["amigo!", "aˈmiɡo!"], ["E", "e"], ["ai", "aj"], ["Deus,", "dews,"], ["se", "se"], ["verrá", "veˈra"], ["cedo!", "ˈtsedo!"]] } },
      },
      {
        name: "Middle Mongolian", wojak: "p6_mongolian", flag: null, speakers: "~1240", scene: "steppe", loc: [47.2, 102.8, "Karakorum, Mongolia"],
        script: "Činggis qahan-u huǰa'ur de'ere tenggeri-eče ǰaya'atu töreksen Börte Čino aǰu'u", scriptLabel: "THE SECRET HISTORY OF THE MONGOLS",
        char: { skin: "light", hair: "braids", hairColor: "black", mustache: true, beardColor: "#1d1d1d", hat: { type: "furhat", color: "#7a1f1f", color2: "#8a6a3b" }, outfit: { type: "coat", color: "#1f4e8c", inner: "#d9b13b" }, expression: "neutral" },
        cards: [
          "The Secret History of the Mongols tells the life of Genghis Khan. The origin of Genghis Khan: there was a blue-grey wolf, born with his destiny from Heaven above.",
          "The Mongol original was lost. It survives only because someone spelled every word out in Chinese characters.",
        ],
        audio: { sim: { model: "kk_KZ-issai-high", scale: 1.15, words: [["Činggis", "ˈtʃiŋɡis"], ["qahan-u", "qaˈhanu"], ["huǰa'ur", "huˈdʒaur"], ["de'ere", "deˈere"], ["tenggeri-eče", "teŋɡeriˈetʃe"], ["ǰaya'atu", "dʒaˈjaːtu"], ["töreksen", "ˈtøreksen"], ["Börte", "ˈbørte"], ["Čino", "ˈtʃino"], ["aǰu'u.", "aˈdʒuː."]] } },
      },
      {
        name: "Middle High German", wojak: "p6_mhg", flag: null, speakers: "~1200", scene: "alps", loc: [48.2, 16.37, "Austria"],
        script: "Uns ist in alten mæren wunders vil geseit von helden lobebæren, von grôzer arebeit", scriptLabel: "THE NIBELUNGENLIED",
        char: { skin: "pale", hair: "long", hairColor: "blonde", outfit: { type: "tunic", color: "#3a4a6b", trim: "#c8a165" }, expression: "neutral" },
        cards: [
          "The Nibelungenlied, a tale of dragon-slaying Siegfried and bloody revenge. In old tales we are told many wonders, of praiseworthy heroes, of great hardship.",
          "Nobody speaks German like this anymore. Over the centuries it turned into modern German.",
        ],
        audio: { sim: { model: "de_DE-thorsten-medium", scale: 1.1, words: [["Uns", "uns"], ["ist", "ɪst"], ["in", "ɪn"], ["alten", "ˈaltən"], ["mæren", "ˈmɛːrən"], ["wunders", "ˈvʊndərs"], ["vil", "fɪl"], ["geseit", "ɡəˈseɪt"], ["von", "fɔn"], ["helden", "ˈhɛldən"], ["lobebæren,", "ˈloːbəbɛːrən,"], ["von", "fɔn"], ["grôzer", "ˈɡroːsər"], ["arebeit.", "ˈarəbeɪt."]] } },
      },
      {
        name: "Old Spanish", wojak: "p6_oldspanish", flag: null, speakers: "~1200", scene: "tuscany", loc: [41.65, -3.69, "Burgos, Spain"],
        script: "De los sos oios tan fuertemientre llorando, tornava la cabeça e estávalos catando", scriptLabel: "CANTAR DE MIO CID",
        char: { skin: "olive", hair: "short", hairColor: "black", mustache: true, beardColor: "#1d1d1d", outfit: { type: "tunic", color: "#8a8a8a", trim: "#7a1f1f" }, expression: "neutral" },
        cards: [
          "The Song of my Cid, the oldest surviving epic in Spanish. Weeping so hard from his eyes, he turned his head and stood looking at them.",
          "Back then the c with a tail was said ts, and j was said like the s in pleasure. Those sounds are gone from modern Spanish.",
        ],
        audio: { sim: { model: "es_ES-davefx-medium", scale: 1.1, words: [["De", "de"], ["los", "los"], ["sos", "sos"], ["oios", "ˈoʒos"], ["tan", "tan"], ["fuertemientre", "fweɾteˈmjentɾe"], ["llorando,", "ʎoˈɾando,"], ["tornava", "toɾˈnaβa"], ["la", "la"], ["cabeça", "kaˈbetsa"], ["e", "e"], ["estávalos", "esˈtaβalos"], ["catando.", "kaˈtando."]] } },
      },
      {
        name: "Old Hungarian", wojak: "p6_hungarian", flag: null, speakers: "~1192", scene: "grassland", loc: [47.5, 19.0, "Hungary"],
        script: "Latiatuc feleym zumtuchel, mic vogmuc. Isa, pur es chomuv uogmuc.", scriptLabel: "THE FUNERAL SERMON",
        char: { skin: "light", hair: "bald", hairColor: "brown", outfit: { type: "robe", color: "#1d1d1d", trim: "#8a8a8a" }, expression: "neutral" },
        cards: [
          "The oldest surviving text in Hungarian, a sermon read at a funeral. Do you see with your own eyes, my brothers, what we are? Behold, we are dust and ashes.",
          "Hungarian is still alive, but every Hungarian student has to study this text, because nobody speaks like this anymore.",
        ],
        audio: { sim: { model: "hu_HU-imre-medium", scale: 1.1, words: [["Latiatuc", "ˈlaːcaːtuk"], ["feleym", "ˈfɛlɛim"], ["zumtuchel,", "ˈsymtykhɛl,"], ["mic", "mik"], ["vogmuc.", "ˈvoɟmuk."], ["Isa,", "ˈiʃa,"], ["pur", "pur"], ["es", "ɛʃ"], ["chomuv", "ˈxomuv"], ["uogmuc.", "ˈvoɟmuk."]] } },
      },
      {
        name: "Old East Slavic", wojak: "p6_eastslavic", flag: null, speakers: "~1113", scene: "village", loc: [50.45, 30.52, "Kyiv"],
        script: "Се повѣсти времяньныхъ лѣтъ, откуду есть пошла руская земля", scriptLabel: "THE PRIMARY CHRONICLE",
        char: { skin: "pale", hair: "long", hairColor: "grey", beard: true, beardColor: "#9a9a9a", outfit: { type: "robe", color: "#1d1d1d", trim: "#d9b13b" }, expression: "neutral" },
        cards: [
          "Written by monks in Kyiv about 900 years ago. These are the tales of bygone years: where the land of the Rus came from.",
          "It is the common ancestor of Ukrainian, Russian and Belarusian, which all grew apart from it.",
        ],
        audio: { sim: { model: "uk_UA-oleksa-high", scale: 1.1, words: [["Се", "se"], ["повѣсти", "poˈvʲesti"], ["времяньныхъ", "vreˈmʲanʲnɪxə"], ["лѣтъ,", "ˈlʲetə,"], ["откуду", "ˈotkudu"], ["есть", "ˈjestʲ"], ["пошла", "poʃˈla"], ["руская", "ˈruskaja"], ["земля.", "zemˈlʲa."]] } },
      },
      {
        name: "Classical Armenian", wojak: "p6_armenian", flag: null, speakers: "405", scene: "caucasus", loc: [40.16, 44.29, "Vagharshapat, Armenia"],
        script: "Ճանաչել զիմաստութիւն եւ զխրատ, իմանալ զբանս հանճարոյ", scriptFont: "Noto Serif Armenian", scriptSize: 50, scriptLabel: "THE FIRST SENTENCE IN THE ARMENIAN ALPHABET",
        char: F({ skin: "olive", hair: "long", hairColor: "black", hat: { type: "headscarf", color: "#7a1f1f", color2: "#d9b13b" }, outfit: { type: "dress", color: "#7a1f1f", color2: "#f4f1e8", trim: "#d9b13b" }, expression: "neutral" }),
        cards: [
          "In 405 the monk Mesrop Mashtots invented the Armenian alphabet. The first sentence he wrote with it was from the Bible: to know wisdom and instruction, to understand words of insight.",
          "Nobody speaks Classical Armenian at home anymore, but the Armenian Church still uses it, and modern Armenian grew out of it.",
        ],
        audio: { sim: { model: "ka_GE-natia-medium", scale: 1.1, words: [["Čanačʿel", "tʃanaˈtʃel"], ["zimastutʿiwn", "zimastuˈtiwn"], ["ew", "ew"], ["zxrat,", "ˈzxrat,"], ["imanal", "imaˈnal"], ["zbans", "zbans"], ["hančaroy.", "hantʃaˈroj."]] } },
      },
      {
        name: "Pali", wojak: "p6_pali", flag: null, speakers: "~29 BC", scene: "andaman", loc: [7.87, 80.65, "Sri Lanka"],
        script: "Manopubbaṅgamā dhammā, manoseṭṭhā manomayā", scriptLabel: "THE DHAMMAPADA, VERSE ONE",
        char: F({ skin: "brown", hair: "bald", hairColor: "black", outfit: { type: "wrap", color: "#e8892b", color2: "#c0661b", trim: "#d9b13b" }, expression: "neutral" }),
        cards: [
          "The language of the oldest Buddhist scriptures, first written down in Sri Lanka around 29 BC. Mind comes before all things. Mind is their chief, they are made by mind.",
          "Nobody grows up speaking Pali, but monks in Sri Lanka, Thailand and Myanmar still chant it every day.",
        ],
        audio: { sim: { model: "hi_IN-priyamvada-medium", scale: 1.15, words: [["Manopubbaṅgamā", "manoːpubbaŋˈɡamaː"], ["dhammā,", "ˈdʰammaː,"], ["manoseṭṭhā", "manoːˈseʈʈʰaː"], ["manomayā.", "manoːˈmajaː."]] } },
      },
    ],
  },
  whistled: {
    title: "Whistled Languages be like",
    part: "",
    layout: "story",
    counterLabel: "whistled",
    items: [
      {
        name: "Whistled Yoruba", wojak: "w_yoruba", flag: "ng", speakers: "Yoruba", scene: "savanna", loc: [7.4, 3.9, "South-west Nigeria"],
        char: { skin: "dark", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#1f6f3f", vest: "#f2c94c" }, expression: "open" },
        cards: [
          "Yoruba is a tonal language: every syllable has a high, mid or low pitch. A whistle can copy those pitches, so words survive without a voice.",
          "This whistler is greeting people working ahead of him: ará iwájú, ẹ kú iṣẹ́ o, well done with the work.",
        ],
        noCaptions: true,
        audio: { seq: ["File:Yoruba-whistle-language-slow.ogg", "File:Yoruba-whistle-language-fast.ogg"], repeat: 2, voice: "keep" },
      },
      {
        name: "Sfyria", wojak: "w_sfyria", flag: "gr", speakers: "Greek", scene: "hills", loc: [38.0, 24.5, "Antia, Euboea, Greece"],
        char: { skin: "olive", hair: "short", hairColor: "grey", mustache: true, beardColor: "#8a8a8a", outfit: { type: "shirt", color: "#f4f1e8", vest: "#3a3a3a" }, expression: "open" },
        cards: [
          "In the village of Antia in Greece, shepherds whistled Greek to each other across the hills.",
          "It is called Sfyria, from the Greek word for whistle. Only a handful of whistlers are left.",
        ],
        audio: { file: "Sfiria Antia.wav", ranges: [[0, 5.9], [8.0, 14.8]], voice: "keep" }, // whistling only; the low-pitched parts are speech
      },
      {
        name: "Whistled Occitan", wojak: "w_aas", flag: "fr", speakers: "Occitan", scene: "alps", loc: [42.97, -0.4, "Aas, French Pyrenees"],
        char: { skin: "pale", hair: "short", hairColor: "brown", hat: { type: "beret", color: "#1d1d1d" }, outfit: { type: "shirt", color: "#f4f1e8", vest: "#6b3a2a" }, expression: "open" },
        cards: [
          "In the Pyrenees village of Aas, shepherds whistled Occitan across the valley. By the 1950s almost nobody could do it anymore.",
          "Today it is being revived and taught again. Hello is adishatz, here whistled by Philippe Biu.",
        ],
        audio: { seq: ["File:Occitan whistle-adishatz.ogv", "File:LL-Q117707514 (oci-whistled)-Philippe (Yug)-adiu.wav", "File:Occitan whistle-petit.ogv", "File:LL-Q117707514 (oci-whistled)-Philippe (Yug)-Aas.wav"], repeat: 2, voice: "keep" },
      },
      {
        name: "Bird Language", wojak: "w_kuskoy", flag: "tr", speakers: "Turkish", scene: "caucasus", loc: [40.73, 38.6, "Kuşköy, Turkey"],
        char: { skin: "light", hair: "short", hairColor: "black", mustache: true, beardColor: "#1d1d1d", hat: { type: "flatcap", color: "#3a3a3a" }, outfit: { type: "coat", color: "#4a3a2a", inner: "#f4f1e8" }, expression: "open" },
        cards: [
          "In Kuşköy, a village in Turkey's Black Sea mountains, people whistle whole conversations in Turkish. They call it kuş dili, bird language.",
          "UNESCO put it on its list of heritage in urgent need of protection in 2017, because mobile phones are replacing it.",
        ],
        noCaptions: true,
        audio: { seq: ["File:VOA Learning English - UN- Technology Threatens Whistled Language in Turkey (crop).ogg"], repeat: 2, voice: "keep" },
      },
      {
        name: "Silbo Gomero", wojak: "w_silbo", flag: "es", speakers: "Spanish", scene: "canary", loc: [28.1, -17.2, "La Gomera, Canary Islands"],
        char: { skin: "olive", hair: "short", hairColor: "grey", outfit: { type: "shirt", color: "#f4f1e8", vest: "#7a2e2e" }, hat: { type: "widehat", color: "#d9b26f", color2: "#7a2e2e" }, expression: "open" },
        cards: [
          "On the Spanish island of La Gomera, a whole island can talk in whistles. Silbo Gomero turns Spanish into just two whistled vowels and four consonants.",
          "A strong whistle carries for kilometres across the ravines. Since 1999 every child on the island learns it at school.",
        ],
        audio: { file: "Silbo.ogg", start: 0, voice: "keep" },
      },
    ],
  },

  // ------------------------------------------------------------------ whistled, part 2 (clips from YouTube, used with the uploaders' permission; build_whistled2.py)
  whistled2: {
    title: "Whistled Languages be like",
    part: "Part 2",
    layout: "story",
    counterLabel: "whistled",
    items: [
      {
        name: "Chinantec", wojak: "w_chinantec", flag: "mx", speakers: "Chinantec", scene: "overcast", loc: [17.9, -96.6, "Sierra Norte, Oaxaca, Mexico"],
        char: { skin: "brown", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#f4f1e8", vest: "#2f6b3f" }, expression: "open" },
        cards: [
          "In the mountains of Oaxaca, Mexico, Chinantec men whistle whole conversations through the fog. Chinantec has seven tones, and the whistle copies them.",
          "A real exchange between two neighbours: 'What are you going to do tomorrow, at noon?' 'Nothing, I will take a nap.' Then a man on a mountain road calls his neighbour to fetch his brother.",
          "Linguist Mark Sicoli recorded both. Young Chinantecs now reach each other by phone, and the whistle is fading.",
        ],
        audio: { file: "cache/whistled2/src/mazatec_2_part3_1.mp4", ranges: [[76.3, 88.8], [0.2, 4.2]], voice: "keep" },
      },
      {
        name: "Hmong", wojak: "w_hmong", flag: "la", speakers: "Hmong", scene: "tropical", loc: [20.4, 104.0, "Houaphan, northern Laos"],
        char: { skin: "tan", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#1d1d1d", vest: "#c0392b" }, expression: "open" },
        cards: [
          "In the forests of northern Laos, Hmong farmers whistle to each other across the valleys. Hmong has up to eight tones, so a whistle can carry the words.",
          "Boys used to whistle love poems to girls at night. The parents heard a bird; the girl heard a proposal.",
          "What you hear: 'I am going to the farm.' 'Going to the farm, why do you ask?' 'I am going to wander around my rice fields.' Only a few older men still do it.",
        ],
        audio: { file: "cache/whistled2/src/hmong.mp4", ranges: [[429.0, 445.5]], voice: "keep" },
      },
      {
        name: "Pirahã", wojak: "w_piraha", flag: "br", speakers: "Pirahã", scene: "amazon", loc: [-7.3, -62.3, "Maici River, Amazonas, Brazil"],
        char: { skin: "brown", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#f2c94c", vest: "#f2c94c" }, expression: "open" },
        cards: [
          "The Pirahã of the Amazon are famous for having no words for numbers. They can also say one sentence five ways: spoken, hummed, shouted, sung, or whistled.",
          "Whistling is for the hunt: both hands stay on the bow, and the monkeys do not run from a whistle. This hunter tells his companion: 'There is a monkey, right above us.' 'I see him.' 'He will be very fast.'",
          "Only eight consonants and three vowels, fewer than 800 speakers, and one of the most argued-about languages on Earth. Its tones carry so much that a whistle keeps the meaning.",
        ],
        audio: { file: "cache/whistled2/src/piraha.mp4", ranges: [[10.8, 27.3]], voice: "keep" },
      },
      {
        name: "Wayãpi", wojak: "w_wayapi", flag: "gf", speakers: "Wayãpi", scene: "amazon", loc: [3.2, -52.3, "Camopi, French Guiana"],
        char: { skin: "brown", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#c0392b", vest: "#c0392b" }, expression: "open" },
        cards: [
          "The Wayãpi of French Guiana can imitate every animal in the forest, and they whistle their own language too. Here two hunters plan a trip.",
          "'oloota ole ia lupi' means: let us leave together by canoe. 'elapa alaa' means: I take my rifle. The whistle keeps the melody of the spoken words.",
          "The clip comes from the work of Julien Meyer, the linguist who has recorded more whistled languages than anyone, together with the Wayãpi themselves.",
        ],
        audio: { file: "cache/whistled2/src/wayapi_2.mp4", ranges: [[21.0, 35.5]], voice: "keep" },
      },
    ],
  },

  // ------------------------------------------------------------------ nearly extinct, part 2 (Wikitongues videos on Commons; build_extinct2.py)
  extinct2: {
    title: "Hear These Languages Before They Disappear",
    part: "Part 2",
    layout: "story",
    counterLabel: "speakers",
    items: [
      {
        name: "Ainu", wojak: "e_ainu", flag: "jp", speakers: "a handful", scene: "forest", loc: [43.1, 142.5, "Hokkaido, Japan"],
        char: F({ skin: "light", hair: "long", hairColor: "grey", outfit: { type: "robe", color: "#1f2a44", trim: "#f4f1e8" }, expression: "neutral" }),
        cards: [
          "Ainu is the language of the indigenous people of Hokkaido, in northern Japan. It is related to nothing else on Earth, not even Japanese.",
          "For a century Japan banned it in schools and pushed the Ainu to assimilate. Today only a handful of elderly native speakers are left.",
          "Japan recognised the Ainu as an indigenous people only in 2019. Night classes and radio lessons are trying to bring the language back.",
        ],
        audio: { file: "cache/extinct2/src/ainu.webm", start: 2.0, voice: "f" },
      },
      {
        name: "Miyako", wojak: "e_miyako", flag: "jp", speakers: "elderly only", scene: "tropical", loc: [24.8, 125.3, "Miyako Islands, Okinawa"],
        char: { skin: "tan", hair: "short", hairColor: "grey", outfit: { type: "shirt", color: "#9bc4e2", vest: "#9bc4e2" }, expression: "smile" },
        cards: [
          "Miyako is spoken on a few small islands south of Okinawa. Tokyo called it a dialect for a century, but a Japanese speaker cannot understand a word of it.",
          "It has sounds no other Japanese-family language has, like syllables made of nothing but a long 'ss' or 'ff'.",
          "Almost every fluent speaker is over sixty. The children of the islands grew up with standard Japanese on TV and in school.",
        ],
        audio: { file: "cache/extinct2/src/miyako.webm", start: 2.0, voice: "m" },
      },
      {
        name: "Mendriq", wojak: "e_mendriq", flag: "my", speakers: "~250", scene: "tropical", loc: [5.2, 101.8, "Kelantan, Malaysia"],
        char: F({ skin: "brown", hair: "long", hairColor: "black", outfit: { type: "wrap", color: "#8e5a2b", color2: "#f2c94c", trim: "#c0392b" }, expression: "neutral" }),
        cards: [
          "Mendriq is spoken by a few hundred Orang Asli, the first peoples of the Malay peninsula, deep in the forests of Kelantan.",
          "It belongs to the Aslian family, cousins of Khmer and Vietnamese, and it was there thousands of years before Malay arrived.",
          "Resettlement villages and Malay schools mean the children answer their grandparents in Malay. Linguists only started recording it properly in the 2010s.",
        ],
        audio: { file: "cache/extinct2/src/mendriq.webm", start: 1.0, voice: "f" },
      },
      {
        name: "Lehali", wojak: "e_lehali", flag: "vu", speakers: "~200", scene: "hawaii", loc: [-13.55, 167.3, "Ureparapara, Vanuatu"],
        char: F({ skin: "dark", hair: "bun", hairColor: "black", outfit: { type: "dress", color: "#2a9d8f", color2: "#f2a541", trim: "#f2a541" }, expression: "smile" }),
        cards: [
          "Vanuatu has more languages per person than any country on Earth: over a hundred for three hundred thousand people.",
          "Lehali is one of them, spoken on a single volcanic island in the north by around two hundred people.",
          "Its neighbours speak different languages a few kilometres away. Bislama, the national creole, is slowly replacing all of them.",
        ],
        audio: { file: "cache/extinct2/src/lehali.webm", start: 2.0, voice: "f" },
      },
      {
        name: "Kensiu", wojak: "e_kensiu", flag: "my", speakers: "~300", scene: "tropical", loc: [5.8, 100.9, "Baling, Kedah, Malaysia"],
        char: { skin: "dark", hair: "short", hairColor: "black", outfit: { type: "shirt", color: "#2f6b3f", vest: "#2f6b3f" }, expression: "neutral" },
        cards: [
          "Kensiu is spoken in one village in northern Malaysia and a few across the Thai border, by about three hundred people.",
          "Its speakers were nomadic forest foragers within living memory. The language has words for forest life that Malay simply does not have.",
          "Like Mendriq, it is Aslian: the sound of the peninsula before the Malay kingdoms, still alive in one village.",
        ],
        audio: { file: "cache/extinct2/src/kensiu.webm", start: 1.0, voice: "m" },
      },
      {
        name: "Laz", wojak: "e_laz", flag: "tr", speakers: "~20,000", scene: "caucasus", loc: [41.2, 41.5, "Rize and Artvin, Turkey"],
        char: { skin: "olive", hair: "short", hairColor: "black", mustache: true, hat: { type: "headscarf", color: "#1d1d1d", color2: "#1d1d1d" }, outfit: { type: "coat", color: "#3a3a3a", inner: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "Laz is spoken on the Black Sea coast of Turkey. It is a cousin of Georgian, not of Turkish, with consonant clusters that make Turkish speakers give up.",
          "It has never been taught in a Turkish state school and has no official status. UNESCO lists it as definitely endangered.",
          "Most speakers are over fifty. A Laz newspaper, a few singers and an alphabet designed in the 1980s are what keeps it visible.",
        ],
        audio: { file: "cache/extinct2/src/laz.webm", start: 2.0, voice: "m" },
      },
      {
        name: "Northern Sami", wojak: "e_sami", flag: "no", speakers: "~20,000", scene: "arctic", loc: [69.0, 23.0, "Kautokeino, Norway"],
        char: F({ skin: "pale", hair: "braids", hairColor: "brown", hat: { type: "beanie", color: "#1f4e8c", color2: "#c0392b" }, outfit: { type: "tunic", color: "#1f4e8c", color2: "#c0392b", trim: "#f2c94c" }, expression: "neutral" }),
        cards: [
          "The Sámi are the indigenous people of the Arctic north of Norway, Sweden and Finland. Northern Sami is the biggest of their nine languages, with about twenty thousand speakers.",
          "It has hundreds of words for snow, ice and reindeer, and it is related to Finnish, not to Norwegian.",
          "Norway banned it in schools until the 1960s. Today there are Sámi schools, a Sámi parliament and a TV channel, but most of the smaller Sámi languages are nearly gone.",
        ],
        audio: { file: "cache/extinct2/src/sami.webm", start: 2.0, voice: "f" },
      },
      {
        name: "Bildts", wojak: "e_bildts", flag: "nl", speakers: "~6,000", scene: "moorland", loc: [53.3, 5.7, "Het Bildt, Netherlands"],
        char: { skin: "pale", hair: "short", hairColor: "grey", hat: { type: "flatcap", color: "#3a3a3a" }, outfit: { type: "coat", color: "#2c3e50", inner: "#f4f1e8" }, expression: "neutral" },
        cards: [
          "Bildts is spoken on a patch of land in the north of the Netherlands that did not exist five hundred years ago: it was reclaimed from the sea in 1505.",
          "The dyke builders came from Holland, the neighbours spoke Frisian, and their children mixed the two into a language of its own.",
          "About six thousand people still speak it. In 2018 the Dutch government refused to recognise it as a language, which only made the locals prouder of it.",
        ],
        audio: { file: "cache/extinct2/src/bildts.webm", start: 2.0, voice: "m" },
      },
    ],
  },
};
