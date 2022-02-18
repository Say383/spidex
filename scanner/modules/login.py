from ftplib import FTP, error_temp
from loguru import logger

import socket
import ftplib

@logger.catch
def anonymous_login(ip,ports):
    if 21 in ports:
        try:
            ftp = FTP(ip)
            ftp.connect(ip, 21, timeout=5)
            ftp.login("anonymous","anonymous")
            ftp.quit()
            return True
            
        except (ftplib.error_temp, ftplib.error_perm, socket.timeout, EOFError, ConnectionRefusedError, OSError):
            return False
 