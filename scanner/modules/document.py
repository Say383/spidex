from datetime import datetime
from loguru import logger

from login import anonymous_login
from config import CITY, ASN
from tags import tags, get_os

import geoip2.database

def create_document(ip, ports_dict, banners, hostname, image, connection):
    try:
        keys = list(ports_dict.keys())
        values = list(ports_dict.values())

        with geoip2.database.Reader(CITY) as geo_reader:
            response = geo_reader.city(ip)
        with geoip2.database.Reader(ASN) as asn_reader:        
            resp = asn_reader.asn(ip)
            
            col = {
                "ip": ip,
                "org": resp.autonomous_system_organization,
                "asn": resp.autonomous_system_number,
                "banners": banners,
                "services": keys,
                "ports": values,
                "hostname": hostname,
                "country": response.country.name,
                "city": response.city.name,
                "country_code": response.country.iso_code,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "screenshot": image,
                "anonymous_login": anonymous_login(ip,ports_dict),
                "tags": tags(ip,ports_dict),
                "os": get_os(banners),
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")

            }
        doc = {k:v for k,v in col.items() if v is not None}
        connection.index(index="devices", document=doc)
    except:
        logger.exception("Exception ocurred:")
    finally:
        logger.success("{} | {} | {} | {}".format(ip,keys,response.country.name,response.city.name))