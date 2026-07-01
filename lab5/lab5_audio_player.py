"""
Lab 5: Audio Player
CYD board: ESP32-2432S028R (original ILI9341 resistive-touch variant)

Goal: Connect a speaker to the CYD and play audio. This lab covers two
approaches: simple tones via PWM, and WAV file playback via I2S.

WIRING (I2S amplifier - MAX98357A or similar):
    BCLK  -> GPIO 26
    LRC   -> GPIO 25  (shared with touch T_CLK - see note below)
    DIN   -> GPIO 22
    VIN   -> 3.3V or 5V (check your amplifier's specs)
    GND   -> GND

IMPORTANT: GPIO 25 is also used by the touch controller's T_CLK. If you
need touch AND audio simultaneously, use GPIO 27 for LRC instead and
update the pin assignment below. For this lab, we disable touch to
keep wiring simple.

ALTERNATIVE WIRING (simple passive buzzer via PWM):
    Buzzer + -> GPIO 26
    Buzzer - -> GND
"""

from machine import Pin, PWM, I2S
import time
import struct

# =============================================================================
# PART A: Simple Tones with PWM (no external DAC needed)
# =============================================================================
# Use this with a passive buzzer or small speaker directly connected.
# Active buzzers won't work (they have their own oscillator).

BUZZER_PIN = 26


def play_tone(frequency, duration_ms, pin=BUZZER_PIN):
    """Play a tone at the given frequency for duration_ms milliseconds."""
    if frequency == 0:
        time.sleep_ms(duration_ms)
        return

    buzzer = PWM(Pin(pin))
    buzzer.freq(frequency)
    buzzer.duty(512)  # 50% duty cycle
    time.sleep_ms(duration_ms)
    buzzer.deinit()


def play_melody():
    """Play a simple melody to test the buzzer."""
    # Note frequencies (Hz) - 0 means rest
    C4 = 262
    D4 = 294
    E4 = 330
    F4 = 349
    G4 = 392
    A4 = 440
    B4 = 494
    C5 = 523
    REST = 0

    # Simple melody: each tuple is (frequency, duration_ms)
    melody = [
        (C4, 200), (D4, 200), (E4, 200), (F4, 200),
        (G4, 400), (G4, 400),
        (A4, 200), (A4, 200), (A4, 200), (A4, 200),
        (G4, 800),
        (A4, 200), (A4, 200), (A4, 200), (A4, 200),
        (G4, 800),
        (F4, 200), (F4, 200), (F4, 200), (F4, 200),
        (E4, 400), (E4, 400),
        (D4, 200), (D4, 200), (D4, 200), (D4, 200),
        (C4, 800),
    ]

    print("Playing melody...")
    for freq, dur in melody:
        play_tone(freq, dur)
        time.sleep_ms(50)  # Small gap between notes
    print("Done!")


# =============================================================================
# PART B: WAV File Playback with I2S (requires I2S DAC/amplifier)
# =============================================================================
# Use this with an I2S amplifier board like MAX98357A, PCM5102, or UDA1334A.

I2S_SCK_PIN = 26   # BCLK (bit clock)
I2S_WS_PIN = 27    # LRC/LRCK (word select) - using 27 to avoid touch conflict
I2S_SD_PIN = 22    # DIN (serial data out)

# I2S configuration for common WAV files
SAMPLE_RATE = 16000
BITS_PER_SAMPLE = 16
BUFFER_SIZE = 4096


def init_i2s():
    """Initialize I2S peripheral for audio output."""
    audio_out = I2S(
        0,                          # I2S peripheral ID
        sck=Pin(I2S_SCK_PIN),       # Bit clock
        ws=Pin(I2S_WS_PIN),         # Word select (left/right clock)
        sd=Pin(I2S_SD_PIN),         # Serial data
        mode=I2S.TX,                # Transmit mode
        bits=BITS_PER_SAMPLE,
        format=I2S.MONO,            # or I2S.STEREO for stereo files
        rate=SAMPLE_RATE,
        ibuf=BUFFER_SIZE,
    )
    return audio_out


def parse_wav_header(file):
    """
    Parse WAV file header and return (channels, sample_rate, bits_per_sample).
    Advances file position to start of audio data.
    """
    # Read RIFF header
    riff = file.read(4)
    if riff != b'RIFF':
        raise ValueError("Not a valid WAV file (missing RIFF)")

    file.read(4)  # File size (skip)

    wave = file.read(4)
    if wave != b'WAVE':
        raise ValueError("Not a valid WAV file (missing WAVE)")

    # Find fmt chunk
    while True:
        chunk_id = file.read(4)
        chunk_size = struct.unpack('<I', file.read(4))[0]

        if chunk_id == b'fmt ':
            fmt_data = file.read(chunk_size)
            audio_format = struct.unpack('<H', fmt_data[0:2])[0]
            channels = struct.unpack('<H', fmt_data[2:4])[0]
            sample_rate = struct.unpack('<I', fmt_data[4:8])[0]
            bits_per_sample = struct.unpack('<H', fmt_data[14:16])[0]

            if audio_format != 1:
                raise ValueError("Only PCM WAV files supported")

        elif chunk_id == b'data':
            # Found the data chunk - audio data starts here
            data_size = chunk_size
            return channels, sample_rate, bits_per_sample, data_size

        else:
            # Skip unknown chunks
            file.read(chunk_size)


def play_wav(filename):
    """
    Play a WAV file through I2S.

    The WAV file should be:
    - PCM format (uncompressed)
    - 16-bit
    - Mono or stereo (mono recommended for simplicity)
    - Sample rate matching SAMPLE_RATE constant (or update it)

    Upload your .wav file to the board using Thonny before running.
    """
    print(f"Opening {filename}...")

    try:
        with open(filename, 'rb') as f:
            channels, sample_rate, bits, data_size = parse_wav_header(f)

            print(f"WAV info: {channels}ch, {sample_rate}Hz, {bits}-bit")
            print(f"Data size: {data_size} bytes")

            # Initialize I2S with the WAV file's parameters
            audio_out = I2S(
                0,
                sck=Pin(I2S_SCK_PIN),
                ws=Pin(I2S_WS_PIN),
                sd=Pin(I2S_SD_PIN),
                mode=I2S.TX,
                bits=bits,
                format=I2S.STEREO if channels == 2 else I2S.MONO,
                rate=sample_rate,
                ibuf=BUFFER_SIZE,
            )

            print("Playing...")

            # Read and play audio data in chunks
            bytes_written = 0
            buf = bytearray(1024)

            while bytes_written < data_size:
                num_read = f.readinto(buf)
                if num_read == 0:
                    break
                audio_out.write(buf[:num_read])
                bytes_written += num_read

            # Allow buffer to drain
            time.sleep_ms(200)
            audio_out.deinit()
            print("Done!")

    except OSError as e:
        print(f"Error: Could not open {filename}")
        print("Make sure the file is uploaded to the board's filesystem.")
        raise


def generate_test_wav():
    """
    Generate a simple test WAV file (440Hz sine wave) on the board.
    Useful if you don't have a WAV file handy.
    """
    import math

    filename = "test_tone.wav"
    sample_rate = 16000
    duration_sec = 2
    frequency = 440  # A4 note

    num_samples = sample_rate * duration_sec

    print(f"Generating {filename}...")

    with open(filename, 'wb') as f:
        # WAV header
        f.write(b'RIFF')
        data_size = num_samples * 2  # 16-bit samples
        file_size = data_size + 36
        f.write(struct.pack('<I', file_size))
        f.write(b'WAVE')

        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))       # Chunk size
        f.write(struct.pack('<H', 1))        # Audio format (PCM)
        f.write(struct.pack('<H', 1))        # Channels (mono)
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * 2))  # Byte rate
        f.write(struct.pack('<H', 2))        # Block align
        f.write(struct.pack('<H', 16))       # Bits per sample

        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', data_size))

        # Generate sine wave samples
        for i in range(num_samples):
            sample = int(16000 * math.sin(2 * math.pi * frequency * i / sample_rate))
            f.write(struct.pack('<h', sample))

    print(f"Created {filename} ({duration_sec}s, {frequency}Hz tone)")
    return filename


# =============================================================================
# DEMO / MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 40)
    print("Lab 5: Audio Player")
    print("=" * 40)
    print()
    print("Options:")
    print("  1. play_melody()      - Play tones via PWM (passive buzzer)")
    print("  2. generate_test_wav() - Create a test WAV file")
    print("  3. play_wav('test_tone.wav') - Play WAV via I2S")
    print()
    print("For quick test with passive buzzer, run:")
    print(">>> play_melody()")
    print()
    print("For I2S audio, first generate a test file:")
    print(">>> generate_test_wav()")
    print(">>> play_wav('test_tone.wav')")
    print()

    # Uncomment one of these to run automatically:
    # play_melody()
    # generate_test_wav()
    # play_wav('test_tone.wav')
