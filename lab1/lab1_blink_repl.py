"""
Lab 1: Blink + REPL
CYD board: ESP32-2432S028R (original ILI9341 resistive-touch variant)

Goal: no display code yet. Just prove you can talk to the board,
control the onboard RGB LED, and read the light sensor (LDR).

Wiring: NONE. Everything used here is already on the board.

RGB LED pins (active-LOW on most CYD boards -- 0 = on, 1 = off):
    Red   -> GPIO 4
    Green -> GPIO 16
    Blue  -> GPIO 17

LDR (light-dependent resistor) light sensor -> GPIO 34 (ADC, input only)
"""

from machine import Pin, ADC
import time

# --- RGB LED setup ---
# NOTE: many CYD boards wire these active-LOW. If "on" looks backwards
# (LED is lit when you set the pin to 1), flip the ON_VALUE constant below.
ON_VALUE = 0
OFF_VALUE = 1

red = Pin(4, Pin.OUT)
green = Pin(16, Pin.OUT)
blue = Pin(17, Pin.OUT)

leds = {"red": red, "green": green, "blue": blue}


def all_off():
    for pin in leds.values():
        pin.value(OFF_VALUE)


def set_color(name):
    """Turn on exactly one LED by name: 'red', 'green', or 'blue'."""
    all_off()
    if name in leds:
        leds[name].value(ON_VALUE)


# --- Light sensor setup ---
# GPIO 34 is ADC1_CH6 on the ESP32. Input-only pin, no pull resistors.
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)  # full 0-3.3V range


def read_light():
    """Returns a raw ADC reading 0-4095. Lower = darker (depends on wiring)."""
    return ldr.read()


# --- Demo loop ---
# Cycles red -> green -> blue, printing the light sensor value each step.
# This is your checkpoint: if you see the LED cycle AND printed values
# in the Thonny shell, your board, USB cable, and MicroPython install
# are all working correctly.

if __name__ == "__main__":
    colors = ["red", "green", "blue"]
    i = 0
    while True:
        color = colors[i % len(colors)]
        set_color(color)
        light_level = read_light()
        print("LED:", color, "  Light sensor:", light_level)
        time.sleep(1)
        i += 1
