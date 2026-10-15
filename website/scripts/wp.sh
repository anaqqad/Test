#!/usr/bin/env bash
# Run WP-CLI against the live site without installing anything in the WordPress container.
# Usage (on the VPS): bash /opt/blackhistoryroom/scripts/wp.sh plugin list
# Reads DB settings from /opt/blackhistoryroom/.env; prints no secret.
set -euo pipefail
cd /opt/blackhistoryroom
set -a; . ./.env; set +a
export WORDPRESS_DB_PASSWORD="$DB_PASSWORD"
exec docker run --rm -i --user 33:33 --network bhr_bhr_internal --volumes-from bhr-wordpress \
  -e WORDPRESS_DB_HOST=bhr-mariadb -e WORDPRESS_DB_NAME="$DB_NAME" -e WORDPRESS_DB_USER="$DB_USER" \
  -e WORDPRESS_DB_PASSWORD -e WORDPRESS_TABLE_PREFIX="$WP_TABLE_PREFIX" \
  wordpress:cli-php8.4 wp "$@"
