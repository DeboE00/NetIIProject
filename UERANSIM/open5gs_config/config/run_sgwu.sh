#!/bin/sh


echo "Launching SGWU..."

touch /var/log/open5gs/sgwu.log

tail -f /var/log/open5gs/sgwu.log &

open5gs-sgwud -c /etc/open5gs/sgwu.yaml
