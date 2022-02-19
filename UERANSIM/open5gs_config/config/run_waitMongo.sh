#!/bin/bash
# Launch the specified Open5GS component waiting for the MongoDB database to be online

export MONGODB_STARTUP_TIME=20

echo "Waiting for " ${MONGODB_STARTUP_TIME} "s for mongodb to be ready..."
sleep ${MONGODB_STARTUP_TIME}

echo "Launching $i..."

touch /var/log/open5gs/$1.log

tail -f /var/log/open5gs/$1.log &

open5gs-$1d -c /etc/open5gs/$1.yaml
