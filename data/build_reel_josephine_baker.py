"""Builds data/reel-josephine-baker.json: a ~3-minute film-clip reel about Josephine Baker.

Every fact lists at least two sources in "facts". Images: public domain / CC0 only
(see public/pd/reel-josephine-baker/credits.json and clips/clips.json).
Film (public domain on Wikimedia Commons): a 1932 Dutch newsreel of her visit ("Josephine Baker in ons land")
and her dance in Le Pompier des Folies Bergere (1928, medium shots only). Download both to a scratch folder as
onsland.webm and pompier.webm before running cut_clips.py.
Voice: Kokoro am_michael (free).
"""
import json
from pathlib import Path

OUT = Path(__file__).with_name("reel-josephine-baker.json")

ASSETS = {
    "npg1926": "File:Josephine Baker by Stanislaus Julian Walery, 1926, gelatin silver print, from the National Portrait Gallery - NPG-NPG 95 105Baker-000001.jpg",
    "walery30": "File:A portrait of Josephine Baker.jpg",
    "manuel": "File:Joséphine Baker - photo Henri Manuel.jpg",
    "poster30": "File:Louis Gaudin - Casino de Paris - Josephine Baker 1930.jpg",
    "alger44": "File:JBaker Alger 1944.jpg",
    "troops43": "File:\"Miss Josephine Baker, popular stage performer, sings the National Anthem as the finale to the show held in the Municipa - NARA - 531160.jpg",
    "vv49": "File:Portrait of Josephine Baker, Paris LCCN2004662545.jpg",
    "vv51": "File:Portrait of Josephine Baker LCCN2004662546.jpg",
    "vv44": "File:Portrait of Josephine Baker LCCN2004662544.jpg",
    "moise": "File:Josephine Baker in Kasteel Les Milandes J B met zoonje Moise, Bestanddeelnr 912-6517.jpg",
    "tribe64": "File:JosephineBaker1964NL.jpg",
    "rotterdam59": "File:Josephine Baker met haar 10 kinderen bezoekt Rotterdam, Bestanddeelnr 910-5757.jpg",
    "milandes61": "File:Josephine Baker in Kasteel Les Milandes Groepskiek in tuin, Bestanddeelnr 912-6516.jpg",
    "garden61": "File:Afhalen van Josephine Baker in Frankrijk Josephine in haar tuin Les Milandes, Bestanddeelnr 912-6479.jpg",
}

ONS = "File:Josephine Baker in ons land.webm"
POM = "File:Le Pompier des Folies Bergère (1928).webm"
o = lambda start, dur, **k: {"file": "onsland.webm", "commons": ONS, "start": start, "dur": dur, **k}
p = lambda start, dur, **k: {"file": "pompier.webm", "commons": POM, "start": start, "dur": dur, **k}
CLIPS = {
    "walk": o(2, 6),
    "med": o(20, 4),
    "talk1": o(25, 6),
    "talk2": o(31, 4),
    "close": o(37.5, 2.5),
    "dance_coat": p(173.9, 1.6, speed=0.6),
    "dance": p(180.8, 4.0),
}


def V(clip, focus, zoom=(1.0, 1.08), anchor=None):
    return {"kind": "video", "clip": clip, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or (0.5, focus[1]))}


def P(img, focus, zoom=(1.05, 1.15), anchor=None):
    return {"kind": "photo", "image": img, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or focus)}


def C(img, cap):
    return {"kind": "card", "image": img, "caption": cap}


def T(t, s):
    return {"kind": "title", "title": t, "sub": s}


DN = (0.36, 0.3)   # her face in the 1928 dance (4:3 film inside a 16:9 frame)
B = []


def b(id, text, vis, **kw):
    x = {"id": id, "text": text, "visual": vis}
    x.update(kw)
    B.append(x)


b("hook", "She spied on the Nazis for France, with secrets hidden in her sheet music. Then a New York nightclub refused to serve her.",
  P("vv49", (0.5, 0.25), (1.0, 1.06), (0.5, 0.36)), section="hook",
  overlays={"hook": "She spied on the Nazis for France. *Then New York refused to serve her.*"}, captions=False, speed=1.3)
b("name", "Her name was Josephine Baker. This is her on film, in 1932.", V("talk1", (0.5, 0.2), (1.25, 1.32), (0.5, 0.3)), section="who")
b("born", "She was born Freda Josephine McDonald, in St. Louis, Missouri, in 1906. As a child, she cleaned houses for white families.",
  P("manuel", (0.5, 0.3), (1.05, 1.15), (0.5, 0.42)), overlays={"pin": {"label": "St. Louis, Missouri"}}, section="story")
b("riot", "In 1917, at eleven years old, she watched East St. Louis burn, as white mobs attacked Black families.",
  T("1917", "East St. Louis"))
b("married", "She was married at thirteen. By fifteen she had married again, and she kept her husband's name: Baker.",
  P("walery30", (0.5, 0.25), (1.1, 1.2), (0.5, 0.32)))
b("shuffle", "She tried out for Shuffle Along, a hit Black musical on Broadway. Producers turned her down, reportedly as too young, too skinny and too dark. She got in as a dresser, and danced her way into the chorus.",
  P("npg1926", (0.5, 0.42), (1.1, 1.25), (0.5, 0.45)), section="break")
b("paris", "In 1925, at nineteen, she sailed for Paris. On October 2nd she opened in a new all-Black revue, and Paris went wild.",
  C("poster30", "Casino de Paris poster, 1930"), overlays={"stamp": "1925"}, section="paris")
b("folies", "In 1926 she danced at the Folies Bergère, in a skirt made of bananas.", V("dance_coat", DN, (1.0, 1.05), (0.5, 0.36)))
b("dance", "Ernest Hemingway called her the most sensational woman anyone ever saw.", V("dance", DN, (1.0, 1.06), (0.5, 0.36)))
b("star", "She became the most successful American entertainer in France. In 1937 she became a French citizen.",
  V("walk", (0.58, 0.35), (1.0, 1.06), (0.5, 0.4)), overlays={"stamp": "1937"})
b("war", "Then, in 1939, war came. French military intelligence recruited her as a spy.",
  V("med", (0.65, 0.3), (1.0, 1.06), (0.5, 0.38)), overlays={"stamp": "1939"}, section="war")
b("ink", "She wrote secret notes in invisible ink on her sheet music. Others she pinned inside her underwear.",
  V("talk2", (0.5, 0.2), (1.25, 1.32), (0.5, 0.3)))
b("uniform", "She joined the Free French Air Force as an officer, and sang for Allied troops in North Africa.",
  C("alger44", "Algiers, 1944: Josephine Baker in uniform"))
b("medals", "France later gave her the Resistance Medal, the War Cross, and the Legion of Honour.",
  C("troops43", "Singing for the troops, 1943"))
b("stork", "But at home, it was different. In 1951, at New York's Stork Club, she said the staff refused to serve her. Protesters picketed the club.",
  P("vv51", (0.5, 0.28), (1.05, 1.15), (0.5, 0.4)), overlays={"stamp": "1951"}, section="insult")
b("miami", "That same year in Miami Beach, she refused to perform unless Black and white fans could sit together. The club gave in.",
  P("vv44", (0.5, 0.28), (1.05, 1.15), (0.5, 0.4)))
b("march", "In 1963, at the March on Washington, she stood at the microphone in her French uniform and medals. She was the only woman on the official speaker list.",
  T("1963", "March on Washington"), section="march")
b("coretta", "After Martin Luther King was killed, Coretta Scott King reportedly asked her to lead the movement. She said no. Her children were too young to lose their mother.",
  C("rotterdam59", "With her children, Rotterdam, 1959"))
b("tribe", "She had adopted twelve children. She called them her Rainbow Tribe, and raised them in a castle in France.",
  C("tribe64", "The Rainbow Tribe, Amsterdam, 1964"), section="fall")
b("evicted", "But she went broke. In 1969 she was thrown out of her own castle.", C("milandes61", "Les Milandes, 1961"))
b("bobino", "In 1975, with help from Princess Grace of Monaco, she opened a comeback show in Paris. Four days later, she died.",
  C("garden61", "In her garden at Les Milandes, 1961"), section="end")
b("funeral", "More than twenty thousand people came to her funeral, and France gave her full military honors.",
  C("moise", "With her son at Les Milandes, 1961"))
b("pantheon", "In 2021, France placed her in the Panthéon, the first Black woman ever honored there.",
  T("2021", "The Panthéon, Paris"), section="legacy")
b("close", "That was Josephine Baker.", P("vv49", (0.5, 0.25), (1.12, 1.2), (0.5, 0.36)))
b("cta", "Follow The Black History Room for more.", {"kind": "endcard"}, section="cta", captions=False)

S = lambda u: {"url": u}
SOURCES = {
    "WP": S("https://en.wikipedia.org/wiki/Josephine_Baker"),
    "NPS": S("https://www.nps.gov/mamc/learn/historyculture/josephine-baker.htm"),
    "NWHM": S("https://www.womenshistory.org/education-resources/biographies/josephine-baker"),
    "MINDEF": S("https://www.defense.gouv.fr/chemins-memoire/histoire-memoires/personnalites/personnalites-lettre-lettre/josephine-baker"),
    "NARA": S("https://rediscovering-black-history.blogs.archives.gov/2021/12/02/josephine-baker-pantheon"),
    "WW2M": S("https://www.nationalww2museum.org/war/articles/siren-resistance-artistry-and-espionage-josephine-baker"),
    "BRIT": S("https://kids.britannica.com/students/article/Josephine-Baker/312995"),
    "NPR": S("https://www.npr.org/2021/05/23/998962830/shuffle-along-changed-musical-theater-100-years-ago"),
    "NYPL": S("https://www.nypl.org/blog/2018/08/07/joy-out-fire-josephine-baker"),
    "LOC": S("https://blogs.loc.gov/loc/2025/03/josephine-baker-at-the-stork-club-a-night-gone-wrong/"),
    "WLRN": S("https://www.wlrn.org/news/2021-11-23/tribute-to-josephine-baker-coming-to-miami-beach-70-years-after-her-stand-for-civil-rights"),
    "NBC": S("https://www.nbcnews.com/news/nbcblk/josephine-baker-becomes-first-black-woman-honored-paris-panthe-rcna6343"),
    "LACROIX": S("https://www.milandes.com/wp-content/uploads/2021/11/dossier-la-croix-lhebdo-1.pdf"),
    "FILM1": S("https://commons.wikimedia.org/wiki/File:Josephine_Baker_in_ons_land.webm"),
    "FILM2": S("https://commons.wikimedia.org/wiki/File:Le_Pompier_des_Folies_Berg%C3%A8re_(1928).webm"),
}
FACTS = [
    {"beat": "hook", "sources": ["MINDEF", "WW2M", "WP", "LOC"]},
    {"beat": "name", "sources": ["FILM1"]},
    {"beat": "born", "sources": ["WP", "NPS", "NWHM", "MINDEF"], "note": "Age she started working differs (8 vs 12): no age said."},
    {"beat": "riot", "sources": ["WP", "BRIT"]},
    {"beat": "married", "sources": ["WP", "NPS"]},
    {"beat": "shuffle", "sources": ["WP", "NPR", "NYPL"], "note": "Reasons for rejection are a repeated story: 'reportedly'."},
    {"beat": "paris", "sources": ["WP", "MINDEF"]},
    {"beat": "folies", "sources": ["WP", "MINDEF"], "note": "Revue name disputed (La Folie du jour 1926 / Un vent de folie 1927): not said."},
    {"beat": "dance", "sources": ["WP", "FILM2"]},
    {"beat": "star", "sources": ["WP", "MINDEF"], "note": "NPS gives 1936 for citizenship; WP and MinDef give 1937."},
    {"beat": "war", "sources": ["WP", "WW2M", "MINDEF"]},
    {"beat": "ink", "sources": ["MINDEF", "WW2M", "WP"], "note": "Underwear (WP, HNN), not bra (weak sources)."},
    {"beat": "uniform", "sources": ["MINDEF", "WP"], "note": "Enlistment date disputed (1943 vs 1944): not said."},
    {"beat": "medals", "sources": ["MINDEF", "WP"], "note": "Resistance Medal 1946; Legion of Honour and Croix de Guerre 1961: no years said."},
    {"beat": "stork", "sources": ["WP", "LOC"], "note": "Grace Kelly walk-out only in listicles: dropped."},
    {"beat": "miami", "sources": ["WP", "WLRN", "NWHM"]},
    {"beat": "march", "sources": ["WP", "NARA"]},
    {"beat": "coretta", "sources": ["WP", "NPS"], "note": "Secondhand (Jo Bouillon's memoir): 'reportedly'."},
    {"beat": "tribe", "sources": ["WP", "NWHM"], "note": "NWHM counts 13."},
    {"beat": "evicted", "sources": ["WP", "LACROIX"], "note": "WP: lost in 1968; physical eviction March 1969."},
    {"beat": "bobino", "sources": ["WP", "MINDEF", "NPS"]},
    {"beat": "funeral", "sources": ["WP", "NPS"]},
    {"beat": "pantheon", "sources": ["WP", "NARA", "NBC", "MINDEF"]},
]

spec = {
    "id": "reel-josephine-baker",
    "title": "She Spied on the Nazis. New York Refused to Serve Her.",
    "format": "reel", "fps": 30, "width": 1080, "height": 1920,
    "music": {"volume": 0.06},
    "mix": {"targetLufs": -14, "ceilingDbtp": -1.5, "musicUnderVoiceDb": 21, "duckDb": 3, "hookBoostDb": 2},
    "brand": {"page": "The Black History Room", "cta": "Follow The Black History Room for more.", "theme": "bhr"},
    "voice": {"engine": "kokoro", "voice": "am_michael", "speed": 1.2, "leadInSeconds": 0.4, "sectionGapSeconds": 1},
    "pronounce": {"St. Louis": "Saint Lewis", "Folies Bergère": "Folly Bair-zhair", "Panthéon": "Pahn-tay-ohn"},
    "assets": {k: {"commons": v} for k, v in ASSETS.items()},
    "clips": CLIPS,
    "beats": B,
    "sources": SOURCES,
    "facts": FACTS,
}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
text = " ".join(x["text"] for x in B)
print(f"{len(B)} beats, {len(text.split())} words, {len(text)} characters")
