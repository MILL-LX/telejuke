import subprocess
import os

mp3_file = "example.mp3"
wav_file = "temp.wav"
device = "hw:1,0"

# Convert MP3 to WAV (44100 Hz, stereo, 16-bit LE)
subprocess.run([
    "ffmpeg", "-y", "-i", mp3_file,
    "-ar", "44100",     # Sample rate
    "-ac", "2",         # Stereo
    "-sample_fmt", "s16",  # 16-bit PCM
    wav_file
], check=True)

# Play using ALSA on USB audio device
try:
    subprocess.run([
        "aplay", "-D", device, wav_file
    ], check=True)
except subprocess.CalledProcessError as e:
    print(f"Playback failed: {e}")

# Optional: Clean up temporary WAV file
os.remove(wav_file)
