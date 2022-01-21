export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)
echo
echo "gNB IP Address: ${IP_ADDR}"
echo
cp /UERANSIM/custom-gnb.yaml /UERANSIM/custom-gnb.final.yaml
sed -i "s/IPADDR/${IP_ADDR}/g" /UERANSIM/custom-gnb.final.yaml
./nr-gnb -c custom-gnb.final.yaml
