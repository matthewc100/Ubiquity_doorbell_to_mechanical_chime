# config/

This folder contains configuration artifacts you can copy to the Raspberry Pi
(and references for the UDM). It is safe to upload the whole `config/` folder to
the Pi and run the scripts with minor edits to match your LAN.

## Files

- **.env.example** — baseline environment for `/opt/unifi-chime/.env`.
- **ufw-allow.sh** — idempotent UFW rules to allow the UDM gateways and (optionally) your Admin LAN/Mac to reach the app.
- **ufw-status.sh** — prints numbered UFW rules and listening sockets.
- **NOTES.md** — quick-start for applying config on the Pi and pointing UniFi Protect at it.

> See also: `docs/FIREWALL.md`, `docs/OPERATIONS.md`, `docs/UNIFI-PROTECT.md`, `docs/UDM-HEALTHCHECK.md`.
