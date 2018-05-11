import json
from pprint import pprint

with open('messages/harrybondpreston_3b4f5b1812/message.json') as json_data:
    data = json.load(json_data)
    json_data.close()
    pprint(data)
    print(len(data['messages']));