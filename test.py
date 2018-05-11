import json
from pprint import pprint
import os
import plotly.offline as offline
import plotly.graph_objs as go

rootdir = '/Users/harrytbp/Desktop/facebook-harrybp'

people = []
numberMessages = []

#Read from files
for subdir, dirs, files in os.walk(rootdir + '/messages'):
	for file in files:
		if file == 'message.json':
			filepath = os.path.join(subdir, file)

			with open(filepath) as json_data:
				data = json.load(json_data)
				json_data.close()
				if 'messages' in data:
					personName = data['title']
					people.append(personName)
					numberMessages.append(len(data['messages']))

#Sort
numberMessages, people = zip(*sorted(zip(numberMessages, people), reverse=True))
people = list(people)
numberMessages = list(numberMessages)
total = 0

#Trim 
filterNumber = 20
for x in range(filterNumber, len(people)):
	total += numberMessages[x];
people = people[0:filterNumber]
numberMessages = numberMessages[0:filterNumber]
people.append('Other')
numberMessages.append(total)

#Plot
data = [go.Bar(
            x=people,
            y=numberMessages
    )]

offline.plot(data, filename='basic-bar')

