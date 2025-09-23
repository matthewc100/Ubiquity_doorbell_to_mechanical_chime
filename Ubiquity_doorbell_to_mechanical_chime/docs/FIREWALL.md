# Firewall Hardening (UFW)

Allow only what you need.

```bash
sudo apt install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Admin LAN → SSH
sudo ufw allow from 192.168.1.0/24 to any port 22 proto tcp

# UDM/UDM-Pro gateway IPs → app port for webhooks
sudo ufw allow from 192.168.1.1   to any port 8080 proto tcp   # LAN gw
sudo ufw allow from 192.168.107.1 to any port 8080 proto tcp   # IoT gw

# (Optional while testing from admin LAN)
# sudo ufw allow from 192.168.1.0/24 to any port 8080 proto tcp

sudo ufw --force enable
sudo ufw status verbose
```

> Always add the SSH allow rule **before** enabling UFW.
