#!/bin/bash
# Create the open5gs image
cd UERANSIM/
git clone https://github.com/open5gs/open5gs.git
cd open5gs/docker
USER=open5gs DIST=ubuntu TAG=focal BRANCH=v2.4.3 docker-compose build
# Create the UERANSIM image
cd ../../../dockerImages/UERANSIM
docker build -t registry.enricodebon.com:5000/university/networking-ii-2022-2021/project:ueransim .