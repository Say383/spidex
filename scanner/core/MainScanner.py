#Local modules
from loguru import logger
from queue import Queue

import sys
import threading

from core.PortScanner import Port_Scanner
from modules.test_time import execution_time
from modules.document import create_document
from modules.ranges import get_ranges

class Scanner():
    def __init__(self,start,end):
        self.targets = get_ranges(start,end)
        self.results = Queue()

    def set_ports(self,ports):
        self.ports = ports

    def job(self,q,timeout):
        try:
            pool_sema.acquire()

            while not q.empty():
                ip = q.get()
                Scanner = Port_Scanner(ip)
                Scanner.start(timeout,self.ports)

                if Scanner.contain_results():
                    ports, banners, hostname = Scanner.get_results()
                    device = create_document(ip,ports,banners,hostname)
                    
                    self.results.put(device)

                q.task_done()
        finally:
            pool_sema.release()

    @execution_time
    def start_threads(self,threads,timeout):
        #Implemeting Queue, safe threading

        q = Queue()
        global pool_sema

        logger.info("Searching connected devices, please wait")
        #Semaphore object limit max number of threads in paralell
        pool_sema = threading.Semaphore(value=400)
        #Count total of results with Queue
        try:
            logger.info("Launching threads")
            for j in self.targets:
                q.put(j)
            logger.info("Waiting for Queue to complete, {} jobs".format(q.qsize()))

            for i in range(threads):
                thread = threading.Thread(target=self.job, args=(q,timeout),daemon=True)
                thread.start()

            q.join()

            logger.info("Total Discovered devices: {}".format(self.results.qsize()))

        except KeyboardInterrupt:
            logger.info("You pressed CTRL+C")
            sys.exit(1)

    def slack_message(self):
        return self.results.qsize()

    def get_devices(self):
        return list(self.results.queue)
    
    