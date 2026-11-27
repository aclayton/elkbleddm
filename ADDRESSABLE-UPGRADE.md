# Addressable LED Strip Upgrade Guide

The current ELK-BLEDDM (SSG1068) controller drives an **analog 4-pin RGB strip**
— the entire strip is one colour at a time. No per-pixel control.

To get individual LED control you need:
1. A **WS2812B** (or similar) addressable strip — 3-wire: +5V, GND, DATA
2. A controller that speaks the WS2812 protocol over WiFi/BLE

---

## Prebuilt Controllers (no soldering)

| Option | Price | Notes |
|---|---|---|
| **GLEDOPTO WLED controller** | ~$12-15 (AliExpress) | ESP32 with mic, WiFi, runs WLED out of the box. 5-24V. Best value prebuilt. |
| **SP110E USB Bluetooth** | ~$8-10 (AliExpress) | Basic Bluetooth app control, addressable strips. No WiFi/WLED. Simplest. |
| **Athom WLED controller** | ~$18-20 | Pre-flashed WLED, solid build quality, WiFi + mic. |

## What You Also Need

| Item | Price | Notes |
|---|---|---|
| **WS2812B LED strip** | ~$8-15 (1m/60 LEDs) | 5V, 3-wire. 30/60/144 LEDs per metre. |
| **WS2812B LED strip** | ~$20 (5m/150 LEDs) | Longer run — needs power injection at far end. |
| **5V power supply** | ~$5 | USB-C brick works for short strips (<1m). Dedicated PSU for longer. |

**Total: ~$20-35** for a complete addressable setup.

---

## Recommendation

**GLEDOPTO ESP32 WLED controller + WS2812B strip** (~$25 total).

WLED has:
- 100+ built-in effects (chase, comet, fire, aurora, …)
- Music reactivity via onboard microphone
- WiFi control + JSON HTTP API
- Scriptable from Linux — same pattern as `led-music` / `led-music2`
- Per-LED effects: spectrum analyser split across the strip, beat-triggered
  segments, colour-wheel chases synced to audio

## WLED JSON API (preview)

```bash
# Set all LEDs to red
curl -X POST http://wled-ip/json/state -d '{"on":true,"bri":128,"seg":[{"col":[[255,0,0]]}]}'

# Set effect to "Chase"
curl -X POST http://wled-ip/json/state -d '{"on":true,"seg":[{"fx":28,"sx":128}]}'

# Get current state
curl http://wled-ip/json/state
```

The same audio analysis code from `led-music` can drive per-segment colours through
this API — each bass/mid/treble band mapping to different regions of the strip.
