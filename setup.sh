#!/bin/bash
# Setup the required package
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# Create the open5gs image
cd UERANSIM/
git clone https://github.com/open5gs/open5gs.git
cd open5gs/docker
USER=open5gs DIST=ubuntu TAG=focal BRANCH=v2.4.3 docker-compose build
# Create the UERANSIM image
cd ../../../dockerImages/UERANSIM
docker build -t registry.enricodebon.com:5000/university/networking-ii-2022-2021/project:ueransim .
# Create the custom mongodb image
cd ../Mongodb
docker build -t registry.enricodebon.com:5000/university/networking-ii-2022-2021/project:mongodb .
# Create the project's images
cd ../../UERANSIM
docker-compose build