# UniFi Protect: Alarm Manager Webhook Setup

## Why Use Alarm Manager?
Official, reliable, and upgrade-safe way to trigger a webhook when the doorbell button is pressed.

## Steps
1. Open **Protect → Alarm Manager**.
2. New **Alarm / Automation**.
3. **Trigger**: Doorbell Ring (your doorbell camera).
4. **Action**: Webhook / HTTP POST
   - URL: `http://<pi-ip>:8080/doorbell?secret=<YOUR_SECRET>`
   - or Header: `X-Webhook-Secret: <YOUR_SECRET>`
   - Body: optional (ignored)
5. Save and press the doorbell to test.
