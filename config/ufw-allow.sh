#!/usr/bin/env bash
set -euo pipefail

# ---- Edit these to match your network ----
PI_PORT="${PI_PORT:-8080}"
ADMIN_LAN="${ADMIN_LAN:-192.168.1.0/24}"
ADMIN_HOST="${ADMIN_HOST:-}"           # optional single host on admin LAN
UDM_LAN_IP="${UDM_LAN_IP:-192.168.1.1}"
UDM_IOT_IP="${UDM_IOT_IP:-192.168.107.1}"

echo "[*] Ensuring UFW is installed and enabled..."
sudo apt-get update -y >/dev/null 2>&1 || true
sudo apt-get install -y ufw >/dev/null 2>&1 || true

sudo ufw default deny incoming || true
sudo ufw default allow outgoing || true

# Function to add a rule if it doesn't exist
add_rule() {
  local rule="$1"
  if sudo ufw status | grep -Fq "$rule"; then
    echo "[-] Rule already present: $rule"
  else
    echo "[+] Adding: $rule"
    sudo ufw insert 1 $rule
  fi
}

# Allow SSH from Admin LAN
add_rule "allow from ${ADMIN_LAN} to any port 22 proto tcp"

# Allow webhook from both UDM gateway IPs
add_rule "allow from ${UDM_LAN_IP} to any port ${PI_PORT} proto tcp"
add_rule "allow from ${UDM_IOT_IP} to any port ${PI_PORT} proto tcp"

# Optional: allow your Admin host to hit healthz on ${PI_PORT}
if [[ -n "${ADMIN_HOST}" ]]; then
  add_rule "allow from ${ADMIN_HOST} to any port ${PI_PORT} proto tcp"
fi

echo "[*] Enabling UFW..."
yes | sudo ufw enable >/dev/null 2>&1 || true
sudo ufw status numbered
