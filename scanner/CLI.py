#!/usr/bin/env python
from loguru import logger
from datetime import datetime

from logo import title
from Commands import get_flags
from Ports import TOP_PORTS, COMMON_PORTS
from MainScanner import Scanner

import sys
import webtech

#Search country IP blocks in https://www.nirsoft.net/countryip{COUNTRY_CODE}.html
def get_country_ip_blocks(file):
    total = []
    with open(file, 'r') as flist:
        blocks = list(filter(None,flist.read().split('\n')))
    for ip in blocks:
        line = ip.split(",")
        block = [line[0],line[1]]
        total.append(block)
    return total

def massive_scan(path,threads,timeout,screenshot,top_ports,all_ports):
    #Scan total of ip blocks in file
    countries = get_country_ip_blocks(path)
    for ip in countries:
        start = ip[0]
        end = ip[1]
        Discover = Scanner(start, end, threads,timeout,screenshot)
        set_port_scan(Discover,top_ports,all_ports)
        Discover.start_threads()

def set_port_scan(Discover,top_ports,all_ports):
    if top_ports:
        Discover.set_ports(TOP_PORTS)
    elif all_ports:
        Discover.set_ports(COMMON_PORTS)
    else:
        Discover.set_ports(TOP_PORTS)

def main():
    print(title)
    start, end, threads, path, timeout, screenshot, top_ports, all_ports, update = get_flags()
    #Verify argument validity
    if  start and end:
        Discover = Scanner(start,end,threads,timeout,screenshot)
        set_port_scan(Discover,top_ports,all_ports)
        Discover.start_threads()

    elif path:
        start = datetime.now()
        massive_scan(path,threads,timeout,screenshot,top_ports,all_ports)
        end = datetime.now()
        elapsed = end-start
        logger.info("Total execution time: {}".format(elapsed))

    elif update: 
        webtech.database.update_database(force=True)        
    else:
        logger.info("Please use -h to see all options")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("You pressed CRTL+C")
        sys.exit(1)
