# n8n → WordPress integration (drafts only)

Prepared and tested 2026-10-15. **No n8n workflow was built and n8n itself was not changed** (brief: prepare only).
The owner adds one credential in n8n (section 3) when the workflow is built.

## 1. Account and what it may do

| | |
| --- | --- |
| WordPress user | `n8n-automation` (ID 2), display name "Newsroom automation" |
| Role | `bhr_automation` = Contributor + `upload_files` |
| Can | create and edit **its own drafts** (Stories, podcast episodes, News posts), set taxonomies and story fields, upload images, set alt text/captions, delete its own drafts |
| Cannot | publish, schedule, edit published posts, edit anyone else's drafts, create taxonomy terms, change settings, log in with a normal password from n8n |
| Auth | WordPress **Application Password** "n8n on srv1998959", stored only in `/opt/blackhistoryroom/.env` as `WP_N8N_USER` / `WP_N8N_APP_PASSWORD` (mode 600). Never in git or chat. |

"Drafts only" is enforced by WordPress itself, not by the workflow: any request with `"status": "publish"` or
`"future"` is rejected with **403**. The owner reviews and publishes in WP Admin.

## 2. Tests run on 2026-10-15 (all passed; test items deleted afterwards)

| # | Request (as `n8n-automation`) | Result |
| --- | --- | --- |
| 1 | `GET /users/me?context=edit` | user `n8n-automation`, role `bhr_automation` |
| 2 | no auth / wrong password | 401 / 401 |
| 3 | create Story draft with section, domain, country, era, years and sources | 201, status `draft`, terms and meta saved |
| 4 | change that draft to `publish`; to `future`; create a new story as `publish` | 403, 403, 403 — still `draft` |
| 5 | upload an image to `/media`, set alt text + caption | 201, saved |
| 6 | set `featured_media` on the draft | saved |
| 7 | read the draft without auth | 401 (hidden) |
| 8 | list own drafts | works |
| 9 | edit the owner's draft (Robert Smalls) | 403 |
| 10 | create a podcast episode draft at `/episodes` with episode number + Spotify URL | 201, `draft` |

## 3. Owner: add the credential in n8n (once)

1. Read the password: open `/opt/blackhistoryroom/.env` with WinSCP (root) and copy the value of
   `WP_N8N_APP_PASSWORD` (with its spaces, they are part of it).
2. n8n → **Credentials → Add credential → "Basic Auth"**. Name: `WordPress BHR (drafts)`.
   User: `n8n-automation`. Password: the value from step 1. Save.
3. In workflows use **HTTP Request** nodes with *Authentication: Generic → Basic Auth → WordPress BHR (drafts)*.
   (n8n's built-in WordPress node only handles normal posts, not our Story type, so HTTP Request is used.)

Use the public URL `https://theblackhistoryroom.com/wp-json/wp/v2/...`. Application Passwords only work over HTTPS;
the public URL goes through Traefik on the same server, so it is fast. (Internal alternative, not needed:
`http://bhr-wordpress/wp-json/...` with header `X-Forwarded-Proto: https` and `Host: theblackhistoryroom.com`.)

**Revoke or rotate:** WP Admin → Users → n8n-automation → Application Passwords → Revoke, or on the VPS
`bash /opt/blackhistoryroom/scripts/wp.sh user application-password list n8n-automation` / `... delete n8n-automation <uuid>`,
then create a new one and update `.env` and the n8n credential.

## 4. Endpoints

Base: `https://theblackhistoryroom.com/wp-json/wp/v2`

| What | Endpoint |
| --- | --- |
| Stories | `POST /stories` create, `POST /stories/<id>` update, `GET /stories?status=draft&author=2&search=...` |
| Podcast episodes | `POST /episodes`, `POST /episodes/<id>` |
| News posts | `POST /posts` (categories by ID, see 5) |
| Images | `POST /media` (binary), then `POST /media/<id>` for `alt_text`, `caption`, `title` |
| Taxonomy lookups | `GET /section`, `/domain`, `/era`, `/country?slug=gh`, `/categories`, `/tags` |
| Check a slug is free | `GET /stories?slug=<slug>&status=draft,publish&context=edit` |

## 5. IDs (stable; still prefer looking up by slug)

**Section:** 16 `african-american-history` · 17 `global-african-history`

**Domain:** 18 politics-government · 19 civil-rights-activism · 20 slavery-emancipation · 21 military ·
22 science-medicine-invention · 23 business-economics · 24 arts-music-literature · 25 sports · 26 religion ·
27 education · 28 women-in-history · 29 exploration · 30 law-justice

**Era:** 31 before-1500 · 32 16th-century · 33 17th-century · 34 18th-century · 35 19th-century · 36 20th-century ·
37 21st-century

**Country:** all 249 ISO 3166-1 countries exist (slug = lower-case alpha-2, e.g. `us` 38, `ml` 39, `gh`, `ng`, `jm`,
`ht`, `br`, `ma`); look the ID up with `GET /country?slug=<iso2>`. Western Sahara is not a separate country on this
site (owner decision). The automation account cannot create terms; a missing one means a wrong code.

**News categories (normal posts):** 1 african-american-history · 2 african-history · 3 civil-rights ·
4 slavery-emancipation · 5 historical-figures · 6 black-women-in-history · 7 science-innovation · 8 military-history ·
9 politics · 10 arts-culture · 11 forgotten-history · 12 black-business · 13 timelines

**Tags** (created on use by an editor): `untold-stories`, `timelines`, `myths-vs-facts`.

## 6. Story fields (`meta` in the JSON)

| Key | Content |
| --- | --- |
| `bhr_full_name` | full name |
| `bhr_birth_year`, `bhr_death_year` | `1839`, `c. 1818`, `-300` (BCE); death blank if living |
| `bhr_event_date` | `YYYY-MM-DD` of the key event (feeds "This week") |
| `bhr_sources` | one per line: `Title \| Publisher \| https://url` — **at least two independent reliable sources** |
| `bhr_image_credit` | e.g. `Library of Congress, Brady-Handy collection. Public domain, via Wikimedia Commons.` |
| `bhr_reel_url`, `bhr_podcast_url` | related video / episode links |

The **excerpt** (about 40 words) is the card text, the deck and the meta description. The title is the person's
name (or the event); years are added automatically on the site and in citations.

Podcast episode fields: `bhr_episode_number` (integer), `bhr_spotify_url`, `bhr_youtube_url`, `bhr_apple_url`,
`bhr_related_posts` (comma-separated story IDs). Excerpt = description, content = transcript.

## 7. Example: create a Story draft

```http
POST /wp-json/wp/v2/stories
Content-Type: application/json
Authorization: Basic (n8n credential)

{
  "title": "Robert Smalls",
  "slug": "robert-smalls",
  "status": "draft",
  "excerpt": "In 1862, an enslaved man stole a Confederate warship and sailed his family to freedom.",
  "content": "<!-- wp:paragraph --><p>…</p><!-- /wp:paragraph -->",
  "section": [16], "domain": [21, 18], "country": [38], "era": [35],
  "meta": {
    "bhr_full_name": "Robert Smalls",
    "bhr_birth_year": "1839", "bhr_death_year": "1915",
    "bhr_event_date": "1862-05-13",
    "bhr_sources": "Robert Smalls | US House of Representatives: History, Art & Archives | https://history.house.gov/People/Detail/21764\nThe Planter: A Strike for Freedom | National Park Service | https://www.nps.gov/",
    "bhr_image_credit": "Library of Congress (Brady-Handy collection). Public domain."
  }
}
```

Image: `POST /wp-json/wp/v2/media` with the file as binary body, headers `Content-Type: image/jpeg` and
`Content-Disposition: attachment; filename=robert-smalls.jpg`; then `POST /media/<id>` with
`{"alt_text": "...", "caption": "Who/what, date. Credit. Licence."}`; then `POST /stories/<story id>` with
`{"featured_media": <media id>}`. JPEG/PNG are stored as WebP automatically (max 2000 px).

Content can use the editorial note styles (Group block classes `is-style-bhr-fact`, `is-style-bhr-interpretation`,
`is-style-bhr-disputed`, `is-style-bhr-legend`; Quote class `is-style-bhr-document`).

## 8. Planned workflow (to build later, on request)

Topic → research → article → **fact check (gate)** → image → SEO fields → n8n → WordPress **draft** → owner review →
owner publishes.

Gates the workflow should apply before calling WordPress: every important claim has two independent reliable
sources; quotes are traceable to a source; disputed points and legends are labelled; images are public domain / CC0
or licensed, with credit, and never AI-generated faces of real people; check the slug is free (no duplicates).
Whatever the workflow does, WordPress will only accept drafts from this account.

## 9. Errors you may see
- `401 rest_not_logged_in` / `incorrect_password`: wrong credential or password revoked.
- `403 rest_cannot_publish` / `rest_cannot_edit`: tried to publish/schedule, or to edit something that is not its own draft.
- `400 rest_invalid_param`: wrong term ID or field type (e.g. `bhr_episode_number` must be a number).
- `429` is only used for `POST /wp-login.php` (login rate limit); the REST API is not rate-limited.

## 10. How it was set up (to repeat on a new server)
```
W="bash /opt/blackhistoryroom/scripts/wp.sh"
$W role create bhr_automation "Automation (drafts only)" --clone=contributor
$W cap add bhr_automation upload_files
$W user create n8n-automation n8n@theblackhistoryroom.com --role=bhr_automation --display_name="Newsroom automation" --porcelain
# Application Password straight into .env, never printed:
P=$($W user application-password create n8n-automation "n8n on srv1998959" --porcelain </dev/null)
printf 'WP_N8N_USER=n8n-automation\nWP_N8N_APP_PASSWORD=%s\n' "$P" >> /opt/blackhistoryroom/.env; unset P
```
Country terms: all ISO 3166-1 countries except Western Sahara were created from `i18n-iso-countries` names
(slug = alpha-2). The podcast REST base is `episodes` (`theme/bhr/inc/podcast.php`).

## 11. Re-test 2026-10-15 (after the redesign)
Story draft with featured image + section/domain/country/era, and a News post draft with featured image + categories
(5, 11) created as `n8n-automation`; publish attempt 403; test items deleted. Episodes also accept `bhr_chapters`
(one chapter per line, "0:00 Welcome").

## 12. Map fields (2026-10-15)
Stories also take: taxonomy `gender` (REST field `gender`, term IDs: woman 290, man 291, group 292) and meta
`bhr_place_name`, `bhr_lat`, `bhr_lng` (decimal degrees as strings, e.g. "32.78", "-79.93"), `bhr_key_year`. A story
without coordinates still appears in lists and filters, just without a pin.
