#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple network topology with all the host running
 the various Open5GS containers and services, and one
 host for UERANSIM's GNB and one for UERANSIM's UE
"""

import argparse

from comnetsemu.clean import cleanup
from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import error, info, setLogLevel
from mininet.node import Controller

def initialize5GNet(interactive):
    bind_dir = "/home/vagrant"
    parent_dir = "/home/vagrant/comnetsemu/comnetsemu_open5gs"

    net = Containernet(controller=Controller, link=TCLink)

    try:
        info("*** Adding Open5G components\n")
        info("*** \tMongoDB server\n")
        mongoDb = net.addDockerHost("mongodb",
                                    dimage="registry.enricodebon.com:5000/university/networking-ii-2022-2021/project:mongodb",
                                    ip="10.1.0.5/24",
                                    docker_args={
                                        "volumes": {
                                            bind_dir + "/mongodbdata": {
                                                "bind": "/data/db",
                                                "mode": "rw",
                                            },
                                            "/etc/timezone": {
                                                "bind": "/etc/timezone",
                                                "mode": "ro",
                                            },
                                            "/etc/localtime": {
                                                "bind": "/etc/localtime",
                                                "mode": "ro",
                                            }
                                        }
                                    })
        mongoDbLoader = net.addDockerHost("mongodbloader",
                                    dimage="mongo:latest",
                                    ip="10.1.0.50/24",
                                    docker_args={                                        
                                        #"environment": {
                                        #    "DB_HOST=10.1.0.5"
                                        #},
                                        "volumes": {
                                            bind_dir + "/open5gs_config/provisioning/db": {
                                                "bind": "/run_db.sh:/tmp/run.sh",
                                                "mode": "ro",
                                            },
                                            bind_dir + "/open5gs_config/provisioning/db": {
                                                "bind": "/subscribers.json:/tmp/subscribers.json",
                                                "mode": "ro",
                                            },
                                            bind_dir + "/open5gs_config/provisioning/db": {
                                                "bind": "/profiles.json:/tmp/profiles.json",
                                                "mode": "ro",
                                            }
                                        }
                                    })
        webui = net.addDockerHost("webui",
                                dimage="open5gs/open5gs-webui:latest",
                                ip="10.1.0.6/24",
                                docker_args={                                    
                                        #"environment": {
                                        #    "DB_URI=mongodb://10.1.0.5/open5gs"
                                        #},                                        
                                        "ports": {
                                            "3000:3000"
                                        },
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro",
                                            }
                                        }
                                    })
        nrf = net.addDockerHost("nrf",
                                dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.10/24",
                                docker_args={                                                                           
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/nrf:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        ausf = net.addDockerHost("ausf",
                                dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.12/24",
                                docker_args={                                                                           
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/ausf:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        udm = net.addDockerHost("udm",
                                dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.13/24",
                                docker_args={                                                                        
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/udm:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        pcf = net.addDockerHost("pcf",
                                dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.14/24",
                                docker_args={                                                                           
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/pcf:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        nssf = net.addDockerHost("nssf",
                                dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.15/24",
                                docker_args={                                                                         
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/nssf:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        bsf = net.addDockerHost("bsf",
                                dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.16/24",
                                docker_args={                                                                          
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/bsf:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        udr = net.addDockerHost("udr",
                                dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.17/24",
                                docker_args={                                                                         
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/udr:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        upf = net.addDockerHost("upf",
                                #TODO:ADD IMAGE
                                dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                #build="./open5gs_config/pgw",
                                ip="10.1.0.19/24",
                                docker_args={                                                                             
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/upf:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        },                                        
                                        "cap_add": [
                                            "NET_ADMIN"
                                        ],
                                        "devices": "/dev/net/tun:/dev/net/tun:rwm"                                        
                                    })
        smf = net.addDockerHost("smf",
                                #TODO:ADD IMAGE
                                #build="./open5gs_config/pgw",
                                ip="10.1.0.18/24",
                                docker_args={                                                                           
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/smf:/var/log/open5gs",
                                                "mode": "rw"
                                            },
                                            bind_dir + "/open5gs_config/config": {
                                                "bind": "/freeDiameter:/etc/freeDiameter",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        pcrf = net.addDockerHost("pcrf",
                                #TODO:ADD IMAGE
                                #dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.20/24",
                                docker_args={                                                                            
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/pcrf:/var/log/open5gs",
                                                "mode": "rw"
                                            },
                                            bind_dir + "/open5gs_config/config": {
                                                "bind": "/freeDiameter:/etc/freeDiameter",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        hss = net.addDockerHost("hss",
                                #TODO:ADD IMAGE
                                #dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.21/24",
                                docker_args={                                     
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/hss:/var/log/open5gs",
                                                "mode": "rw"
                                            },
                                            bind_dir + "/open5gs_config/config": {
                                                "bind": "/freeDiameter:/etc/freeDiameter",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        sgwc = net.addDockerHost("sgwc",
                                #TODO: ADD IMAGE
                                #dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.23/24",
                                docker_args={                                      
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/sgwc:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        sgwu = net.addDockerHost("sgwu",
                                #TODO:ADD IMAGE
                                #dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.24/24",
                                docker_args={                                       
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/sgwu:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        mme = net.addDockerHost("mme",
                                #TODO:ADD IMAGE
                                #dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.22/24",
                                docker_args={                                       
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/mme:/var/log/open5gs",
                                                "mode": "rw"
                                            },
                                            bind_dir + "/open5gs_config/config": {
                                                "bind": "/freeDiameter:/etc/freeDiameter",
                                                "mode": "rw"
                                            }
                                        }
                                    })
        amf = net.addDockerHost("amf",
                                #TODO:ADD IMAGE, fix 2 IPs thing
                                #dimage="open5gs/ubuntu-focal-open5gs-build:latest",
                                ip="10.1.0.11/24",
                                docker_args={
                                        "ports": {
                                            "36412:36412",
                                            "36412:36412/udp",
                                            "2123",
                                            "2123/udp"
                                        },                                       
                                        "volumes": {
                                            bind_dir + "/open5gs_config": {
                                                "bind": "/config:/etc/open5gs",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/open5gs_config/log": {
                                                "bind": "/amf:/var/log/open5gs",
                                                "mode": "rw"
                                            }
                                        }
                                    })
    #UERANSIM SERVICES
        gnb = net.addDockerHost("gnb",
                                dimage="registry.enricodebon.com:5000/university/networking-ii-2022-2021/project:ueransim",
                                ip="10.0.0.11/24",
                                docker_args={
                                        "ports": {
                                            "38412:38412/sctp",
                                            "2152:2152/udp"
                                        },
                                        "cap add": [
                                            "NET_ADMIN"
                                        ],
                                        "devices": "/dev/net/tun:/dev/net/tun:rwm",                                       
                                        "volumes": {
                                            bind_dir + "/startGnb.sh": {
                                                "bind": "/UERANSIM/startGnb.sh",
                                                "mode": "ro"
                                            },
                                            bind_dir + "/custom-gnb.yaml": {
                                                "bind": "/UERANSIM/custom-gnb.yaml",
                                                "mode": "ro"
                                            }
                                        }
                                    })
        ue1 = net.addDockerHost("ue1",
                                dimage="registry.enricodebon.com:5000/university/networking-ii-2022-2021/project:ueransim",
                                ip="10.0.0.25/24",
                                docker_args={                                       
                                        "cap_add": [
                                            "NET_ADMIN"
                                        ],
                                        "devices": "/dev/net/tun:/dev/net/tun:rwm",                                                                                                                      
                                        "volumes": {
                                            bind_dir + "/custom-ue.yaml": {
                                                "bind": "/UERANSIM/custom-ue.yaml",
                                                "mode": "ro"
                                            }
                                        }                                      
                                    })                   
        info("*** Adding controller\n")
        net.addController("c0")

        info("*** Adding switches\n")
        sOpen = net.addSwitch("s1")
        sUeransim = net.addSwitch("s2")

        info("*** Adding links\n")
        net.addLink(mongoDb, sOpen, bw=1000, delay="1ms", intfName1="mongoDb1-s1", intfName2="s1-mongoDb1")

        info("*** Starting network\n")
        net.start()
        net.pingAll()

        if interactive:
            spawnXtermDocker("mongoDb")

            CLI(net)
        else:
            input("Emulation setup ready. Press enter to terminate")
    
    except Exception as e:
        error("*** Emulation has errors: \n")
        error(e, "\n")
        net.stop()

    except KeyboardInterrupt:
        info("*** Aborted, stopping network\n")
        net.stop()
    
    finally:
        info("*** Stopping network\n")
        if interactive:
            net.stop()
        cleanup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Flag to run the script in interactive mode
    parser.add_argument("-i",
                        default=False,
                        const=True,
                        type=bool,
                        nargs="?",
                        help="Run the setup interactively with xterms")

    # Flag to run the script with debug log enabled
    parser.add_argument("-d",
                        default=False,
                        const=True,
                        type=bool,
                        nargs="?",
                        help="Set log level to debug")
    
    args = parser.parse_args()

    # Setup debug log level
    if args.d:
        setLogLevel("debug")
    else:
        setLogLevel("info")
    
    initialize5GNet(args.i)