import os, time, importlib
import pytest

os.environ["RELAY_PIN"] = "17"
os.environ["PULSE_MS"] = "50"
os.environ["LOCKOUT_SEC"] = "0.2"
os.environ["ACTIVE_HIGH"] = "true"
os.environ["SHARED_SECRET"] = "s3cr3t"

class FakeRelay:
    def __init__(self): self.events=[]
    def on(self): self.events.append(("on", time.time()))
    def off(self): self.events.append(("off", time.time()))

@pytest.fixture()
def client(monkeypatch):
    from unifi_chime import relay as relay_module
    monkeypatch.setattr(relay_module, "build_relay_from_env", lambda: FakeRelay())
    from unifi_chime import app as app_module
    importlib.reload(app_module)
    app = app_module.create_app()
    return app.test_client()

def test_test_endpoint(client):
    r = client.post("/test")
    assert r.status_code == 200

def test_doorbell_auth(client):
    assert client.post("/doorbell").status_code == 401
    assert client.post("/doorbell?secret=s3cr3t").status_code == 200
    assert client.post("/doorbell", headers={"X-Webhook-Secret":"s3cr3t"}).status_code == 200

def test_lockout(client):
    ok = client.post("/doorbell?secret=s3cr3t")
    assert ok.status_code == 200
    ignored = client.post("/doorbell?secret=s3cr3t")
    assert ignored.status_code == 200
    assert ignored.get_json().get("reason") == "lockout"
