# WordPress admin guide (owner)

Site: https://theblackhistoryroom.com · Admin: https://theblackhistoryroom.com/wp-admin/

## First login (once)
1. Username and password: `WP_ADMIN_USER` / `WP_ADMIN_PASSWORD` in `/opt/blackhistoryroom/.env` (open it with
   WinSCP as root). Put them in your password manager.
2. **Users → Profile**: set a new strong password, then delete the `WP_ADMIN_PASSWORD` line from `.env`.
   Note: password-reset emails do not work yet (no email set up, see `DNS_SETUP.md`), so keep the password safe.
3. Same page: *Display name*. Citations use the **organisation** ("The Black History Room") as author unless the
   author's profile has a **Last name**; leave first/last name empty to keep the organisation as author.
4. More than 5 wrong logins a minute from one place are blocked for about a minute (HTTP 429). Just wait.

## Review and publish a draft Story (the main job)
**Stories → All stories → Drafts**. 19 drafts are waiting (seeded from the reels); n8n will add more.

In the editor:
1. **Title** = the person's name (or the event). Years are added automatically from the fields.
2. **Text**: the story. Use *Heading 2* for sections (a table of contents appears on long stories). For editorial
   labels, select a block → *Group*, then in the sidebar *Styles* choose **Verified fact**, **Interpretation**,
   **Disputed claim** or **Legend / myth**. For quoting an original document: *Quote* block → style
   **Archival document**.
3. **Excerpt** (sidebar, about 40 words): shown on cards, under the title and as the Google description.
4. **Sidebar → Sections / Domains / Countries / Eras**: tick one Section, one or more Domains, the Country, the Era.
   Tags: add `untold-stories` to show it in "Untold stories" on the homepage; `timelines`, `myths-vs-facts` for the
   Special Features links.
5. **Featured image** (sidebar): public domain / CC0 / licensed only; never AI-generated faces of real people.
   Best size about 1600 px wide; square crops are made automatically for cards. In the image's **Caption** write
   who/what, date, author, licence and source. Fill **Alternative text** (what the image shows).
6. **Story details** box (below the text): full name, birth/death year, key date (YYYY-MM-DD, used by "This week"),
   **Sources** (at least two, one per line: `Title | Publisher | https://url`), **Image credits**, reel and podcast links.
7. **Yoast SEO** box: check the green/orange lights; you may edit the SEO title and meta description.
8. **Preview**, then **Publish** (or the arrow next to it to **schedule** a date/time).

Before publishing, check: two reliable sources per important fact; no untraceable quotes; disputed points and
legends labelled; image licence and credit. The seeded drafts have known gaps listed in `CONTENT_MODEL.md`
(short texts for Smalls and Coleman, missing years for Ellen Craft and Mansa Musa, source links, Rosa Parks photo
rights).

After publishing: the story appears in Latest stories, its section page, the country on the map (Global section),
"This week" (if it has a key date in the coming 7 days), and the sitemap. The newest published story is the
homepage's Featured story.

## Podcast episodes
**Podcast → Add episode**: Title, Excerpt = episode description, text = transcript, Featured image = cover.
Fields in *Custom fields*: `bhr_episode_number`, `bhr_spotify_url`, `bhr_youtube_url`, `bhr_apple_url`,
`bhr_related_posts` (story IDs, comma-separated). If *Custom fields* is not visible: editor ⋮ menu → Preferences →
Panels → Custom fields. In the story, put the episode page URL in *Related podcast episode URL*.
3 episode drafts are waiting (Douglass, Smalls, Carver); add per-episode Spotify links and transcripts.

## News (normal posts) and pages
- **Posts** = News and updates (`/news/`), using the News categories.
- **Pages**: About, Contact, Donate, Sources & Bibliography, Editorial Policy, Corrections Policy, and the legal
  placeholders **Privacy Policy, Terms of Use, Cookie Policy — to be written by you** (they say "Placeholder").
  Section pages (African American History, Global African History) show your intro text above the lists; the lists
  and the map are automatic.
- **Footer menu**: Appearance → Menus → "Footer menu". The top mega-menu is built automatically from the sections and
  subjects (change requests go through the theme code).

## Media
Upload in **Media → Add new** or from the editor. JPEG/PNG are converted to WebP and resized automatically
(largest kept 2000 px). Always fill Caption (credit) and Alternative text.

## Caching (automatic)
Pages are cached for visitors (WP Super Cache) and the database is cached (Redis). Publishing or editing a story
clears the affected pages automatically. If something looks old: **Settings → WP Super Cache → Delete cache**.
Logged-in users always see fresh pages.

## Launch checklist (when the first stories are ready)
1. Publish at least 5–10 reviewed stories.
2. **Settings → Reading → uncheck "Discourage search engines from indexing this site"** (it is checked until launch).
3. Google Search Console: add the domain, verify (DNS TXT record in hPanel), submit
   `https://theblackhistoryroom.com/sitemap_index.xml`.
4. Optional: Google Analytics or Cloudflare Web Analytics (ask first; keep it to one lightweight script).
5. Write the Privacy, Terms and Cookie pages; add a contact email on Contact.

## What not to do
- Do not install page builders, security suites or many plugins: ask first (plugin policy in the brief).
  Installed: Yoast SEO, Redis Object Cache, WP Super Cache.
- Theme/plugin file editing in the admin is disabled on purpose. Theme and site code live in git
  (`website/theme`, `website/mu-plugins`).
- Do not give the `n8n-automation` user more rights; it must stay drafts-only.

## Backups and help
- Automatic: database every day, full backup every Sunday, on the server in `/root/backups/bhr/`
  (see `BACKUP_AND_RESTORE.md`). Download a weekly set now and then.
- Other docs: `CONTENT_MODEL.md` (structure, map, citations), `N8N_WORDPRESS_INTEGRATION.md`, `SECURITY.md`,
  `DNS_SETUP.md`, `INSTALLATION.md`, `ARCHITECTURE.md`.

## Map and filters (each story)
In **Story details**: *Map place* (e.g. "Charleston Harbor, South Carolina"), *Map latitude* / *Map longitude*
(decimal degrees; north and east positive, south and west negative — right-click a place in Google Maps or
OpenStreetMap to copy them), *Key year* if birth/death years are unknown. In the sidebar tick **Gender** (Woman / Man /
Group; both Woman and Man for a couple). The interactive map at `/global-african-history/` updates by itself.

## Expanded story texts waiting for approval
Stories → Drafts → titles ending in "-expanded" (13 of them). When approved, ask Claude to apply them (or run
`BHR_MODE=apply` with `website/scripts/story_expansions.php`); the old text stays in the story's revisions.

## Newsletter sign-ups
WP Admin → **Newsletter**: list of sign-ups (email + consent date) and an **Export CSV** button for MailerLite / Brevo.
