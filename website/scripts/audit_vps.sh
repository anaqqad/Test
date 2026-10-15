#!/usr/bin/env bash
# READ-ONLY audit of the Hostinger VPS before adding the WordPress site for The Black History Room.
# It changes nothing: no installs, no restarts, no edits. Secrets are masked before printing.
#
# Run on the VPS (as root or a sudo user):
#     bash audit_vps.sh > audit.txt 2>&1
# or from your own computer, without copying the file:
#     ssh USER@HOST 'sudo bash -s' < website/scripts/audit_vps.sh > audit.txt 2>&1
# Then check audit.txt and paste it back to Claude.
set -u

mask() {
  # hide values of anything that looks like a secret (KEY=..., PASSWORD: "...", tokens, Traefik basicauth labels,
  # password hashes, URLs with credentials). Quoted values are masked whole.
  sed -E \
    -e 's/(([A-Za-z0-9_.-]*(PASS|PASSWORD|SECRET|TOKEN|KEY|AUTH|CREDENTIAL|SALT|PRIVATE)[A-Za-z0-9_.-]*)"?[[:space:]]*[=:][[:space:]]*)("[^"]*"|'"'"'[^'"'"']*'"'"'|[^[:space:],"]+)/\1****/Ig' \
    -e 's/\$\$?(apr1|2[aby]|1|5|6|y)\$\$?[^[:space:],"]+/****/g' \
    -e 's#(://[^:/@[:space:]]+):[^@[:space:]]+@#\1:****@#g'
}
section() { printf '\n==================== %s ====================\n' "$1"; }
run() { printf '\n$ %s\n' "$*"; eval "$@" 2>&1 | mask; }

section "SYSTEM"
run "cat /etc/os-release | head -4"
run "uname -r"
run "nproc; lscpu | grep -E 'Model name|^CPU\\(s\\)'"
run "free -h"
run "df -h -x tmpfs -x devtmpfs"
run "uptime"

section "DOCKER"
run "docker --version"
run "docker compose version || docker-compose --version"
run "docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'"
run "docker network ls"
run "docker volume ls"
run "docker compose ls 2>/dev/null || echo 'docker compose ls not available'"
run "docker system df -v | sed -n '/VOLUME NAME/,/^$/p'"
run "docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'"

section "CONTAINER DETAILS (env values masked)"
for c in $(docker ps -a --format '{{.Names}}' 2>/dev/null); do
  printf '\n--- %s ---\n' "$c"
  docker inspect "$c" --format 'image={{.Config.Image}} restart={{.HostConfig.RestartPolicy.Name}}
networks={{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}
ports={{json .HostConfig.PortBindings}}
mounts={{range .Mounts}}{{.Type}}:{{.Source}}->{{.Destination}} {{end}}
labels={{json .Config.Labels}}' 2>&1 | mask
  echo "env names (values hidden):"
  docker inspect "$c" --format '{{range .Config.Env}}{{println .}}{{end}}' 2>/dev/null | sed -E 's/=.*$/=****/'
done

section "COMPOSE FILES (secrets masked)"
for f in $(find / -maxdepth 4 \( -name 'docker-compose*.yml' -o -name 'docker-compose*.yaml' -o -name 'compose.yml' -o -name 'compose.yaml' \) -not -path '*/proc/*' 2>/dev/null); do
  printf '\n--- %s ---\n' "$f"; mask < "$f"
done
echo
echo ".env files found (contents NOT printed):"
find / -maxdepth 4 -name '.env' -not -path '*/proc/*' 2>/dev/null

section "PORTS AND FIREWALL"
run "ss -tulpn"
run "ufw status verbose || echo 'ufw not installed'"
run "iptables -S | head -40"

section "REVERSE PROXY AND SSL"
run "systemctl is-active nginx apache2 caddy traefik 2>/dev/null"
run "ls /etc/nginx/sites-enabled /etc/nginx/conf.d 2>/dev/null"
run "grep -rhE 'server_name|proxy_pass|listen' /etc/nginx/sites-enabled /etc/nginx/conf.d 2>/dev/null | sort -u"
run "ls /etc/letsencrypt/live 2>/dev/null"
run "grep -vhE '^[[:space:]]*#' /etc/caddy/Caddyfile 2>/dev/null | grep -E '\\{|reverse_proxy' || echo 'no /etc/caddy/Caddyfile'"
run "ls /etc/traefik /opt/traefik 2>/dev/null || echo 'no host traefik config dir'"
run "for c in \$(docker ps --format '{{.Names}}'); do echo \"\$c: \$(docker inspect \$c --format '{{range \$k,\$v := .Config.Labels}}{{\$k}}={{\$v}}{{println}}{{end}}' | grep -E '^(traefik\\.http\\.routers\\.[^=]*\\.(rule|tls[^=]*|entrypoints)|caddy[^=]*)=' | tr '\\n' ' ')\"; done"
run "docker ps --format '{{.Names}} {{.Image}}' | grep -Ei 'traefik|caddy|nginx|proxy' || echo 'no proxy container'"

section "DNS (current public records)"
DOMAIN="${DOMAIN:-theblackhistoryroom.com}"
run "curl -s -4 --max-time 5 https://ifconfig.me; echo ' <- this VPS public IPv4'"
run "getent ahosts $DOMAIN | head -3 || echo '$DOMAIN does not resolve'"
run "getent ahosts www.$DOMAIN | head -3 || echo 'www.$DOMAIN does not resolve'"

section "DATABASES"
run "docker ps --format '{{.Names}} {{.Image}}' | grep -Ei 'mysql|mariadb|postgres|redis' || echo 'no database containers'"
run "systemctl is-active mysql mariadb postgresql redis-server 2>/dev/null"

section "SECURITY BASICS"
run "systemctl is-active fail2ban 2>/dev/null || echo 'fail2ban not active'"
run "grep -E '^(PermitRootLogin|PasswordAuthentication|Port)' /etc/ssh/sshd_config"
run "apt list --upgradable 2>/dev/null | wc -l"
run "dpkg -l unattended-upgrades 2>/dev/null | tail -1"

section "DONE (nothing was changed)"
