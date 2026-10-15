# Server audit: Hostinger KVM 2 VPS (Phase 1, read-only)

Date: 2026-10-15, 18:39 server time. Method: `website/scripts/audit_vps.sh` run over SSH as root (key login).
The script only reads; secret values are masked and no `.env` contents were printed. **Nothing on the server was
changed.** (Only the key login was added by the owner, in `/root/.ssh/authorized_keys2`; see section 9.)

Labels: [M] measured by the audit, [E] estimate.

## 1. Summary

- The server has plenty of disk and enough RAM for a small WordPress stack (~4.5 GB available) [M].
- **Traefik v3 already terminates HTTPS for everything** and picks up containers by Docker labels [M].
  WordPress can be added as a **separate Compose project** with Traefik labels, so we never edit, restart or
  recreate the n8n project (`/docker/n8n/docker-compose.yml`).
- **`theblackhistoryroom.com` is not registered** (registry lookup returns 404; DNS says NXDOMAIN) [M].
  It has to be bought before the site can go live on that name (costs money: owner's decision).
- Security items to fix later, with the owner's OK: root login with password is allowed, no fail2ban, host
  firewall off, 43 package updates pending and a reboot is pending.

## 2. System

| Item | Value |
| --- | --- |
| OS | Ubuntu 24.04.4 LTS, kernel 6.8.0-138 [M] |
| CPU | 2 vCPU, AMD EPYC 9354P [M] |
| RAM | 7.8 GiB total, 3.3 GiB used, **4.5 GiB available**, **no swap** [M] |
| Disk | `/` 96 GB, 36 GB used, **60 GB free** (38 %) [M] |
| Uptime / load | 23 days, load 0.03 [M] |
| Docker | 29.7.2, Compose v5.5.0 [M] |
| Public IPv4 | `2.25.239.36` [M] |
| Hostname | `srv1998959` (`n8n.srv1998959.hstgr.cloud`) [M] |
| Other agents | `monarx-agent` (Hostinger's malware scanner) on localhost only [M] |

## 3. Containers and Compose projects

| Compose project (file) | Containers | Host port | Memory [M] |
| --- | --- | --- | --- |
| **n8n** (`/docker/n8n/docker-compose.yml`) | `n8n-n8n-1` (n8n) | 127.0.0.1:5678 | 469 MiB |
| | `n8n-traefik-1` (Traefik v3.7.13, image tag `traefik` = latest) | **0.0.0.0:80, :443** | 21 MiB |
| | `n8n-images-1` (nginx, serves `/local-files` at `/images/`) | none | 60 MiB |
| | `n8n-image-uploader-1` (python) | none | 32 MiB |
| bizdocsforge (`/opt/bizdocsforge/…`) | `bizdocsforge-renderer` | 127.0.0.1:8029 | 561 MiB |
| graded-readers-factory (`/opt/graded-readers-factory/…`) | `graded-reader-api`, `graded-reader-db` (Postgres 16) | 127.0.0.1:8731 | 109 MiB |
| | `graded-reader-worker` | **Exited (137) 2 weeks ago** | - |
| lingova-factory (`/opt/lingova-factory/…`) | `lingova-factory-lingova-factory-1` | 127.0.0.1:8766 | 52 MiB |
| simple-graded-readers (`/opt/simple-graded-readers/…`) | `simple-graded-readers` | 127.0.0.1:8765 | 43 MiB |
| (no Compose, `docker run`) | `kokoro-tts` | 127.0.0.1:8880 | **1.67 GiB** |

All restart policies are `always` or `unless-stopped` [M]. `graded-reader-worker` exited with code 137
(killed, often out-of-memory) two weeks ago; it is not part of this project, so it is noted only.

### n8n details [M]
- Image `docker.n8n.io/n8nio/n8n` (latest tag), restart `always`.
- Data: Docker volume **`n8n_n8n_data`** (1.04 GB) mounted at `/home/node/.n8n`, plus bind `/local-files`.
- Networks: `n8n_default`, `lingova-net`.
- Public URL via Traefik: `https://n8n.srv1998959.hstgr.cloud` (router `n8n`, cert resolver `mytlschallenge`).
- Settings come from `/docker/n8n/.env` (not printed).
- There is also an **unused volume `n8n_data`** (8.5 MB, 0 containers), probably from an older install. It is
  left alone: never delete volumes.

### Volumes [M]
`n8n_n8n_data` (1.04 GB, in use), `n8n_data` (8.5 MB, unused), `traefik_data` (certificates, in use),
`graded-readers-factory_reader_pgdata` (48.5 MB, in use).

### Networks [M]
`n8n_default`, `lingova-net`, `bizdocsforge-private`, `graded-readers-factory_reader_egress`,
`graded-readers-factory_reader_private`, `simple-graded-readers_reader_private`, plus Docker defaults.
Traefik is attached to **`n8n_default`** and `lingova-net`.

## 4. Reverse proxy and SSL [M]

- **Traefik v3.7.13** in the n8n project is the only reverse proxy. No nginx, Apache or Caddy runs on the host;
  no host Let's Encrypt (`/etc/letsencrypt`) and no host Traefik config directory.
- Configuration is only command-line flags in the n8n Compose file:
  - Docker provider, `exposedbydefault=false` (a container is public only if it has `traefik.enable=true`).
  - Entrypoint `web` (:80) globally redirects to `websecure` (:443).
  - Certificates: Let's Encrypt resolver **`mytlschallenge`** using the **TLS-ALPN challenge**, stored in the
    `traefik_data` volume (`/letsencrypt/acme.json`).
  - `--api.insecure=true`: the Traefik dashboard/API listens on port 8080 *inside* Docker networks. It is not
    published on the host, but any container on `n8n_default` or `lingova-net` can read it.
  - Docker socket mounted read-only.
- Current routes, all on `n8n.srv1998959.hstgr.cloud`: n8n (`/`), images (`/images/`), bizdocsforge
  (`/etsy/oauth/callback`, `/artifacts/`).
- New sites need no Traefik restart: Traefik watches Docker and adds a route, plus a certificate, when a
  container with the right labels starts.

## 5. Ports and firewall [M]

Open to the internet: **22 (SSH), 80, 443 (Traefik)**. Every other service is bound to `127.0.0.1` or not
published. Postgres (5432) is not published.

- `ufw`: **inactive**. iptables `INPUT` policy: **ACCEPT** (only Docker's own rules).
  Note: Docker publishes ports around ufw, so ufw alone would not protect container ports anyway. The safe
  pattern here (bind to 127.0.0.1 or don't publish) is already used.
- Hostinger also offers a panel firewall (hPanel → VPS → Firewall); it was not checked from the server.

## 6. Databases [M]
- One Postgres 16 (`graded-reader-db`) for the graded-readers project. **No MySQL/MariaDB and no Redis** exist.
- No databases run directly on the host.

## 7. Domains and DNS [M]
- In use: `n8n.srv1998959.hstgr.cloud` (Hostinger's free hostname).
- **`theblackhistoryroom.com`: not registered** (Verisign RDAP 404, NXDOMAIN from 1.1.1.1). `www.` does not
  resolve either. The owner needs to buy it (or choose another name) before launch.

## 8. Security basics [M]

| Check | Result | Risk |
| --- | --- | --- |
| SSH root login | `PermitRootLogin yes` | Medium |
| SSH passwords | **yes**: `sshd_config.d/50-cloud-init.conf` sets it and wins over `60-cloudimg-settings.conf` (`no`); the server offers `publickey,password` (checked in Phase 2) | **High** with root + no fail2ban |
| fail2ban | not active | Medium |
| Host firewall | ufw inactive, INPUT ACCEPT | Low (only 22/80/443 listen publicly) |
| Updates | 43 packages upgradable; `unattended-upgrades` installed but the login banner says some updates failed and **a restart is required** | Medium |
| Traefik dashboard | `--api.insecure=true` (internal networks only) | Low |
| Image tags | `traefik` and `n8n` use `latest`; a future `docker compose pull` in `/docker/n8n` could jump versions | Low |

These are recommendations only. Changing SSH, the firewall or rebooting could affect n8n and the other
projects, so each one needs the owner's OK and its own plan (Phase 2/security). **A reboot restarts n8n**
(it comes back by itself, `restart: always`), so it should be scheduled by the owner.

## 9. Access used for this audit
- A dedicated SSH key (`claude-bhr-vps`, ED25519) was added by the owner to `/root/.ssh/authorized_keys2`.
  It is in `authorized_keys2` because Hostinger's browser terminal rewrites `authorized_keys` with a temporary
  key. Remove that line to revoke Claude's access.
- A first attempt copied the script to `/root/audit_vps.sh` with Windows line endings, so it failed at line 10
  before doing anything. The real run was streamed over SSH (`bash -s`) instead. That leftover copy can be
  removed (`rm /root/audit_vps.sh`). `.gitattributes` now keeps `website/**/*.sh` on LF line endings.

## 10. Resource budget for WordPress [E]

| Component | Expected RAM |
| --- | --- |
| WordPress (PHP 8.3 + Apache or php-fpm + nginx) | 150-400 MB |
| MariaDB 11 (tuned small: `innodb_buffer_pool_size=256M`) | 250-400 MB |
| Redis 7 (`maxmemory 128mb`) | 20-130 MB |
| **Total** | **~0.5-0.9 GB** of the 4.5 GB available |

Disk: a few GB for the first year (images in WebP). Fine with 60 GB free.
Risk: there is **no swap**, and Kokoro uses 1.7 GB; a memory spike could kill a container (like the exited
worker). Recommendation: add a 2 GB swap file and set memory limits on the new containers (owner's OK first).

## 11. Safest way to add WordPress without touching n8n

**Recommended: a separate Compose project in `/opt/blackhistoryroom/` that plugs into the existing Traefik
through labels.**

```
/opt/blackhistoryroom/            (new, own project name "bhr")
├── docker-compose.yml            (in git as website/docker-compose.yml)
├── .env                          (secrets, chmod 600, never in git)
└── backups/

Networks
  n8n_default (existing, external)  ← only the WordPress web container joins, so Traefik can reach it
  bhr_internal (new, internal: true) ← WordPress + MariaDB + Redis; no internet, no other project

Containers (all new)
  bhr-wordpress   PHP 8.x, Traefik labels: Host(theblackhistoryroom.com, www → non-www redirect),
                  certresolver=mytlschallenge, traefik.docker.network=n8n_default, no host ports
  bhr-mariadb     bhr_internal only, no ports, own DB + user
  bhr-redis       bhr_internal only, no ports, maxmemory + no persistence needed
Volumes (all new)  bhr_wp_files, bhr_db_data
```

Why this is safe for n8n:
1. **The n8n Compose file and `.env` are not edited**; `/docker/n8n` is never `up`/`down`/`restart`ed.
2. Traefik needs no restart: it reads the new container's labels live. Existing routers (`n8n`, `images`,
   `bizdocsforge-public`) match only `n8n.srv1998959.hstgr.cloud`, and the new router matches only the new
   domain, so they cannot overlap.
3. MariaDB and Redis sit on an `internal` network that n8n and the other projects cannot see. No new host
   ports are opened.
4. New names (`bhr-*`) and new volumes, so nothing can collide with existing containers or volumes.
5. Uses the existing `mytlschallenge` Let's Encrypt resolver; certificates for the new domain are added to the
   same `acme.json` without touching the n8n certificate.

Trade-off: the WordPress web container shares `n8n_default` with n8n, the images server and two other apps.
The alternative (a new `bhr_proxy` network attached to Traefik) would need either a runtime
`docker network connect` (lost when Traefik is recreated) or an edit to the n8n Compose file, which the rules
forbid. Sharing `n8n_default` is the standard pattern here and also lets n8n call WordPress internally.

**Rollback** at any time: `docker compose -p bhr down` in `/opt/blackhistoryroom` (keeps volumes) removes the
site's containers and router; n8n is unaffected.

### Points to decide before Phase 2/3

1. **Domain (costs money):** buy `theblackhistoryroom.com` (it is available as of this audit) or pick another
   name. Until then we could build and test on a temporary subdomain like
   `blog.srv1998959.hstgr.cloud`, if Hostinger's DNS for that hostname allows it (to check), or locally.
2. **Cloudflare:** the current certificates use the TLS-ALPN challenge, which **fails behind Cloudflare's
   orange-cloud proxy**. Options: (a) DNS only (grey cloud): works as-is; (b) Cloudflare proxy with a
   Cloudflare Origin Certificate or a DNS-01 challenge: both need a change to Traefik's config, which lives in
   the n8n Compose file, so that would need your explicit OK and a backup first. Recommendation: start with (a).
3. **Hostinger snapshot** before Phase 3 (hPanel → VPS → Snapshots); check whether it is included in your
   plan before using it.
4. Swap file, SSH hardening (keys only, `PermitRootLogin prohibit-password`), fail2ban, pending updates and
   reboot window: each with your OK.

**Next step (after your OK): Phase 2, `BACKUP_PLAN.md`, and backups of `/docker/n8n` (Compose + `.env`, copied
not printed) and the `traefik_data` volume, before anything is installed.**
