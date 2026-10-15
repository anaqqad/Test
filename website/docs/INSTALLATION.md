# Installation (done 2026-10-15)

All commands run on the VPS as root. Nothing under `/docker/n8n` is used or changed.

## 1. Domain and DNS (owner, hPanel)
`theblackhistoryroom.com` registered at Hostinger on 2026-10-15 (1 year, renews 2027-10-15, auto-renew on).
Records: `A @ 2.25.239.36`, `AAAA @ 2a02:4780:75:bddb::1`, `CNAME www theblackhistoryroom.com`, TTL 300.
See `DNS_SETUP.md` (to be written) for details.

## 2. Files
```
/opt/blackhistoryroom/           (chmod 750)
├── docker-compose.yml           = website/docker-compose.yml
├── .env                         secrets, chmod 600, created by scripts/make_env.sh (never in git)
├── .env.example                 = website/.env.example
├── config/  mariadb.cnf  php.ini  apache-bhr.conf
└── scripts/ make_env.sh  wp.sh
```
Copy the files from the repo (use Unix line endings), then create the secrets:
```
bash /opt/blackhistoryroom/scripts/make_env.sh <admin-username> <admin-email>
cd /opt/blackhistoryroom && docker compose config --quiet
```

## 3. Start
```
cd /opt/blackhistoryroom
docker compose pull && docker compose up -d
docker compose ps        # bhr-mariadb and bhr-redis "healthy", bhr-wordpress "Up"
```
Traefik picks up the router and gets the Let's Encrypt certificate within seconds.

**Run step 4 immediately.** Until WordPress is installed, anyone who opens the site can run the installer; bots
watching new certificates hit `/wp-admin/install.php` within a minute of the first start (seen in the logs).

## 4. Install WordPress (WP-CLI, no browser)
```
W=/opt/blackhistoryroom/scripts/wp.sh
set -a; . /opt/blackhistoryroom/.env; set +a
bash $W core install --url="https://$DOMAIN" --title="The Black History Room" \
  --admin_user="$WP_ADMIN_USER" --admin_email="$WP_ADMIN_EMAIL" --admin_password="$WP_ADMIN_PASSWORD" --skip-email
bash $W option update blogdescription "Powerful people, moments, struggles and achievements from Black history"
bash $W option update blog_public 0            # no indexing until launch
bash $W option update default_comment_status closed
bash $W option update default_ping_status closed
bash $W option update default_pingback_flag 0
bash $W rewrite structure "/history/%postname%/" --hard
bash $W plugin delete hello akismet
bash $W post delete 1 --force && bash $W post delete 2 --force   # sample post and page
```

## 5. Installed versions [M]
WordPress 7.1.3, PHP 8.4.26 (Apache), MariaDB 11.8, Redis 7 (alpine), theme Twenty Twenty-Five 1.5 (temporary,
until the custom theme). No plugins.

## 6. First login (owner)
- URL: `https://theblackhistoryroom.com/wp-admin/`
- Username and password: in `/opt/blackhistoryroom/.env` (`WP_ADMIN_USER`, `WP_ADMIN_PASSWORD`). Open it with WinSCP
  (root) and copy them into your password manager. You can then change the password in WordPress (Users → Profile)
  and delete the `WP_ADMIN_PASSWORD` line from `.env`; it is only used at install time.

## 7. Tests run on 2026-10-15 [M]
| Test | Result |
| --- | --- |
| `http://theblackhistoryroom.com/` | 301 → `https://theblackhistoryroom.com/` |
| `http://www…/` | 301 → `https://www…/` → 301 → `https://theblackhistoryroom.com/` |
| `https://www…/history/test/?a=1` | 301 → `https://theblackhistoryroom.com/history/test/?a=1` |
| Home page | 200; title "The Black History Room" |
| Certificate | Let's Encrypt, SAN `theblackhistoryroom.com` + `www…`, valid to 2027-01-13 (auto-renewed by Traefik) |
| IPv6 | 200 via `2a02:4780:75:bddb::1` |
| Headers | HSTS, nosniff, SAMEORIGIN, Referrer-Policy, Permissions-Policy; no X-Powered-By; gzip |
| `/xmlrpc.php`, `/wp-config.php`, `/readme.html` | 403 |
| REST API `/wp-json/` | 200 |
| Unknown story `/history/no-such-story/` | 404 with WordPress "Page not found" page |
| Redis from WordPress | `PONG` |
| DB / Redis from `n8n_default`, host ports 3306/6379 | not reachable / not published |
| Real visitor IPs in logs | yes (mod_remoteip) |
| n8n after install | same start time (2026-09-30 14:27:59 UTC), 0 restarts, `/healthz` 200, editor 200; Traefik 0 restarts |
| Memory | WordPress 132 MB, MariaDB 105 MB, Redis 7 MB; host 4.3 GB available |
