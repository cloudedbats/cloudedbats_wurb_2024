# CloudedBats WURB-2024

Next major release - work in progress...

## For ordinary users

Please use the older version called CloudedBats WURB-2020.
That version is well tested by many users and works well
both as a mobile detector and for stationary use.

More info here:
<https://github.com/cloudedbats/cloudedbats_wurb_2020>

## Introduction

This GitHub repository contains the software needed to build a bat detector
that can be used both for active and passive monitoring.

The software is completely open and free, based on the MIT software license.

Please also consider sharing the recordings made by this software for free
(with the license CC0 or CC-BY). We have to collaborate more to learn
more about bats.

What you need to build your own bat detector is:

- An ultrasonic USB microphone. Normally one that can sample at 384 kHz, but 192 kHz will
be enough for many common bat species.
- A Raspberry Pi computer. Raspberry Pi 5 is recommended but it will work on other models too.
- An SD card for all software and settings, recordings, etc.
- Power supply. 5V USB charger or Powerbank will work in most cases.
- USB memory stick. (Optional, you can store everything on the SD card.)
- USB GPS receiver. Not needed for stationary deployments but handy for active monitoring.

Then you also need a unit that can run a web browser and connect to a WiFi network.
For field work a mobile phone will work, or any laptop/computer.
It is also possible to set up the detector for remote access since it is developed as an
ordinary web server, but that kind of setup is for advanced users only.

## About the new version

The functionality when recording bats is mainly the same as in the WURB-2020 version,
but the user interface is reorganized and settings are "behind" each panel.

A new page for "Field annotations" is added where it is possible to check recordings
as spectrograms. Then you can assign quality stamps, tags and comments on each recorded file
even during an ongoing monitoring session.

Another page called "Administration" can then use this information in various ways.
For example, it will be possible to remove trash files directly in the detector,
or to generate an Excel report containing annotations and other useful metadata.

Another difference is that the new software is more generic and it will be possible to
generate executable files for both Windows and macOS.

## For developers and early adopters

The reasons for this new version are:

- I really wanted to have the possibility to check recordings directly in the detectors
user interface during monitoring.
And then it should be handy to make annotations directly without the need for paper/pencil or Excel.
- I have done a lot of testing with remote control and file sync over internet that works really well.
That kind of deployments will be easier to explain in this new version.
- The structure of the software needed a big overhaul. It is all reorganized and major parts are
completely rewritten.
- A system for basic configuration was needed. A YAML-based system is now used for that.
- Sqlite is a better choice for settings than text files. Also used for annotations.
- Sound management differ on different platform. There is now support for both ALSA (for Linux)
and PortAudio (Windows, macOS).

The detector is developed as a "full-stack" web application. The backend uses Python with asyncio to
handle parallel processes. The API uses the Python framework FastAPI. The user interface is pure
HTML and JavaScript with Bulma.io for CSS.

Raspberry Pi 5 is recently released that gives a lot of new opportunities, but also things that must
be managed to keep the compatibility with earlier version.
The installation process is modified to match RPi 5 and the new OS release called Bookworm.

Please help to test the new version, stability and reliability is absolutely priority number one
for a bat detector. Contact info below.

Also contact me if you want a download link to an executable file to test the detector on Windows.

## Installation - Raspberry Pi

This is my primary test setup:

- Raspberry Pi 5.
- SD: SanDisk ExtremePRO - 64GB, read 200, write 90 MB/s.
- Microphone: Pettersson u384.
- USB memory: SanDisk Ultra USB 3.0
- Any 5V power supply (including solar panel + LiFePO4 battery).
- Ethernet cable or HUAWEI E3372 for 4G/LTE.
(both are optional but good during test and development when the detector is running as a WiFi hotspot).

By default microphones from Pettersson, Dodotronic, AudioMoth, etc. are identified automatically.
Other microphones can be used after modifications in the configuration file.

### Install the Raspberry Pi OS

If you are new to this, please check the installation in the earlier version.
This instruction is more "minimalistic".

- Use the "Raspberry Pi Imager" to install the operating system.
- Select Raspberry Pi OS Lite (32-bit), Debian Bookworm - no desktop.

Edit settings. User must be "wurb".
Replace other parts, marked as bold, to match your needs:

- Hostname: **wurb01**
- User: wurb
- Password: **secret-password**
- WiFi SSID: **home-network**
- Password: **home-network-password**
- Wireless LAN country: **SE**
- Time zone: **Europe/Stockholm**
- Keyboard: **se**
- Activate SSH. Is located under the tab "Services".

### Basic configuration

Start the Raspberry Pi and connect with SSH from a terminal window.

    ssh wurb@wurb01.local

Basic installation

    sudo apt update
    sudo apt upgrade -y
    # Run this if you want additional configurations.
    sudo raspi-config

### The WURB-2024 detector software

    sudo apt install git python3-venv python3-dev libatlas-base-dev pmount -y
    sudo apt install pulseaudio python3-numpy python3-scipy -y

    git clone https://github.com/cloudedbats/cloudedbats_wurb_2024.git
    cd cloudedbats_wurb_2024/
    python -m venv --system-site-packages venv
    source venv/bin/activate
    pip install -r requirements.txt

    sudo cp raspberrypi_files/wurb_2024.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable wurb_2024.service
    sudo systemctl start wurb_2024.service

Now it should be up and running. Start a web browser with this address:

    http://wurb01.local:8080

### Extra on Raspberry Pi

This is needed if you are planning to use the Pettersson M500 microphone,
the one that is running at 500 kHz. (Note, not implemented in WURB-2024 yet.)

    sudo cp raspberrypi_files/pettersson_m500_batmic.rules /etc/udev/rules.d/

If the detector should be accessed away from the home network, then it can run
in a hotspot mode and enable it's own WiFi network.

    sudo nmcli con add con-name wurb-hotspot ifname wlan0 type wifi ssid WiFi-wurb01
    sudo nmcli con modify wurb-hotspot wifi-sec.key-mgmt wpa-psk
    sudo nmcli con modify wurb-hotspot wifi-sec.psk chiroptera
    sudo nmcli con modify wurb-hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared

Use this tool to check the network connections:

    sudo nmtui

If you run the "nmtui" tool and deactivate the connection to your home network the
detector will directly switch over to the hotspot mode.
The SSH session will stop immediately since the Raspberry Pi only contains one WiFi unit
that either can be used to connect to a WiFi network, or to run as a hotspot.
The hotspot mode is really useful if you have the 4G/LTE modem attached, or an Ethernet cable.
In the example above the WiFi ame will be "WiFi-wurb01" and password "chiroptera".

When using the hotspot the detector will use the IP address 10.42.0.1 and then either
"<http://wurb01.local:8080>" or "<http://10.42.0.1:8080>" can be used to access the detectors
user interface.

### USB ###

If you are planning to store recorded files on USB memory sticks the you have to either
mount them manually via SSH, or install some software that mounts them automatically.
These commands will setup the automatic version.

    sudo cp raspberrypi_files/usb_pmount.rules /etc/udev/rules.d/
    sudo cp raspberrypi_files/usb_pmount_handler@.service /lib/systemd/system/
    sudo cp raspberrypi_files/usb_pmount_script /usr/local/bin/
    sudo chmod +x /usr/local/bin/usb_pmount_script

Some useful commands to check attached USB devices are:

    ls /media/
    df -h
    sudo fdisk -l

Note that in the configuration file for the detector "wurb_settings/wurb_config.yaml"
these USB devices are accessible and named like "media_path: /media/USB-sda1".

### Extra on Raspberry Pi 5

Raspberry Pi 5 has introduced some new and useful things.

- There is an on/off button.
- It is possible to add an extra battery to run an included Real-Time-Clock, RTC.
- It can be configured to not use power when the Raspberry Pi is turned off.
- When using the RTC it is possible to let it sleep for a specified time.

To enable this the bootloader (EEPROM) must be updated.
Note that the EEPROM is not a part of the operating system, it is a part of the
hardware. That means that it must be done manually once for each new Raspberry Pi 5 unit.
After that you don't have to repeat it when installing a new SD card with updated OS/software.

    sudo rpi-eeprom-config -e

    # Add/replace to this.
    BOOT_UART=1
    POWER_OFF_ON_HALT=1
    WAKE_ON_GPIO=0
    BOOT_ORDER=0xf416

Then you have to do a reboot.

    sudo reboot

You can test the sleep functionality with this.
The Raspberry Pi will then be turned off for 10 minutes (600 sec)
and then turned on automatically.
This can be set up to run as a cron job to save battery during daytime.

    echo +600 | sudo tee /sys/class/rtc/rtc0/wakealarm
    sudo halt

## Executable file - Windows

First step is to check that Python is installed.
Then the WURB-2024 has to be installed.
Dependent on how Python is installed on your computer you may have to
type in the whole path to Python.

    git clone https://github.com/cloudedbats/cloudedbats_wurb_2024.git
    cd cloudedbats_wurb_2024/
    python3 -m venv venv
    venv/Script/activate
    pip install -r requirements_pyaudio.txt

The detector should now be possible to run.
Then start a web browser with the address "<http://localhost:8080>".

    python3 wurb_main.py

To build an executable "exe" file run this.

    pip install pyinstaller
    pyinstaller wurb_main_pyinstaller.spec

The exe-file will then be created in a directory called "dist".

## Configurations for the detector

When the detector is started for the first time three directories will be created.
They are wurb_settings, wurb_logging and wurb_recordings.
The two first directories are located on the SD card directly under /home/wurb,
but wurb_recordings can be placed at some different locations depending
on configuration settings and available devices for storage.

Check the file wurb_settings/wurb_config.yaml and make adjustments if needed.

If you want to use another type of microphones, then attach it to the detector
and start the detector.
In the log file wurb_logging/wurb_debug_log.txt there will be some
info about connected devices that can be used in the wurb_config.yaml file.

More info on this topic later...

## Contact

Arnold Andreasson, Sweden.

<info@cloudedbats.org>
