#!/usr/bin/env bash
# Backups for The Black History Room (never touches n8n).
#   backup.sh daily    database dump                              -> /root/backups/bhr/daily/   (keeps 14)
#   backup.sh weekly   database + WordPress files + site config     -> /root/backups/bhr/weekly/  (keeps 8)
# Every archive gets a .sha256 file; the newest result is written to /root/backups/bhr/last-<kind>.log.
# Run from cron (/etc/cron.d/bhr-backup). Prints no secret.
set -euo pipefail
umask 077

KIND="${1:-daily}"
ROOT=/root/backups/bhr
SITE=/opt/blackhistoryroom
TS=$(date +%Y%m%d-%H%M%S)
DIR="$ROOT/$KIND"
LOG="$ROOT/last-$KIND.log"
case "$KIND" in
	daily) KEEP=14 ;;
	weekly) KEEP=8 ;;
	*) echo "usage: $0 daily|weekly" >&2; exit 2 ;;
esac
mkdir -p "$DIR"
exec > >(tee "$LOG") 2>&1
echo "[$(date -Is)] $KIND backup start"

# Free space guard: stop if less than 2 GB free.
FREE_KB=$(df --output=avail "$ROOT" | tail -1)
[ "$FREE_KB" -gt 2097152 ] || { echo "ERROR: less than 2 GB free, backup skipped"; exit 1; }

# 1. Database (consistent dump while the site runs; password stays inside the DB container).
DB="$DIR/bhr-db-$TS.sql.gz"
docker exec bhr-mariadb sh -c 'exec mariadb-dump -uroot -p"$MARIADB_ROOT_PASSWORD" --single-transaction --quick --routines --triggers --databases "$MARIADB_DATABASE"' | gzip -6 > "$DB"
gzip -t "$DB"
TABLES=$(zcat "$DB" | grep -c '^CREATE TABLE' || true)
[ "$TABLES" -gt 10 ] || { echo "ERROR: dump has only $TABLES tables"; exit 1; }
sha256sum "$DB" > "$DB.sha256"
echo "database: $(basename "$DB") $(du -h "$DB" | cut -f1), $TABLES tables"

# 2. Weekly: WordPress files (uploads, plugins, wp-config.php; page cache excluded) + site config incl. .env.
if [ "$KIND" = weekly ]; then
	FILES="$DIR/bhr-files-$TS.tar.gz"
	docker run --rm --volumes-from bhr-wordpress:ro -v "$DIR":/out alpine:3.20 \
		tar -czf "/out/$(basename "$FILES")" -C /var/www/html --exclude=./wp-content/cache --exclude=./wp-content/themes/bhr --exclude=./wp-content/mu-plugins .
	CONF="$DIR/bhr-config-$TS.tar.gz"
	tar -czf "$CONF" -C "$SITE" .
	for f in "$FILES" "$CONF"; do
		gzip -t "$f"
		sha256sum "$f" > "$f.sha256"
		echo "$(basename "$f") $(du -h "$f" | cut -f1)"
	done
fi

# 3. Retention: keep the newest $KEEP sets.
for prefix in bhr-db bhr-files bhr-config; do
	{ ls -1t "$DIR"/$prefix-*.tar.gz "$DIR"/$prefix-*.sql.gz 2>/dev/null || true; } | tail -n +$((KEEP + 1)) | while read -r old; do
		rm -f "$old" "$old.sha256"
		echo "removed old $(basename "$old")"
	done
done

echo "[$(date -Is)] $KIND backup OK"
