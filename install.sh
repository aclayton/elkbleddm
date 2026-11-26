#!/usr/bin/env bash
set -e

BIN_DIR="${HOME}/.local/bin"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing ELK-BLEDDM LED controller scripts to ${BIN_DIR}..."

mkdir -p "${BIN_DIR}"

install -m 755 "${SCRIPT_DIR}/led" "${BIN_DIR}/led"
install -m 755 "${SCRIPT_DIR}/led-twirl" "${BIN_DIR}/led-twirl"
install -m 644 "${SCRIPT_DIR}/elkbleddm_common.py" "${BIN_DIR}/elkbleddm_common.py"

# Check if ~/.local/bin is in PATH
if ! echo "${PATH}" | grep -q "${BIN_DIR}"; then
    echo ""
    echo "NOTE: ${BIN_DIR} is not in your PATH."
    echo "Add this to your ~/.bashrc or ~/.zshrc:"
    echo '  export PATH="${HOME}/.local/bin:${PATH}"'
fi

echo ""
echo "Installed! Usage:"
echo "  led on              Turn lights on"
echo "  led off             Turn lights off"
echo "  led color FF0000    Set color (hex RGB)"
echo "  led brightness 50   Set brightness (0-100)"
echo "  led mode 3          Set built-in effect"
echo "  led speed 50        Set effect speed (0-100)"
echo "  led-twirl           Color cycle animation (Ctrl+C to stop)"
echo ""
echo "Requirements: python3, python-dbus, glib2 (already on most Linux systems)"
