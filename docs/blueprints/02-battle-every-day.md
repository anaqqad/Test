# Blueprint 02: Battle "Every Day" format, premium version

The reference is **Visual History** (@visualhistory4). I analysed the video you supplied, "Invasion of Poland 1939: Every Day on the Map", plus a screenshot of the channel's video list.

You say the channel was monetised within a month. I can't verify that: the channel's analytics aren't visible to me. Every number below is either measured from the file or read off the screenshot, and is labelled as such.

## 1. What the reference does

### Measured from the video file
- 1:06 long, 16:9, 1280×720 at 30 fps as downloaded.
- Music only. I inferred this from the audio: there is no centred voice, and the side channel carries about as much energy as the full mix. Loudness is −13.8 LUFS.
- 56 days (1 Sep to 26 Oct 1939) in about 64 s, so about **0.9 days per second**, at a steady pace.
- **No intro.** The video opens on day 1.

### From the screenshot
| Video | Length | Views | Uploaded |
|---|---|---|---|
| Invasion of Poland | 1:07 | 2.6K | 2 d ago |
| Stalingrad | 1:01 | 3.6K | 7 d ago |
| Leningrad | 1:01 | 1.6K | 11 d ago |
| Jassy–Kishinev | 1:01 | 700 | 12 d ago |
| Second Kharkov | — | — | 12 d ago |

So it uploads roughly every 2–5 days, with videos around 1 minute long.

### Layout
The map is full-frame, with no sidebar:
- **Top-left:** the date as `1939 / 09 / 21`, with a losses table under it (dead, wounded, prisoners per side).
- **Top-right:** a legend of round flag badges, a 100 km scale bar and the channel handle.
- **On the map:**
  - Each side's army strength as a round badge and a big number, which drops as losses mount.
  - Round flag badges as units, crowded along every front with a few inside each territory.
  - City dots with bold labels.
- **Bottom:** a caption bar of one dated sentence, changing about every 4 s (about 14 captions per video).

### Look
- A dark slate basemap with a faint texture.
- Flat territory colours: Germany dark grey, Poland pink, the USSR red.
- A bright sea, and no terrain.

### Packaging
- **Titles:**
  - `[Battle] Every Day [Year] to [Year]`
  - `[Event] [Year]: Every Day on the Map`
- **Thumbnails:** a frame of the video, with the date, counters and badges visible.

## 2. The formula

| Element | What it is |
|---|---|
| Input | A famous WWII battle lasting a few weeks |
| Promise | The whole battle, in one minute |
| Story | The clock running at about 1 day per second |
| Sources of tension | Fronts closing, pockets forming, counters rising |
| Delivery | A short, very high-completion video |
| Output | A cheap, fast, repeatable series (every 2–5 days) |

Why it works:
- **Retention:** one minute of constant change, with the end always in sight.
- **Curiosity:** "how fast did it actually happen?"
- **Reach:** WWII is the largest evergreen history niche, and a 1-minute runtime suits suggested video and Shorts-adjacent viewing.

How it can make money [inference]:
- Long-form videos of about 1 minute earn watch hours slowly. Reaching 4,000 hours takes about 300,000 full views.
- The quick monetisation you report would therefore need either a few breakout videos or Shorts views (10M in 90 days).
- From **1 February 2027**, new applicants need **8,000 watch hours** (YouTube blog). Video length and upload cadence matter more after that.

## 3. Premium upgrades (all built into the engine)

| Area | Reference | Ours |
|---|---|---|
| Terrain | Flat slate texture | **Real hillshaded relief** from elevation tiles (Ardennes, Alps, Carpathians, river valleys), at any zoom |
| Hydrography | Few rivers | **Natural Earth rivers and lakes**, weighted by size: battles turn on the Meuse, Oder, Dnieper and Vistula |
| Movement | Units only | **Animated offensive arrows** that grow along each thrust's path between its dates, then fade |
| Front | Fringe of units | Units, plus a glowing front line |
| Units | Round badges | Round badges drawn in code, **dated per contingent** (for example, US troops appear on the day they landed) |
| Opening | None | **3-second globe cold open** that zooms to the theatre, with the title and a one-line hook |
| Typography | Generic bold sans | The Cinzel and Barlow Condensed system, with gold accents and frosted panels |
| Trust | None visible | Sources in the description; draft banner until checked; neutral captions |
| Audio | Music | Music levelled to −14 LUFS; licence credit written into the description automatically |
| Packaging | Raw frame | Thumbnail still from the same data: the key moment, a highlight ring, 0–4 words |

The JSON fields that switch this on:
```
"style": "warroom", "layout": "full"
map.relief, map.rivers, map.flagShape: "round", map.markerSpacing, map.borders
arrows[], forces[], counters[kind: "table"]
```

Before rendering, fetch the terrain once per video:
```
node scripts/fetch-terrain.mjs <id>
```
The tiles are Terrain Tiles on AWS Open Data. The description must credit them:

> Terrain Tiles (Mapzen/Tilezen) from SRTM, GMTED2010, ETOPO1, EU-DEM (Copernicus)

## 4. Production spec, per video

| Item | Spec |
|---|---|
| Runtime | 60–80 s. Pace of about 0.7–1.2 days per second, slower on decisive days. |
| Intro | Globe, 3 s |
| End card | 6 s |
| Captions | 15–20 events, one every 3–5 s. Each is under 12 words and dated. |
| Arrows | 6–10 main thrusts per battle |
| Losses | A table of killed, wounded and captured. Interpolated between sourced totals, and the description says so. |
| Strength | On-map numbers for each side, from sourced start and end strengths |
| Units | Spacing [56, 15], interior density 0.5, round badges |
| Titles | `The [Battle], Day by Day ([years])`, or `[Battle] [year]: Every Day on the Map` style. Keep our own wording. |
| Thumbnail | Pocket or breakthrough moment, highlight ring, 2–3 words |

## 5. Test slate

| # | Video | Why it was chosen | What it tests |
|---|---|---|---|
| 1 | The Battle of France, Day by Day (1940) | Huge demand. The "sickle cut" and the Dunkirk pocket are perfect map drama. | Baseline, Western Front |
| 2 | The Battle of the Bulge, Day by Day (1944–45) | US audience (highest ad value). The bulge shape is iconic. Terrain matters (the Ardennes). | Does the premium terrain look lift retention? |
| 3 | Operation Bagration, Day by Day (1944) | The biggest German defeat; a dramatic collapse and encirclements. Less covered. | Eastern Front, a less famous topic |
| 4 | The Battle of Berlin, Day by Day (1945) | The end of the war: encirclement, the Elbe link-up, the Reichstag. | Climax story, city-scale zoom |

The data for each comes from research agents. Their sources are listed in each builder under `channel/tools/`.

## 6. Upload plan for the test

- Publish one video every 2–3 days, in the order 2, 1, 4, 3.
- After 14 days, compare CTR, average percentage viewed and suggested traffic.
- Decision rules (my suggestion):
  - **Continue at 2–3 uploads a week** if average viewed is 70% or more on these short videos and suggested traffic is the top source.
  - **Test 2-minute versions** for watch hours if retention holds but impressions stall.
