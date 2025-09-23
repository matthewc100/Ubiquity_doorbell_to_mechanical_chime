# Quick notes for configuring the Pi

## 1) Copy and edit environment
```bash
sudo mkdir -p /opt/unifi-chime
sudo chown $USER:$USER /opt/unifi-chime
cp config/.env.example /opt/unifi-chime/.env
nano /opt/unifi-chime/.env
# Set: SECRET=<long random>; PULSE_MS=400; RINGS=2; GAP_MS=1000; LOCKOUT_SEC=3.0
```

## 2) Install deps + service (if not already)
```bash
sudo apt update && sudo apt install -y python3-venv pigpio ufw
sudo systemctl enable --now pigpiod
cd /opt/unifi-chime
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip -q && pip install -r requirements.txt
sudo cp systemd/unifi-chime.service /etc/systemd/system/unifi-chime.service
sudo mkdir -p /etc/systemd/system/unifi-chime.service.d
sudo cp systemd/unifi-chime.service.d/override.conf /etc/systemd/system/unifi-chime.service.d/override.conf
sudo systemctl daemon-reload
sudo systemctl enable --now unifi-chime.service
```

## 3) Apply UFW rules
Edit defaults at the top of `config/ufw-allow.sh` if your subnets differ, then:
```bash
sudo bash config/ufw-allow.sh
sudo ufw status numbered
```

## 4) Point UniFi Protect (Alarm Manager → Doorbell Ring → Webhook)
- **Method:** POST
- **URL:** `http://<pi-ip>:8080/doorbell?secret=<YOUR_SECRET>` *(or use header `X-Webhook-Secret`)*

## 5) Test
```bash
curl -X POST http://127.0.0.1:8080/test
curl -X POST http://<pi-ip>:8080/test
curl http://<pi-ip>:8080/healthz
```

## 6) UDM-based health check (optional)
See `docs/UDM-HEALTHCHECK.md` for a portable on-boot loop that logs OK/FAIL.
