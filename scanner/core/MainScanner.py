#Local modules
from loguru import logger
import queue

import sys
import threading

from core.PortScanner import Port_Scanner
from modules.test_time import execution_time
from modules.document import create_document
from modules.ranges import get_ranges

class Scanner():
    def __init__(self,start,end):
        self.targets = get_ranges(start,end)
        self.results = queue.Queue()
        self.count = 0
        self.q = queue.Queue()
        self.lock = threading.Lock()

    def set_ports(self,ports):
        self.ports = ports

    def job(self,timeout):
        while True:
            try:
                ip = self.q.get(timeout=3)
            except queue.Empty:
                return
            Scanner = Port_Scanner(ip)
            Scanner.start(timeout,self.ports)

            if Scanner.contain_results():
                banners, hostname, ports, tags = Scanner.get_results()
                device = create_document(ip,banners,hostname,ports,tags)

                self.results.put_nowait(device)

            with self.lock:

                self.count += 1
                percent = (self.count*100)/len(self.targets)
                output = "{}% {}/{}".format(percent,self.count,len(self.targets))
                print(output, end="\r")

            self.q.task_done()

    def set_ports(self,ports):
        self.ports = ports

    @execution_time
    def start_threads(self,threads_number,timeout):
        #Implemeting Queue, safe threading

        logger.info("Searching connected devices, please wait")
        #Count total of results with Queue
        try:
            logger.info("Launching threads")
            for j in self.targets:
                self.q.put_nowait(j)

            logger.info(f"Waiting for Queue to complete, {self.q.qsize()} jobs")

            for _ in range(threads_number):
                thread = threading.Thread(target=self.job,args=(timeout,),daemon=True)
                thread.start()

            self.q.join()

            logger.info(f"Total discovered devices: {self.results.qsize()}")

        except KeyboardInterrupt:
            logger.info("You pressed CTRL+C")
            sys.exit(1)

    def slack_message(self):
        return self.results.qsize()

    def get_devices(self):
        return list(self.results.queue)
