#/bin/sh -e
stty -F /dev/ttyACM0 9600 raw -echo -echoe -echok -echoctl -echoke
echo "B#101010-0100#202020-0100" > /dev/ttyACM0
echo "F1000" > /dev/ttyACM0
