from datetime import datetime
from loguru import logger

from modules.login import anonymous_login
from configs.config import CITY, ASN
from modules.tags import tags, get_os

import geoip2.database

def create_document(ip, ports, banners, hostname):
    try:
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
                "tags": tags(ip,ports),
                "os": get_os(banners),
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")

            }
        doc = {k:v for k,v in col.items() if v is not None}
    except:
        logger.exception("Exception ocurred:")
    finally:
        logger.success("{} | {} | {} | {}".format(ip,ports,response.country.name,response.city.name))
        return doc