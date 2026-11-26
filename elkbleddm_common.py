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

bus = dbus.SystemBus()


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
