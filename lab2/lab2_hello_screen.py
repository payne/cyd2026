"""
Lab 2: Hello, Screen
CYD board: ESP32-2432S028R (original ILI9341 resistive-touch variant)

Goal: draw static text and shapes on the display. No touch yet.

REQUIRED FILES on the board (upload via Thonny BEFORE running this):
    ili9341.py   <- from github.com/rdagger/micropython-ili9341
    xpt2046.py   <- from github.com/rdagger/micropython-ili9341 (not used yet, but upload now)

Display SPI pins (CYD standard wiring -- do not rewire, this is built-in):
    MOSI -> GPIO 13
    MISO -> GPIO 12
    CLK  -> GPIO 14
    CS   -> GPIO 15
    DC   -> GPIO 2
    RST  -> None (tied to EN on most boards; pass None)
    Backlight (LED) -> GPIO 21
"""

from machine import Pin, SPI
from ili9341 import Display, color565
import time

# --- Backlight ---
# Some CYD revisions need this pin driven HIGH to turn the backlight on.
backlight = Pin(21, Pin.OUT)
backlight.value(1)

# --- Display setup ---
spi = SPI(2, baudrate=40000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))

display = Display(
    spi,
    cs=Pin(15),
    dc=Pin(2),
    rst=None,
    width=240,
    height=320,
    rotation=90,  # landscape; try 0/180/270 if your image looks rotated
)

# --- Colors (RGB565 via color565(r, g, b), each 0-255) ---
BLACK = color565(0, 0, 0)
WHITE = color565(255, 255, 255)
RED = color565(255, 0, 0)
GREEN = color565(0, 200, 0)
BLUE = color565(0, 0, 255)
YELLOW = color565(255, 220, 0)


def draw_demo():
    display.clear(BLACK)

    # Title text
    display.draw_text8x8(60, 10, "Hello, CYD!", WHITE, BLACK)

    # A few shapes to prove drawing primitives work
    display.draw_rectangle(20, 40, 100, 60, RED)
    display.fill_rectangle(140, 40, 100, 60, GREEN)
    display.draw_circle(170, 160, 40, BLUE)
    display.fill_circle(60, 160, 40, YELLOW)

    display.draw_text8x8(20, 220, "Shapes drawn OK", WHITE, BLACK)


if __name__ == "__main__":
    draw_demo()
    print("Done. If you see a black screen, check backlight wiring/pin")
    print("and double-check ili9341.py is actually on the board's filesystem.")
