#!/bin/sh

echo "Launching SMF..."

ip tuntap add name ogstun mode tun
sysctl -w net.ipv6.conf.ogstun.disable_ipv6=0
ip addr add 45.45.0.1/16 dev ogstun
ip link set ogstun up

# masquerade
sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -I INPUT -i ogstun -j ACCEPT

touch /var/log/open5gs/smf.log

tail -f /var/log/open5gs/smf.log &

open5gs-smfd -c /etc/open5gs/smf.yaml