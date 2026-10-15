# Changes after the owner's review and design brief (2026-10-15)

Each item was tested on the live site; [M] = measured.

## 1. Stories
- The 20 stories were already published (owner's "yes publish"). Owner chose: keep them live, write expanded
  versions of the short ones as **drafts** for review.
- 13 expanded drafts (slug `<story>-expanded`, linked by `bhr_revision_of`): Robert Smalls, Bessie Coleman, Matthew
  Henson, Booker T. Washington, Bass Reeves, Muhammad Ali, Frederick Douglass, George Washington Carver, Ida B. Wells,
  Rosa Parks, Jesse Owens, Hiram Revels, Jack Johnson. 250–330 words each (counting numbers) [M], built only from
  `data/reel-*.json` (facts + notUsed), `publish/reels/*.md` and `data/podcast-ep0*.json`; disputed points labelled;
  extra sources added where podcast facts were used. Text: `website/content/story-expansions-2026-10-15.json`.
- Apply after approval: `BHR_MODE=apply` (or `BHR_ONLY=slug1,slug2`) with `website/scripts/story_expansions.php`.
- The other 7 stories are already 258–279 words.
- Reel links: **no reel URLs exist in the repo**; the owner must provide them (Story details → Related reel URL).

## 2. REST API
`/wp/v2/stories` and `/wp/v2/episodes` [M 200]. As `n8n-automation`: Story draft with featured image + section/domain/
country/era, and a News post draft with featured image + categories, created [M]; publish attempt → 403 [M].

## 3 + design brief. Homepage and layout
- Full-width header (logo 40 px from the left, search + Donate 40 px from the right); one row from 1600 px, two rows
  (logo + tools / menu) from 1024 px, Menu button below 1024 px. Container 1440 px, padding 40/24/16 px; article
  column 720 px.
- Sections 104 px apart (56 px on phones); backgrounds: dark featured story → cream → white → dark map → cream…
- Cards: 12 px radius, soft shadow, lift on hover, 4:3 image cropped from the top (faces), 22 px title with years on
  the same line, 2-line excerpt, gold "Read more" button, equal heights.
- Featured story: image ~60 % width, rounded, text vertically centred.
- Typography: Playfair Display (headings), Source Sans 3 (UI, excerpts, buttons; self-hosted, 29 KB, swap),
  Source Serif 4 for article body; H1 56/40, H2 36/28, card title 22, body 18 / 1.6.
- Gold accent brightened to `#e0a93b` (dark text on it: 7.8:1); outlined secondary buttons.
- Homepage: featured story, Latest, People who changed history, Explore the map (with static map preview image),
  Africa, African American History, Untold stories*, This week*, Podcast, **Who we are** (Harriet Tubman portrait,
  public domain; Our Mission → /about/#mission, About Us), Newsletter. *Hidden while empty (no `untold-stories` tag,
  no key dates yet).
- Screenshots before/after: 1920, 1440, 1024, 390 px. No horizontal scroll at 390 px on 9 page types [M].

## 4. Podcast and Reels
- Episodes 1–3 (drafts, for review): cover, description, chapters (11/9/10), Spotify link, full transcript from the
  scripts (~1,300 words each) [M, rendered server-side]. New field `bhr_chapters`.
- `/videos/`: grid of 19 reel cover stills (Henry "Box" Brown has none); no iframe on load [M]; a YouTube link in a
  story turns its card into click-to-load (youtube-nocookie) once URLs are added.

## 5. Social sharing
Default image `theme/bhr/assets/og-default.jpg` (1200×630, brand colours, monogram) on pages without one; stories share
their 1200×630 crop with the correct `og:image:type` [M]. Twitter/X: summary_large_image. Facebook Sharing Debugger needs
a Facebook login: owner to run https://developers.facebook.com/tools/debug/?q=https://theblackhistoryroom.com/

## 6. Map
Map page HTML 170 KB → 47 KB (10 KB gzipped) [M]; world SVG is a static file (`assets/map/world-110m.svg`, 45 KB
compressed, cached 1 year) fetched only on the map page; countries with stories coloured red and linked
(Mali 1, United States 19) [M]; A–Z list first on phones and as no-JS fallback [M]. Homepage map preview is a static
SVG in `uploads/bhr/`, rebuilt only when the set of countries changes.

## 7. Test story (published, checked, then deleted)
Breadcrumbs, title + years, reading time, APA/MLA citations, Copy button, sources (“Title,” Publisher, URL), image
credit, Ko-fi line, Article + BreadcrumbList schema; after unpublish → 404; then deleted [M]. Discover more checked on
Robert Smalls: 3 cards (same country, then same domain) [M]. Owner display name set to "The Black History Room"
(was the login name in bylines and schema).

## 8. Mobile and speed
390 px: Menu opens/closes, panels open, Donate visible, no horizontal scroll, map list first [M].
Lighthouse 12.8.2 (PageSpeed's API was over its daily quota; same engine run locally):

| Page | Mobile perf / a11y / best | Desktop perf / a11y / best |
| --- | --- | --- |
| Home | 98 / 100 / 100 (LCP 2.2 s) | 100 / 100 / 100 |
| Map | 100 / 100 / 100 | 100 / 100 / 100 |
| Story | 97 / 100 / 100 (LCP 2.6 s) | 100 / 100 / 100 |

SEO 63–66 only because indexing is still switched off. Fixed: footer button contrast (1.85:1 → AA), CSS/JS cache
1 year, 480 px card images for phones.

## 9. Newsletter (free)
Own sign-up form (no third party): consent checkbox, honeypot, 5 per IP per hour; subscribers stored privately in WP
Admin → **Newsletter**, Export CSV. Tested: valid, duplicate, no consent, bad email, bot, rate limit [M]; test entries
deleted. To send later (owner's choice, free tiers): MailerLite (up to 1,000 subscribers) or Brevo (300 emails/day);
import the CSV. The Privacy Policy page must mention the newsletter before launch.

## 10. Search Console
Steps in `SEARCH_CONSOLE.md`.
