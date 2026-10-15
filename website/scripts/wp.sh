#!/usr/bin/env bash
# Run WP-CLI against the live site without installing anything in the WordPress container.
# Usage (on the VPS): bash /opt/blackhistoryroom/scripts/wp.sh plugin list
# Reads DB settings from /opt/blackhistoryroom/.env; prints no secret.
set -euo pipefail
cd /opt/blackhistoryroom
set -a; . ./.env; set +a
export WORDPRESS_DB_PASSWORD="$DB_PASSWORD"
# Same extra wp-config settings as the site (Redis host, WP_HOME, ...), taken from the running container.
WORDPRESS_CONFIG_EXTRA="$(docker exec bhr-wordpress printenv WORDPRESS_CONFIG_EXTRA)"
export WORDPRESS_CONFIG_EXTRA
# Shares the WordPress container's network: reaches the DB/Redis and the internet (plugin downloads).
exec docker run --rm -i --user 33:33 --network container:bhr-wordpress --volumes-from bhr-wordpress \
  -e WORDPRESS_DB_HOST=bhr-mariadb -e WORDPRESS_DB_NAME="$DB_NAME" -e WORDPRESS_DB_USER="$DB_USER" \
  -e WORDPRESS_DB_PASSWORD -e WORDPRESS_TABLE_PREFIX="$WP_TABLE_PREFIX" -e WORDPRESS_CONFIG_EXTRA \
  wordpress:cli-php8.4 wp "$@"
