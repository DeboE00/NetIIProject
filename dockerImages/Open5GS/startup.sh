export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)
echo
echo "AMF IP Address: ${IP_ADDR}"
echo
cp /etc/open5gs/amf.template.yaml /etc/open5gs/amf.yaml
sed -i "s/IPADDR/${IP_ADDR}/g" /etc/open5gs/amf.yaml
systemctl restart open5gs-amfd
