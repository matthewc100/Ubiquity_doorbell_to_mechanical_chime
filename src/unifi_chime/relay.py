import os

class BaseRelay:
    def on(self) -> None: ...
    def off(self) -> None: ...

class GpioZeroRelay(BaseRelay):
    def __init__(self, pin: int, active_high: bool = True) -> None:
        from gpiozero import LED
        self._led = LED(pin, active_high=active_high)
    def on(self) -> None:
        self._led.on()
    def off(self) -> None:
        self._led.off()

def build_relay_from_env() -> BaseRelay:
    pin = int(os.environ.get("RELAY_PIN", "17"))
    active = os.environ.get("ACTIVE_HIGH", "true").lower() == "true"
    return GpioZeroRelay(pin, active)
