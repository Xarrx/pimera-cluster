#/bin/sh -e
stty -F /dev/ttyACM0 9600 raw -echo -echoe -echok -echoctl -echoke
echo "B#001000-0100#002000-0100" > /dev/ttyACM0
echo "F1000" > /dev/ttyACM0
