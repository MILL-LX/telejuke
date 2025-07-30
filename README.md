# telejuke

Telephone World Jukebox

## OS

Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to create the OS image for your Pi.

This project has been developed on a Raspberry Pi 4 running Bookwork Desktop 64-bit* with SSH enabled.

Drop your public SSH key in ```~/.ssh/authorized_keys``` if you like. Installing the public key will make your life easier if you like to use the VSCode Remote SSH plugin to develop directly on the Pi.

## System Packages for Python Development and FBCP Build

```bash
sudo apt update
sudo apt full-upgrade
sudo apt install \
    git \
    python3 \
    python3-pip \
    python3-venv \
    # cmake \
    # libraspberrypi-dev \
    # libraspberrypi0 \
    # xserver-xorg-video-fbturbo \
    -y

python -m venv env --system-site-packages
```

## Clone this project

```bash
git clone https://github.com/MILL-LX/telejuke.git --recursive
cd telejuke
```

## Install FBCP

### Compile and install the binary

```bash
cd dependencies

```

### Start FBCP as a system service

```bash
sudo cp systemd/fbcp.service /etc/systemd/system/fbcp.service

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start at boot
sudo systemctl enable fbcp.service

# Start the service now
sudo systemctl start fbcp.service

# Check service status
sudo systemctl status fbcp.service
```

### Enable Autologin

```bash
sudo raspi-config nonint do_boot_behaviour B2
sudo raspi-config nonint do_wayland W1
sudo reboot
```

## Add WiFi Networks

If this will join networks besides the one configured when creatind the SD Card, you can add them with the Text UI for the Network Manager.

```bash
sudo nmtui
```

## [uv](https://github.com/astral-sh/uv) for Python Dependency Management

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Touch Screen Setup

Based on the [Waveshare Wiki](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(A)_Manual_Configuration#For_Raspberry_Pi_4_.26_Raspberry_Pi_5)

Download and install the driver:

```bash
mkdir waveshare-install
cd waveshare-install
wget https://files.waveshare.com/upload/1/1e/Waveshare35a.zip
unzip Waveshare35a.zip
sudo cp waveshare35a.dtbo /boot/overlays
```

Download, build, and install the Frame Buffer Copying Daemon

```bash
wget https://files.waveshare.com/upload/1/1e/Rpi-fbcp.zip
unzip ./Rpi-fbcp.zip
cd rpi-fbcp/
rm -rf build
mkdir build
cd build
cmake ..
make -j4
sudo install fbcp /usr/local/bin/fbcp
```

Edit `/boot/firmware/config.txt`:

Comment out:

```bash
# Enable DRM VC4 V3D driver
dtoverlay=vc4-kms-v3d
max_framebuffers=2
```

Add:

```bash
dtparam=spi=on
dtoverlay=waveshare35a
hdmi_force_hotplug=1
max_usb_current=1
hdmi_group=2
hdmi_mode=1
hdmi_mode=87
hdmi_cvt 480 320 60 6 0 0 0
hdmi_drive=2
display_rotate=180
```

### Start Window Manager

Add the following to `~/.bash_profile`:

MOFIX: Probably want to start this as a service so as not to require logging in.

```bash
if [ "$(cat /proc/device-tree/model | cut -d ' ' -f 3)" = "5" ]; then
    # rpi 5B configuration
    export FRAMEBUFFER=/dev/fb1
    startx  2> /tmp/xorg_errors
else
    # Non-pi5 configuration
    export FRAMEBUFFER=/dev/fb0
    # fbcp &
    startx  2> /tmp/xorg_errors
fi
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

### Make the Project's Python Virtual Environment

Make sure to include the site packages to gain acces to the Picamera2 that was installed with `apt`

```bash
cd telejuke/app
uv venv #MOFIX --system-site-packages
uv sync
```
