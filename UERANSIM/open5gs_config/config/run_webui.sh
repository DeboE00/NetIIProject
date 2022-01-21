#!/bin/sh

export MONGODB_STARTUP_TIME=15

echo "Waiting for " ${MONGODB_STARTUP_TIME} "s for mongodb to be ready..."
sleep ${MONGODB_STARTUP_TIME}

npm run start --prefix /usr/src/open5gs/webui
