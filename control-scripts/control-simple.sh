#!/bin/bash

if [ -z "$1" ]; then
	echo "usage: $0 command"
	exit
fi

# set action to value of $1
ACTION="$1"

# declare arrays
declare -a ips
declare -a res

# generate the IP list or use the existing one
if [ ! -e "ip_list" ]; then
	# discover all IPs on this network
	echo "obtaining IPs on this network and generating new ip_list..."
	nmap -n -sn 10.0.1.* -oG - | awk '/Up$/{print $2}' | tee ip_list
fi

# for each active IP that is not the router or the client
for i in $(cat ip_list); do
	if [ $i != "10.0.1.1" -a $i != $(hostname -I) ]; then
	
		# add ip to the list
		ips+=("${i}")
		
		# capture the result of ssh
		res+=("$(ssh -f $i $ACTION)")
		
	fi
done

# create a index variable for output purposes
c=0

# iterate over the ips
for j in "${ips[@]}"; do
	echo " $j"
	echo "  ${res[$c]}"
	echo ""
	((c++))
done
