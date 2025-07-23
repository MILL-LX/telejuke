# telejuke
Telephone World Jukebox

### OS

Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to create the OS image for your Pi.

This project has been developed on a Raspberry Pi 4 running *Bullseye Desktop 32-bit* with SSH enabled.

Drop your public SSH key in ```~/.ssh/authorized_keys``` if you like. Installing the public key will make your life easier if you like to use the VSCode Remote SSH plugin to develop directly on the Pi.

### System Packages for Python Development

```bash
sudo apt update
sudo apt full-upgrade
sudo apt install \
    git \
    python3 \
    python3-pip \
    python3-venv
sudo apt autoremove
sudo apt autoclean

python -m venv env --system-site-packages

pip3 install --upgrade adafruit-python-shell click
git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git
cd Raspberry-Pi-Installer-Scripts
```

Add arm_64bit=0 to /boot/firmware/config.txt

### Add WiFi Networks 

If this will join networks besides the one configured when creatind the SD Card, you can add them with the Text UI for the Network Manager.

```bash
sudo nmtui
```

### [uv](https://github.com/astral-sh/uv) for Python Dependency Management

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
## Touch Screen Setup

Enable SPI with raspi-config

```bash
sudo apt install cmake
sudo raspi-config
sudo apt update
sudo apt install libraspberrypi-dev
```

```bash
git clone https://github.com/MILL-LX/LCD-show.git
cd LCD-show
sudo ./LCD4-show
```

## Application Setup

### Add OS Dependencies - REVISIT BASED ON ACTUAL PYTHON LIBRARIES USED


```bash
sudo apt update
sudo apt install ffmpeg libffi-dev
sudo apt install libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt update
sudo apt install python3-dev python3-pip python3-venv gfortran libopenblas-dev liblapack-dev build-essential meson ninja-build
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
