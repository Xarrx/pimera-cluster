#!/bin/bash

echo 'Starting control script installation...'

# create symbolic links for the control scripts in /usr/local/bin
ln -s $(pwd)/ledctrl.py /usr/local/bin/ledctrl

echo 'Done!'
exit
