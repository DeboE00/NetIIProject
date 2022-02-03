#!/bin/bash
# Specify here if you want to perform a complete recompile
ADDITIONAL_DOCKER_PARAMS="--no-cache"
# Setup the required docker-compose if not installed
if ! [ -x "$(command -v docker-compose)" ]; then
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi
# Create the open5gs image
cd UERANSIM/
if [ -d "open5gs" ]; then
    cd open5gs
    git pull
    cd ..
else
    git clone https://github.com/open5gs/open5gs.git
fi

cd open5gs/docker
USER=open5gs DIST=ubuntu TAG=focal BRANCH=v2.4.4 docker-compose build $ADDITIONAL_DOCKER_PARAMS
# Create the open5gs images with tools
cd ../../../dockerImages/open5gsWtools
docker build $ADDITIONAL_DOCKER_PARAMS -t project:open5gsWtools .
# Create the open5gs web image with tools
cd ../open5gsWebWtools
docker build $ADDITIONAL_DOCKER_PARAMS -t project:open5gsWebWtools .
# Create the UERANSIM image
cd ../UERANSIM
docker build $ADDITIONAL_DOCKER_PARAMS -t project:ueransim .
# Create the custom mongodb image
cd ../Mongodb
docker build $ADDITIONAL_DOCKER_PARAMS -t project:mongodb .
# Create the project's images
cd ../../UERANSIM
docker-compose build $ADDITIONAL_DOCKER_PARAMS