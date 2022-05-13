#!/usr/bin/env python
from loguru import logger
from core.ranges import single_range, multiple_ranges
from core.parser import get_flags
from core.threadscan import Threadscan
from core.logo import title
import config
import sys

def launch_scanner(targets,threads,timeout,top_ports,all_ports,custom):
    Discover = Threadscan(targets)
    Settings = config.Config()

    if top_ports:
        Discover.set_ports(Settings.top_ports)
    elif all_ports:
        Discover.set_ports(Settings.ports)
    elif custom:
        Discover.set_ports(custom)
    else:
        logger.info("Please set port scan mode")
        exit()

    Discover.start_threads(threads,timeout)
    
    devices = Discover.get_devices()

def main():

    print(title)
    
    iprange,threads,path,timeout,top_ports,all_ports,custom,logs = get_flags()

    logger.remove(0)

    logger.add(sys.stderr,colorize=True,format="<blue>{time:HH:mm:ss}</blue> | <level>{level: <8}</level> | <level>{message}</level>", enqueue=True)

    if logs:
        logger.add("logs/{time}.log", enqueue=True)
        
    if  iprange:
        targets = single_range(iprange)
        launch_scanner(targets,threads,timeout,top_ports,all_ports,custom)

    elif path:
        targets = multiple_ranges(path)
        launch_scanner(targets,threads,timeout,top_ports,all_ports,custom)
    else:
        logger.info("Please use -h to see all options")
        exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("You pressed CRTL+C")
        exit()
