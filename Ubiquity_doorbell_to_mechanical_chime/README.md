# Ubiquity Doorbell → Mechanical Chime

Bridge a UniFi (Ubiquiti) **PoE doorbell** to a classic **mechanical “ding-dong” chime** using a Raspberry Pi + 5 V Songle relay. It listens for a **webhook** from UniFi Protect (Doorbell Ring) and closes a dry contact to simulate the old doorbell button.

## Highlights
- **Reliable GPIO** via `pigpio` pin factory
- **Multi-ring** support: set `RINGS` and `GAP_MS` for double-ding with timing you like
- **Tunable pulse** (`PULSE_MS`) and **lockout** (`LOCKOUT_SEC`)
- **Hardened** with UFW examples + UniFi Policy Engine notes
- Minimal dependencies; runs as a `systemd` service via `waitress`

## Quick Start (TL;DR)
1. **Copy repo to Pi** at `/opt/unifi-chime`, then create a venv and install deps:
   ```bash
   sudo apt update && sudo apt install -y python3-venv pigpio
   sudo systemctl enable --now pigpiod
   cd /opt && sudo mkdir -p unifi-chime && sudo chown $USER:$USER unifi-chime
   cd /opt/unifi-chime
   python3 -m venv .venv && source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
2. **Configure**: copy `.env.example` → `.env`, then adjust values (see table below).
3. **Install service**:
   ```bash
   sudo cp systemd/unifi-chime.service /etc/systemd/system/unifi-chime.service
   sudo mkdir -p /etc/systemd/system/unifi-chime.service.d
   sudo cp systemd/unifi-chime.service.d/override.conf /etc/systemd/system/unifi-chime.service.d/override.conf
   sudo systemctl daemon-reload
   sudo systemctl enable --now unifi-chime.service
   ```
4. **Firewall (UFW)** on the Pi:
   ```bash
   sudo apt install -y ufw
   sudo ufw default deny incoming; sudo ufw default allow outgoing
   sudo ufw allow from 192.168.1.0/24 to any port 22 proto tcp              # Admin LAN → SSH
   sudo ufw allow from 192.168.1.1     to any port 8080 proto tcp            # UDM LAN → webhook
   sudo ufw allow from 192.168.107.1   to any port 8080 proto tcp            # UDM IoT → webhook
   sudo ufw --force enable; sudo ufw status verbose
   ```
5. **Test locally**:
   ```bash
   curl -X POST http://127.0.0.1:8080/test
   ```
6. **UniFi Protect** → Alarm Manager → Doorbell Ring → **Webhook (POST)**  
   URL: `http://<pi-ip>:8080/doorbell`  
   Header: `X-Webhook-Secret: <your secret>`

### Key Environment Variables
| Var | Meaning | Example |
|---|---|---|
| `RELAY_PIN` | BCM GPIO pin for relay input | `17` |
| `ACTIVE_HIGH` | `true` if relay triggers on HIGH (yours does) | `true` |
| `PULSE_MS` | ON duration per ring (ms) | `400` |
| `RINGS` | Number of ding-dongs per trigger | `2` |
| `GAP_MS` | Gap between rings (ms) | `1000` |
| `LOCKOUT_SEC` | Ignore triggers within this window | `2.8` |
| `SECRET` | Required for `/doorbell` (header or `?secret=`) | `long-random` |
| `LISTEN_HOST` / `LISTEN_PORT` | HTTP bind | `0.0.0.0` / `8080` |

> Use **POST** for tests (`/test`), not GET/HEAD. `/doorbell` requires the secret.

## Troubleshooting
- **Method not allowed** → use `curl -X POST`, not `-I` or GET.  
- **401 Unauthorized** → secret mismatch; use header `X-Webhook-Secret`.  
- **Relay clicks, no ring** → wire **COM = transformer hot**, **NO = front feed** (do **not** relay between `TRANS` and `FRONT`). Confirm with an ohmmeter across **COM–NO** during `/test`.  
- **No packets from LAN** → UniFi **Policy Engine** rule order; place **Allow LAN→Pi (22,8080)** and **Allow UDM→Pi (8080)** **above** inter-VLAN denies.  
- **GPIO warnings** → install `pigpio`, run `pigpiod`, and set service drop-in env `GPIOZERO_PIN_FACTORY=pigpio`.

<!-- AUTOLINKS:BEGIN -->
## Reference & Docs
- **Firewall (UFW) hardening:** [FIREWALL.md](docs/FIREWALL.md)
- **Operations (service, logs, updates):** [OPERATIONS.md](docs/OPERATIONS.md)
- **UniFi Protect setup:** [UNIFI-PROTECT.md](docs/UNIFI-PROTECT.md)
- **Project log:** [PROJECT_LOG.md](docs/PROJECT_LOG.md)
- **License:** [LICENSE](LICENSE)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Codeowners:** [CODEOWNERS](CODEOWNERS)

### Hardware
- **Fritzing design (.fzz):** [Front Door chime.fzz](hardware/fritzing/Front%20Door%20chime.fzz)
- **Enclosure (3D models):** [enclosure](hardware/enclosure)
- **Bill of Materials:** [BOM.csv](hardware/BOM.csv)
<!-- AUTOLINKS:END -->

## License
See [LICENSE](LICENSE). Code ownership: see [CODEOWNERS](CODEOWNERS).
