#!/bin/bash

export MONGODB_STARTUP_TIME=20

echo "Waiting for " ${MONGODB_STARTUP_TIME} "s for mongodb to be ready..."
sleep ${MONGODB_STARTUP_TIME}

echo "Launching $i..."

touch /var/log/open5gs/$1.log

tail -f /var/log/open5gs/$1.log &

open5gs-$1d -c /etc/open5gs/$1.yaml
