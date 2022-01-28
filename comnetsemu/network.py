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
    
    except Excpetion as e:
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