# Networking II project
## Description
Integrating 4G/5G RAN in ComNetsEmu:

The goal is to integrate in ComNetsEmu VM a mobile cellular RAN using (in our case) UERANSIM.

The integration can be performed by dockerinzing the new components, ~~or connecting the comnetsemu VM with another VM/docker (external integration)~~ and providing the related python scripts.

## Usage
### Requirements
- `git`
- `docker`
- `docker-compose`
### Installation of the necessary files
```bash
cd comnetsemu/app/
git clone https://github.com/DeboE00/NetIIProject -o network2_project
cd network2_project
sudo bash setup.sh
```
### Start up (without `ComNetsEmu`)
```bash
cd UERANSIM
docker-compose up
sudo bash ../hostScripts/fix_IPTables.sh
```

### Start up (within `ComNetsEmu`)
```bash
sudo bash setup.sh
cd comnetsemu
sudo python3 network.py # Insert eventual flags here
```

The `network.py script` have some flags, used for enabling some normally-hidden features:

| Flag | Description |
| :--: | :---------- |
| `-i` | Run a terminal inside each container (without starting the actual network) |
| `-p` | Plots the network graph (file `netTopo.png`) |
| `-d` | Set logging to `debug` |

### Test network speed
In order to test the UE network speed, enter inside the container, and run the following commands:
```bash
ip route del default
ip route add default via 10.45.0.1 dev uesimtun0
ip route add 10.45.0.0/16 dev uesimtun0
```

### UE troubleshooting
In case the UE don't connect, it is possible to restart it by issuing the following commands:
```bash
docker exec -it ue1 /bin/bash
top
# Find the pid of the process called "nr-ue" than terminate with Ctrl+C
kill <pid>
./nr-ue -c custom-ue.yaml &
```

### Access the Open5GS web terminal
If you are running the project on your machine (without the Vagrant VM), just launch your browser, go to `localhost:3000` and login with username `admin` and password `1423`.

When running inside the ComNetsEmu Vagrant VM, install Firefox or Google Chrome (disabling hardware acceleration) and go to `10.1.0.6:3000`.

## Folder structure
- `comnetsemu`: Folder containing the scripts used by ComNetsEmu 
- `dockerImages`: Folder containing the various docker images used for the project;
- - `Mongodb`: Docker image for Mongodb;
- - `open5gs`: Docker image for Open5GS;
- - `UERANSIM`: Docker image for UERANSIM;
- `hostScripts`: Folder containing some scripts that have to be run on the host;
- `UERANSIM`: Folder containing all the configurations for UERANSIM.