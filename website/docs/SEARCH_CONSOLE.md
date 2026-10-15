# Google Search Console: verify the domain and submit the sitemap

Do this when you are ready to launch (the site still asks search engines not to index it).

## 1. Allow indexing
WP Admin → **Settings → Reading** → untick **"Discourage search engines from indexing this site"** → Save.
Check: https://theblackhistoryroom.com/robots.txt should no longer block, and pages should no longer carry
`noindex` (view source of the homepage, search for `robots`).

## 2. Add the domain property
1. Go to https://search.google.com/search-console and sign in with your Google account.
2. **Add property** → choose **Domain** (left box) → type `theblackhistoryroom.com` → Continue.
3. Google shows a TXT record like `google-site-verification=AbC123...`. Copy it.

## 3. Add the TXT record at Hostinger (DNS)
hPanel → Domains → theblackhistoryroom.com → **DNS / Nameservers** → Add record:

| Type | Name | Value | TTL |
| --- | --- | --- | --- |
| TXT | `@` | `google-site-verification=...` (the value Google gave you) | 3600 |

Save, wait a few minutes (up to an hour), then click **Verify** in Search Console. Keep the TXT record afterwards:
Google re-checks it.

## 4. Submit the sitemap
Search Console → your property → **Sitemaps** → "Add a new sitemap": type `sitemap_index.xml` → Submit.
(Full address: https://theblackhistoryroom.com/sitemap_index.xml — made by Yoast SEO; it lists stories, pages,
podcast episodes and topics, and updates itself when you publish.)

## 5. Check after a few days
- **Pages** report: published stories should move to "Indexed".
- **URL inspection**: paste a story URL → "Request indexing" for the most important ones.
- **Enhancements**: Breadcrumbs should show as valid (Article and BreadcrumbList structured data are on every story).

Optional: Bing Webmaster Tools can import the property directly from Search Console.
