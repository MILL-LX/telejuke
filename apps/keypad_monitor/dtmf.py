import numpy as np
import sounddevice as sd
import time

# DTMF frequency mapping
DTMF_FREQS = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633)
}

def generate_dtmf_tone(digit, duration=0.5, sample_rate=44100):
    if digit not in DTMF_FREQS:
        raise ValueError(f"Invalid DTMF digit: {digit}")
    
    freq1, freq2 = DTMF_FREQS[digit]
    
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate the two sine waves and combine them
    tone1 = np.sin(2 * np.pi * freq1 * t)
    tone2 = np.sin(2 * np.pi * freq2 * t)
    dtmf_tone = (tone1 + tone2) * 0.3  # Scale amplitude
    
    return dtmf_tone

digit_tones = {}
def init_digit_tones():
    global digit_tones
    for digit in "1234567890*#":
        digit_tones[str(digit)] = generate_dtmf_tone(str(digit), duration=30)

def play_digit(digit):
    tone = digit_tones.get(str(digit))
    if tone is not None:
        sd.play(tone, samplerate=44100)
    else:
        print(f"No pre-generated tone for digit {digit}")

def stop_playing_digit():
    sd.stop()

