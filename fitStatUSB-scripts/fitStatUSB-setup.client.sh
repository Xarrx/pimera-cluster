#/bin/sh -e
stty -F /dev/ttyACM0 9600 raw -echo -echoe -echok -echoctl -echoke
echo "B#000020-0200#000040-0200" > /dev/ttyACM0
echo "F1000" > /dev/ttyACM0
