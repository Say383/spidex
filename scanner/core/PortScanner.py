import socket
from loguru import logger

#logger.add(enqueue=True, level="DEBUG", backtrace=True, diagnose="True")

#Basic exception handling
class Port_Scanner():
    def __init__(self, ip):
        self.ip = ip
        self.hostname = []
        self.banners = []
        self.ports = {}
        
    def start(self,timeout,ports):
        for port in ports:

            target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target.settimeout(timeout)
            target.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                response = target.connect_ex((self.ip, port))
                if  response == 0:
                    service = socket.getservbyport(port)
                    self.banners.append(self.get_banner(target,service))
                    self.hostname = socket.gethostbyaddr(self.ip)[0]
                    self.ports.update({service : port})

            except socket.timeout: logger.debug("{} | Socket timed out".format(self.ip))
            except ConnectionResetError: logger.debug("{} | Connection reseted by host".format(self.ip))
            except OSError: logger.error("Disconnected from the network")
            finally:
                target.close()

    def get_banner(self,target,service):
        if "http" in service: target.send(b'GET HTTP/1.1 \r\n')
        return target.recv(1024).decode("utf-8", errors='ignore')

    def contain_results(self):
        if len(self.ports.keys()) != 0: return True
    
    def get_results(self):
        return self.ports, self.banners, self.hostname
