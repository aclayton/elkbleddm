"""Shared BLE connection helpers for the ELK-BLEDDM LED controller.

Both `led` and `led-twirl` import from this module so the connection logic and
device constants live in exactly one place.
"""
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import time

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

BUS_NAME = "org.bluez"
DEV_MAC = "BE:68:12:00:8E:00"
DEV_PATH = f"/org/bluez/hci0/dev_{DEV_MAC.replace(':', '_')}"
CHAR_PATH = f"{DEV_PATH}/service0001/char0002"
NOTIFY_CHAR_PATH = f"{DEV_PATH}/service0001/char0004"

SETTLE = 0.35  # ELK-BLEDDM requires 300ms+ between commands

# Built-in firmware effects. Mode numbers are from the SSG1068 / ELK-BLEDOM
# "EFFECTS" effect table (variant-byte 0x07 firmware). Each effect runs inside
# the controller, so crossfades are hardware-interpolated and therefore smooth
# (unlike the software `led-twirl`, which is limited by the 350ms BLE settle
# time and appears to step).
EFFECTS = {
    # Jump effects (discrete color changes, no fade)
    "jump_rgb": 135,
    "jump_rgb_wycm": 136,
    # Crossfade effects (hardware-interpolated, smooth)
    "crossfade_rgb": 137,
    "crossfade_rgb_wycm": 138,
    "crossfade_red": 139,
    "crossfade_green": 140,
    "crossfade_blue": 141,
    "crossfade_yellow": 142,
    "crossfade_cyan": 143,
    "crossfade_magenta": 144,
    "crossfade_white": 145,
    "crossfade_red_green": 146,
    "crossfade_red_blue": 147,
    "crossfade_green_blue": 148,
    # Blink effects
    "blink_rgb_wycm": 149,
    "blink_red": 150,
    "blink_green": 151,
    "blink_blue": 152,
    "blink_yellow": 153,
    "blink_cyan": 154,
    "blink_magenta": 155,
    "blink_white": 156,
}

# Friendly aliases for the most commonly used effects.
EFFECT_ALIASES = {
    "rainbow": "crossfade_rgb_wycm",          # full-rainbow crossfade (smooth)
    "rainbow_rgb": "crossfade_rgb",           # red/green/blue crossfade
    "rainbow_jump": "jump_rgb_wycm",          # full-rainbow jump
    "fade": "crossfade_rgb",
}

bus = dbus.SystemBus()


def resolve_effect(name):
    """Resolve an effect name (or numeric mode) to a firmware mode number."""
    key = str(name).strip().lower()
    if key.isdigit():
        return int(key)
    key = EFFECT_ALIASES.get(key, key)
    if key in EFFECTS:
        return EFFECTS[key]
    raise ValueError(f"unknown effect: {name!r}")


def ensure_connected():
    """Connect to device if not already connected; returns the Device1 object."""
    adapter = dbus.Interface(
        bus.get_object(BUS_NAME, "/org/bluez/hci0"),
        "org.bluez.Adapter1",
    )

    # Try existing device object first
    try:
        dev = bus.get_object(BUS_NAME, DEV_PATH)
        props = dbus.Interface(dev, "org.freedesktop.DBus.Properties")
        if props.Get("org.bluez.Device1", "Connected"):
            return dev
        # Try connecting to existing object
        dbus.Interface(dev, "org.bluez.Device1").Connect()
        time.sleep(1)
        return dev
    except dbus.exceptions.DBusException:
        pass  # Stale or missing - re-discover
    except Exception:
        pass

    # Remove stale device and re-discover
    try:
        adapter.RemoveDevice(DEV_PATH)
    except Exception:
        pass

    adapter.StartDiscovery()
    time.sleep(3)
    adapter.StopDiscovery()

    dev = bus.get_object(BUS_NAME, DEV_PATH)
    dbus.Interface(dev, "org.bluez.Device1").Connect()
    time.sleep(1)
    return dev


def send(data):
    """Send raw bytes to the LED controller write characteristic."""
    char = bus.get_object(BUS_NAME, CHAR_PATH)
    char_iface = dbus.Interface(char, "org.bluez.GattCharacteristic1")
    char_iface.WriteValue(
        dbus.Array(data, signature='y'),
        dbus.Dictionary({}, signature='sv'),
    )


def disconnect():
    """Disconnect from the device (turns the lights off)."""
    try:
        dev = bus.get_object(BUS_NAME, DEV_PATH)
        dbus.Interface(dev, "org.bluez.Device1").Disconnect()
    except Exception:
        pass
