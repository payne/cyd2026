"""
Lab 3: Touch Echo
CYD board: ESP32-2432S028R (original ILI9341 resistive-touch variant)

Goal: draw a dot wherever the user touches the screen. Introduces the
polling loop pattern -- the embedded equivalent of an event listener.

REQUIRED FILES on the board (same as Lab 2, plus touch driver):
    ili9341.py
    xpt2046.py

Touch SPI pins (separate SPI bus from the display on most CYD boards):
    T_IRQ  -> GPIO 36 (input, tells us when a touch is happening)
    T_DIN  (MOSI) -> GPIO 32
    T_OUT  (MISO) -> GPIO 39
    T_CLK  -> GPIO 25
    T_CS   -> GPIO 33
"""

from machine import Pin, SPI
from ili9341 import Display, color565
from xpt2046 import Touch
import time

# --- Backlight ---
backlight = Pin(21, Pin.OUT)
backlight.value(1)

# --- Display setup (same as Lab 2) ---
display_spi = SPI(2, baudrate=40000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = Display(
    display_spi, cs=Pin(15), dc=Pin(2), rst=None, width=240, height=320, rotation=90
)

# --- Touch setup ---
# NOTE: the touch controller is on a DIFFERENT SPI bus than the display.
# Mixing these up (e.g. wiring touch to bus 2) is the #1 reason students
# get "touch never registers."
touch_spi = SPI(1, baudrate=2500000, sck=Pin(25), mosi=Pin(32), miso=Pin(39))

touch = Touch(
    touch_spi,
    cs=Pin(33),
    int_pin=Pin(36),
    int_handler=None,  # we'll poll manually instead of using interrupts
)

BLACK = color565(0, 0, 0)
WHITE = color565(255, 255, 255)
DOT_COLOR = color565(0, 255, 120)

# --- Calibration ---
# Raw touch ADC values do NOT map 1:1 to screen pixels. These are
# reasonable starting values for a fresh ESP32-2432S028R, but every
# physical panel is slightly different -- see the calibration note
# in the checkpoint/gotchas section of the lab handout.
X_MIN, X_MAX = 200, 1900
Y_MIN, Y_MAX = 200, 1900


def to_screen_coords(raw_x, raw_y):
    """Map raw touch ADC values to screen pixel coordinates."""
    x = int((raw_x - X_MIN) * 240 / (X_MAX - X_MIN))
    y = int((raw_y - Y_MIN) * 320 / (Y_MAX - Y_MIN))
    # clamp so a slightly-off calibration doesn't crash draw calls
    x = max(0, min(239, x))
    y = max(0, min(319, y))
    return x, y


def main():
    display.clear(BLACK)
    display.draw_text8x8(40, 10, "Touch the screen", WHITE, BLACK)

    while True:
        point = touch.get_touch()  # returns None or (raw_x, raw_y)
        if point:
            raw_x, raw_y = point
            x, y = to_screen_coords(raw_x, raw_y)
            display.fill_circle(x, y, 4, DOT_COLOR)
            print("touch at raw:", raw_x, raw_y, " screen:", x, y)
        time.sleep(0.02)  # ~50Hz poll rate, gentle on the CPU


if __name__ == "__main__":
    main()
