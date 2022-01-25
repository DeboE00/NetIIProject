#!/bin/sh
export AMF_STARTUP_TIME=20
export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)
echo
echo "gNB IP Address: ${IP_ADDR}"
echo

echo "Waiting for " ${AMF_STARTUP_TIME} "s for the AMF to be ready..."
sleep ${AMF_STARTUP_TIME}

cp /UERANSIM/custom-gnb.yaml /UERANSIM/custom-gnb.final.yaml
sed -i "s/IPADDR/${IP_ADDR}/g" /UERANSIM/custom-gnb.final.yaml
./nr-gnb -c custom-gnb.final.yaml
