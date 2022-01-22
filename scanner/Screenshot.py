from requests import get
from config import RENDER_URL

def take_screenshot(ip,ports):
    if "http" in ports:
        image = "{}:{}".format(ip, ports["http"])
        path = "../screenshots/{}.png".format(image)
        response = get(RENDER_URL + "http://{}".format(image), stream=True)

        if (response.status_code == 200):
            with open(path, 'wb') as file:
                for x in response:
                    file.write(x)
            return path
        else:
            return None
