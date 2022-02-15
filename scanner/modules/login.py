from ftplib import FTP, error_temp
from loguru import logger

import socket
import ftplib

def anonymous_login(ip,ports):
    if "ftp" in ports:
        try:
            ftp = FTP(ip)
            ftp.connect(ip, ports["ftp"], timeout=5)
            ftp.login("anonymous","anonymous")
            ftp.quit()
            logger.info("Detected default login on: {}".format(ip))
            return True
            #Fix issue with EOFError
        except (ftplib.error_temp, ftplib.error_perm, socket.timeout, EOFError, ConnectionRefusedError, OSError):
            return False
 