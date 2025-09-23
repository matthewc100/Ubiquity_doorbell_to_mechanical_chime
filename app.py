# app.py
# UniFi Doorbell → Legacy Mechanical Chime bridge
# - Flask app exposing POST /doorbell (auth via header or ?secret=)
# - POST /test for local testing (no auth)
# - RINGS and GAP_MS let you create multiple "ding-dong" pulses
#
# Env vars (with defaults):
#   RELAY_PIN=17
#   ACTIVE_HIGH=true          # set false if your relay is LOW-trigger
#   PULSE_MS=700              # ms the relay stays ON for each ring
#   RINGS=1                   # number of ding-dongs per trigger
#   GAP_MS=700                # ms between rings
#   LOCKOUT_SEC=2.5           # ignore triggers within this window
#   SECRET=...                # required for /doorbell if set (header or query)
#   LISTEN_HOST=0.0.0.0
#   LISTEN_PORT=8080

import os
import time
import threading
import logging
from flask import Flask, request, abort, jsonify
from gpiozero import DigitalOutputDevice

# ---- Configuration ----
PIN = int(os.getenv("RELAY_PIN", "17"))
ACTIVE_HIGH = os.getenv("ACTIVE_HIGH", "true").strip().lower() in ("1", "true", "yes", "on")
PULSE_MS = int(os.getenv("PULSE_MS", "700"))
RINGS = int(os.getenv("RINGS", "1"))
GAP_MS = int(os.getenv("GAP_MS", "700"))
LOCKOUT_SEC = float(os.getenv("LOCKOUT_SEC", "2.5"))
SECRET = os.getenv("SECRET", "")  # if empty, /doorbell is open (not recommended)
LISTEN_HOST = os.getenv("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", "8080"))

# ---- GPIO device ----
relay = DigitalOutputDevice(PIN, active_high=ACTIVE_HIGH, initial_value=False)

# ---- App & logging ----
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("chime")

# ---- Concurrency/lockout ----
_last_fire_start = 0.0
_seq_lock = threading.Lock()


def _now() -> float:
    return time.time()


def _should_lockout() -> bool:
    # Lockout measured from the start of the last sequence
    return (_now() - _last_fire_start) < LOCKOUT_SEC


def _fire_sequence(pulse_ms: int, rings: int, gap_ms: int) -> None:
    """Drive the relay for N pulses with a gap between each pulse."""
    for i in range(rings):
        relay.on()
        time.sleep(max(pulse_ms, 0) / 1000.0)
        relay.off()
        if i < rings - 1:
            time.sleep(max(gap_ms, 0) / 1000.0)


def _is_authorized(req) -> bool:
    """If SECRET is set, require header X-Webhook-Secret or ?secret= to match."""
    if not SECRET:
        return True
    supplied = req.headers.get("X-Webhook-Secret")
    if supplied is None:
        supplied = req.args.get("secret", default=None, type=str)
    return (supplied is not None) and (supplied == SECRET)


@app.post("/doorbell")
def doorbell():
    """Production endpoint: requires SECRET when set."""
    global _last_fire_start
    if not _is_authorized(request):
        log.warning("Unauthorized /doorbell")
        abort(401)

    with _seq_lock:
        if _should_lockout():
            log.info("Doorbell request within lockout window; ignoring.")
            return ("", 204)  # intentionally ignored

        _last_fire_start = _now()
        log.info(
            "Doorbell: rings=%d pulse_ms=%d gap_ms=%d active_high=%s",
            RINGS, PULSE_MS, GAP_MS, ACTIVE_HIGH,
        )
        _fire_sequence(PULSE_MS, RINGS, GAP_MS)

    return ("", 204)


@app.post("/test")
def test():
    """Local test endpoint (no auth). Respects lockout."""
    global _last_fire_start
    with _seq_lock:
        if _should_lockout():
            return jsonify({"status": "locked-out", "lockout_sec": LOCKOUT_SEC}), 429

        _last_fire_start = _now()
        log.info(
            "Test: rings=%d pulse_ms=%d gap_ms=%d active_high=%s",
            RINGS, PULSE_MS, GAP_MS, ACTIVE_HIGH,
        )
        _fire_sequence(PULSE_MS, RINGS, GAP_MS)

    return jsonify({"status": "ok"}), 200


@app.get("/healthz")
def healthz():
    """Simple GET health endpoint so you (or UDM) can probe without POST."""
    return jsonify(
        {
            "ok": True,
            "pin": PIN,
            "active_high": ACTIVE_HIGH,
            "pulse_ms": PULSE_MS,
            "rings": RINGS,
            "gap_ms": GAP_MS,
            "lockout_sec": LOCKOUT_SEC,
        }
    ), 200


# Allow running directly (useful outside systemd). In production we use waitress via systemd.
if __name__ == "__main__":
    try:
        from waitress import serve
        serve(app, host=LISTEN_HOST, port=LISTEN_PORT)
    finally:
        relay.off()
        relay.close()
