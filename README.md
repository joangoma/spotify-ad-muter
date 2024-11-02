# Spotify Ad Muter

A Python script that automatically reduces the volume during Spotify advertisements and restores it when your music continues. This script works on Linux systems using PulseAudio for sound management.

## Features

- Automatically detects Spotify advertisements
- Reduces volume during ads instead of completely muting (prevents playback issues)
- Automatically restores original volume when music resumes
- Can run in the background
- Optional automatic startup with system
- Supports virtual environments

## Prerequisites

The following packages are required:

```bash
sudo apt-get update
sudo apt-get install python3-dev python3-dbus playerctl pulseaudio-utils
```

For other distributions, use your package manager to install equivalent packages.

## Installation

1. Clone or download this repository:
```bash
git clone https://github.com/joangoma/spotify-ad-muter.git
cd spotify-ad-muter
```

2. (Optional) Set up a virtual environment:
```bash
# Create virtual environment
python3 -m venv ~/.virtualenvs/spotify-muter

# Activate virtual environment
source ~/.virtualenvs/spotify-muter/bin/activate

# Install requirements
pip install dbus-python
```

3. Copy the script to your local bin directory:
```bash
mkdir -p ~/.local/bin
cp spotify_ad_muter.py ~/.local/bin/
chmod +x ~/.local/bin/spotify_ad_muter.py
```

## Usage

### Manual Running

1. If using a virtual environment, activate it:
```bash
source ~/.virtualenvs/spotify-muter/bin/activate
```

2. Run the script:
```bash
python3 ~/.local/bin/spotify_ad_muter.py
```

The script will run silently in the background. Press Ctrl+C to stop it.

### Automatic Startup (Optional)

You can set up the script to run automatically when you log in spotify.


1. Create the systemd user directory:
```bash
mkdir -p ~/.config/systemd/user/
```

2. Create the service file:
```bash
nano ~/.config/systemd/user/spotify-muter.service
```

3. Add the following content (replace YOUR_USERNAME with your actual username):

If using system Python:
```ini
[Unit]
Description=Spotify Advertisement Muter
After=spotify.service
PartOf=graphical-session.target

[Service]
ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/.local/bin/spotify_ad_muter.py
Restart=on-failure
RestartSec=3

[Install]
WantedBy=default.target
```

If using virtual environment:
```ini
[Unit]
Description=Spotify Advertisement Muter
After=spotify.service
PartOf=graphical-session.target

[Service]
Environment=PATH=/home/YOUR_USERNAME/.virtualenvs/spotify-muter/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/home/YOUR_USERNAME/.virtualenvs/spotify-muter/bin/python3 /home/YOUR_USERNAME/.local/bin/spotify_ad_muter.py
Restart=on-failure
RestartSec=3

[Install]
WantedBy=default.target
```

4. Enable and start the service:
```bash
systemctl --user daemon-reload
systemctl --user enable spotify-muter.service
systemctl --user start spotify-muter.service
```

## Managing the Service

Check status:
```bash
systemctl --user status spotify-muter.service
```

View logs:
```bash
journalctl --user -u spotify-muter.service -f
```

Stop the service:
```bash
systemctl --user stop spotify-muter.service
```

Disable autostart:
```bash
systemctl --user disable spotify-muter.service
```

## Troubleshooting

1. If the script can't find Spotify's audio sink:
   - Make sure Spotify is playing audio
   - Verify PulseAudio is running: `pulseaudio --check`
   - Check if Spotify appears in your system's volume mixer

2. If the volume isn't being restored:
   - Check if the script has proper permissions
   - Verify the PulseAudio sink is correctly identified
   - Try restarting PulseAudio: `pulseaudio -k && pulseaudio --start`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
