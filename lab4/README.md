# Lab 4: Button UI

**Goal:** Create interactive buttons with tap detection—the closest analog to `onClick` from web development.

---

## Prerequisites

Same as Lab 3:

| File | Purpose |
|------|---------|
| `ili9341.py` | Display driver |
| `xpt2046.py` | Touch driver |

---

## Concepts Covered

- **Hit-Testing** - Detecting if a point is inside a rectangle (what browsers do for you)
- **UI State Management** - Tracking and updating application state
- **Debouncing** - Preventing multiple triggers from a single physical action
- **Separation of Concerns** - Rendering logic vs. interaction logic

---

## The Web Dev Connection

In JavaScript, the browser handles hit-testing automatically:

```javascript
button.addEventListener('click', (e) => {
    // Browser already determined this element was clicked
});
```

In embedded systems, **you** write the hit-testing:

```python
def point_in_button(x, y, btn):
    return (btn["x"] <= x <= btn["x"] + btn["w"] and
            btn["y"] <= y <= btn["y"] + btn["h"])
```

This is the same math the browser does internally—now you understand it!

---

## Running the Lab

1. Open `lab4_button_ui.py` in Thonny
2. Click **Run**
3. Three colored buttons appear at the bottom
4. Tap a button—the "Selected:" text updates

---

## Success Criteria

- [ ] Three buttons visible (RED, GREEN, BLUE)
- [ ] Tapping a button updates the status text
- [ ] Rapid tapping doesn't cause glitchy behavior

---

## Understanding the Code

### Buttons as Data

```python
buttons = [
    {"label": "RED",   "x": 10,  "y": 240, "w": 70, "h": 60, "color": RED},
    {"label": "GREEN", "x": 90,  "y": 240, "w": 70, "h": 60, "color": GREEN},
    {"label": "BLUE",  "x": 170, "y": 240, "w": 70, "h": 60, "color": BLUE},
]
```

This is the same mental model as DOM elements—a list of objects with properties.

### Debouncing

```python
DEBOUNCE_MS = 200  # Ignore repeated triggers

if time.ticks_diff(now, last_touch_time) > DEBOUNCE_MS:
    # Process the tap
    last_touch_time = now
```

A single physical press can register multiple times. Debouncing ensures only the first one counts.

---

## Troubleshooting

<details>
<summary>Buttons don't respond to taps</summary>

Same calibration issue as Lab 3. The touch coordinates may not align with where buttons are drawn.

Test by printing touch coordinates and comparing to button positions.

</details>

<details>
<summary>One tap triggers multiple times</summary>

Increase the debounce delay:
```python
DEBOUNCE_MS = 300  # or 400
```

</details>

<details>
<summary>Wrong button responds</summary>

Check that button `x`, `y`, `w`, `h` values match your screen layout. Remember screen coordinates start at (0,0) in the top-left.

</details>

---

## Extensions

Once the lab works, try these challenges:

1. **Add a fourth button** that clears the selection
2. **Visual feedback** - briefly change button color when tapped
3. **Toggle mode** - tapping the same button deselects it
4. **Counter** - display how many times each button was pressed

---

## Code

See [`lab4_button_ui.py`](lab4_button_ui.py)

---

[← Back to Main README](../README.md)
