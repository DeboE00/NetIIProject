#!/bin/bash
# Simply launch the specified Open5GS component 

echo "Launching $1..."

touch /var/log/open5gs/$1.log

tail -f /var/log/open5gs/$1.log &

open5gs-$1d -c /etc/open5gs/$1.yaml
