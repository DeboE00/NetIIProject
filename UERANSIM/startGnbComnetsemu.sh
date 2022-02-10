#!/bin/sh
export AMF_STARTUP_TIME=30
export IP_ADDR=$(ifconfig gnb1-s2 | grep 'inet' | cut -d ' ' -f 10)
echo
echo "gNB IP Address: ${IP_ADDR}"
echo

echo "Waiting for " ${AMF_STARTUP_TIME} "s for the AMF to be ready..."
sleep ${AMF_STARTUP_TIME}

cp /UERANSIM/custom-gnb.yaml /UERANSIM/custom-gnb.final.yaml
sed -i "s/IPADDR/${IP_ADDR}/g" /UERANSIM/custom-gnb.final.yaml
./nr-gnb -c custom-gnb.final.yaml
