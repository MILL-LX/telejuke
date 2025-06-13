import requests
import random
import subprocess
import sounddevice as sd

USB_AUDIO_DEVICE_NAME = "USB Audio Device"  # Adjust to match your system
SAMPLE_RATE = 44100
CHANNELS = 2
BLOCKSIZE = 4096  # Bytes per chunk (multiple of frame size)

def get_usb_output_device_id(name_hint):
    for i, device in enumerate(sd.query_devices()):
        if device['max_output_channels'] > 0 and name_hint.lower() in device['name'].lower():
            return i
    raise RuntimeError("USB audio output device not found.")

# def get_random_french_station():
#     url = "https://de1.api.radio-browser.info/json/stations/bycountrycodeexact/FR"
#     resp = requests.get(url)
#     stations = [s for s in resp.json() if s.get("url_resolved")]
#     if not stations:
#         raise RuntimeError("No French stations found.")
#     return random.choice(stations)

def stream_radio(url, device_id):
    print(f"Starting ffmpeg for stream: {url}")
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", url,
        "-f", "s16le",               # Raw PCM 16-bit little endian
        "-acodec", "pcm_s16le",      # PCM codec
        "-ac", str(CHANNELS),        # Number of audio channels
        "-ar", str(SAMPLE_RATE),     # Sampling rate
        "-"                          # Output to stdout
    ]

    with subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=BLOCKSIZE) as proc:
        with sd.RawOutputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCKSIZE // (2 * CHANNELS),  # 2 bytes/sample * channels
            dtype='int16',
            channels=CHANNELS,
            device=device_id
        ) as stream:
            print("Streaming audio...")
            try:
                while True:
                    data = proc.stdout.read(BLOCKSIZE)
                    if not data:
                        break
                    stream.write(data)
            except KeyboardInterrupt:
                print("\nStopping stream...")
            finally:
                proc.kill()


from pyradios import RadioBrowser

rb = RadioBrowser()
results = rb.search(countrycode="FR", limit=1000)
# Filtering out stations with no votes
results = [s for s in results if s.get('votes', 0) > 0]
results.sort(key=lambda x: x.get('votes', 0), reverse=True)
# limit to top 20 stations
results = results[:20]

#results = rb.search(name="RTL2",name_exact=False, limit=1000)

# print(results)

# Select a random station from the results
if not results:
    raise RuntimeError("No stations found for the specified criteria.")

station = None
while station is None:  
    station = random.choice(results)
    if not station.get('url_resolved'):
        print(f"Skipping station {station['name']} due to missing stream URL.")
        results.remove(station)
        station = None

print(f"Found {len(results)} stations. Selected station: {station['name']}")
# pretty print the station details
import pprint
pprint.pprint(station)

device_id = get_usb_output_device_id(USB_AUDIO_DEVICE_NAME)
if not device_id:
    raise RuntimeError("USB audio output device not found.")
if not station.get('url_resolved'):
    raise RuntimeError("Selected station does not have a valid stream URL.")

print(f"Selected Station: {station['name']}")
print(f"Stream URL: {station['url_resolved']}")
stream_radio(station['url_resolved'], device_id)