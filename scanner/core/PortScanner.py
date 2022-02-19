import socket
from loguru import logger
from modules.tags import get_web_technologies

class Port_Scanner():
    def __init__(self, ip):
        self.ip = ip
        self.hostname = []
        self.banners = []
        self.ports = []
        self.tags = None

    @logger.catch
    def start(self,timeout,ports):
        for port in ports:

            target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            target.settimeout(timeout)

            try:
                response = target.connect_ex((self.ip, port))
                if  response == 0:
                    self.ports.append(port)

                    banner = self.get_banner(target)
                    self.banners.append(banner)
                    self.tags = get_web_technologies(self.ip,banner,port)
                    try:
                        self.hostname = socket.gethostbyaddr(self.ip)[0]
                    except socket.herror:
                        self.hostname = None

            except socket.timeout:
                logger.debug(f"{self.ip} Socket timed out")
            except ConnectionResetError:
                logger.debug(f"{self.ip} Connection refused")
            except OSError:
                logger.debug(f"{self.ip} Network error")
            finally:
                target.close()

    def get_banner(self,target):

        byte = "GET / HTTP/1.1\r\nHost: {}\r\nAccept: text/html\r\nConnection: close\r\n\r\n".format(self.ip)
        data = str.encode(byte)
        target.sendall(data)
        return target.recv(4096).decode("utf-8", errors='ignore')

    def contain_results(self):
        if self.ports: return True

    def get_results(self):
        return self.banners, self.hostname, self.ports, self.tags
