# Ubiquity Doorbell → Mechanical Chime Bridge

Trigger a traditional mechanical chime when your **Ubiquiti/UniFi Protect** doorbell is pressed.
This service listens for a **webhook** from **Protect Alarm Manager** and pulses an **isolated relay**
across the chime’s `TRANS ↔ FRONT` terminals.

## Features
- Secure: shared-secret check on webhook calls
- Reliable: configurable pulse length and debounce lockout
- Runs as a `systemd` service behind a local firewall
- Clean repo scaffold with tests, Makefile, and docs

## Hardware
- Raspberry Pi (3B+/4B/Zero 2 W)
- 5V, 1‑channel **Songle**-based relay module (HiLetgo etc.)
  - Control: `IN`, `DC+` (5V), `DC-` (GND)
  - Contacts: `COM`, `NO`, `NC` (NC unused)
- Existing mechanical chime + transformer (16–18 VAC typical)
- Ethernet (recommended with PoE splitter) or Wi‑Fi

## Wiring (summary)
- Pi **5V (pin 2/4)** → Relay **DC+**
- Pi **GND (pin 6 etc.)** → Relay **DC-**
- Pi **GPIO17 (pin 11)** → Relay **IN**
- Relay **COM** → Chime **TRANS**
- Relay **NO** → Chime **FRONT** (NC unused)

## Install (Pi)
```bash
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get -y install python3 python3-venv python3-pip
```

Clone the repo and use the Makefile:
```bash
make install
nano /opt/unifi-chime/.env   # set RELAY_PIN, PULSE_MS, ACTIVE_HIGH, SHARED_SECRET
make install-service
make logs
```

Test:
```bash
curl -X POST "http://<pi-ip>:8080/test"
```

## UniFi Protect (Alarm Manager)
Create an automation: **Doorbell Ring → Webhook (HTTP POST)** to
`http://<pi-ip>:8080/doorbell?secret=<your-secret>`
(or header `X-Webhook-Secret: <your-secret>`). See [`docs/UNIFI-PROTECT.md`](docs/UNIFI-PROTECT.md).

## Firewall
Lock port 8080 to your UDM-Pro (and optionally your admin machine). See `docs/FIREWALL.md`.

## Development
```bash
make venv
make test
make run


<!-- AUTOLINKS:BEGIN -->
## Reference & Docs
- **Firewall (UFW) hardening:** [FIREWALL.md](docs/FIREWALL.md)
- **Operations (service, logs, updates):** [OPERATIONS.md](docs/OPERATIONS.md)
- **Project log:** [PROJECT_LOG.md](docs/PROJECT_LOG.md)
- **UniFi Protect setup:** [UNIFI-PROTECT.md](docs/UNIFI-PROTECT.md)
- **License:** [LICENSE](LICENSE)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Codeowners:** [CODEOWNERS](CODEOWNERS)

### Hardware
- **Fritzing design (.fzz):** [Front Door chime.fzz](hardware/fritzing/Front%20Door%20chime.fzz)
- **Enclosure (3D models):** [enclosure](hardware/enclosure)
- **Bill of Materials:** [BOM.csv](hardware/BOM.csv)
<!-- AUTOLINKS:END -->


```

## License
MIT — see `LICENSE`.

## Hardware & Enclosure
- Fritzing design and diagrams: [`hardware/fritzing/`](hardware/fritzing/)
- 3D-printable enclosure (3MF source; add STL/STEP exports as desired): [`hardware/enclosure/`](hardware/enclosure/)
- Bill of Materials: [`hardware/BOM.csv`](hardware/BOM.csv)

- Project log: [`docs/PROJECT_LOG.md`](docs/PROJECT_LOG.md)
