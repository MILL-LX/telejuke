import os
from pydub import AudioSegment
from pydub.playback import play
import time

def play_mp3(file_path):
    """
    Play an MP3 file using pydub
    
    Args:
        file_path (str): Path to the MP3 file
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found")
            return
        
        # Load the MP3 file
        print(f"Loading: {file_path}")
        audio = AudioSegment.from_mp3(file_path)
        
        # Get audio info
        duration = len(audio) / 1000  # Convert to seconds
        print(f"Duration: {duration:.2f} seconds")
        print(f"Channels: {audio.channels}")
        print(f"Frame rate: {audio.frame_rate} Hz")
        
        # Play the audio
        print("Playing...")
        play(audio)
        print("Playback finished")
        
    except Exception as e:
        print(f"Error playing audio: {e}")

def play_mp3_with_volume(file_path, volume_change_db=0):
    """
    Play an MP3 file with volume adjustment
    
    Args:
        file_path (str): Path to the MP3 file
        volume_change_db (float): Volume change in decibels (positive = louder, negative = quieter)
    """
    try:
        audio = AudioSegment.from_mp3(file_path)
        
        # Adjust volume if specified
        if volume_change_db != 0:
            audio = audio + volume_change_db
            print(f"Volume adjusted by {volume_change_db} dB")
        
        play(audio)
        
    except Exception as e:
        print(f"Error playing audio: {e}")

def play_mp3_segment(file_path, start_time=0, end_time=None):
    """
    Play a specific segment of an MP3 file
    
    Args:
        file_path (str): Path to the MP3 file
        start_time (float): Start time in seconds
        end_time (float): End time in seconds (None = play to end)
    """
    try:
        audio = AudioSegment.from_mp3(file_path)
        
        # Convert seconds to milliseconds
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000) if end_time else len(audio)
        
        # Extract segment
        segment = audio[start_ms:end_ms]
        
        print(f"Playing segment: {start_time}s to {end_time or len(audio)/1000}s")
        play(segment)
        
    except Exception as e:
        print(f"Error playing audio segment: {e}")

# Example usage
if __name__ == "__main__":
    # Basic playback
    mp3_file = "../assets/A001.mp3"  # Replace with your MP3 file path
    
    print("=== Basic MP3 Playback ===")
    play_mp3(mp3_file)
    
    print("\n=== MP3 Playback with Volume Boost ===")
    play_mp3_with_volume(mp3_file, volume_change_db=5)  # 5dB louder
    
    print("\n=== MP3 Segment Playback ===")
    play_mp3_segment(mp3_file, start_time=10, end_time=30)  # Play from 10s to 30s