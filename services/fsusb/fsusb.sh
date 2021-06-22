#/bin/bash
#
# TODO: Implement a way to gather the serial device w/o hardcoding.
#
# find serial device
#touch /dev/ttyACM0 &> /dev/null
#if [ $? = 0 ] ; then
#  serial_device='/dev/ttyACM0'
#else
#  # test for the other serial device
#  touch /dev/ttyAMA0 &> /dev/null
#  if [ $? = 0 ] ; then
#    serial_device='/dev/ttyAMA0'
#  else
#    echo 'Failed to locate serial device, exiting...'
#    exit
#  fi
#fi

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
#echo "B#002000-0200#004000-0200" > $serial_device
#echo "F1000" > $serial_device

# set default color using the control script
../../control-scripts/ledctrl.py -d
exit
