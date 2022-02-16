import socket
from loguru import logger

#logger.add(enqueue=True, level="DEBUG", backtrace=True, diagnose="True")

#Basic exception handling
class Port_Scanner():
    def __init__(self, ip):
        self.ip = ip
        self.hostname = []
        self.banners = []
        self.ports = []

    def start(self,timeout,ports):
        for port in ports:

            target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            target.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            target.settimeout(timeout)

            try:
                response = target.connect_ex((self.ip, port))

                if  response == 0:
                    self.ports.append(port)

                    self.banners.append(self.get_banner(target,port))
                    try:
                        self.hostname = socket.gethostbyaddr(self.ip)[0]
                    except socket.herror:
                        self.hostname = None



            except socket.timeout: logger.debug("{} | Socket timed out".format(self.ip))
            except ConnectionResetError: logger.debug("{} | Connection reseted by host".format(self.ip))
            except: logger.exception("Exception ocurred: ")
            finally:
                target.close()

    def get_banner(self,target,port):

        ports = [80,8080,8081,8000,8001,82,8888]

        if port in ports:
            byte = "HEAD / HTTP/1.1\r\nHost: http://{}:{}\r\nAccept: text/html\r\n\r\n".format(self.ip,port)
            data = str.encode(byte)
            target.sendall(data)

        return target.recv(1024).decode("utf-8", errors='ignore')

    def contain_results(self):
        if self.ports: return True

    def get_results(self):
        return self.ports, self.banners, self.hostname
