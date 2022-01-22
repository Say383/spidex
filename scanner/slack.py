from config import SLACK_URL
import json
import requests
import sys

def send_message(time,results):
    content = "Total discovered devices: {} \nElapsed time: {}".format(results,time)
    slack_data = {
   "username":"Pwndora BOT",
   "icon_emoji":":snake:",
   "attachments":[
      {
         "color":"#7bf538",
         "fields":[
            {
               "title":"Scan results",
               "value": content,
            }
         ]
      }
   ]
}
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(SLACK_URL, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
