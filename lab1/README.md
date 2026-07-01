# Lab 1: Blink + REPL

**Goal:** Verify board connectivity, control the onboard RGB LED, and read the light sensor.

No display code yet—just prove you can talk to the board.

---

## Wiring

**None required.** Everything used in this lab is already on the board.

---

## Concepts Covered

- **REPL** (Read-Eval-Print Loop) - Interactive Python shell over serial
- **GPIO Output** - Controlling pins to turn LEDs on/off
- **ADC Input** - Reading analog values from sensors
- **Active-LOW Logic** - When 0 means "on" and 1 means "off"

---

## Hardware Used

| Component | GPIO | Notes |
|-----------|:----:|-------|
| Red LED | 4 | Active-LOW |
| Green LED | 16 | Active-LOW |
| Blue LED | 17 | Active-LOW |
| Light Sensor (LDR) | 34 | ADC input, 0-4095 range |

---

## Running the Lab

1. Open `lab1_blink_repl.py` in Thonny
2. Click the **Run** button (or press F5)
3. Watch the RGB LED cycle through colors
4. Observe light sensor values in the Shell

---

## Success Criteria

- [ ] LED cycles: red → green → blue
- [ ] Light sensor values print every second
- [ ] Covering the sensor changes the readings

---

## Code

See [`lab1_blink_repl.py`](lab1_blink_repl.py)

---

[← Back to Main README](../README.md)
