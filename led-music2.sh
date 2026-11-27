#!/bin/bash
# Wrapper script for led-music2 on iomarchy.
# Ensures the dongle (hci1) path is patched before starting.
cd ~/elkbleddm || exit 1
sed -i 's|/org/bluez/hci0|/org/bluez/hci1|g' elkbleddm_common.py 2>/dev/null
exec python3 ./led-music2 "$@"
