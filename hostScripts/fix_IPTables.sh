#!/bin/bash

if [[ $EUID -ne 0 ]]; then
# Check if I am root
   echo "This script must be run as root, use sudo "$0" instead" 1>&2
   exit 1
fi

echo "Configuring IPTables to enable communication with internet through uesimtun0 tunnel inside the UEs..."

#commands coming from: https://github.com/free5gc/free5gc-compose/issues/26
sudo iptables -t nat -A POSTROUTING -o eth0  -j MASQUERADE
sudo iptables -I FORWARD 1 -j ACCEPT

echo "Done"