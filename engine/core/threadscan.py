#Local modules
from loguru import logger
import queue

import threading

from core.portscan import Portscan
from core.timer import execution_time
from core.geoparser import create_json

'''
Threadscan class receives the queue with the ip addresses and starts threads.
Then it instantiates the portscan object.
If the portscan contains valid targets, it calls a function to process and send that data to an API.
'''

class Threadscan():
    def __init__(self,targets):
        self.q = targets
        self.results = queue.Queue()
        self.lock = threading.Lock()
        self.count = 0
        self.total = self.q.qsize()

    def set_ports(self,ports):
        self.ports = ports

    def job(self,timeout):
        while True:
            try:
                ip = self.q.get(timeout=3)
                self.progress_bar()

            except queue.Empty:
                return

            Scanner = Portscan(ip)
            Scanner.start(timeout,self.ports)

            if Scanner.contain_results():
                banners, hostname, ports, tags = Scanner.get_results()
                device = create_json(ip,banners,hostname,ports,tags)
                #MODULO API
                self.results.put_nowait(device)
                
            self.q.task_done()

    @execution_time
    def start_threads(self,max_threads,timeout):
        #Implemeting Queue, safe threading

        logger.info("Searching connected devices, please wait")
        #Count total of results with Queue
        try:
            logger.info("Launching threads")

            logger.info(f"Waiting for Queue to complete, {self.q.qsize()} jobs")

            for _ in range(max_threads):
                thread = threading.Thread(target=self.job,args=(timeout,),daemon=True)
                thread.start()

            self.q.join()
            logger.info(f"Total discovered devices: {self.results.qsize()}")

        except KeyboardInterrupt:
            logger.info("You pressed CTRL+C")
            exit()

    def progress_bar(self):
        with self.lock:

            self.count += 1
            percent = (self.count * 100) / self.total
            output = "{}% {}/{}".format(percent,self.count, self.total)
            print(output, end="\r")

    def get_devices(self):
        return self.results.qsize()


