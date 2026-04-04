import pytest
from device.seat_device import SeatDevice

# fixture is a reusable piece of code, that refreshes everytime it is used
@pytest.fixture
def device_off():
    #creates an new device that is off
    return SeatDevice("6A")

@pytest.fixture
def device_on():
    device = SeatDevice("6A")
    #turn the device on
    device.power_on()
    
    return device


# power tests

# Brand new devies start with default state values
def test_initial_state(device_off):
    status = device_off.get_status()
    # brand new devices should have zeroed default states
    assert status["powered_on"] == False
    assert status["volume"] == 0
    assert status["current_channel"] == None
    assert status["brightness"] == 0
    assert status["call_button_active"] == False
# Powers on device
def test_power_on(device_off):
    device_off.power_on()
    status = device_off.get_status()

    assert status["powered_on"] == True
    assert status["volume"] == 50
    assert status["brightness"] == 50
# after turning device of, state must reset to default values
def test_power_off_reset_state(device_on):
    device_on.set_volume(75)
    device_on.select_channel("Sports")

    device_on.power_off()
    status = device_on.get_status()
    assert status["powered_on"] == False
    assert status["volume"] == 0
    assert status["current_channel"] is None
    assert status["brightness"] == 0

# volume tests

# volume should update correctly
def test_set_volume(device_on):
    device_on.set_volume(28)
    assert device_on.volume == 28

def test_volume_boundary_values(device_on):
    device_on.set_volume(100)
    status = device_on.get_status()
    assert status["volume"] == 100

    device_on.set_volume(0)
    status2 = device_on.get_status()
    assert status2["volume"] == 0

def test_set_volum_out_of_range(device_on):
    with pytest.raises(ValueError):
        device_on.set_volume(101)

    with pytest.raises(ValueError):
        device_on.set_volume(-1)

 # Sending commands when powered off should raise RuntimeError
def test_set_volume_when_off_invalide(device_off):
    with pytest.raises(RuntimeError):
        device_off.set_volume(80)

# channel tests

# should update test channel correctly
def test_select_channel(device_on):
    device_on.select_channel("Sports")
    assert device_on.get_status()["current_channel"] == "Sports"
# commands should not work when device is powered off
def test_select_channel_when_off_invalid(device_off):
    with pytest.raises(RuntimeError):
        device_off.select_channel("Sports")
# using an empty string as channel is not supported
def test_select_empty_channel_invalid(device_on):
    with pytest.raises(ValueError):
        device_on.select_channel("")

# brightness tests

# should correctly update brightness
def test_set_brightness(device_on):
    device_on.set_brightness(90)
    assert device_on.get_status()["brightness"] == 90

def test_set_brightness_out_of_range_invalid(device_on):
    with pytest.raises(ValueError):
        device_on.set_brightness(101)
    with pytest.raises(ValueError):
        device_on.set_brightness(-1)

def test_set_brightness_boundary_values(device_on):
    device_on.set_brightness(0)
    assert device_on.get_status()["brightness"] == 0

    device_on.set_brightness(100)
    assert device_on.get_status()["brightness"] == 100

def test_brightenss_when_off_invalid(device_off):
    with pytest.raises(RuntimeError):
        device_off.set_brightness(30)

# call button test

# pressing the button should activate it
def test_call_button(device_on):
    device_on.press_call_button()
    assert device_on.get_status()["call_button_active"] == True
# Resetting should deactivate call button
def test_reset_call_button(device_on):
    device_on.press_call_button()
    device_on.reset_call_button()
    assert device_on.get_status()["call_button_active"] == False

# cannot activate call button when device is powered off
def test_call_button_when_off_invalid(device_off):
    with pytest.raises(RuntimeError):
        assert device_off.press_call_button()

def test_reset_button_when_off_valid(device_off):
    device_off.reset_call_button()
    assert device_off.get_status()["call_button_active"] == False

# Wifi Tests

def test_connected_wifi(device_on):
    device_on.connect_wifi()

    assert device_on.get_status()["wifi_connected"] == True

def test_disconnect_wifi(device_on):
    device_on.connect_wifi()
    device_on.disconnect_wifi()

    assert device_on.get_status()["wifi_connected"] == False

def test_wifi_when_off_invalid(device_off):
    with pytest.raises(RuntimeError):
        device_off.connect_wifi()

def test_disconnect_wifi_when_off_invalid(device_off):
    with pytest.raises(RuntimeError):
        device_off.disconnect_wifi()

# language Tests

def test_set_language(device_on):
    #happy path: device should set language correctly
    device_on.set_language("es")
    assert device_on.get_status()["language"] == "es"


def test_set_language_invalid(device_on):
    # handles user entering invalid language
    with pytest.raises(ValueError):
        device_on.set_language("invalid_language")

def test_set_language_when_off_invalid(device_off):
    # cannot set language when seat is off
    with pytest.raises(RuntimeError):
        assert device_off.set_language("es")

def test_all_languages_valid(device_on):
    languages = ["en", "fr", "ma", "es"]
    for lang in languages:
        device_on.set_language(lang)
        assert device_on.get_status()["language"] == lang

def test_reboot_resets_state(device_on):
    # reboots should affect volume, channel, brightness and wifi to default
    device_on.set_volume(80)
    device_on.select_channel("Sports")
    device_on.connect_wifi()
    device_on.reboot()
    status = device_on.get_status()
    assert status["powered_on"] == True
    assert status["volume"] == 50
    assert status["current_channel"] is None
    assert status["wifi_connected"] == False
    assert status["brightness"] == 50

def test_reboot_not_change_language(device_on):
    # reboot should not affect language
    device_on.set_language("fr")
    device_on.reboot()
    assert device_on.get_status()["language"] == "fr"

def test_reboot_device_stays_on(device_on):
    #  device should not completely power off after reboot but remain on
    device_on.reboot()
    assert device_on.get_status()["powered_on"] == True
