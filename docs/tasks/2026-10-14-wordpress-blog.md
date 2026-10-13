# Task for 2026-10-14: The Black History Room WordPress blog on the Hostinger KVM 2 VPS

Status: NOT STARTED. Saved on 2026-10-13 at the owner's request.

## Before starting (notes added by Claude)
- The cloud session has no access to the VPS. This must run where the VPS is reachable: a local Claude Code session
  with SSH access, or the owner runs the audit commands and pastes the output. Never ask for passwords or keys in
  chat; use SSH keys and environment variables.
- Step 1 is the read-only audit only. Change nothing until the owner has read SERVER_AUDIT.md and agrees.
- n8n is already running on this VPS and must keep working exactly as before.
- Paid items (domain, Cloudflare plans, paid plugins, image generation) need the owner's OK first.
- The docs for this project go in a `docs/` folder for the website (decide the repo/folder with the owner; the
  owner's rule is that work goes to anaqqad/Test unless they say otherwise).

## The owner's brief (verbatim)

You are a senior DevOps engineer, WordPress developer, web designer, SEO specialist, and publishing-system architect.

I want you to build ONE production-ready WordPress blog on my existing Hostinger KVM 2 VPS.

PROJECT NAME:
The Black History Room

PURPOSE:
A high-quality editorial website focused on Black history, African history, African-American history, important historical figures, forgotten events, civil rights, culture, politics, science, inventions, and lesser-known historical stories.

IMPORTANT:
My VPS already runs n8n.

DO NOT break, replace, reinstall, reset, or modify my working n8n installation unless absolutely necessary.

==================================================
PHASE 1 — AUDIT BEFORE CHANGING ANYTHING
==================================================

First perform a READ-ONLY audit of the server.

Identify:

- Ubuntu version
- CPU
- RAM
- available disk
- Docker version
- Docker Compose version
- existing containers
- existing Docker networks
- existing volumes
- open ports
- firewall configuration
- reverse proxy currently used
- SSL configuration
- n8n container/configuration
- existing databases
- existing domains/subdomains
- current resource usage

Create:

SERVER_AUDIT.md

Explain the safest way to add WordPress without interfering with n8n.

DO NOT install or modify anything until the audit is complete.

==================================================
PHASE 2 — BACKUP
==================================================

Before making changes:

- back up relevant configuration files
- back up Docker Compose files
- back up reverse-proxy configuration
- document existing n8n configuration
- record currently exposed ports

Create:

BACKUP_PLAN.md

Never delete existing containers or volumes.

==================================================
PHASE 3 — ARCHITECTURE
==================================================

Preferred architecture:

Docker
├── existing n8n
├── wordpress-blackhistory
├── MariaDB
├── Redis
└── existing reverse proxy

Use:

theblackhistoryroom.com
or

[DOMAIN I PROVIDE]

Do not change DNS unless I explicitly provide access and ask you to do so.

If DNS is not configured yet, prepare everything and tell me exactly which DNS records I need to add.

WordPress and n8n must remain isolated.

==================================================
PHASE 4 — WORDPRESS INSTALLATION
==================================================

Install WordPress securely using Docker Compose.

Requirements:

- latest stable WordPress
- PHP 8.x
- MariaDB
- persistent Docker volumes
- Redis object cache
- automatic restart
- secure passwords stored in .env
- no credentials hardcoded in Compose files
- HTTPS
- www → non-www canonical redirect
- HTTP → HTTPS redirect

Use a dedicated database and database user for this website.

==================================================
PHASE 5 — WEBSITE DESIGN
==================================================

Brand:

THE BLACK HISTORY ROOM

Design style:

- premium editorial history publication
- black / cream / deep red / muted gold palette
- strong typography
- archival/documentary feeling
- clean modern layout
- not cluttered
- highly readable
- mobile-first
- fast-loading
- no unnecessary animations
- no generic corporate look

Visual inspiration:

historical archive
+
documentary magazine
+
modern editorial publication

Do NOT copy another website.

==================================================
HEADER
==================================================

Logo / title:

THE BLACK HISTORY ROOM

Navigation:

Home
Stories
People
Africa
African-American History
Civil Rights
Culture
Science & Innovation
Timelines
Podcast
About

Add search.

==================================================
HOMEPAGE
==================================================

Build a homepage containing:

1. HERO STORY

Large featured article with:
image
category
headline
short excerpt

2. LATEST STORIES

Grid of newest articles.

3. UNTOLD STORIES

Feature lesser-known historical stories.

4. PEOPLE WHO CHANGED HISTORY

Historical figures.

5. THIS WEEK IN BLACK HISTORY

Date-related historical events.

6. AFRICA

Featured African-history stories.

7. AFRICAN-AMERICAN HISTORY

Featured U.S. history stories.

8. PODCAST

Section promoting:

BLACK HISTORY IN 10 MINUTES

9. NEWSLETTER

Simple email signup area.

10. FOOTER

About
Contact
Privacy Policy
Terms
Editorial Policy
Corrections Policy

==================================================
ARTICLE DESIGN
==================================================

Every article page should have:

Category

H1 title

Subtitle / deck

Featured image

Author

Publication date

Updated date if applicable

Estimated reading time

Article body

Table of contents for long articles

Inline images

Image captions

Source citations

Related articles

Previous / next story

Share buttons

Newsletter CTA

==================================================
EDITORIAL CATEGORIES
==================================================

Create these initial categories:

African History
African-American History
Civil Rights
Slavery & Emancipation
Historical Figures
Black Women in History
Science & Innovation
Military History
Politics
Arts & Culture
Forgotten History
Black Business
Timelines

Do not create hundreds of tags.

==================================================
SEO
==================================================

Configure technical SEO properly.

Requirements:

- clean URLs

Example:

/history/tuskegee-airmen/

NOT:

/?p=123

- XML sitemap
- robots.txt
- canonical URLs
- OpenGraph metadata
- Twitter/X cards
- schema.org Article markup
- breadcrumbs
- author schema
- organization schema
- optimized title tags
- meta descriptions
- image alt text
- proper H1/H2/H3 hierarchy

Install only a lightweight SEO plugin.

Prefer:
Rank Math
or
Yoast

Choose whichever has lower unnecessary overhead.

==================================================
PERFORMANCE
==================================================

This site will primarily contain:

TEXT
+
IMAGES

Optimize aggressively.

Targets:

Google PageSpeed:

Mobile > 85
Desktop > 95 where realistically possible.

Implement:

- full-page caching
- Redis object caching
- WebP / AVIF
- lazy loading
- responsive images
- Brotli/Gzip
- browser caching
- Cloudflare-ready configuration
- optimized database
- minimal JavaScript
- lightweight theme

Avoid heavy page builders such as Elementor unless absolutely necessary.

Prefer Gutenberg / native blocks or a lightweight custom theme.

==================================================
IMAGE HANDLING
==================================================

Automatically generate:

thumbnail
medium
large
social-sharing image

Use WebP/AVIF where supported.

Do not store unnecessarily huge images.

Recommended article featured image:

1600 × 900

==================================================
SECURITY
==================================================

Implement:

- firewall review
- fail2ban if appropriate
- strong admin credentials
- disable XML-RPC unless required
- disable file editing from WordPress admin
- restrict database exposure
- containers should not expose unnecessary ports
- automated security updates where safe
- login-rate limiting
- HTTPS only
- secure headers
- database backups
- WordPress backups

Do NOT expose MariaDB publicly.

==================================================
BACKUPS
==================================================

Configure automatic backups.

Daily:
database

Weekly:
WordPress files + database

Keep multiple restore points.

Document the restore procedure.

Create:

BACKUP_AND_RESTORE.md

==================================================
CONTENT QUALITY
==================================================

This is a history site.

Accuracy is extremely important.

Do NOT automatically publish historical claims without source verification.

Articles should distinguish between:

verified historical facts
historical interpretation
disputed claims
legends/myths

Prefer reliable sources such as:

- Library of Congress
- National Archives
- Smithsonian
- universities
- museums
- peer-reviewed research
- government historical archives
- reputable books
- primary sources

Wikipedia can help locate sources but should not be the sole source for important claims.

==================================================
EDITORIAL POLICY PAGE
==================================================

Create an Editorial Policy explaining:

- historical accuracy
- sourcing standards
- corrections
- AI-assisted workflows
- human/editorial review
- distinction between fact and interpretation

==================================================
AUTOMATION PREPARATION
==================================================

Prepare WordPress so my existing n8n installation can later publish content using the WordPress REST API.

Do NOT build the automation yet unless I ask.

Prepare:

- dedicated WordPress API user
- Application Password authentication
- REST API verification
- category IDs
- media upload support

Document everything in:

N8N_WORDPRESS_INTEGRATION.md

Future workflow will be:

Topic
↓
Research
↓
Article
↓
Fact checking
↓
Image generation
↓
SEO metadata
↓
n8n
↓
WordPress draft
↓
Review
↓
Publish

IMPORTANT:

The default automation should create DRAFTS, not automatically publish articles.

==================================================
PODCAST
==================================================

Create a Podcast page for:

BLACK HISTORY IN 10 MINUTES

Prepare fields for:

episode title
episode number
description
Spotify link
YouTube link
Apple Podcasts link
transcript
related articles

Do not invent podcast episodes.

==================================================
ANALYTICS
==================================================

Prepare support for:

Google Search Console
Google Analytics
Cloudflare Analytics

Do not install excessive tracking scripts.

==================================================
LEGAL / TRUST PAGES
==================================================

Create placeholders for:

About
Contact
Privacy Policy
Terms
Editorial Policy
Corrections Policy
Cookie Policy

Do not invent legal claims about my company.

==================================================
ADMIN EXPERIENCE
==================================================

Keep WordPress admin simple.

Remove unnecessary plugins and dashboards.

I should easily be able to:

create article
upload image
choose category
set featured image
edit SEO
schedule article
publish

==================================================
PLUGIN POLICY
==================================================

Use as few plugins as possible.

Before installing every plugin explain:

1. Why it is needed
2. Whether WordPress can do it natively
3. Security implications
4. Performance impact

Avoid abandoned plugins.

==================================================
DELIVERABLES
==================================================

Create documentation:

/docs/
    SERVER_AUDIT.md
    ARCHITECTURE.md
    INSTALLATION.md
    SECURITY.md
    BACKUP_AND_RESTORE.md
    N8N_WORDPRESS_INTEGRATION.md
    DNS_SETUP.md
    WORDPRESS_ADMIN_GUIDE.md

Also provide:

docker-compose.yml
.env.example

Never include real passwords inside documentation.

==================================================
FINAL TESTING
==================================================

Before declaring completion test:

Homepage
Article pages
Mobile layout
Desktop layout
HTTPS
Redirects
Images
Caching
Database
Redis
WordPress admin
REST API
SEO sitemap
robots.txt
structured data
404 page
search
categories
backup
restore procedure

Verify that n8n still works exactly as it did before installation.

==================================================
FINAL REPORT
==================================================

At completion tell me:

Website URL:
WordPress status:
HTTPS status:
Database status:
Redis status:
Backup status:
n8n status:
RAM usage:
Disk usage:
Docker containers:
Remaining tasks requiring me:

Do NOT claim completion for anything you did not actually verify.

Start with the server audit only.

Do not change anything yet.
