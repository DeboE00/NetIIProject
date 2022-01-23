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
```

## Folder structure
- `dockerImages`: Folder containing the various docker images used for the project;
- `dockerImages/UERANSIM`: Docker image for UERANSIM;
- `UERANSIM`: Folder containing all the configurations for UERANSIM.