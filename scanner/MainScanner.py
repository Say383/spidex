#Local modules
from logging import exception
from ipaddress import ip_address
from loguru import logger
from datetime import datetime

import queue
import sys
import threading

from Connect import elastic
from login import anonymous_login
from Screenshot import take_screenshot
from Elastic import create_document
from PortScanner import Port_Scanner

class Scanner():
    def __init__(self,start,end,threads,timeout,screenshot):
        self.timeout = timeout
        self.screenshot = screenshot
        self.targets = self.get_ranges(start,end)
        self.threads = threads
        self.connection = elastic
        self.image = None

    def set_ports(self,ports):
        self.ports = ports

    def get_ranges(self,start,end):
        #Get total of ip addresses
        start_int = int(ip_address(start).packed.hex(), 16)
        end_int = int(ip_address(end).packed.hex(), 16)
        return [ip_address(ip).exploded for ip in range(start_int, end_int)]

    def job(self,q,results):
        pool_sema.acquire()
        try:
            while not q.empty():
                ip = q.get()
                Scanner = Port_Scanner(ip)
                Scanner.start(self.timeout,self.ports)
                
                if Scanner.contain_results():
                    ports, banners, hostname = Scanner.get_results()
                    default = anonymous_login(ip,ports)
                    if self.screenshot: self.image = take_screenshot(ip,ports)
                    create_document(ip,ports,banners,hostname,self.image,default,self.connection)
                    results.put(ip)
                q.task_done()
        finally:
            pool_sema.release()

    def start_threads(self):
        #Implemeting Queue, safe threading
        logger.info("Searching connected devices, please wait")
        start = datetime.now()
        q = queue.Queue()
        #Semaphore object limit max number of threads in paralell
        global pool_sema
        pool_sema = threading.Semaphore(value=900)
        #Count total of results with Queue
        results = queue.Queue()
        try:
            logger.info("Launching threads")
            for j in self.targets:
                q.put(j)
            logger.info("Waiting for Queue to complete, {} jobs".format(q.qsize()))
    
            for i in range(self.threads):
                thread = threading.Thread(target=self.job, args=(q,results),daemon=True)
                thread.start()
                
            q.join()
            end = datetime.now()
            elapsed = end-start
            logger.info("Execution time: {}".format(elapsed))
            logger.info("Total discovered devices: {}".format(results.qsize()))
        except KeyboardInterrupt:
            logger.info("You pressed CTRL+C")
            sys.exit(1)
