# Content model, navigation and map (built 2026-10-15)

Implements `docs/tasks/website-structure-and-map.md` on top of the main brief. Code: `website/mu-plugins/bhr-core*`
(data model, must-use plugin) and `website/theme/bhr/` (display). Both are mounted read-only into the WordPress
container from `/opt/blackhistoryroom/` (see `docker-compose.yml`), so a deploy is: copy the files, clear the page cache.

## Stories

| | |
| --- | --- |
| Post type | `story` ("Stories" in the admin). URL `/story/<slug>/`, all stories `/stories/`. REST: `/wp-json/wp/v2/stories` |
| Section | `african-american-history`, `global-african-history` |
| Domain | 13 subjects, same list for both sections: politics-government, civil-rights-activism, slavery-emancipation, military, science-medicine-invention, business-economics, arts-music-literature, sports, religion, education, women-in-history, exploration, law-justice |
| Country | slug = ISO 3166-1 alpha-2 (`us`, `ml`, `gh`...). Archive `/global-african-history/<iso2>/` |
| Era | before-1500, 16th-century ... 21st-century |
| Tags | normal WordPress tags; `untold-stories`, `timelines`, `myths-vs-facts` feed the homepage / menu |

Fields ("Story details" box under the editor; also REST meta for n8n):
`bhr_full_name`, `bhr_birth_year`, `bhr_death_year` (blank if living; "c. 1818" allowed; "-300" = 300 BCE),
`bhr_event_date` (YYYY-MM-DD, feeds This week), `bhr_sources` (one per line: `Title | Publisher | https://url`),
`bhr_image_credit`, `bhr_reel_url`, `bhr_podcast_url`. The **Excerpt** (about 40 words) is the card summary and deck.
Normal posts still exist for News (`/news/`) with the 13 categories created earlier.

## URLs

| URL | What |
| --- | --- |
| `/african-american-history/` | section page: filters (subject, country, era), A–Z, card grid, pagination (`?bhr_pg=2`) |
| `/african-american-history/<domain>/` | same, filtered by subject |
| `/global-african-history/` | world map + country list, then the section list with filters |
| `/global-african-history/topic/<domain>/` | Global section filtered by subject |
| `/global-african-history/<iso2>/` | country archive |
| `/stories/`, `/topic/<domain>/`, `/era/<era>/`, `/section/<section>/` | other story archives |
| `/videos/`, `/this-week/`, `/sources/`, `/donate/` | Reels & videos, This week, Sources & bibliography, Donate |

## Header and footer
- Logo left ("ROOM" in gold), mega-menu (African American History, Global African History, Special Features with a
  featured story, Resources, About), search, gold **Donate** button (Ko-fi, new tab), always visible incl. phones.
- Mega-menu: buttons with `aria-expanded`, click/tap to open, Escape closes, click outside closes; without JS the panel
  opens on keyboard focus. Phones: everything in the Menu panel as an accordion, search inside the panel.
- Footer: "Support our work" (Ko-fi), Explore links, Donate page; footer menu includes Donate.

## End of every Story
1. **Cite this entry**: APA (default tab), MLA, Chicago, built from author (the organisation unless the author's user
   profile has a last name), publish date, title + years, site name, permalink. Plain text; Copy button (JS, only
   shown when the clipboard is available). "Last updated" shown separately when modified more than a day later.
2. **Sources of the author's information**: `“Title,” Publisher, URL` (links open in a new tab), then image credits.
3. Watch the reel / Listen to the podcast episode buttons when the fields are filled.
4. **Discover more**: 3 cards, same Country first, then same Domain, then same Section.
5. "Support our work on Ko-fi" line.

Tested with design-test stories (removed afterwards): APA output
`The Black History Room. (2026, October 15). Design Test Person 5 (1909–1972). The Black History Room. https://theblackhistoryroom.com/story/design-test-person-5/`,
tabs switch without JS, Discover more order correct.

## Global African History map
- Data: Natural Earth 1:110m admin-0 (public domain) via `world-atlas@2.0.2`, projected once at build time
  (`website/scripts/build_map.mjs`, d3-geo Natural Earth projection) into `theme/bhr/assets/map/world-110m.json`
  (175 shapes, about 115 KB, 43 KB gzipped). Rebuild only if the projection or data must change.
- Rendered by PHP as inline SVG **only on that page**: countries with published stories are links (deep red, gold on
  hover/focus, `aria-label` "Ghana: 2 stories", native tooltip), others are grey and not interactive.
- Country list beside the map (first on phones) with the same links: this is the no-JS and screen-reader path.
- Zoom + / − / Reset: 20 lines of inline JS on that page; no map library, no API key.
- Counts are cached in Redis and cleared when a story's terms or status change.
- Western Sahara is drawn as part of Morocco (one shape, no inner border), as decided by the owner on 2026-10-15
  (`MERGE` in `build_map.mjs`; 175 shapes).

## Seeded stories (2026-10-15): created as drafts, published by the owner's decision the same evening
Built by `website/scripts/build_seed.mjs` (repo data) + `seed_stories.php` (WordPress). Text is the already-checked
reel post text (`publish/reels/<slug>.md`), unchanged; sources and image credits from the same files; cover = the
reel's opening image with its credit from `public/pd/reel-<slug>/credits.json`.

20 stories (Matthew Henson added later the same day): Bass Reeves, Bessie Coleman, Booker T. Washington, Ellen and William Craft, Frederick Douglass,
Garrett Morgan, George Washington Carver, Harriet Tubman, Henry "Box" Brown, Hiram Revels, Ida B. Wells, Jack Johnson,
Jesse Owens, Major Taylor, Mansa Musa (Global / Mali), Muhammad Ali, Robert Smalls, Rosa Parks, Sojourner Truth.
3 podcast episode drafts (1 Douglass, 2 Smalls, 3 Carver), linked to their stories.

To check before publishing each one:
- Robert Smalls (1 paragraph) and Bessie Coleman (2) are short: they come from the pilot reels' short post texts.
- Ellen Craft and Mansa Musa have no birth/death years (not in the reel data); add them with two sources if wanted.
- Sources are mostly names without links; add URLs in the `Title | Publisher | https://url` format.
- Section / domains / era were assigned by me (see `MAP` in `build_seed.mjs`); adjust in the editor.
- Rosa Parks' cover (Gene Herrick, AP, 1956) is recorded as public domain in our credits file; confirm before
  publishing. Mansa Musa's cover is the Catalan Atlas drawing (not a likeness; the caption says so).
- Reel URLs are empty; podcast episodes link to the Spotify show page (no per-episode links in our files) and have no
  transcript yet.
- Matthew Henson was not seeded: there is no `publish/reels/matthew-henson.md` (his post text is only in
  `docs/black-history-room-context.md`).

## Measured (design-test content, then removed)
Lighthouse 12.8.2 on `/`, `/global-african-history/`, a Story page: performance 100, accessibility 100, best
practices 100 on mobile and desktop; LCP 1.5–1.7 s mobile, 0.3–0.4 s desktop; CLS ≤ 0.006. SEO score is limited only
by the intentional `noindex` until launch. No horizontal scrolling at 375 px on 8 page types.
