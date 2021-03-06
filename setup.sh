#!/bin/bash
# Setup script

# Specify here if you want to perform a complete recompile
ADDITIONAL_DOCKER_PARAMS="--no-cache"
# Setup the required docker-compose if not installed
if ! [ -x "$(command -v docker-compose)" ]; then
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi
# Setup graphviz, for graphing the network
sudo apt update
sudo apt install graphviz python3-pygraphviz -y --no-install-recommends
# Install the python requirements for the project
sudo pip install -r requirements.txt
# Create the open5gs image
cd dockerImages/open5gs
OPEN5GS_VERSION=v2.4.4 docker build $ADDITIONAL_DOCKER_PARAMS --force-rm -t project:open5gs .
# Create the UERANSIM image
cd ../UERANSIM
docker build $ADDITIONAL_DOCKER_PARAMS --force-rm -t project:ueransim .
# Create the custom mongodb image
cd ../Mongodb
docker build $ADDITIONAL_DOCKER_PARAMS --force-rm -t project:mongodb .
# Create the project's images
cd ../../UERANSIM
docker-compose build $ADDITIONAL_DOCKER_PARAMS