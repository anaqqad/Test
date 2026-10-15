#!/usr/bin/env bash
# Phase 2 backup: copies configs and records state. Reads only from existing services; writes only to /root/backups.
set -euo pipefail
umask 077
TS=$(date +%Y%m%d-%H%M%S)
B=/root/backups/bhr-phase2-$TS
mkdir -p "$B"/{configs,volumes,n8n,state}
chmod 700 /root/backups "$B"

# 1. n8n project folder (compose, .env, old compose backups, uploader script)
cp -a /docker/n8n "$B/configs/docker-n8n"

# 2. Compose files and .env of the other projects (configs only, no data)
for d in /opt/*/; do
  for f in "$d"docker-compose*.yml "$d"compose*.yml "$d".env; do
    [ -f "$f" ] && cp -a --parents "$f" "$B/configs/"
  done
done

# 3. Traefik certificates volume (acme.json)
tar -czf "$B/volumes/traefik_data.tar.gz" -C /var/lib/docker/volumes/traefik_data _data

# 4. n8n database: consistent online copy (SQLite backup API, read-only on the source) + config (encryption key)
python3 - "$B/n8n/database.sqlite" <<'PY'
import sqlite3, sys
src = sqlite3.connect("file:/var/lib/docker/volumes/n8n_n8n_data/_data/database.sqlite?mode=ro", uri=True)
dst = sqlite3.connect(sys.argv[1])
src.backup(dst)
src.close()
print("n8n db integrity:", dst.execute("PRAGMA integrity_check").fetchone()[0])
print("n8n workflows:", dst.execute("SELECT count(*) FROM workflow_entity").fetchone()[0])
print("n8n credentials:", dst.execute("SELECT count(*) FROM credentials_entity").fetchone()[0])
dst.close()
PY
cp -a /var/lib/docker/volumes/n8n_n8n_data/_data/config "$B/n8n/config"

# 5. State record (inspect files contain env values: they stay in this 700 folder, never printed)
docker ps -a --no-trunc > "$B/state/docker-ps.txt"
docker inspect $(docker ps -aq) > "$B/state/docker-inspect.json"
docker images --digests > "$B/state/docker-images.txt"
docker network ls > "$B/state/docker-networks.txt"
docker network inspect $(docker network ls -q) > "$B/state/docker-network-inspect.json"
docker volume ls > "$B/state/docker-volumes.txt"
docker compose ls > "$B/state/compose-projects.txt"
ss -tulpn > "$B/state/ports.txt"
iptables-save > "$B/state/iptables.rules"
ip6tables-save > "$B/state/ip6tables.rules" 2>/dev/null || true
ufw status verbose > "$B/state/ufw.txt" 2>&1 || true
cp -a /etc/ssh/sshd_config "$B/state/sshd_config"
cp -a /etc/ssh/sshd_config.d "$B/state/sshd_config.d" 2>/dev/null || true
free -h > "$B/state/memory.txt"; df -h > "$B/state/disk.txt"
docker exec n8n-n8n-1 n8n --version > "$B/state/n8n-version.txt" 2>&1 || true
curl -s -o /dev/null -w '%{http_code}\n' https://n8n.srv1998959.hstgr.cloud/healthz > "$B/state/n8n-healthz-before.txt" || true

# 6. Checksums and one archive for off-server copies
(cd "$B" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
tar -czf "$B.tar.gz" -C /root/backups "bhr-phase2-$TS"
chmod 600 "$B.tar.gz"
echo "BACKUP_DIR=$B"
echo "ARCHIVE=$B.tar.gz ($(du -h "$B.tar.gz" | cut -f1))"
