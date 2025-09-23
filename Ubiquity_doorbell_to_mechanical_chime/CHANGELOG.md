# Changelog

All notable changes to this project will be documented here.

## [0.2.0] - 2025-09-23
### Added
- **Multi-ring** support: `RINGS` and `GAP_MS` to produce double-ding with definable pause.
- **Pigpio** backend option with systemd drop-in (`GPIOZERO_PIN_FACTORY=pigpio`).

### Changed
- Default timings tuned for classic xylophone chime: `PULSE_MS=400`, `RINGS=2`, `GAP_MS=1000`, `LOCKOUT_SEC=2.8`.

### Fixed
- Documentation for UniFi Policy Engine (rule order, LAN→IoT allows, webhook source).

## [0.1.0] - 2025-09-20
- Initial working bridge: Flask + gpiozero + waitress, UFW examples, systemd unit.
