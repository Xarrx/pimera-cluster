#!/bin/bash

{
  # disable old version
  systemctl disable node-monitor

  # cleanup old files
  rm -f /etc/systemd/system/node-monitor.service

  # install this version
  cp node_monitor.service /etc/systemd/system/.
  systemctl enable node-monitor.service
  systemctl start node-monitor.service
} &> /tmp/node-monitor-install.log


