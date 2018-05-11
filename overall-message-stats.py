import json
from pprint import pprint
import os
import plotly.offline as offline
import plotly.graph_objs as go

#Settings
rootdir = 'C:\\Users\\David\\Developer\\facebook-message-analytics\\facebook-leetdavid'
filterGroupChats = False
stackedBar = False

#Find your name
with open(rootdir + '/profile_information/profile_information.json') as json_data:
	data = json.load(json_data)
	json_data.close()
	me = data['profile']['name']

people = []
messageCount = []
messageCountYou = []
messageCountOther = []

#Read from files
for subdir, dirs, files in os.walk(rootdir + '/messages'):
	for file in files:
		if file == 'message.json':
			filepath = os.path.join(subdir, file)
			with open(filepath) as json_data:
				data = json.load(json_data)
				json_data.close()

				if 'messages' in data and 'title' in data and 'participants' in data:
					if not(filterGroupChats and len(data['participants']) > 1):
						personName = data['title']
						you = 0
						other = 0
						for message in data['messages']:
							if 'sender_name' in message and message['sender_name'] == me:
								you+=1
							else:
								other+=1
						people.append(personName)
						messageCount.append(len(data['messages']))
						messageCountYou.append(you)
						messageCountOther.append(other)

#Sort
messageCount, messageCountOther, messageCountYou, people = zip(*sorted(zip(messageCount, messageCountOther, messageCountYou, people), reverse=True))
people = list(people)
messageCount = list(messageCount)
messageCountYou = list(messageCountYou)
messageCountOther = list(messageCountOther)

#Trim 
totalYou = 0
totalOther = 0
total = 0
filterNumber = 20
for x in range(filterNumber, len(people)):
	totalYou += messageCountYou[x]
	totalOther += messageCountOther[x]
	total += messageCount[x]
people = people[0:filterNumber]
messageCountYou = messageCountYou[0:filterNumber]
messageCountOther = messageCountOther[0:filterNumber]
messageCount = messageCount[0:filterNumber]
people.append('Other')
messageCountYou.append(totalYou)
messageCountOther.append(totalOther)
messageCount.append(total)

#Plot
if stackedBar:
	trace1 = go.Bar(x=people, y=messageCountYou, name='You')
	trace2 = go.Bar(x=people, y=messageCountOther, name='Other')
	data = [trace1, trace2]
	layout = go.Layout(barmode='stack')
	fig = go.Figure(data=data, layout=layout)
	offline.plot(fig, filename='stacked-bar.html')
else:
	data = [go.Bar(x=people, y=messageCount)]
	offline.plot(data, filename='basic-bar.html')





