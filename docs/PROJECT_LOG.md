# Project Log — Ubiquity Doorbell → Mechanical Chime

_Last updated: 2025-09-17 22:25_

## Snapshot
- **Pi IP (reserved):** `192.168.107.195` on IoT VLAN `192.168.107.0/24`
- **Listener:** HTTP `:8080`
- **Service:** `unifi-chime.service` (systemd) — **running**
- **Secret:** present in `.env` (long/random) — **do not commit**
- **Relay test:** `/test` endpoint **energizes** relay (verified by click + continuity)
- **Chime wiring:** _TBD — not connected at time of this entry_
- **Repo:** base scaffold prepared (ZIP delivered); hardware assets added (Fritzing + 3MF)

## Completed
- Created Pi user, enabled SSH; disabled default `pi`.
- Installed Python venv and app dependencies (`Flask`, `waitress`, `gpiozero`, `python-dotenv`).
- Implemented Flask webhook bridge with lockout + shared-secret.
- Deployed as `systemd` service; verified via `curl` to `/test`.
- Verified relay hardware path (COM↔NO closes on pulse).
- DHCP reservation set for the Pi (`192.168.107.195`).
- Repo scaffold generated (code, docs, tests, service, Makefile, CI).
- Added **Fritzing** (`hardware/fritzing/Front Door chime.fzz`) and **enclosure** 3MF files.
- Documented **snap‑fit PLA enclosure**; BOM starter added.

## In Progress
- Connect relay **COM→TRANS** and **NO→FRONT** to the mechanical chime.
- Tune `PULSE_MS` (start `700 ms`; adjust to `500–600 ms` if needed).

## Parking Lot (near‑term)
- **UniFi Protect automation:** Alarm Manager → _Doorbell Ring → Webhook_ to `/doorbell?secret=...`.
- **Firewall (UFW) on Pi:** allow only UDM‑Pro (and optional admin host) to TCP/8080.
- **PoE/Ethernet migration:** use PoE splitter; disable Wi‑Fi after verifying DHCP reservation on `eth0`.
- **Repo push:** create GitHub repo `Ubiquity_doorbell_to_mechanical_chime` and commit base set.
- **Git LFS:** track `.fzz`, `.3mf` (and future `.stl`, `.step`).
- **Add images:** enclosure photos; optional Fritzing exports (`breadboard.png`, `schematic.svg`).
- **Docs:** optional `SECURITY.md`, `CONTRIBUTING.md`, `MIGRATION.md` (Wi‑Fi → PoE).

## Decisions
- **Auth:** shared secret required (header or query param).
- **GPIO pin:** `GPIO17` (BCM) for relay `IN`.
- **Topology:** local‑only webhook (no external exposure).

## Risks & Mitigations
- **Double rings** — Increase `LOCKOUT_SEC` (e.g., 2.5–3.0 s).
- **Harsh/overlong ring** — Reduce `PULSE_MS` to 500–600 ms.
- **Wi‑Fi stability** — Migrate to PoE/Ethernet; keep DHCP reservation.
- **Unauthorized triggers** — Apply UFW rules; keep secret long/random.
- **Service drift** — Track via repo; CI runs tests on PR/push.

## Test Checklist
- [ ] `/test` from Pi (`127.0.0.1`) energizes relay.
- [ ] `/test` from admin host energizes relay (until UFW tightened).
- [ ] Chime rings once at target `PULSE_MS`.
- [ ] Protect Alarm Manager webhook triggers chime on real button press.
- [ ] UFW blocks non‑authorized hosts on TCP/8080.

## Milestones
- **v0.1.0 — Initial working build**: service up, relay verified, repo seeded.
- **v0.2.0 — Hardened**: UFW, PoE/Ethernet, Protect automation live, enclosure photos/docs.

