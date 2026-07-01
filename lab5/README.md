# Lab 5: Audio Player

**Goal:** Connect a speaker to the CYD and play sounds—from simple tones to WAV file playback.

This lab covers two approaches:
- **Part A:** Simple tones using PWM (just a passive buzzer)
- **Part B:** WAV file playback using I2S (requires an amplifier module)

---

## Prerequisites

Completed Labs 1-4. No additional MicroPython libraries required—audio uses built-in `machine.PWM` and `machine.I2S`.

---

## Concepts Covered

- **PWM for Audio** - Using pulse-width modulation to generate tones
- **I2S Protocol** - Industry-standard digital audio interface
- **WAV File Format** - Understanding PCM audio file structure
- **Binary File I/O** - Reading and parsing binary data in Python

---

## Part A: Simple Tones (PWM)

The easiest way to make sound—no external DAC required.

### Components Needed

| Component | Quantity | Notes |
|-----------|:--------:|-------|
| Passive buzzer | 1 | **Must be passive** (no internal oscillator) |
| Jumper wires | 2 | Male-to-female |

> **Active vs Passive Buzzer:** Active buzzers make a fixed tone when powered. Passive buzzers need a signal to vibrate—that's what we want for variable frequencies.

### Wiring

| Buzzer Pin | CYD Pin |
|------------|---------|
| + (positive) | GPIO 26 |
| - (ground) | GND |

### Running Part A

```python
from lab5_audio_player import play_melody

play_melody()  # Plays a simple tune
```

Or play individual tones:

```python
from lab5_audio_player import play_tone

play_tone(440, 500)   # A4 note for 500ms
play_tone(523, 500)   # C5 note for 500ms
play_tone(0, 200)     # Rest (silence) for 200ms
```

---

## Part B: WAV File Playback (I2S)

For real audio—music, voice, sound effects—you need an I2S DAC or amplifier.

### Components Needed

| Component | Quantity | Notes |
|-----------|:--------:|-------|
| I2S amplifier module | 1 | MAX98357A, PCM5102, or UDA1334A |
| Small speaker | 1 | 4Ω or 8Ω, 2-3W |
| Jumper wires | 5 | Male-to-female |

<details>
<summary><strong>Which I2S Module Should I Buy?</strong></summary>

| Module | Price | Notes |
|--------|:-----:|-------|
| **MAX98357A** | ~$3-5 | Mono, built-in 3W amp, most common choice |
| **PCM5102** | ~$5-8 | Stereo, high quality, needs separate amp for speaker |
| **UDA1334A** | ~$4-6 | Stereo, good balance of quality and simplicity |

For beginners, the **MAX98357A** is recommended—it's a complete solution with amplifier included.

</details>

### Wiring (MAX98357A)

| MAX98357A Pin | CYD Pin | Notes |
|---------------|---------|-------|
| BCLK | GPIO 26 | Bit clock |
| LRC | GPIO 27 | Left/Right clock (word select) |
| DIN | GPIO 22 | Data input |
| VIN | 5V | Power (can also use 3.3V) |
| GND | GND | Ground |

Connect your speaker to the **+** and **-** terminals on the MAX98357A.

<details>
<summary><strong>Pin Conflict Note</strong></summary>

The original wiring used GPIO 25 for LRC, but GPIO 25 is shared with the touch controller's T_CLK. We use GPIO 27 instead to avoid conflicts.

If you need both touch AND audio simultaneously, this works. If you're only using audio (no touch), you could use GPIO 25.

</details>

### Preparing a WAV File

Your WAV file must be:
- **PCM format** (uncompressed)
- **16-bit**
- **Mono** (recommended) or stereo
- **8000-44100 Hz** sample rate (16000 Hz recommended for small files)

<details>
<summary><strong>Converting Audio Files</strong></summary>

Use [Audacity](https://www.audacityteam.org/) (free) or FFmpeg:

**Audacity:**
1. Open your audio file
2. Tracks → Mix → Mix Stereo Down to Mono
3. Tracks → Resample → 16000 Hz
4. File → Export → Export as WAV
5. Select "Signed 16-bit PCM"

**FFmpeg (command line):**
```bash
ffmpeg -i input.mp3 -ar 16000 -ac 1 -acodec pcm_s16le output.wav
```

</details>

<details>
<summary><strong>Uploading WAV Files to the Board</strong></summary>

In Thonny:
1. **View → Files** to show the file browser
2. Navigate to your WAV file on your computer
3. Right-click → **Upload to /**
4. Verify it appears in the MicroPython device files

**File size warning:** The ESP32 has limited flash. Keep WAV files under 500KB. For longer audio, use lower sample rates (8000 Hz) or external SD card storage.

</details>

### Running Part B

**Option 1: Generate a test tone file**
```python
from lab5_audio_player import generate_test_wav, play_wav

generate_test_wav()           # Creates test_tone.wav on the board
play_wav('test_tone.wav')     # Play it
```

**Option 2: Play your own WAV file**
```python
from lab5_audio_player import play_wav

play_wav('mysound.wav')       # Your uploaded file
```

---

## Success Criteria

### Part A (PWM Tones)
- [ ] Buzzer plays the melody
- [ ] Different frequencies produce different pitches
- [ ] `play_tone(440, 1000)` plays a clear A4 note

### Part B (I2S WAV Playback)
- [ ] `generate_test_wav()` creates a file without errors
- [ ] `play_wav('test_tone.wav')` produces audible sound
- [ ] WAV file info prints correctly (channels, sample rate, bits)

---

## Troubleshooting

<details>
<summary><strong>No sound from passive buzzer</strong></summary>

1. **Check polarity** - Some passive buzzers are polarized
2. **Verify it's passive** - Active buzzers won't respond to PWM frequencies
3. **Try a different GPIO** - GPIO 26 might be in use; try GPIO 27
4. **Test the buzzer** - Connect directly to 3.3V briefly; passive buzzers make a click, active buzzers beep

</details>

<details>
<summary><strong>No sound from I2S amplifier</strong></summary>

1. **Check wiring** - BCLK, LRC, DIN must be correct
2. **Verify power** - Module needs 3.3V or 5V on VIN
3. **Check speaker connection** - Ensure speaker is connected to amp output terminals
4. **Volume** - Some modules have a gain pin; try connecting GAIN to VIN for max volume
5. **Print debug info** - Ensure `play_wav` shows correct WAV parameters

</details>

<details>
<summary><strong>"Not a valid WAV file" error</strong></summary>

The file isn't in the correct format. Ensure:
- It's a `.wav` file (not `.mp3`, `.ogg`, etc.)
- It's PCM encoded (not compressed WAV)
- Use Audacity or FFmpeg to re-export as "Signed 16-bit PCM"

</details>

<details>
<summary><strong>Audio plays but sounds distorted</strong></summary>

1. **Sample rate mismatch** - The code auto-detects sample rate, but verify your WAV file's rate is standard (8000, 16000, 22050, 44100)
2. **Speaker too small** - Very small speakers distort at high volume
3. **Power issue** - The amplifier may need more current; try powering from 5V instead of 3.3V

</details>

<details>
<summary><strong>Audio plays too fast or too slow</strong></summary>

Sample rate mismatch. Check what sample rate your WAV file actually is (the code prints this) and ensure it matches what the I2S is configured for.

</details>

<details>
<summary><strong>OSError: [Errno 2] ENOENT</strong></summary>

File not found. Ensure:
1. The WAV file is uploaded to the board's root filesystem
2. The filename matches exactly (case-sensitive)
3. Use `import os; os.listdir()` to see files on the board

</details>

---

## Understanding the Code

### PWM Tone Generation

```python
buzzer = PWM(Pin(26))
buzzer.freq(440)      # Set frequency to 440Hz (A4 note)
buzzer.duty(512)      # 50% duty cycle (loudest)
time.sleep_ms(500)    # Play for 500ms
buzzer.deinit()       # Stop
```

PWM rapidly switches the pin on/off. The frequency determines the pitch; the duty cycle affects volume (50% = loudest).

### I2S Audio Streaming

```python
audio_out = I2S(
    0,                    # I2S peripheral ID
    sck=Pin(26),          # Bit clock
    ws=Pin(27),           # Word select (L/R)
    sd=Pin(22),           # Serial data
    mode=I2S.TX,          # We're transmitting
    bits=16,              # 16-bit samples
    format=I2S.MONO,      # Mono audio
    rate=16000,           # 16kHz sample rate
    ibuf=4096,            # Internal buffer size
)

audio_out.write(audio_data)  # Send audio bytes
```

I2S streams digital audio data to the amplifier, which converts it to an analog signal for the speaker.

### WAV File Structure

```
RIFF header (12 bytes)
├── "RIFF" marker
├── File size
└── "WAVE" marker

fmt chunk (24 bytes)
├── Audio format (1 = PCM)
├── Number of channels
├── Sample rate
└── Bits per sample

data chunk (variable)
├── Data size
└── Raw audio samples...
```

The code parses this header to configure I2S with the correct parameters.

---

## Extensions

1. **Touch-triggered sounds** - Combine with Lab 4 to play different sounds when buttons are tapped
2. **Volume control** - Add a slider UI to control PWM duty cycle or amplifier gain
3. **Sound effects library** - Upload multiple short WAV files and trigger them based on events
4. **Tone sequencer** - Create a simple music composition tool using the touch screen

---

## Code

See [`lab5_audio_player.py`](lab5_audio_player.py)

---

[← Back to Main README](../README.md)
