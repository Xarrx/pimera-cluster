#!/bin/bash

{
  # disable old version
  systemctl disable fitStatUSB-setup.service
  systemctl disable fsusb-start.service

  # cleanup old files
  rm -f /etc/systemd/system/fitStatUSB-setup.service
  rm -f /etc/systemd/system/fitStatUSB-setup.client.service
  rm -f /etc/systemd/system/fsusb-start.service

  # install this version
  cp fsusb-start.service /etc/systemd/system/.
  systemctl enable fsusb-start.service
  systemctl start fsusb-start.service
} &> /tmp/fsusb-install.log

