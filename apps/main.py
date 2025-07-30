from pydub import AudioSegment
import sounddevice as sd
import numpy as np

for idx, device in enumerate(sd.query_devices()):
    print(f"{idx}: {device['name']}")

# Load MP3 and convert to 44100 Hz stereo
audio = AudioSegment.from_mp3("../assets/instructions.mp3").set_frame_rate(44100).set_channels(2)

# Convert to NumPy float32 array
samples = np.array(audio.get_array_of_samples()).astype(np.float32) / (2**15)

# Reshape for stereo playback if necessary
samples = samples.reshape((-1, 2))

# Play on the Raspberry Pi's built-in audio output
# Lower sound quality - use for voice playback
device = sd.query_devices("bcm2835 Headphones", "output")
if device is None:
    raise ValueError("bcm2835 Headphones not found")
if device['max_output_channels'] < 2:
    raise ValueError("bcm2835 Headphones does not support stereo output")
print(f"Playing on bcm2835 Headphones: {device['name']}")
sd.play(samples, samplerate=44100, device=device['name'])
sd.wait()


# Play on the USB Audio Device
# Better sound quality - use for music playback
device = sd.query_devices("USB Audio Device", "output")
if device is None:
    raise ValueError("USB Audio Device not found")
if device['max_output_channels'] < 2:
    raise ValueError("USB Audio Device does not support stereo output")
print(f"Playing on USB Audio Device: {device['name']}")
sd.play(samples, samplerate=44100, device=device['name'])
sd.wait()