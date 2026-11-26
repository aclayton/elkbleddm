# ELK-BLEDDM LED Controller

Linux CLI controller for SSG1068-based Bluetooth LED backlights (rebadged as ELK-BLEDDM C6, GIPOYENT, etc.).

## Install

```bash
./install.sh
```

## Usage

```
led on                  Turn lights on
led off                 Turn lights off (disconnects BLE)
led color RRGGBB        Set color (e.g. FF0000, 00FF00, 0000FF)
led brightness 0-100    Set brightness
led mode N              Built-in effects
led speed 0-100         Effect speed
led-twirl               Color cycle animation (Ctrl+C to stop)
led-twirl 3             Slower rotation (3 seconds)
```

## Requirements

- Linux with BlueZ
- Python 3
- `python-dbus` and `glib2` (standard on most distros)

## Protocol

Uses the SSG1068 firmware variant of the ELK protocol:
- Service: `0000fff0-0000-1000-8000-00805f9b34fb`
- Write char: `0000fff3-0000-1000-8000-00805f9b34fb`
- Frame format: `7E 07 ... EF` (9-byte frames, variant byte `0x07`)
- 350ms inter-command delay required

## Device MAC

Edit the `DEV_MAC` variable in `led` and `led-twirl` to match your device.
Default: `BE:68:12:00:8E:00`
