# CYD MicroPython Beginner Unit

A hands-on curriculum for learning embedded systems programming with the **Cheap Yellow Display (CYD)** ESP32 board using MicroPython.

> **Target Board:** ESP32-2432S028R (ILI9341 display with resistive touch)

---

## Table of Contents

- [Overview](#overview)
- [Hardware Requirements](#hardware-requirements)
- [Software Setup](#software-setup)
- [Curriculum Labs](#curriculum-labs)
  - [Lab 1: Blink + REPL](#lab-1-blink--repl)
  - [Lab 2: Hello Screen](#lab-2-hello-screen)
  - [Lab 3: Touch Echo](#lab-3-touch-echo)
  - [Lab 4: Button UI](#lab-4-button-ui)
  - [Lab 5: Audio Player](#lab-5-audio-player)
- [Resources](#resources)
- [Advanced: LVGL MicroPython](#advanced-lvgl-micropython)
- [Community](#community)

---

## Overview

This curriculum bridges **web development concepts** to **embedded programming**. Students familiar with JavaScript event listeners will learn how those patterns translate to hardware polling loops and manual hit-testing.

### Learning Progression

| Lab | Topic | Key Concepts |
|:---:|-------|--------------|
| 1 | Blink + REPL | GPIO, ADC, serial communication |
| 2 | Hello Screen | SPI displays, drawing primitives |
| 3 | Touch Echo | Polling loops, coordinate mapping |
| 4 | Button UI | Hit-testing, state management |
| 5 | Audio Player | PWM tones, I2S protocol, WAV files |

---

## Hardware Requirements

<details>
<summary><strong>Required Components</strong></summary>

| Component | Quantity | Notes |
|-----------|:--------:|-------|
| ESP32-2432S028R (CYD) | 1 | 2.8" ILI9341 resistive touch variant |
| USB-A to Micro-USB cable | 1 | **Data cable**, not charge-only |
| Computer with USB port | 1 | Windows, macOS, or Linux |

</details>

<details>
<summary><strong>Which CYD Should I Buy?</strong></summary>

The **ESP32-2432S028R** is the recommended starting board:
- 2.8" ILI9341 display
- Resistive touch (more forgiving for beginners)
- Onboard RGB LED and light sensor
- Well-documented pinouts

See the community discussion: [Best CYD to Buy (Reddit)](https://www.reddit.com/r/esp32/comments/1rla17j/best_cyd_to_buy/)

**Avoid** boards with capacitive touch for this curriculum—the touch driver differs.

</details>

<details>
<summary><strong>CYD Board Pinout Reference</strong></summary>

### Display (SPI Bus 2)
| Function | GPIO |
|----------|:----:|
| MOSI | 13 |
| MISO | 12 |
| CLK | 14 |
| CS | 15 |
| DC | 2 |
| Backlight | 21 |

### Touch (SPI Bus 1)
| Function | GPIO |
|----------|:----:|
| T_IRQ | 36 |
| T_DIN (MOSI) | 32 |
| T_OUT (MISO) | 39 |
| T_CLK | 25 |
| T_CS | 33 |

### Onboard Peripherals
| Component | GPIO |
|-----------|:----:|
| Red LED | 4 |
| Green LED | 16 |
| Blue LED | 17 |
| LDR (Light Sensor) | 34 |

> **Note:** RGB LEDs are typically **active-LOW** (0 = on, 1 = off)

</details>

---

## Software Setup

<details>
<summary><strong>Step 1: Install Thonny IDE</strong></summary>

1. Download [Thonny](https://thonny.org/) for your operating system
2. Install and launch Thonny
3. Go to **Tools → Options → Interpreter**
4. Select **MicroPython (ESP32)**
5. Click **Install or update MicroPython**

</details>

<details>
<summary><strong>Step 2: Flash MicroPython Firmware</strong></summary>

1. Download the latest ESP32 MicroPython firmware from [micropython.org](https://micropython.org/download/esp32/)
2. In Thonny: **Tools → Options → Interpreter → Install or update MicroPython**
3. Select your board's COM/serial port
4. Choose the downloaded `.bin` firmware file
5. Click **Install**

> **Troubleshooting:** If the board isn't detected, you may need [CP210x drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) or [CH340 drivers](https://sparks.gogo.co.nz/ch340.html)

</details>

<details>
<summary><strong>Step 3: Upload Required Libraries</strong></summary>

Before Labs 2-4, upload these files to the board's filesystem:

1. **ili9341.py** - Display driver
2. **xpt2046.py** - Touch driver

Download from: [rdagger/micropython-ili9341](https://github.com/rdagger/micropython-ili9341)

In Thonny:
1. Open the `.py` file
2. **File → Save as...**
3. Select **MicroPython device**
4. Save with the same filename

</details>

---

## Curriculum Labs

### Lab 1: Blink + REPL

**Goal:** Verify board connectivity, control the onboard RGB LED, and read the light sensor.

<details>
<summary><strong>What You'll Learn</strong></summary>

- Using the REPL (Read-Eval-Print Loop) for interactive testing
- GPIO output for controlling LEDs
- ADC input for reading analog sensors
- Active-LOW vs active-HIGH logic

</details>

<details>
<summary><strong>Checkpoints</strong></summary>

- [ ] Board connects to Thonny without errors
- [ ] RGB LED cycles through red, green, blue
- [ ] Light sensor values print to the console
- [ ] Covering the sensor changes the printed values

</details>

<details>
<summary><strong>Common Gotchas</strong></summary>

| Problem | Solution |
|---------|----------|
| LED colors appear inverted | Change `ON_VALUE = 0` to `ON_VALUE = 1` |
| "No module named machine" | Board isn't running MicroPython—reflash firmware |
| Serial port not found | Try a different USB cable (must be data-capable) |

</details>

**Code:** [`lab1/lab1_blink_repl.py`](lab1/lab1_blink_repl.py)

---

### Lab 2: Hello Screen

**Goal:** Initialize the display and draw static text and shapes.

<details>
<summary><strong>What You'll Learn</strong></summary>

- SPI bus configuration
- Display initialization and rotation
- RGB565 color format
- Drawing primitives (rectangles, circles, text)

</details>

<details>
<summary><strong>Checkpoints</strong></summary>

- [ ] Screen displays "Hello, CYD!" text
- [ ] Colored shapes are visible (red rectangle, green filled rectangle, blue circle, yellow filled circle)
- [ ] No white/garbled screen

</details>

<details>
<summary><strong>Common Gotchas</strong></summary>

| Problem | Solution |
|---------|----------|
| Black/blank screen | Check backlight pin (GPIO 21) is set HIGH |
| "No module named ili9341" | Upload `ili9341.py` to the board first |
| Image is rotated | Change `rotation=` parameter (try 0, 90, 180, 270) |
| Garbled display | Verify SPI baudrate (40MHz) and pin assignments |

</details>

**Code:** [`lab2/lab2_hello_screen.py`](lab2/lab2_hello_screen.py)

---

### Lab 3: Touch Echo

**Goal:** Draw dots wherever the user touches the screen—introducing the polling loop pattern.

<details>
<summary><strong>What You'll Learn</strong></summary>

- Touch controller setup (separate SPI bus)
- Polling loops (the embedded equivalent of event listeners)
- Coordinate mapping and calibration
- Raw ADC values vs screen pixels

</details>

<details>
<summary><strong>Checkpoints</strong></summary>

- [ ] Touching the screen draws colored dots
- [ ] Touch coordinates print to the console
- [ ] Dots appear reasonably close to where you touch

</details>

<details>
<summary><strong>Common Gotchas</strong></summary>

| Problem | Solution |
|---------|----------|
| Touch never registers | Touch is on SPI bus **1**, display is on bus **2**—don't mix them |
| Dots appear offset from touch | Adjust calibration constants (`X_MIN`, `X_MAX`, `Y_MIN`, `Y_MAX`) |
| Touch works but is mirrored | Check `rotation` parameter matches display rotation |

</details>

<details>
<summary><strong>Touch Calibration</strong></summary>

Every physical panel has slightly different touch calibration. The default values work for most boards:

```python
X_MIN, X_MAX = 200, 1900
Y_MIN, Y_MAX = 200, 1900
```

**To calibrate your specific board:**
1. Run the lab and touch the **top-left corner**
2. Note the raw X,Y values printed
3. Touch the **bottom-right corner**
4. Note those raw values
5. Update the constants accordingly

This is intentionally a teaching moment—real hardware requires calibration!

</details>

**Code:** [`lab3/lab3_touch_echo.py`](lab3/lab3_touch_echo.py)

---

### Lab 4: Button UI

**Goal:** Create interactive buttons with tap detection—the closest analog to `onClick` from web development.

<details>
<summary><strong>What You'll Learn</strong></summary>

- Hit-testing (what browsers do automatically, you write manually)
- UI state management
- Debouncing touch input
- Separating rendering from logic

</details>

<details>
<summary><strong>Checkpoints</strong></summary>

- [ ] Three colored buttons appear at the bottom of the screen
- [ ] Tapping a button updates the "Selected:" text
- [ ] Rapid taps don't cause glitchy behavior (debouncing works)

</details>

<details>
<summary><strong>Common Gotchas</strong></summary>

| Problem | Solution |
|---------|----------|
| Buttons don't respond | Same calibration issue as Lab 3—verify touch coordinates |
| Multiple triggers per tap | Increase `DEBOUNCE_MS` (try 300-400) |
| Wrong button registers | Check button `x`, `y`, `w`, `h` values match screen layout |

</details>

<details>
<summary><strong>Understanding Hit-Testing</strong></summary>

In web development, the browser handles hit-testing automatically:

```javascript
button.addEventListener('click', handler);
```

In embedded systems, **you** implement the hit-testing:

```python
def point_in_button(x, y, btn):
    return (btn["x"] <= x <= btn["x"] + btn["w"] and
            btn["y"] <= y <= btn["y"] + btn["h"])
```

This is the same math the browser does internally—now you understand it!

</details>

**Code:** [`lab4/lab4_button_ui.py`](lab4/lab4_button_ui.py)

---

### Lab 5: Audio Player

**Goal:** Connect a speaker to the CYD and play sounds—from simple tones to WAV file playback.

<details>
<summary><strong>What You'll Learn</strong></summary>

- PWM for generating tones (no external hardware needed beyond a buzzer)
- I2S digital audio protocol
- WAV file format and binary parsing
- Connecting external amplifier modules

</details>

<details>
<summary><strong>Hardware Options</strong></summary>

**Option A: Simple Tones (PWM)**
| Component | Notes |
|-----------|-------|
| Passive buzzer | Must be passive, not active |

**Option B: WAV Playback (I2S)**
| Component | Notes |
|-----------|-------|
| I2S amplifier | MAX98357A recommended |
| Small speaker | 4Ω or 8Ω, 2-3W |

</details>

<details>
<summary><strong>Wiring (I2S Amplifier)</strong></summary>

| MAX98357A | CYD GPIO |
|-----------|:--------:|
| BCLK | 26 |
| LRC | 27 |
| DIN | 22 |
| VIN | 5V |
| GND | GND |

</details>

<details>
<summary><strong>Checkpoints</strong></summary>

- [ ] Passive buzzer plays melody via PWM
- [ ] I2S amplifier produces sound
- [ ] WAV file plays with correct pitch and speed

</details>

<details>
<summary><strong>Common Gotchas</strong></summary>

| Problem | Solution |
|---------|----------|
| No sound from buzzer | Ensure it's a **passive** buzzer (active buzzers won't respond to PWM) |
| No sound from I2S amp | Check BCLK/LRC/DIN wiring; verify 5V power |
| "Not a valid WAV file" | Re-export as 16-bit PCM WAV (not compressed) |
| Audio too fast/slow | Sample rate mismatch—check WAV file properties |

</details>

**Code:** [`lab5/lab5_audio_player.py`](lab5/lab5_audio_player.py)

---

## Resources

### Official Documentation

- [MicroPython ESP32 Quick Reference](https://docs.micropython.org/en/latest/esp32/quickref.html)
- [ILI9341 Display Driver (rdagger)](https://github.com/rdagger/micropython-ili9341)
- [Thonny IDE](https://thonny.org/)

### Tutorials & Guides

- [Total Beginner's Guide to Using a Cheap Yellow Display](https://www.reddit.com/r/Esphome/comments/1knxi21/total_beginners_guide_to_using_a_cheap_yellow/) - Comprehensive walkthrough for first-time CYD users

### Curriculum Document

The complete curriculum with parts lists, checkpoints, and detailed instructions is available in:
- [`CYD-MicroPython-Beginner-Unit.docx`](CYD-MicroPython-Beginner-Unit.docx)

---

## Advanced: LVGL MicroPython

Once you've completed the basic labs, you may want to explore **LVGL** (Light and Versatile Graphics Library)—a professional-grade UI framework that provides widgets, animations, and touch handling out of the box.

> **Note:** This is an advanced topic. Complete Labs 1-4 first to understand the fundamentals before moving to LVGL.

<details>
<summary><strong>Why LVGL?</strong></summary>

The basic labs teach you to write your own hit-testing and drawing code. LVGL provides:

- **Pre-built widgets** - Buttons, sliders, charts, keyboards, etc.
- **Automatic touch handling** - No manual hit-testing required
- **Animations and themes** - Professional-looking UIs
- **Better performance** - Optimized rendering with partial screen updates

The tradeoff: LVGL requires custom firmware (larger binary) and has a steeper learning curve.

</details>

<details>
<summary><strong>Step 1: Identify Your Exact Board Variant</strong></summary>

**Critical first step.** CYD boards vary significantly:

| Variant | Processor | Display | Touch |
|---------|-----------|---------|-------|
| ESP32-2432S028R | ESP32-D0WD | ILI9341 | XPT2046 (resistive) |
| ESP32-2432S028C | ESP32-D0WD | ILI9341 | Capacitive |
| ESP32-S3 variants | ESP32-S3 | ST7789 or ILI9341 | Various |

Check the chip markings on the back of your board. There are at least 3-4 "CYD" sub-variants with different pin mappings.

**Pin reference for confirmation:** [rzeldent/esp32-smartdisplay](https://github.com/rzeldent/esp32-smartdisplay) — even though it targets a different framework, the pin definitions are reliable for cross-referencing.

</details>

<details>
<summary><strong>Step 2: Check for Prebuilt Firmware (Recommended)</strong></summary>

Before building from source, search for **prebuilt lv_micropython `.bin` files for CYD**. Community members have already built firmware for common CYD variants.

Search terms:
- `lv_micropython CYD bin`
- `lv_micropython ESP32-2432S028 firmware`
- `LVGL MicroPython CYD prebuilt`

This can save significant toolchain setup time, especially if you're working with multiple board variants.

</details>

<details>
<summary><strong>Step 3: Build Environment Setup (If Building from Source)</strong></summary>

```bash
# Clone lv_micropython
git clone https://github.com/lvgl/lv_micropython.git
cd lv_micropython
git submodule update --init --recursive lib/lv_bindings
```

You'll need the ESP-IDF toolchain:
1. Install [ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/) (check lv_micropython README for supported version—v4.x or v5.x)
2. Source the export script: `source $IDF_PATH/export.sh`

</details>

<details>
<summary><strong>Step 4: Board Configuration</strong></summary>

lv_micropython needs a board manifest that configures:
- SPI pins for the ILI9341 display
- SPI pins for the XPT2046 touch (often a separate bus)
- Backlight pin
- Display rotation/mirroring settings

**Finding a config:**
- Search GitHub for `lv_micropython CYD` or `lv_micropython ESP32-2432S028`
- Check [lvgl/lv_micropython](https://github.com/lvgl/lv_micropython) issues and discussions
- Use the [CYD Board Pinout Reference](#cyd-board-pinout-reference) above to verify pin assignments

Place your board manifest in `boards/` in your lv_micropython clone.

</details>

<details>
<summary><strong>Step 5: Build and Flash</strong></summary>

**Build:**
```bash
make -C ports/esp32 BOARD=YOUR_CYD_BOARD submodules
make -C ports/esp32 BOARD=YOUR_CYD_BOARD
```

**Flash (erase first—CYDs often have factory demo firmware that can cause issues):**
```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 build-YOUR_CYD_BOARD/firmware.bin
```

On macOS, the port is typically `/dev/cu.usbserial-*` or `/dev/cu.SLAB_USBtoUART`.

</details>

<details>
<summary><strong>Step 6: Verify LVGL from REPL</strong></summary>

```python
import lvgl as lv
import ili9XXX  # or whatever display driver your board config provides
import xpt2046

lv.init()

# Initialize display driver (per your board config's example)
# Initialize touch driver

# Create a simple button to test
scr = lv.scr_act()
btn = lv.btn(scr)
btn.center()
label = lv.label(btn)
label.set_text("Hello CYD")
```

If the button renders and touch registers, you're ready to build real LVGL applications.

</details>

<details>
<summary><strong>LVGL Resources</strong></summary>

- [LVGL Documentation](https://docs.lvgl.io/)
- [lv_micropython Repository](https://github.com/lvgl/lv_micropython)
- [LVGL MicroPython Examples](https://github.com/lvgl/lv_micropython/tree/master/examples)
- [rzeldent/esp32-smartdisplay](https://github.com/rzeldent/esp32-smartdisplay) — Pin reference for CYD variants

</details>

---

## Community

### Reddit Communities

| Subreddit | Description |
|-----------|-------------|
| [r/CheapYellowDisplay](https://www.reddit.com/r/CheapYellowDisplay/) | Dedicated CYD community—projects, troubleshooting, inspiration |
| [r/esp32](https://www.reddit.com/r/esp32/) | General ESP32 discussion |
| [r/Esphome](https://www.reddit.com/r/Esphome/) | ESPHome projects (alternative firmware) |

### Recommended Threads

- [Best CYD to Buy](https://www.reddit.com/r/esp32/comments/1rla17j/best_cyd_to_buy/) - Community recommendations on which board to purchase
- [ESP32 CYD PDA Updates and New Functions](https://www.reddit.com/r/CheapYellowDisplay/comments/1txmgkg/esp32_cyd_pda_updates_and_new_functions/) - Advanced project inspiration

---

## License

This curriculum is provided for educational use. Feel free to adapt for your classroom.

---

<p align="center">
  <em>Built for hands-on learning at the intersection of web development and embedded systems.</em>
</p>
