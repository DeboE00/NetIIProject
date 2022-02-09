#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple network topology with all the host running
 the various Open5GS containers and services, and one
 host for UERANSIM's GNB and one for UERANSIM's UE
"""

import argparse
import time

from comnetsemu.clean import cleanup
from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet
from mininet.link import TCLink
from mininet.log import error, info, setLogLevel
from mininet.node import Controller

def initialize5GNet(interactive):
    bind_dir = "/home/vagrant/comnetsemu/app/network2_project/UERANSIM"
    net = Containernet(controller=Controller, link=TCLink)

    try:
        info("*** Adding Open5G components\n")
        info("*** \t[MongoDB]\tserver\n")
        mongoDb = net.addDockerHost("mongodb",
                                    dimage="project:mongodb",
                                    ip="10.1.0.5/24",
                                    docker_args={
                                        "hostname": "mongodb",
                                        "volumes": {
                                            # Disable temporary the mount dir, as it doesn't work
                                            #bind_dir + "/mongodbdata/": {
                                            #    "bind": "/data/db",
                                            #    "mode": "rw",
                                            #},
                                            bind_dir + "/open5gs_config/log/mongodb": {
                                                "bind": "/var/log/mongodb",
                                                "mode": "rw"
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

        info("*** \t[MongoDB]\tloader\n")
        mongoDbLoader = net.addDockerHost("mongodbloader",
                                    dimage="project:mongodb",
                                    ip="10.1.0.50/24",
                                    docker_args={                                        
                                        "environment": [
                                            "DB_HOST=10.1.0.5"
                                        ],
                                        "hostname": "mongodbloader",
                                        "volumes": {
                                            bind_dir + "/open5gs_config/provisioning/db/run_db.sh": {
                                                "bind": "/tmp/run.sh",
                                                "mode": "ro",
                                            },
                                            bind_dir + "/open5gs_config/provisioning/db/subscribers.json": {
                                                "bind": "/tmp/subscribers.json",
                                                "mode": "ro",
                                            },
                                            bind_dir + "/open5gs_config/provisioning/db/profiles.json": {
                                                "bind": "/tmp/profiles.json",
                                                "mode": "ro",
                                            }
                                        }
                                    })

        info("*** \t[Open5GS]\tWebUI\n")
        webui = net.addDockerHost("webui",
                                dimage="project:open5gsWebWtools",
                                ip="10.1.0.6/24",
                                docker_args={                                    
                                    "environment": [
                                        "DB_URI=mongodb://10.1.0.5/open5gs"
                                    ],                                        
                                    "ports": {
                                        "3000": 3000
                                    },
                                    "hostname": "webui",
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro",
                                        }
                                    }
                                })
        
        info("*** \t[Open5GS]\tnrf\n")
        nrf = net.addDockerHost("nrf",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.10/24",
                                docker_args={
                                    "hostname": "nrf",                                                                   
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/nrf": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tausf\n")
        ausf = net.addDockerHost("ausf",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.12/24",
                                docker_args={
                                    "hostname": "ausf",                                                                    
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/ausf": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    }
                                })
                                
        info("*** \t[Open5GS]\tudm\n")
        udm = net.addDockerHost("udm",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.13/24",
                                docker_args={  
                                    "hostname": "udm",                                                               
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/udm": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tpcf\n")
        pcf = net.addDockerHost("pcf",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.14/24",
                                docker_args={
                                    "hostname": "pcf",                                                              
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/pcf": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tnssf\n")
        nssf = net.addDockerHost("nssf",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.15/24",
                                docker_args={   
                                    "hostname": "nssf",                                                              
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/nssf": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tbsf\n")
        bsf = net.addDockerHost("bsf",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.16/24",
                                docker_args={
                                    "hostname": "bsf",              
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/bsf": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tudr\n")
        udr = net.addDockerHost("udr",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.17/24",
                                docker_args={       
                                    "hostname": "udr",                                                           
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/udr": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tupf\n")
        upf = net.addDockerHost("upf",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.19/24",
                                docker_args={
                                    "hostname": "upf",                                                                
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/upf": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    },                                        
                                    "cap_add": [
                                        "NET_ADMIN"
                                    ],
                                    "devices": "/dev/net/tun:/dev/net/tun:rwm"                                        
                                })

        info("*** \t[Open5GS]\tsmf\n")
        smf = net.addDockerHost("smf",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.18/24",
                                docker_args={
                                    "hostname": "smf",                                                                     
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/smf": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        },
                                        bind_dir + "/open5gs_config/config/freeDiameter": {
                                            "bind": "/etc/freeDiameter",
                                            "mode": "ro"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tpcrf\n")
        pcrf = net.addDockerHost("pcrf",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.20/24",
                                docker_args={
                                    "hostname": "pcrf",                                                               
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/pcrf": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        },
                                        bind_dir + "/open5gs_config/config/freeDiameter": {
                                            "bind": "/etc/freeDiameter",
                                            "mode": "ro"
                                        }
                                    }
                                })
        
        info("*** \t[Open5GS]\thss\n")
        hss = net.addDockerHost("hss",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.21/24",
                                docker_args={
                                    "hostname": "hss",                    
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/hss": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        },
                                        bind_dir + "/open5gs_config/config/freeDiameter": {
                                            "bind": "/etc/freeDiameter",
                                            "mode": "ro"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tsgwc\n")
        sgwc = net.addDockerHost("sgwc",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.23/24",
                                docker_args={
                                    "hostname": "sgwc",
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/sgwc": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tsgwu\n")
        sgwu = net.addDockerHost("sgwu",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.24/24",
                                docker_args={
                                    "hostname": "sgwu",
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/sgwu": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tmme\n")
        mme = net.addDockerHost("mme",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.22/24",
                                docker_args={
                                    "hostname": "mme",
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/mme": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        },
                                        bind_dir + "/open5gs_config/config/freeDiameter": {
                                            "bind": "/etc/freeDiameter",
                                            "mode": "ro"
                                        }
                                    }
                                })

        info("*** \t[Open5GS]\tamf\n")
        amf = net.addDockerHost("amf",
                                dimage="project:open5gsWtools",
                                ip="10.1.0.11/24",
                                docker_args={
                                    "ports": {
                                        "36412":36412,
                                        "36412/udp":36412,
                                        "2123":2123,
                                        "2123/udp":2123
                                    },                                       
                                    "hostname": "amf",
                                    "volumes": {
                                        bind_dir + "/open5gs_config/config": {
                                            "bind": "/etc/open5gs",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/amf": {
                                            "bind": "/var/log/open5gs",
                                            "mode": "rw"
                                        }
                                    }
                                })

        #UERANSIM SERVICES
        info("*** Adding UERANSIM components\n")
        info("*** \t[UERANSIM]\tgnb\n")
        gnb = net.addDockerHost("gnb",
                                dimage="project:ueransim",
                                ip="10.0.0.11/24",
                                docker_args={
                                    "ports": {
                                        "38412/sctp":38412,
                                        "2152/udp":2152
                                    },
                                    "cap_add": [
                                        "NET_ADMIN"
                                    ],
                                    "hostname": "gnb",
                                    "devices": "/dev/net/tun:/dev/net/tun:rwm",                                       
                                    "volumes": {
                                        bind_dir + "/startGnb.sh": {
                                            "bind": "/UERANSIM/startGnb.sh",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/custom-gnb.yaml": {
                                            "bind": "/UERANSIM/custom-gnb.yaml",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/ueransim": {
                                            "bind": "/var/log/ueransim",
                                            "mode": "rw"
                                        }
                                    }
                                })

        info("*** \t[UERANSIM]\tue1\n")
        ue1 = net.addDockerHost("ue1",
                                dimage="project:ueransim",
                                ip="10.0.0.25/24",
                                docker_args={                                       
                                    "cap_add": [
                                        "NET_ADMIN"
                                    ],
                                    "devices": "/dev/net/tun:/dev/net/tun:rwm",     
                                    "hostname": "ue1",                                                                                                                 
                                    "volumes": {
                                        bind_dir + "/custom-ue.yaml": {
                                            "bind": "/UERANSIM/custom-ue.yaml",
                                            "mode": "ro"
                                        },
                                        bind_dir + "/open5gs_config/log/ueransim": {
                                            "bind": "/var/log/ueransim",
                                            "mode": "rw"
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
        net.addLink(mongoDbLoader, sOpen, bw=1000, delay="1ms", intfName1="mongoDbL1-s1", intfName2="s1-mongoDbL1")
        net.addLink(webui, sOpen, bw=1000, delay="1ms", intfName1="webui1-s1", intfName2="s1-webui1")
        net.addLink(nrf, sOpen, bw=1000, delay="1ms", intfName1="nrf1-s1", intfName2="s1-nrf1")
        net.addLink(ausf, sOpen, bw=1000, delay="1ms", intfName1="ausf1-s1", intfName2="s1-ausf1")
        net.addLink(udm, sOpen, bw=1000, delay="1ms", intfName1="udm1-s1", intfName2="s1-udm1")
        net.addLink(pcf, sOpen, bw=1000, delay="1ms", intfName1="pcf1-s1", intfName2="s1-pcf1")
        net.addLink(nssf, sOpen, bw=1000, delay="1ms", intfName1="nssf1-s1", intfName2="s1-nssf1")
        net.addLink(bsf, sOpen, bw=1000, delay="1ms", intfName1="bsf1-s1", intfName2="s1-bsf1")
        net.addLink(udr, sOpen, bw=1000, delay="1ms", intfName1="udr1-s1", intfName2="s1-udr1")
        net.addLink(upf, sOpen, bw=1000, delay="1ms", intfName1="upf1-s1", intfName2="s1-upf1")
        net.addLink(smf, sOpen, bw=1000, delay="1ms", intfName1="smf1-s1", intfName2="s1-smf1")
        net.addLink(pcrf, sOpen, bw=1000, delay="1ms", intfName1="pcrf1-s1", intfName2="s1-pcrf1")
        net.addLink(hss, sOpen, bw=1000, delay="1ms", intfName1="hss1-s1", intfName2="s1-hss1")
        net.addLink(sgwc, sOpen, bw=1000, delay="1ms", intfName1="sgwc1-s1", intfName2="s1-sgwc1")
        net.addLink(sgwu, sOpen, bw=1000, delay="1ms", intfName1="sgwu1-s1", intfName2="s1-sgwu1")
        net.addLink(mme, sOpen, bw=1000, delay="1ms", intfName1="mme1-s1", intfName2="s1-mme1")

        # Connect the AMF to both networks
        net.addLink(amf, sOpen, bw=1000, delay="1ms", intfName1="amf1-s1", intfName2="s1-amf1")
        net.addLink(amf, sUeransim, bw=1000, delay="1ms", intfName1="amf1-s2", intfName2="s2-amf1")
        amf.intfs[1].setIP('10.0.0.4/24')

        net.addLink(gnb, sUeransim, bw=1000, delay="1ms", intfName1="gnb1-s2", intfName2="s2-gnb1")
        net.addLink(ue1, sUeransim, bw=1000, delay="1ms", intfName1="ue1-s2", intfName2="s2-ue1")

        info("*** Starting network\n")
        net.start()
        # Ping all open5gs hosts
        net.ping([mongoDb, webui, nrf, ausf, udm, pcf, nssf, bsf, udr, upf, smf, pcrf, hss, sgwc, sgwu, mme, amf])
        # Ping all UERANSIM hosts
        net.ping([amf, gnb, ue1])

        if interactive:
            spawnXtermDocker("mongoDb")
            spawnXtermDocker("mongoDbLoader")
            spawnXtermDocker("webui")
            spawnXtermDocker("nrf")
            spawnXtermDocker("ausf")
            spawnXtermDocker("udm")
            spawnXtermDocker("pcf")
            spawnXtermDocker("nssf")
            spawnXtermDocker("bsf")
            spawnXtermDocker("udr")
            spawnXtermDocker("upf")
            spawnXtermDocker("smf")
            spawnXtermDocker("pcrf")
            spawnXtermDocker("hss")
            spawnXtermDocker("sgwc")
            spawnXtermDocker("sgwu")
            spawnXtermDocker("mme")
            spawnXtermDocker("amf")
            spawnXtermDocker("gnb")
            spawnXtermDocker("ue1")

            CLI(net)
        else:
            info("*** Starting MongoDB...\n")
            mongoDb.sendCmd("mongod --dbpath /data/db --logpath /var/log/mongodb/mongodb.log --logRotate reopen --logappend --bind_ip_all")

            info("*** Import MongoDB data\n")
            mongoDbLoader.sendCmd("/bin/sh /tmp/run.sh")

            info("*** Starting webui...\n")
            webui.sendCmd("/bin/sh /etc/open5gs/run_webui.sh")

            info("*** Starting nrf...\n")
            nrf.sendCmd("/bin/sh /etc/open5gs/run_waitMongo.sh nrf")
            time.sleep(5)
            
            info("*** Starting ausf...\n")
            ausf.sendCmd("/bin/sh /etc/open5gs/run_standalone.sh ausf")

            info("*** Starting udm...\n")
            udm.sendCmd("/bin/sh /etc/open5gs/run_standalone.sh udm")

            info("*** Starting pcf...\n")
            pcf.sendCmd("/bin/sh /etc/open5gs/run_waitMongo.sh pcf")

            info("*** Starting nssf...\n")
            nssf.sendCmd("/bin/sh /etc/open5gs/run_standalone.sh nssf")

            info("*** Starting bsf...\n")
            bsf.sendCmd("/bin/sh /etc/open5gs/run_waitMongo.sh bsf")

            info("*** Starting udr...\n")
            udr.sendCmd("/bin/sh /etc/open5gs/run_waitMongo.sh udr")

            info("*** Starting upf...\n")
            upf.sendCmd("/bin/sh /etc/open5gs/run_virtualNet.sh upf")
            time.sleep(5)

            info("*** Starting smf...\n")
            smf.sendCmd("/bin/sh /etc/open5gs/run_virtualNet.sh smf")
            time.sleep(5)

            info("*** Starting pcrf...\n")
            pcrf.sendCmd("/bin/sh /etc/open5gs/run_waitMongo.sh pcrf")

            info("*** Starting hss...\n")
            hss.sendCmd("/bin/sh /etc/open5gs/run_waitMongo.sh hss")

            info("*** Starting sgwc...\n")
            sgwc.sendCmd("/bin/sh /etc/open5gs/run_standalone.sh sgwc")
            time.sleep(5)

            info("*** Starting sgwu...\n")
            sgwu.sendCmd("/bin/sh /etc/open5gs/run_standalone.sh sgwu")

            info("*** Starting mme...\n")
            mme.sendCmd("/bin/sh /etc/open5gs/run_standalone.sh mme")

            info("*** Starting amf...\n")
            amf.sendCmd("/bin/sh /etc/open5gs/run_waitMongo.sh amf")
            time.sleep(5)

            info("*** Starting the gnb...\n")
            gnb.sendCmd("bash startGnb.sh >> /var/log/ueransim/gnb.log")

            info("*** Starting the UE...\n")
            ue1.sendCmd("./nr-ue -c custom-ue.yaml >> /var/log/ueransim/ue1.log")

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