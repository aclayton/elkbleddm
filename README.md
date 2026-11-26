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
led color NAME          Set color by name (red, green, blue, white, yellow,
                        cyan, magenta, purple, orange, pink, teal, warmwhite,
                        coolwhite, black)
led preset NAME         Apply a preset (relax, focus, movie, night, party)
led presets             List available presets
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

Edit the `DEV_MAC` variable in `elkbleddm_common.py` to match your device.
Default: `BE:68:12:00:8E:00`

## Presets

Presets are stored in `~/.config/elkbleddm/presets.json` (created on first use
is not required; built-in defaults ship with the tool). Each preset maps a name
to a `color` and optional `brightness`:

```json
{
  "relax": {"color": "FF7800", "brightness": 60}
}
```

User-defined presets override the built-in defaults of the same name.
