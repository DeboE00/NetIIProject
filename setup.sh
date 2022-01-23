#!/bin/bash
cd UERANSIM/
git clone https://github.com/open5gs/open5gs.git
cd open5gs/docker
USER=open5gs DIST=ubuntu TAG=bionic BRANCH=v2.4.3 docker-compose build
