# Security (The Black History Room)

Status 2026-10-15. Items marked **pending** need the owner's OK because they affect the whole server (and n8n).

## In place and tested
| Measure | How | Tested |
| --- | --- | --- |
| HTTPS only | Traefik global HTTP→HTTPS redirect, Let's Encrypt certificate for both names | 301/308 redirects |
| Security headers | HSTS (1 year), nosniff, SAMEORIGIN, Referrer-Policy, Permissions-Policy, no X-Powered-By | response headers |
| Login rate limit | Traefik `ratelimit` on `POST /wp-login.php`: 5 per minute per IP (burst 5), then HTTP 429 | 12 quick POSTs: 5×200 then 7×429; normal again after a minute |
| XML-RPC off | Apache denies `xmlrpc.php` (403); WordPress filter off | 403 |
| No file editing in admin | `DISALLOW_FILE_EDIT` | config |
| Database not exposed | MariaDB and Redis only on the internal network, no host ports | unreachable from `n8n_default`; no 3306/6379 on the host |
| Secrets | `/opt/blackhistoryroom/.env` (600), never in git, never printed | — |
| Automatic security updates | WordPress minor/security releases auto-update | config |
| Backups | daily DB, weekly full, restore tested | see `BACKUP_AND_RESTORE.md` |
| Memory limits | WordPress 768 MB, MariaDB 640 MB, Redis 192 MB | `docker stats` |
| Real visitor IPs | Apache `mod_remoteip` behind Traefik (for logs) | logs |

## Pending (owner decision; each one touches the whole server)
1. **SSH**: root login with password is allowed and passwords are enabled (`sshd_config.d/50-cloud-init.conf`).
   Recommended: keys only (`PasswordAuthentication no`, `PermitRootLogin prohibit-password`) after making sure your
   own key login works (WinSCP/PuTTY or the Hostinger browser terminal). Also change the root password that was
   pasted in chat on 2026-10-15.
2. **fail2ban for SSH**: bans IPs after repeated failed SSH logins. Not installed yet.
3. **Pending OS updates and reboot**: 43 packages, reboot required. A reboot restarts n8n (it comes back on its own);
   choose a quiet time.
4. **Hostinger firewall** (hPanel): allow only 22, 80, 443.
5. **Swap file (2 GB)**: protects against out-of-memory kills (there is no swap today).

## Accounts
- One administrator (`bhr_owner`). Credentials are in `.env` on the server; after first login, store them in a
  password manager, change the password, and delete `WP_ADMIN_PASSWORD` from `.env`.
- For n8n: a separate Editor-level user with an Application Password (planned in `N8N_WORDPRESS_INTEGRATION.md`),
  which creates **drafts only**.
