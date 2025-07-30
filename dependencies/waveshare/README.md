# Waveshare Driver for Raspberry Pi

## Download New Version (if necessary)

```bash
wget https://files.waveshare.com/upload/1/1e/Waveshare35a.zip
unzip Waveshare35a.zip
```

## Install the driver

```bash
sudo cp waveshare35a.dtbo /boot/overlay
```

Edit `/boot/firmware/config.txt` to include:

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
display_rotate=0
```
