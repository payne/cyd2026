# Lab 2: Hello Screen

**Goal:** Initialize the display and draw static text and shapes.

---

## Prerequisites

Upload these files to your board **before** running this lab:

| File | Source |
|------|--------|
| `ili9341.py` | [rdagger/micropython-ili9341](https://github.com/rdagger/micropython-ili9341) |
| `xpt2046.py` | Same repo (upload now for Lab 3) |

---

## Concepts Covered

- **SPI Communication** - Serial Peripheral Interface for fast data transfer
- **Display Initialization** - Setting up resolution, rotation, and backlight
- **RGB565 Color Format** - 16-bit color encoding for embedded displays
- **Drawing Primitives** - Rectangles, circles, and text rendering

---

## Display Pinout (SPI Bus 2)

| Function | GPIO |
|----------|:----:|
| MOSI | 13 |
| MISO | 12 |
| CLK | 14 |
| CS | 15 |
| DC | 2 |
| Backlight | 21 |

---

## Running the Lab

1. Ensure `ili9341.py` is uploaded to the board
2. Open `lab2_hello_screen.py` in Thonny
3. Click **Run**
4. You should see "Hello, CYD!" with colored shapes

---

## Success Criteria

- [ ] Screen is not blank (backlight working)
- [ ] "Hello, CYD!" text visible at top
- [ ] Four shapes visible: red outline rectangle, green filled rectangle, blue outline circle, yellow filled circle

---

## Troubleshooting

<details>
<summary>Screen is completely black</summary>

Check the backlight pin:
```python
backlight = Pin(21, Pin.OUT)
backlight.value(1)  # Must be HIGH
```

</details>

<details>
<summary>Image appears rotated</summary>

Change the `rotation` parameter in the Display constructor:
```python
display = Display(..., rotation=90)  # Try 0, 90, 180, or 270
```

</details>

<details>
<summary>"No module named ili9341"</summary>

The driver file isn't on the board. In Thonny:
1. Open `ili9341.py`
2. File → Save as...
3. Select "MicroPython device"
4. Save as `ili9341.py`

</details>

---

## Code

See [`lab2_hello_screen.py`](lab2_hello_screen.py)

---

[← Back to Main README](../README.md)
