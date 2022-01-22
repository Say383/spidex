import webtech


os_list = ["CentOS","Ubuntu","Debian","Microsoft","Windows Server","Red Hat"]

def get_tags(ip,ports):
    try:
        for key, value in ports.items():
            if "http" in key:
                if key == "http-alt":
                    key = "http"
                wt = webtech.WebTech(options={'json': False})
                tags = wt.start_from_url("{}://{}:{}".format(key,ip,value), timeout=1)
                return tags
    except webtech.utils.ConnectionException:
        return None

#Filter report from webtech and only return web technologies
def tags(ip,ports):
    save = get_tags(ip,ports)
    if save != None:
        techs = save.replace("\t-","").splitlines()
        filt = [x.strip() for x in techs if not "Detected" in x and not "Target" in x]
        filt2 = [i for i in filt if not i in os_list]
        return filt2
    else:
        return None

def get_os(banners):
    if banners:
        for b in banners:
            for os in os_list:
                if os in b: return os
