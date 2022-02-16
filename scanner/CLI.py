#!/usr/bin/env python
from loguru import logger
from modules.logo import title
from modules.Commands import get_flags
from configs.Ports import TOP_PORTS, COMMON_PORTS
from core.MainScanner import Scanner
from modules.mongo import collection
from modules.slack import send_message
import sys

#Search country IP blocks in https://www.nirsoft.net/countryip{COUNTRY_CODE}.html
def get_country_ip_blocks(file):
    total = []
    with open(file, 'r') as flist:
        blocks = list(filter(None,flist.read().splitlines()))
    for ip in blocks:
        line = ip.split(",")
        block = [line[0],line[1]]
        total.append(block)
    return total

def launch_scanner(start,end,threads,timeout,top_ports,all_ports,slack):
    Discover = Scanner(start,end)

    if top_ports:
        Discover.set_ports(TOP_PORTS)
    elif all_ports:
        Discover.set_ports(COMMON_PORTS)
    else:
        Discover.set_ports(TOP_PORTS)

    Discover.start_threads(threads,timeout)
    results = Discover.slack_message()
    send_message(results,slack)

    devices = Discover.get_devices()
    if devices:
        logger.info("Inserting results in database...")
        collection.insert_many(devices)

def main():
    print(title)
    start, end, threads, path, timeout, top_ports, all_ports, slack = get_flags()
    #Verify argument validity
    if  start and end:
        launch_scanner(start,end,threads,timeout,top_ports,all_ports,slack)

    elif path:
        countries = get_country_ip_blocks(path)
        for ip in countries:
            start = ip[0]
            end = ip[1]
            launch_scanner(start,end,threads,timeout,top_ports,all_ports,slack)
    else:
        logger.info("Please use -h to see all options")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("You pressed CRTL+C")
        sys.exit(1)
