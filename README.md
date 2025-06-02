# telejuke
Telephone World Jukebox

### OS

Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to create the OS image for your Pi.

This project has been developed on a Raspberry Pi 4 running *Bullseye Lite 32-bit* with SSH enabled and a public key installed. Installing the public key will make your life easier if you like to use the VSCode Remote SSH plugin to develop directly on the Pi.

### System Packages for Python Development

```bash
sudo apt update
sudo apt full-upgrade
sudo apt install \
    git \
    python3 \
    python3-pip 
```

### Add WiFi Networks 

If this will join networks besides the one configured when creatind the SD Card, you can add them with the Text UI for the Network Manager.

```bash
sudo nmtui
```

### [uv](https://github.com/astral-sh/uv) for Python Dependency Management

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Application Setup

### Add OS Dependencies

```bash
sudo apt update
sudo apt install ffmpeg libasound2-dev
```

### Clone this project

```bash
git clone https://github.com/MILL-LX/telejuke.git
```

### Make the Project's Python Virtual Environment

Make sure to include the site packages to gain acces to the Picamera2 that was installed with `apt`

```bash
cd telejuke/app
uv venv #MOFIX --system-site-packages
uv sync
```
