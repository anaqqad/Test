# Backup plan (Phase 2): before adding WordPress

Date: 2026-10-15, 18:45 server time. Goal: be able to put n8n, Traefik and the other projects back exactly as they
were if anything in Phase 3 goes wrong. The full WordPress backup routine (daily DB, weekly files, restores) comes
later in `BACKUP_AND_RESTORE.md`.

Labels: [M] measured, [E] estimate.

## 1. What was done

One script (kept in git as `website/scripts/phase2_backup.sh`) was streamed over SSH. It **only reads** from the
running services and **only writes** under `/root/backups/`. No container, volume, network, Compose file or
setting was changed, started or stopped.

| Item | Result [M] |
| --- | --- |
| Backup folder | `/root/backups/bhr-phase2-20261015-184554/` (126 MB, mode 700, root only) |
| Single archive | `/root/backups/bhr-phase2-20261015-184554.tar.gz` (40 MB, mode 600) |
| Checksums | `SHA256SUMS`, 39 files, `sha256sum -c` passes |
| Archive check | `gzip -t` passes, 54 entries listed |
| n8n database copy | `PRAGMA integrity_check` = **ok**; 29 workflows, 13 credentials |
| n8n before / after | container `n8n-n8n-1` started 2026-09-30 14:27:59 UTC, **0 restarts**, the same after the backup |
| Traefik before / after | `n8n-traefik-1` started 2026-09-25 20:50:38 UTC, **0 restarts**, the same after the backup |
| n8n health | `https://n8n.srv1998959.hstgr.cloud/healthz` returned **200** before and after |

## 2. What is in the backup

```
bhr-phase2-20261015-184554/
├── configs/
│   ├── docker-n8n/          full copy of /docker/n8n: docker-compose.yml, .env, the 4 older
│   │                        docker-compose.yml.backup* files, uploader/uploader.py
│   └── opt/<project>/       docker-compose*.yml + .env for bizdocsforge (+ override),
│                            bizdocsforge_reset_20260926_201010, graded-readers-factory,
│                            lingova-factory, simple-graded-readers
├── volumes/traefik_data.tar.gz   Traefik's Let's Encrypt store (acme.json)
├── n8n/
│   ├── database.sqlite      consistent online copy (SQLite backup API, read-only on the source)
│   └── config               n8n settings file with the ENCRYPTION KEY (needed to read the credentials)
├── state/                   docker ps / inspect / images (with digests) / networks / volumes,
│                            compose projects, listening ports, iptables + ip6tables rules, ufw,
│                            sshd_config (+ sshd_config.d), memory, disk, n8n version, n8n health
└── SHA256SUMS
```

Not included, on purpose:
- n8n event logs (`n8nEventLog-*.log`, ~20 MB): history only, not needed to restore.
- `/local-files` (1.2 GB of images used by n8n workflows): data, not config. Phase 3 does not touch it.
- Other projects' data (graded-readers Postgres, etc.): Phase 3 does not touch them.

**The backup contains secrets** (every `.env`, the n8n encryption key, `acme.json` private keys, and environment
values inside `docker-inspect.json`). It stays root-only on the server; nothing from it was printed, logged or
committed.

## 3. Baseline: n8n and the proxy as they are now [M]

| | Value |
| --- | --- |
| n8n version | 2.39.10 |
| n8n image | `docker.n8n.io/n8nio/n8n:latest`, digest `sha256:94d70bcbc868123de206d6f89786bb90f753c26b8f28889f8ddc5e224b230247` |
| Traefik image | `traefik:latest` (v3.7.13), digest `sha256:24841fe2de7304c149343d877d2923b4c8800a38ba015dea9174c23b20e344a0` |
| n8n Compose project | `n8n`, file `/docker/n8n/docker-compose.yml` (last edited 2026-09-27), settings in `/docker/n8n/.env` |
| n8n data | volume `n8n_n8n_data` → `/home/node/.n8n`; bind `/local-files` → `/home/node/.n8n-files` |
| n8n URL | `https://n8n.srv1998959.hstgr.cloud` (also `/images/` → nginx, `/etsy/oauth/callback` and `/artifacts/` → bizdocsforge) |
| Networks | n8n: `n8n_default`, `lingova-net`; Traefik: the same two |
| Public ports | 22 (sshd), 80 and 443 (Traefik). Everything else on 127.0.0.1: 5678 n8n, 8029 bizdocsforge, 8731 graded-reader-api, 8765 simple-graded-readers, 8766 lingova, 8880 kokoro; 53 local DNS; 65529/1721 monarx |
| SSH | `PermitRootLogin yes`; passwords allowed: `sshd_config.d/50-cloud-init.conf` says `PasswordAuthentication yes` and is read before `60-cloudimg-settings.conf` (`no`), so **yes** wins |

Because both images use `latest`, a later `docker compose pull` in `/docker/n8n` would change versions. To go
back to exactly today's versions, use the digests above (`image: docker.n8n.io/n8nio/n8n@sha256:94d7…`).

## 4. Off-server copies (owner action)

A backup that is only on the VPS does not help if the VPS itself is lost. Recommended, both free of extra tools:

1. **Download the archive** with WinSCP: `/root/backups/bhr-phase2-20261015-184554.tar.gz` (40 MB). Keep it in a
   private place (not Google Drive shared folders, not git): it holds passwords and keys.
2. **Hostinger snapshot** just before Phase 3 (hPanel → VPS → Snapshots & backups). Check in hPanel whether a
   snapshot is included in your plan before using it; it replaces the previous snapshot.

## 5. Rules for Phase 3 (what will and will not be touched)

Will **not** be touched: `/docker/n8n/*`, `/opt/*`, the volumes `n8n_n8n_data`, `n8n_data`, `traefik_data`,
`graded-readers-factory_reader_pgdata`, `/local-files`, any existing container, network or firewall rule,
SSH settings.

Will be **added** only: `/opt/blackhistoryroom/` (new Compose project `bhr`), new containers `bhr-*`, new volumes
`bhr_*`, a new internal network `bhr_internal`, and the new WordPress container joined to the existing
`n8n_default` network (this does not modify that network's settings or its other members).

Check after every Phase 3 step: n8n container start time and restart count unchanged, `/healthz` = 200, and the
n8n editor opens in the browser (owner).

## 6. Restore procedures

Only with the owner's OK. Use the folder `B=/root/backups/bhr-phase2-20261015-184554`.

**First, the simplest rollback of the website itself** (keeps its data, never touches n8n):
```
cd /opt/blackhistoryroom && docker compose -p bhr down
```

**n8n / Traefik configuration** (if a file was changed by mistake):
```
cd $B && sha256sum -c SHA256SUMS
diff $B/configs/docker-n8n/docker-compose.yml /docker/n8n/docker-compose.yml
diff $B/configs/docker-n8n/.env /docker/n8n/.env >/dev/null && echo ".env unchanged"
cp -a $B/configs/docker-n8n/docker-compose.yml $B/configs/docker-n8n/.env /docker/n8n/
cd /docker/n8n && docker compose up -d   # recreates only containers whose config differs
```

**Traefik certificates** (if `acme.json` was damaged): stop Traefik, restore, start.
```
cd /docker/n8n && docker compose stop traefik
tar -xzf $B/volumes/traefik_data.tar.gz -C /var/lib/docker/volumes/traefik_data
chmod 600 /var/lib/docker/volumes/traefik_data/_data/acme.json
docker compose start traefik
```
(Let's Encrypt would also simply issue new certificates; this only avoids rate limits.)

**n8n database** (last resort; brings workflows and credentials back to 2026-10-15 18:45):
```
D=/var/lib/docker/volumes/n8n_n8n_data/_data
cd /docker/n8n && docker compose stop n8n
mkdir -p /root/backups/n8n-db-before-restore && cp -a $D/database.sqlite* /root/backups/n8n-db-before-restore/
cp $B/n8n/database.sqlite $D/database.sqlite && rm -f $D/database.sqlite-wal $D/database.sqlite-shm
chown --reference=$D/config $D/database.sqlite && chmod 644 $D/database.sqlite
docker compose start n8n
```
The `config` file (encryption key) must match the database; it is backed up in `$B/n8n/config` and was not
changed.

**Other projects:** their Compose files and `.env` are in `$B/configs/opt/<project>/`; restore the same way
(`cp -a`, then `docker compose up -d` in that project folder).

## 7. Retention

Keep this backup at least until the WordPress site has run without problems for 30 days, then the owner decides.
Nothing is deleted automatically. The ongoing WordPress backups (daily database, weekly files, several restore
points) are planned in `BACKUP_AND_RESTORE.md` (Phase 4+).
