import subprocess
import time

def get_spotify_sink_input():
    """Get Spotify's sink input number."""
    try:
        sink_inputs = subprocess.run(['pactl', 'list', 'sink-inputs'], 
                                   capture_output=True, text=True).stdout
        
        lines = sink_inputs.split('\n')
        current_sink = None
        
        for i, line in enumerate(lines):
            if 'Sink Input #' in line:
                current_sink = line.split('#')[1].strip()
            
            if current_sink and any(identifier in line.lower() for identifier in 
                                  ['spotify', 'application.name = "spotify"', 
                                   'media.name = "spotify"']):
                return current_sink
        return None
    except Exception as e:
        return None

def get_spotify_metadata():
    """Get current Spotify track metadata using playerctl."""
    try:
        result = subprocess.run(['playerctl', '--player=spotify', 'metadata'], 
                              capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None

def get_current_volume(sink_input_number):
    """Get current volume level."""
    try:
        result = subprocess.run(['pactl', 'list', 'sink-inputs'], 
                              capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if f'Sink Input #{sink_input_number}' in line:
                for j in range(i, min(i + 20, len(lines))):
                    if 'Volume:' in lines[j] and 'Base' not in lines[j]:
                        vol = lines[j].split('/')[1].strip()
                        return int(vol.replace('%', ''))
        return 100
    except Exception:
        return 100

def set_spotify_volume(sink_input_number, volume_percent):
    """Set Spotify volume to specified percentage."""
    try:
        if sink_input_number:
            subprocess.run(['pactl', 'set-sink-input-volume', 
                          sink_input_number, f'{volume_percent}%'])
            return True
    except Exception:
        pass
    return False

def is_spotify_running():
    """Check if Spotify process is running."""
    try:
        result = subprocess.run(['pgrep', '-f', 'spotify'], 
                              capture_output=True, text=True)
        return bool(result.stdout.strip())
    except Exception:
        return False

def monitor_spotify():
    """Monitor Spotify and control volume during advertisements."""
    print("Spotify ad muter is running... Press Ctrl+C to stop")
    is_currently_muted = False
    original_volume = None
    
    while True:
        try:
            if not is_spotify_running():
                time.sleep(2)
                continue
            
            metadata = get_spotify_metadata()
            sink_input_number = get_spotify_sink_input()
            
            if metadata and sink_input_number:
                is_ad = ('advertisement' in metadata.lower() or 
                        'spotify' in metadata.lower() and 'free' in metadata.lower())
                
                if is_ad and not is_currently_muted:
                    # Store the current volume before reducing it
                    if original_volume is None:
                        original_volume = get_current_volume(sink_input_number)
                    set_spotify_volume(sink_input_number, 5)
                    is_currently_muted = True
                    
                elif not is_ad and is_currently_muted:
                    # Restore the original volume
                    if original_volume is not None:
                        set_spotify_volume(sink_input_number, original_volume)
                    is_currently_muted = False
                    
        except Exception:
            pass
        
        time.sleep(1)

if __name__ == "__main__":
    try:
        monitor_spotify()
    except KeyboardInterrupt:
        print("\nStopping Spotify ad muter...")