#!/usr/bin/env python
import collections
from loguru import logger
from modules.logo import title
from modules.Commands import get_flags
from configs.Ports import TOP_PORTS, COMMON_PORTS
from core.MainScanner import Scanner
from modules.mongo import insert_data
from modules.slack import send_message
from modules.save  import save_json

from configs import log
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

def launch_scanner(start,end,threads,timeout,top_ports,all_ports,slack,custom,save):
    Discover = Scanner(start,end)

    if top_ports:
        Discover.set_ports(TOP_PORTS)
    elif all_ports:
        Discover.set_ports(COMMON_PORTS)
    elif custom:
        Discover.set_ports(custom)

    Discover.start_threads(threads,timeout)
    results = Discover.slack_message()
    send_message(results,slack)

    devices = Discover.get_devices()
    if devices:
        if save == "mongodb":
            insert_data(devices)
        elif save == "json":
            logger.info("Saving results at {}".format(save_json(devices)))

def main():
    print(title)
    start, end, threads, path, timeout, top_ports, all_ports, custom, slack, save, logs = get_flags()

    if logs:
        logger.add("logs/{time}.log", enqueue=True)
        
    if  start and end:
        launch_scanner(start,end,threads,timeout,top_ports,all_ports,slack,custom,save)

    elif path:
        countries = get_country_ip_blocks(path)
        for ip in countries:
            start = ip[0]
            end = ip[1]
            launch_scanner(start,end,threads,timeout,top_ports,all_ports,slack,custom,save)
    else:
        logger.info("Please use -h to see all options")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("You pressed CRTL+C")
        sys.exit(1)
