# Networking II project
## Description
Integrating 4G/5G RAN in Comnetsemu:

The goal is to integrate in comnetsemu VM a mobile cellular RAN using (in our case) UERANSIM.

The integration can be performed by dockerinzing the new components, or connecting the comnetsemu VM with another VM/docker (external integration) and providing the related python scripts.

## Usage
### Requirements
- `git`
- `docker`
- `docker-compose`
### Installation of the necessary files
```bash
bash setup.sh
```
### Start up
```bash
cd UERANSIM
docker-compose up
sudo bash hostScripts/fix_IPTables.sh
```

### Test network speed
In order to test the UE network speed, enter inside the container, and run the following commands:
```bash
ip route del default
ip route add default via 10.45.0.1 dev uesimtun0
ip route add 10.45.0.0/16 dev uesimtun0
```

### Access the open5gs web terminal
Just launch your browser, go to `localhost:3000` and login with username `admin` and password `1423`. 

## Folder structure
- `dockerImages`: Folder containing the various docker images used for the project;
- `dockerImages/UERANSIM`: Docker image for UERANSIM;
- `hostScripts`: Folder containing some scripts that have to be run on the host;
- `UERANSIM`: Folder containing all the configurations for UERANSIM.