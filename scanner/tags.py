import webtech

def get_tags(ip,ports):
    try:
        if "http" in ports:
            wt = webtech.WebTech(options={'json': True})
            tags = wt.start_from_url("http://{}:{}".format(ip,ports["http"]), timeout=1)
            return tags
    except webtech.utils.ConnectionException():
        return None

#Filter JSON report from Webtech App, and convert to list, with only Web Technologies TAGS and versions
def tags(ip,ports):
    filt = []
    update = []
    result = []
    save = get_tags(ip,ports)
    if save != None:
        if "tech" in save:
            for x in save.values(): filt.append(x) 
            for j in filt[0]: update.append(list(j.values()))
            for i in update: result.append(list(filter(None, i)))
            concat = list(map(" ".join,result))
            return concat
    else:
        return None
