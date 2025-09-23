# UniFi Protect Setup (Webhook)

1. Open **Protect → Automations / Alarm Manager**.
2. Create an automation:
   - **Trigger:** Doorbell Ring (select your UniFi doorbell camera)
   - **Action:** Webhook
     - **Method:** POST
     - **URL:** `http://<pi-ip>:8080/doorbell`
     - **Header:** `X-Webhook-Secret: <your secret>`

## Network / Firewall notes
- In UniFi **Policy Engine** (or legacy LAN IN rules), ensure **Allow LAN→Pi (22,8080)** is **above** any inter-VLAN deny.
- Allow the **UDM/UDM-Pro gateway IP** (e.g., `192.168.1.1` and/or `192.168.107.1`) to reach the Pi on **TCP 8080**.

## Test
```bash
# From Mac
curl -X POST http://<pi-ip>:8080/test

# Full path with secret
curl -X POST http://<pi-ip>:8080/doorbell -H "X-Webhook-Secret: <SECRET>"
```
