# Lab 3: Touch Echo

**Goal:** Draw dots wherever the user touches the screen—introducing the polling loop pattern.

---

## Prerequisites

Same as Lab 2, plus the touch driver:

| File | Purpose |
|------|---------|
| `ili9341.py` | Display driver |
| `xpt2046.py` | Touch driver |

---

## Concepts Covered

- **Separate SPI Buses** - Touch and display use different buses
- **Polling Loops** - The embedded equivalent of event listeners
- **Coordinate Mapping** - Converting raw ADC values to screen pixels
- **Calibration** - Real hardware requires tuning

---

## Touch Pinout (SPI Bus 1)

| Function | GPIO |
|----------|:----:|
| T_IRQ | 36 |
| T_DIN (MOSI) | 32 |
| T_OUT (MISO) | 39 |
| T_CLK | 25 |
| T_CS | 33 |

> **Important:** Touch is on SPI bus **1**, display is on bus **2**. Mixing these up is the #1 cause of "touch doesn't work."

---

## Running the Lab

1. Ensure both drivers are uploaded
2. Open `lab3_touch_echo.py` in Thonny
3. Click **Run**
4. Touch the screen—dots should appear

---

## Success Criteria

- [ ] Touching the screen draws green dots
- [ ] Raw and screen coordinates print to console
- [ ] Dots appear reasonably close to touch location

---

## Touch Calibration

Every physical panel is slightly different. Default values:

```python
X_MIN, X_MAX = 200, 1900
Y_MIN, Y_MAX = 200, 1900
```

### To Calibrate Your Board

1. Run the lab and touch the **top-left corner**
2. Note the raw X,Y values printed (e.g., `raw: 180, 210`)
3. Touch the **bottom-right corner**
4. Note those values (e.g., `raw: 1850, 1920`)
5. Update the constants:
   ```python
   X_MIN, X_MAX = 180, 1850
   Y_MIN, Y_MAX = 210, 1920
   ```

**This is intentional!** Learning to calibrate hardware is part of embedded development.

---

## Troubleshooting

<details>
<summary>Touch never registers anything</summary>

1. Verify `xpt2046.py` is on the board
2. Check you're using SPI bus **1** for touch (not bus 2)
3. Ensure `int_pin=Pin(36)` matches the T_IRQ pin

</details>

<details>
<summary>Dots appear far from where I touch</summary>

Calibration issue. Follow the calibration steps above to tune your constants.

</details>

<details>
<summary>Touch coordinates are mirrored/flipped</summary>

Your display rotation may not match touch orientation. Try swapping X/Y or inverting the mapping formula.

</details>

---

## Code

See [`lab3_touch_echo.py`](lab3_touch_echo.py)

---

[← Back to Main README](../README.md)
