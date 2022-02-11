#!/bin/bash

echo "Launching $1..."

ip tuntap add name ogstun mode tun
#sysctl -w net.ipv6.conf.ogstun.disable_ipv6=1
ip addr add 10.45.0.1/16 dev ogstun
ip link set ogstun up
iptables -t nat -A POSTROUTING -s 10.45.0.1/16 ! -o ogstun -j MASQUERADE

# masquerade
#sysctl -w net.ipv4.ip_forward=1
#iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
#iptables -I INPUT -i ogstun -j ACCEPT

touch /var/log/open5gs/$1.log

tail -f /var/log/open5gs/$1.log &

open5gs-$1d -c /etc/open5gs/$1.yaml
