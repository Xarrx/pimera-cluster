#/bin/sh -e
stty -F /dev/ttyACM0 9600 raw -echo -echoe -echok -echoctl -echoke
echo "B#002000-0200#004000-0200" > /dev/ttyACM0
echo "F1000" > /dev/ttyACM0
