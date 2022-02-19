from datetime import datetime
from loguru import logger

from modules.login import anonymous_login
from configs.config import CITY, ASN

import geoip2.errors
import geoip2.database
from colorama import Fore

@logger.catch
def search_geolocation(ip):
    try:
        with geoip2.database.Reader(CITY) as geo_reader:
            response = geo_reader.city(ip)
        with geoip2.database.Reader(ASN) as asn_reader:
            resp = asn_reader.asn(ip)
            return resp.autonomous_system_organization, resp.autonomous_system_number, response.country.name, response.city.name, response.country.iso_code, response.location.latitude, response.location.longitude

    except geoip2.errors.AddressNotFoundError:
        return None

def create_document(ip,banners, hostname,ports,tags):

    org,asn,country,city,iso_code,lat,long = search_geolocation(ip)
    col = {
            "ip": ip,
            "org": org,
            "asn": asn,
            "banners": banners,
            "ports": ports,
            "hostname": hostname,
            "country": country,
            "city": city,
            "country_code": iso_code,
            "latitude": lat,
            "longitude": long,
            "anonymous_login": anonymous_login(ip,ports),
            "tags": tags,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
    doc = {k:v for k,v in col.items() if v is not None}
    #Formatting output, removig None values
    if tags != None:
        output = f"{ip} {Fore.LIGHTMAGENTA_EX}{ports} {Fore.BLUE}{tags} {Fore.CYAN}{country} {Fore.WHITE}{city}"
    else:
        output = f"{ip} {Fore.LIGHTMAGENTA_EX}{ports} {Fore.CYAN}{country} {Fore.WHITE}{city}"

    logger.success(output)
    return doc
