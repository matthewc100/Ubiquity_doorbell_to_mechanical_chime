# Operations (service, logs, updates)

## Service control
```bash
sudo systemctl status unifi-chime.service --no-pager
sudo systemctl restart unifi-chime.service
sudo systemctl enable unifi-chime.service
sudo journalctl -u unifi-chime.service -n 50 --no-pager
```

## Pigpio backend
```bash
sudo apt install -y pigpio
sudo systemctl enable --now pigpiod
# Drop-in already included in systemd/unifi-chime.service.d/override.conf
```

## Update code/config
```bash
# edit /opt/unifi-chime/.env then:
sudo systemctl restart unifi-chime.service
```

## Console recovery (HDMI)
```bash
sudo ss -tlnp | grep :8080
curl -I http://127.0.0.1:8080/healthz
sudo ufw status numbered
```

## Common issues
- Use **POST** to `/test` and `/doorbell`.
- Unauthorized → secret mismatch (header `X-Webhook-Secret`).
- Relay clicks, no ring → wire COM=transformer hot, NO=front feed.
