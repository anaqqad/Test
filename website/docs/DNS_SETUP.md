# DNS setup: theblackhistoryroom.com

Checked live on 2026-10-15 (Cloudflare resolver 1.1.1.1 and Hostinger's nameservers).

## Domain
- Registered at Hostinger on 2026-10-15 19:26 UTC, expires **2027-10-15** (auto-renew on, $19.99/year + tax).
- Owner email verified. WHOIS privacy included.
- Nameservers: `aurora.dns-parking.com`, `nebula.dns-parking.com` (Hostinger DNS). Manage in
  hPanel → Domains → theblackhistoryroom.com → DNS / Nameservers.

## Records in use

| Type | Name | Value | TTL | Purpose |
| --- | --- | --- | --- | --- |
| A | `@` | `2.25.239.36` | 300 | VPS IPv4 (was Hostinger parking `2.57.91.91`) |
| AAAA | `@` | `2a02:4780:75:bddb::1` | 300 | VPS IPv6 |
| CNAME | `www` | `theblackhistoryroom.com` | 300 | `www` follows `@`; the site redirects `www` → bare domain (301) |

No MX, TXT or CAA records exist. Let's Encrypt certificates (both names) are issued and renewed automatically by
Traefik with the TLS-ALPN challenge on port 443; this needs the A/AAAA records to point at the VPS.

## Recommended changes (owner, in hPanel; nothing here was changed by Claude)

1. **Raise the TTL** of the three records from 300 to 3600 once everything is stable (fewer lookups, same result).
2. **Anti-spoofing while the domain sends no email** (stops others sending mail "from" your domain):

   | Type | Name | Value |
   | --- | --- | --- |
   | TXT | `@` | `v=spf1 -all` |
   | TXT | `_dmarc` | `v=DMARC1; p=reject; adkim=s; aspf=s` |

   When you set up email (see below), these two must be replaced with the values your email provider gives you.
3. **Optional CAA** (only Let's Encrypt may issue certificates for the domain):

   | Type | Name | Value |
   | --- | --- | --- |
   | CAA | `@` | `0 issue "letsencrypt.org"` |

## Email (not set up)
WordPress on this server **cannot send email** yet (no mail program in the container; tested: `wp_mail()` fails).
Effects: no password-reset emails, no notifications. Options, owner's choice (some cost money):
- Hostinger email for the domain (check your plan), then an SMTP setting in WordPress.
- A free transactional SMTP service (e.g. Brevo free tier) + a small SMTP setting in WordPress.
Each option needs its own MX / SPF / DKIM / DMARC records, which replace item 2 above. Ask before choosing.

## Cloudflare (not used)
DNS stays at Hostinger. If you move DNS to Cloudflare later: keep the records **DNS only (grey cloud)**. The orange
proxy would break the current certificate method (TLS-ALPN) and needs a Traefik change first.

## If the server IP changes
Update the A and AAAA records to the new addresses (`curl -4 ifconfig.me`, `curl -6 ifconfig.me` on the server).
With TTL 300, the change is visible within about 5 minutes.
