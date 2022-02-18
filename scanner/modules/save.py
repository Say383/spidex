import json
import pathlib
from datetime import datetime

def save_json(results):
    path = "{}/reports/{}.json".format(pathlib.Path().resolve(),datetime.now())
    json_results = json.dumps(results)
    file = open(path,"w")
    file.write(json_results)
    file.close()
    return path
