#/bin/sh -e
stty -F /dev/ttyACM0 9600 raw -echo -echoe -echok -echoctl -echoke
echo "B#000010-0100#000020-0100" > /dev/ttyACM0
echo "F1000" > /dev/ttyACM0
