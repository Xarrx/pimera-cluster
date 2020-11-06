#!/bin/bash
#IFS=' ' read -r -a a <<< $(ifconfig eth0 | grep ether) && echo ${a[1]}
#str=$(ifconfig eth0 | grep ether) && echo $str | cut -d ' ' -f 2
str=$(ip address show dev eth0 | grep ether) && echo $str | cut -d ' ' -f 2

