"""
Lab 4: Button UI
CYD board: ESP32-2432S028R (original ILI9341 resistive-touch variant)

Goal: draw 2-3 rectangles as "buttons", detect taps inside their bounds,
and change on-screen state. This is the closest analog to onClick/
addEventListener from the JS course -- except YOU write the hit-testing
that the browser normally does for you.

REQUIRED FILES on the board: ili9341.py, xpt2046.py (same as Lab 3)
Wiring: identical to Lab 3.
"""

from machine import Pin, SPI
from ili9341 import Display, color565
from xpt2046 import Touch
import time

backlight = Pin(21, Pin.OUT)
backlight.value(1)

display_spi = SPI(2, baudrate=40000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = Display(
    display_spi, cs=Pin(15), dc=Pin(2), rst=None, width=240, height=320, rotation=90
)

touch_spi = SPI(1, baudrate=2500000, sck=Pin(25), mosi=Pin(32), miso=Pin(39))
touch = Touch(touch_spi, cs=Pin(33), int_pin=Pin(36), int_handler=None)

BLACK = color565(0, 0, 0)
WHITE = color565(255, 255, 255)
GRAY = color565(60, 60, 60)
RED = color565(200, 30, 30)
GREEN = color565(30, 180, 60)
BLUE = color565(30, 80, 200)

X_MIN, X_MAX = 200, 1900
Y_MIN, Y_MAX = 200, 1900


def to_screen_coords(raw_x, raw_y):
    x = int((raw_x - X_MIN) * 240 / (X_MAX - X_MIN))
    y = int((raw_y - Y_MIN) * 320 / (Y_MAX - Y_MIN))
    return max(0, min(239, x)), max(0, min(319, y))


# --- "Buttons" are just dicts describing a rectangle + label + color ---
# This is the same mental model as a list of DOM elements -- we just
# have to do our own hit-testing instead of the browser doing it.
buttons = [
    {"label": "RED", "x": 10, "y": 240, "w": 70, "h": 60, "color": RED},
    {"label": "GREEN", "x": 90, "y": 240, "w": 70, "h": 60, "color": GREEN},
    {"label": "BLUE", "x": 170, "y": 240, "w": 70, "h": 60, "color": BLUE},
]

state = {"selected": None}


def point_in_button(x, y, btn):
    return btn["x"] <= x <= btn["x"] + btn["w"] and btn["y"] <= y <= btn["y"] + btn["h"]


def draw_buttons():
    for btn in buttons:
        display.fill_rectangle(btn["x"], btn["y"], btn["w"], btn["h"], btn["color"])
        display.draw_text8x8(btn["x"] + 10, btn["y"] + 25, btn["label"], WHITE, btn["color"])


def draw_status():
    display.fill_rectangle(0, 0, 240, 100, BLACK)  # clear status area
    if state["selected"]:
        display.draw_text8x8(20, 40, "Selected: " + state["selected"], WHITE, BLACK)
    else:
        display.draw_text8x8(20, 40, "Tap a button below", GRAY, BLACK)


def handle_tap(x, y):
    for btn in buttons:
        if point_in_button(x, y, btn):
            if state["selected"] != btn["label"]:
                state["selected"] = btn["label"]
                draw_status()
            return  # stop after first match, like event bubbling stopping


def main():
    display.clear(BLACK)
    draw_buttons()
    draw_status()

    last_touch_time = 0
    DEBOUNCE_MS = 200  # ignore repeated triggers from one physical press

    while True:
        point = touch.get_touch()
        if point:
            now = time.ticks_ms()
            if time.ticks_diff(now, last_touch_time) > DEBOUNCE_MS:
                raw_x, raw_y = point
                x, y = to_screen_coords(raw_x, raw_y)
                handle_tap(x, y)
                last_touch_time = now
        time.sleep(0.02)


if __name__ == "__main__":
    main()
