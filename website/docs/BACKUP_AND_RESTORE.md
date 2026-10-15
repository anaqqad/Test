# Backup and restore (The Black History Room)

Set up and tested 2026-10-15. Covers only the website (`bhr-*` containers). n8n has its own data and is not touched;
the one-off n8n/Traefik safety backup from before the install is described in `BACKUP_PLAN.md`.

## What runs automatically

| When (server time, UTC) | What | Where | Kept |
| --- | --- | --- | --- |
| Every day 03:15 | Database dump | `/root/backups/bhr/daily/bhr-db-*.sql.gz` | newest 14 |
| Sundays 03:45 | Database + WordPress files + site config | `/root/backups/bhr/weekly/` (`bhr-db-*`, `bhr-files-*`, `bhr-config-*`) | newest 8 |

- Script: `/opt/blackhistoryroom/scripts/backup.sh daily|weekly` (= `website/scripts/backup.sh`).
- Schedule: `/etc/cron.d/bhr-backup` (= `website/config/cron-bhr-backup`).
- Each archive has a `.sha256` file. The result of the latest run is in `/root/backups/bhr/last-daily.log` and
  `last-weekly.log` (ends with "backup OK").
- The script refuses to run with less than 2 GB free and fails if a dump has fewer than 10 tables.
- **Files archive** = everything in the WordPress volume (uploads, plugins, `wp-config.php` with the salts) except the
  page cache and our theme/mu-plugin (those are in git). **Config archive** = `/opt/blackhistoryroom` including `.env`.
- Database dumps are consistent while the site runs (`--single-transaction`); the DB password never leaves the
  database container.
- All backup folders and files are root-only (700/600). They contain secrets (`.env`, `wp-config.php`): never copy
  them anywhere public.

Measured on 2026-10-15: database 52 KB (18 tables), files 87 MB, config 224 KB, weekly run 10 s.

## Tested restore (2026-10-15)
- Database: imported the latest weekly dump into a throwaway MariaDB container with no network (deleted afterwards):
  18 tables, 19 draft stories, 15 published pages, `siteurl` = `https://theblackhistoryroom.com`.
- Files: extracted the latest files archive into a temporary folder (deleted afterwards): 6,635 files, `wp-config.php`
  present, 273 uploads.
- Checksums: `sha256sum -c` passes.

## Off-server copies (owner)
Backups on the VPS do not help if the VPS itself is lost. Free options, choose one:
1. Download the newest `weekly/` set with WinSCP once a month and keep it on your PC / a private drive.
2. Hostinger VPS snapshot (hPanel → VPS → Snapshots) before big changes; check whether your plan includes it.
3. Later, if you want it automatic: an rclone copy to a cloud drive (needs your account authorisation; ask me first).

## How to restore

All commands as root on the VPS. Pick the backup set first:
```
ls -lt /root/backups/bhr/weekly/ /root/backups/bhr/daily/
cd /root/backups/bhr/weekly && sha256sum -c bhr-db-YYYYMMDD-HHMMSS.sql.gz.sha256
```

**A. Database only** (content mistake, bad plugin update). Take a fresh dump first, then load the old one:
```
/opt/blackhistoryroom/scripts/backup.sh daily
zcat /root/backups/bhr/daily/bhr-db-YYYYMMDD-HHMMSS.sql.gz \
  | docker exec -i bhr-mariadb sh -c 'exec mariadb -uroot -p"$MARIADB_ROOT_PASSWORD"'
docker exec bhr-redis redis-cli flushall
docker exec bhr-wordpress sh -c 'rm -rf wp-content/cache/supercache/*'
```
(The dump contains `CREATE DATABASE IF NOT EXISTS` / `USE bhr_wp` and drops and recreates each table.)

**B. WordPress files** (lost uploads, broken plugin files):
```
cd /opt/blackhistoryroom && docker compose stop wordpress
docker run --rm --volumes-from bhr-wordpress -v /root/backups/bhr/weekly:/in:ro alpine:3.20 \
  sh -c 'cd /var/www/html && tar -xzf /in/bhr-files-YYYYMMDD-HHMMSS.tar.gz'
docker compose start wordpress
```
This overwrites files with the backup copy; files added after the backup are kept.

**C. Whole site on a new server** (VPS lost): install Docker, restore `/opt/blackhistoryroom` from the config archive
(`tar -xzf bhr-config-*.tar.gz -C /opt/blackhistoryroom`), make sure Traefik and the `n8n_default` network exist
(restore n8n first, see `BACKUP_PLAN.md`), `docker compose up -d db redis`, then do **A**, then
`docker compose up -d wordpress` and **B**, then point DNS to the new server's IP.

After any restore: open the homepage, a story, `/wp-admin/`, and check n8n: `curl -s -o /dev/null -w "%{http_code}"
https://n8n.srv1998959.hstgr.cloud/healthz` must print 200.

## Before risky changes
`/opt/blackhistoryroom/scripts/backup.sh weekly` takes a full set on demand (about 10 seconds).
