#!/bin/bash
# Ask for informations used by the various certificates
echo "[*] Information used to generate the various certficates"
echo "[*]   Please enter country name (for example IT for Italy):"
read COUNTRYNAME
echo "[*]   Please enter your state (for example Trentino Alto Adige):"
read STATENAME
echo "[*]   Please enter your locality (for example Povo):"
read LOCALITYNAME
echo "[*]   Please enter your organization name (for example Networking II project):"
read ORGANIZATIONNAME

# Generate the root certificate
echo "[*] Generating the root certificate..."
openssl genrsa -out ca.key.pem 1024
openssl req -new -x509 -key ca.key.pem -out ca.cert.pem -subj "/C=$COUNTRYNAME/ST=$STATENAME/L=$LOCALITYNAME/O=$ORGANIZATIONNAME/CN=ca.localdomain"

echo "[*] Generating the various certificates for the modules"
certficatesToGenerate=( hss mme pcrf smf )
for i in "${certficatesToGenerate[@]}"
do
    echo "[*]   Generating certificate for $i"
    # Modify the template
    cp certconfig.template.conf certconfig.conf
    sed -i "s/KEYFILENAME/$i.key.pem/g" certconfig.conf
    sed -i "s/CTOUSE/$COUNTRYNAME/g" certconfig.conf
    sed -i "s/STTOUSE/$STATENAME/g" certconfig.conf
    sed -i "s/LTOUSE/$LOCALITYNAME/g" certconfig.conf
    sed -i "s/ORGTOUSE/$ORGANIZATIONNAME/g" certconfig.conf
    sed -i "s/CNTOUSE/$i.localdomain/g" certconfig.conf
    # Create a certificate request
    openssl req -new -out $i.localdomain.csr -config certconfig.conf
    # Generate the certificate
    openssl x509 -req -in $i.localdomain.csr -CA ca.cert.pem -CAkey ca.key.pem -CAcreateserial -out $i.cert.new.pem -days 3652
    # Merge the certificate request with the certificate itself
    openssl req -noout -text -in $i.localdomain.csr > $i.cert.pem
    cat $i.cert.new.pem >> $i.cert.pem
    # Remove useless files
    rm $i.localdomain.csr
    rm $i.cert.new.pem
done
echo "[*] Done, cleaning up some files"
rm certconfig.conf