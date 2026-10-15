#!/usr/bin/env bash
# Creates /opt/blackhistoryroom/.env with strong random secrets. Prints no secret.
# Usage (on the VPS): bash make_env.sh <admin-username> <admin-email>
# Refuses to overwrite an existing .env.
set -euo pipefail
umask 077
ENV=/opt/blackhistoryroom/.env
[ -e "$ENV" ] && { echo "$ENV already exists; not touching it."; exit 1; }
rnd() { openssl rand -base64 48 | tr -dc 'A-Za-z0-9' | head -c "$1"; }
cat > "$ENV" <<EOF
DOMAIN=theblackhistoryroom.com

DB_NAME=bhr_wp
DB_USER=bhr_wp
DB_PASSWORD=$(rnd 32)
DB_ROOT_PASSWORD=$(rnd 32)
WP_TABLE_PREFIX=bhr_

WP_ADMIN_USER=$1
WP_ADMIN_EMAIL=$2
WP_ADMIN_PASSWORD=$(rnd 24)
EOF
chmod 600 "$ENV"
echo "Wrote $ENV ($(stat -c %a "$ENV")), $(grep -c = "$ENV") settings; secrets not shown."
