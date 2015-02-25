#!/bin/bash

##
# This script writes the rasbian image to an SD card.
##

IMG_URL="http://downloads.raspberrypi.org/raspbian/images/raspbian-2015-02-17/2015-02-16-raspbian-wheezy.zip"
IMG_NAME="2015-02-16-raspbian-wheezy"

if [ $# -lt 1 ]; then
  echo "USAGE: $0 <SD device>"
  echo "Double check that the device is not mounted!"
  exit 1
fi

if [ ! -b $1 ]; then
  echo "The SD device does not exist. You provided: $1"
  exit 1
fi

if [ ! -d image ]; then
  mkdir image
  cd image
  wget ${IMG_URL}
  unzip ${IMG_NAME}.zip
  cd ..
fi

read -p "This will delete all data from $1. Are you sure? [N/y]" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo
  sudo dd if=image/${IMG_NAME}.img of=$1 bs=4MB
  sudo sync
fi

echo
echo "Image written. Remove SD card, and put into raspberry pi."
echo "To continue with Pivi installation you should:"
echo "Find out rpi IP address using:"
echo "$ sudo nmap -sP <LAN>/<MASK>. eg sudo nmap -sP 192.168.1.0/24"
echo "Expand the rpi root fs and disable kernel messages on serial port:"
echo "  - ssh into rpi:"
echo "  - $ sudo raspi-config"
echo "  - Look for the appropriate options."
echo "  - reboot the rpi."
echo "Copy your ssh ID to the rPI:"
echo "  - $ ssh-copyid pi@<pi IP address>"
echo "Run installation script from the PC:"
echo "(while on the install/ directory)"
echo "$ fab install -H pi@<pi IP address>"
echo
