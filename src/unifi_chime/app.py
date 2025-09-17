"""
UniFi Protect doorbell → legacy mechanical chime bridge.

Endpoints:
  POST /doorbell  - called by Protect (requires secret)
  POST /test      - manual test (no auth)

See README and docs/ for wiring and configuration.
"""

from __future__ import annotations
import os, time
from threading import Lock
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from .relay import build_relay_from_env, BaseRelay

ENV_PATH = os.environ.get("UNIFI_CHIME_ENV", "/opt/unifi-chime/.env")
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)

RELAY_PIN   = int(os.environ.get("RELAY_PIN", "17"))
PULSE_MS    = int(os.environ.get("PULSE_MS", "700"))
LOCKOUT_SEC = float(os.environ.get("LOCKOUT_SEC", "2.0"))
ACTIVE_HIGH = os.environ.get("ACTIVE_HIGH", "true").lower() == "true"
LISTEN_HOST = os.environ.get("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "8080"))
SHARED      = os.environ.get("SHARED_SECRET", "")

_relay: BaseRelay | None = None
_last_ts = 0.0
_lock = Lock()

def _pulse(ms: int) -> None:
    assert _relay is not None, "Relay not initialized"
    _relay.on()
    time.sleep(ms/1000.0)
    _relay.off()

def create_app() -> Flask:
    global _relay, _last_ts
    _relay = build_relay_from_env()
    _last_ts = 0.0
    app = Flask(__name__)

    @app.post("/doorbell")
    def doorbell():
        token = request.headers.get("X-Webhook-Secret") or request.args.get("secret", "")
        if SHARED and token != SHARED:
            abort(401, "Unauthorized")
        global _last_ts
        with _lock:
            now = time.time()
            if (now - _last_ts) < LOCKOUT_SEC:
                return jsonify({"status":"ignored","reason":"lockout"}), 200
            _last_ts = now
        _pulse(PULSE_MS)
        return jsonify({"status":"ok"}), 200

    @app.post("/test")
    def test():
        _pulse(PULSE_MS)
        return jsonify({"status":"manual-ok"}), 200

    return app

app = create_app()
