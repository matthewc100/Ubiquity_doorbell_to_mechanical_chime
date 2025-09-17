# Operations Guide

## Service
```bash
sudo systemctl status unifi-chime.service --no-pager
sudo systemctl restart unifi-chime.service
sudo journalctl -u unifi-chime.service -f -n 100
```

## Update
```bash
cd /opt/unifi-chime
git pull
make install
sudo systemctl restart unifi-chime
```

## Config
Edit `/opt/unifi-chime/.env`, then restart the service.

## Troubleshooting
- Energizes on boot → set `ACTIVE_HIGH=false`
- Harsh ring → lower `PULSE_MS` (500–600 ms)
- Double ring → increase `LOCKOUT_SEC` (2.5–3.0 s)
- No click → `curl -X POST http://127.0.0.1:8080/test`
