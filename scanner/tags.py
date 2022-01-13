import webtech

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
        return filt
    else:
        return None
