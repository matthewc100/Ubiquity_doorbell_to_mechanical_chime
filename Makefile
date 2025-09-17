    # ---- Config ----
    APP_DIR ?= /opt/unifi-chime
    PYTHON  ?= python3
    VENV    ?= .venv
    PORT    ?= 8080

    BIN     := $(VENV)/bin
    PY      := $(BIN)/python
    PIP     := $(BIN)/pip

    .PHONY: help
    help:
	@echo "Targets:"
	@echo "  make venv              - Create venv & install requirements"
	@echo "  make run               - Run app locally (dev)"
	@echo "  make test              - Run unit tests (pytest)"
	@echo "  make install           - Copy app to $(APP_DIR) and build venv there"
	@echo "  make install-service   - Install & start systemd service"
	@echo "  make status            - Service status"
	@echo "  make logs              - Follow service logs"
	@echo "  make restart           - Restart service"
	@echo "  make clean             - Remove venv and caches"

    $(VENV):
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

    .PHONY: venv
    venv: $(VENV)

    .PHONY: run
    run: venv
	UNIFI_CHIME_ENV=$(APP_DIR)/.env PYTHONPATH=src $(PY) -m flask --app src/unifi_chime/app.py run --host 0.0.0.0 --port $(PORT)

    .PHONY: test
    test: venv
	PYTHONPATH=src $(BIN)/pytest -q

    .PHONY: install
    install:
	sudo mkdir -p $(APP_DIR)
	sudo chown $$USER:$$USER $(APP_DIR)
	rsync -a --delete src/ $(APP_DIR)/src/
	@if [ -f config/.env.example ]; then cp -n config/.env.example $(APP_DIR)/.env || true; fi
	cd $(APP_DIR) && $(PYTHON) -m venv .venv && . .venv/bin/activate && pip install --upgrade pip && pip install -r /etc/alternatives/../.. || true
	# Fallback if above path weirdness; install directly:
	cd $(APP_DIR) && . .venv/bin/activate && pip install -r $(PWD)/requirements.txt || true
	@echo "Edit $(APP_DIR)/.env before starting the service."

    .PHONY: install-service
    install-service:
	sudo cp service/unifi-chime.service /etc/systemd/system/unifi-chime.service
	sudo systemctl daemon-reload
	sudo systemctl enable --now unifi-chime.service
	@echo "Service installed. Tail logs with: sudo journalctl -u unifi-chime.service -f"

    .PHONY: status
    status:
	sudo systemctl status unifi-chime.service --no-pager || true

    .PHONY: logs
    logs:
	sudo journalctl -u unifi-chime.service -f -n 100

    .PHONY: restart
    restart:
	sudo systemctl restart unifi-chime.service

    .PHONY: clean
    clean:
	rm -rf $(VENV)
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
