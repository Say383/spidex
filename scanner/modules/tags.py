import webtech
from bs4 import BeautifulSoup

def get_tags(ip,port):
    try:
        wt = webtech.WebTech(options={'json': False})
        result = wt.start_from_url(f"http://{ip}:{port}", timeout=1)
        return result
    except webtech.utils.ConnectionException:
        return None

#Filter report from webtech and only return web technologies
def tags(ip,banners,ports):
    tags_list = []

    for index, value in enumerate(banners):
        #Checks if the banners received contain HTML to analyze technologies

        if bool(BeautifulSoup(value, "html.parser").find()):
            #If true, send the port of the list, in the same position as the banners.
            tags = get_tags(ip,ports[index])

            if tags != None:
            #Removing unnecessary words and duplicates from the received list

                techs = tags.replace("\t-","").splitlines()
                filt = [x.strip() for x in techs if not "Detected" in x and not "Target" in x]
                tags_list.append(filt)

    flat_list = [item for sublist in tags_list for item in sublist]
    if flat_list:
        return list(set(flat_list))
    else:
        return None
