import json
import os
from pprint import pprint
import plotly.offline as offline
import plotly.graph_objs as go

###############################################################################
#Returns the name of the person the data belongs to
def findName(rootdir):
	with open(rootdir + '/profile_information/profile_information.json') as json_data:
		data = json.load(json_data)
		json_data.close()
		return data['profile']['name']

###############################################################################
#Create graph of most messaged people
def graph(rootdir, filename, filterGroupChats):
	people, messageCount, messageCountYou, messageCountOther = getMessageCounts(rootdir, filterGroupChats, 100)
	trace1 = go.Bar(
		x=people, 
		y=messageCountYou, 
		name='You',  
		hoverinfo='none'
    )
	trace2 = go.Bar(
		x=people, 
		y=messageCountOther, 
		name='Other',
		hoverinfo='text',
    	text=[('Total: ' + "{:,}".format(x + y) + '<br>Other: ' + "{:,}".format(x) + '<br>You: ' + "{:,}".format(y) ) for x, y in zip(messageCountOther, messageCountYou)] 
    )
	data = [trace1, trace2]
	config={'displayModeBar': False, 'showLink': False}
	layout = go.Layout(
	    height=500,
    	margin=go.Margin(
	        l=50,
	        r=50,
	        b=50,
	        t=50,
	    ),
		barmode='stack', 
		paper_bgcolor='rgba(0,0,0,0)', 
		plot_bgcolor='rgba(0,0,0,0)',
		showlegend=False, 
		xaxis={
		    "autorange": False, 
		    "range": [-0.5, 20.5], 
		    "rangeslider": { "autorange": True, "visible": True }, 
		    "type": "category"
		},  
		yaxis={
        'title':'Message Count',
        'titlefont':{
            'family':'Courier New, monospace',
            'size':18,
            'color':'#7f7f7f'
    	    }
   		}
	)
	fig = go.Figure(data=data, layout=layout)
	if not os.path.exists('graphs/'):
		os.makedirs('graphs/')
	offline.plot(fig, filename='graphs/' +filename + '.html', auto_open=False, config=config)


###############################################################################
#Returns an array of people, and array of the count of messages overall, sent and recieved to each person
def getMessageCounts(rootdir, filterGroupChats, filterNumber):
	me = findName(rootdir)
	people = []
	messageCount = []
	messageCountYou = []
	messageCountOther = []
	filepaths = get_immediate_subdirectories(rootdir + '/messages')			

	for i, chatName in enumerate(filepaths):
		message_dir = rootdir + '/messages/' + chatName + '/message.json'
		if os.path.exists(message_dir):
			print('[{:15s}] ({:3d}/{:3d}) {:s}'.format('Analysing Chat', i, len(filepaths), chatName), end='\r', flush=True)
			with open(message_dir) as json_data:
				data = json.load(json_data)
				json_data.close()
				if 'messages' in data and 'title' in data and 'participants' in data:
					if not(filterGroupChats and len(data['participants']) > 1):
						personName = data['title']
						if len(personName) > 15:
							personName = personName[:13] + '..'
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
	print()
	return people, messageCount, messageCountYou, messageCountOther

###############################################################################
#Returns the number of one-on-one conversations and the number of group chats
def getConversationCounts(rootdir):
	groupChatCount = 0
	convoCount = 0

	#Read from files
	for subdir, dirs, files in os.walk(rootdir + '/messages'):
		for file in files:
			if file == 'message.json':
				filepath = os.path.join(subdir, file)
				with open(filepath) as json_data:
					data = json.load(json_data)
					json_data.close()
					if 'messages' in data and 'title' in data and 'participants' in data:
						if len(data['participants']) > 1:
							groupChatCount += 1
						else:
							convoCount += 1
	return convoCount, groupChatCount		

###############################################################################
# Get all subdirectories
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


