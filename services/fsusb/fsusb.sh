#/bin/bash

# Pull serial device out of the dmesg log.
serial_device=$(dmesg | awk '/USB ACM device/ {print $5}' | cut -c -7)

# check that the device is in /dev
touch /dev/$serial_device &> /dev/null
if [ ! $? = 0 ] ; then
  echo "Error: Failed to locate a valid serial device."
  exit
fi


stty -F /dev/$serial_device 9600 raw -echo -echoe -echok -echoctl -echoke
# write the serial device discovered to a file to be used by other scripts.
printf "/dev/$serial_device" > /tmp/tty_device
echo "Serial device located: /dev/$serial_device"


#
# TODO: No hardcoded paths! Fix!
#
# set default color using the control script
../../control-scripts/ledctrl.py -d
exit
