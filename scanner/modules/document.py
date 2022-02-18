from datetime import datetime
from loguru import logger

from modules.login import anonymous_login
from configs.config import CITY, ASN
from modules.tags import tags

import geoip2.database

from colorama import Fore

def create_document(ip, banners, hostname,ports):
    try:
        tag = tags(ip,banners,ports)

        with geoip2.database.Reader(CITY) as geo_reader:
            response = geo_reader.city(ip)
        with geoip2.database.Reader(ASN) as asn_reader:
            resp = asn_reader.asn(ip)

            col = {
                "ip": ip,
                "org": resp.autonomous_system_organization,
                "asn": resp.autonomous_system_number,
                "banners": banners,
                "ports": ports,
                "hostname": hostname,
                "country": response.country.name,
                "city": response.city.name,
                "country_code": response.country.iso_code,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "anonymous_login": anonymous_login(ip,ports),
                "tags": tag,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")

            }
        doc = {k:v for k,v in col.items() if v is not None}
    except:
        logger.exception("Exception ocurred:")
    finally:
        #Formatting output, removig None values
        if tag != None:
            output = f"{ip} {Fore.LIGHTMAGENTA_EX}{ports} {Fore.BLUE}{tag} {Fore.CYAN}{response.country.name} {Fore.WHITE}{response.city.name}"
        else:
            output = f"{ip} {Fore.LIGHTMAGENTA_EX}{ports} {Fore.CYAN}{response.country.name} {Fore.WHITE}{response.city.name}"

        logger.success(output)
    return doc
