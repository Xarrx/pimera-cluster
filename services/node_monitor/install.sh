#!/bin/bash

{
  # disable old version
  systemctl disable node_monitor

  # cleanup old files
  rm -f /etc/systemd/system/node_monitor.service

  # install this version
  cp node_monitor.service /etc/systemd/system/.
  systemctl enable node_monitor.service
  systemctl start node_monitor.service
} &> /tmp/node_monitor-install.log


