# Firewall Configuration (Raspberry Pi with UFW)

## Why Lock It Down?
The Pi listens on TCP/8080 for webhooks. Without a firewall, any device on the VLAN could trigger the chime. With UFW rules in place, only your UDM-Pro (and optionally your admin Mac) can access it.

## Setup
```bash
sudo apt-get -y install ufw
sudo ufw allow from <UDM-PRO-IP> to any port 8080 proto tcp
# Optional: also allow your Mac for testing
sudo ufw allow from <YOUR-MAC-IP> to any port 8080 proto tcp
sudo ufw enable
sudo ufw status verbose
```
