# I used a class because it has a State (volume, channel, power) and
# Behavior (turn on, change channel). So grouping them together mirrors
# how real hardware works

class SeatDevice:
    def __init__(self, seat_id: str) -> None:
        # initial state of every device before powering on
        self.seat_id = seat_id
        self.powered_on = False
        self.volume = 0
        self.current_channel = None
        self.brightness = 0
        self.call_button_active = False # flight attendant call button

        self.wifi_connected = False
        self.language = "en"

    # when device powers on, we set default values
    def power_on(self):
        self.powered_on = True
        self.volume = 50 
        self.brightness = 50

    # when device powers off, reset values
    def power_off(self):
        self.powered_on = False
        self.volume = 0
        self.current_channel = None
        self.brightness = 0
        self.call_button_active = False
        self.wifi_connected = False

    # every method that changes the device's state must validate that the device
    # is on and the input is within acceptable bounds called "failing fast"

    def set_volume(self, level: int):
        if self.powered_on == False:
            raise RuntimeError("Cannot set volume when device is powered off")
        if level < 0 or level > 100:
            raise ValueError(f"Volume must be between 0 - 100, got {level}")
        
        self.volume = level
        
    def select_channel(self, channel: str):
        if not self.powered_on:
            raise RuntimeError("Cannot change channels when power is off")
        if not channel:
            raise ValueError("Channel cannot be empty")
        
        self.current_channel = channel


    def set_brightness(self, level: int):
        if not self.powered_on:
            raise RuntimeError("Cannot set brightness when device is powered is off")
        if level < 0 or level > 100:
            raise ValueError("Brightness must be between 0 and 100")
        self.brightness = level
        
    def press_call_button(self):
        if not self.powered_on:
            raise RuntimeError("Cannot press call button when device is powered off")
        
        self.call_button_active = True
    # you can reset button when device is powered off
    # flight attendeds come help then reset button  on the arm rest panel independent of screen
    def reset_call_button(self):
        self.call_button_active = False

    def get_status(self) -> dict:
        return {
            "seat_id": self.seat_id,
            "powered_on": self.powered_on,
            "volume": self.volume,
            "current_channel": self.current_channel,
            "brightness": self.brightness,
            "call_button_active": self.call_button_active,
            "wifi_connected": self.wifi_connected,
            "language": self.language
        }

    def connect_wifi(self):
        if not self.powered_on:
            raise RuntimeError("Cannot connect WIFI: device is powered off")
        self.wifi_connected = True

    def disconnect_wifi(self):
        if not self.powered_on:
            raise RuntimeError("Cannot disconnect WIFI: device is powered off")
        self.wifi_connected = False

    def set_language(self, lang: str):
        if not self.powered_on:
            raise RuntimeError("Cannot set language: device is powered off")
        supported = ["en", "fr", "ma", "es"]

        if lang not in supported:
            raise ValueError(f"Unsupported language: {lang} | supported: {supported}")
        self.language = lang

    def reboot(self):
        # resets all states like power off
        # Except for language it persists
        current_language = self.language
        self.power_off()
        self.power_on()
        self.language = current_language
