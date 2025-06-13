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

def play_dtmf_sequence(sequence, tone_duration=0.2, pause_duration=0.1):
    for digit in sequence:
        if digit == ' ':
            time.sleep(pause_duration * 3)  # Longer pause for spaces
        else:
            tone = generate_dtmf_tone(digit, tone_duration)
            sd.play(tone, samplerate=44100)
            sd.wait()  # Wait for tone to finish
            time.sleep(pause_duration)