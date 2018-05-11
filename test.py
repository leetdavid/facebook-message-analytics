import json
from pprint import pprint
import os
rootdir = '/Users/harrytbp/Desktop/facebook-harrybp/messages'

people = {}

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file == 'message.json':
			filepath = os.path.join(subdir, file)

			with open(filepath) as json_data:
				data = json.load(json_data)
				json_data.close()
				if 'messages' in data:
					personNameList = subdir.split('/')
					personName = personNameList[-1]
					people[personName] = len(data['messages'])

print(sorted(people.items(), key=lambda x:x[1]))