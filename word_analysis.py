import os
import json
import string
import unicodedata
import sys
from pprint import pprint
import plotly.offline as offline
import plotly.graph_objs as go

###############################################################################
# Punctuation Remover
tbl = dict.fromkeys(i for i in range(sys.maxunicode)
    if unicodedata.category(chr(i)).startswith('P'))
def remove_punctuation(text):
    return text.translate(tbl)

###############################################################################
# Filters words from a list
def filterCommonWords(dictionary):
	temp = dict(dictionary)
	common_words = ['lol','as','i','u','ur','im','you','the','and','to','a','is','but','for','of','was','do','not','are','or','be','it','so','its','that','on','have','with','dont','if','this','got','thats','then','we','right','did','like','in','me','at']
	for word in dictionary:
	    if word in common_words:
	        del temp[word]
	return temp        

###############################################################################
# Generate word frequency graph for given chat   
def createWordFreqGraph(root, chatName):
	message_dir = root + '/messages/' + chatName + '/message.json'
	if os.path.exists(message_dir):
		dictionary = {}
		#Read the file
		with open(message_dir, encoding='utf-8') as json_data:
		    data = json.load(json_data)
		    json_data.close()

		    if 'messages' in data and 'title' in data:
		        for msg in data['messages']:
		            if 'content' in msg:
		                content = msg['content']
		                strip_punct = remove_punctuation(content)
		                for word in strip_punct.split():
		                    if word.isalnum():
		                        word = word.lower()
		                        if word in dictionary:
		                            dictionary[word] += 1
		                        else:
		                            dictionary[word] = 1

		#Filter and sort
		dictionary = filterCommonWords(dictionary)
		if len(dictionary) > 1:
			freq, words = zip(*sorted(zip(list(dictionary.values()),list(dictionary.keys())), reverse=True))
		else:
			freq = list(dictionary.values())
			words = list(dictionary.keys())

		#Trim
		trim_amount = 50 #show top 50 words
		freq = freq[:trim_amount]
		words = words[:trim_amount]

		#Create directory path and save graph
		if not os.path.exists('graphs/'):
			os.makedirs('graphs/')
		if not os.path.exists('graphs/individual-word-freq'):
			os.makedirs('graphs/individual-word-freq')
		plotdata = [go.Bar(x=words, y=freq)]
		layout = go.Layout(
		    height=500,
	    	margin=go.Margin(
		        l=50,
		        r=50,
		        b=50,
		        t=50,
		    ),
			paper_bgcolor='rgba(0,0,0,0)', 
			plot_bgcolor='rgba(0,0,0,0)',
			yaxis={
		        'title':'Word Frequency',
		        'titlefont':{
		            'family':'Courier New, monospace',
		            'size':18,
		            'color':'#7f7f7f'
		    	    }
		   		}
		)
		fig = go.Figure(data=plotdata, layout=layout)
		config={'displayModeBar': False, 'showLink': False}
		offline.plot(fig, filename='graphs/individual-word-freq/' + chatName + '.html',auto_open=False, config=config)

###############################################################################
# Find name of chat given its filename
def findName(root,chatName):
	message_dir = root + '/messages/' + chatName + '/message.json'
	if os.path.exists(message_dir):
		with open(message_dir, encoding='utf-8') as json_data:
			    data = json.load(json_data)
			    json_data.close()
			    if 'title' in data:
			    	return data['title']

###############################################################################
# Graph all chats, return dict of filenames: chatnames
def graphAllChats(root):
	allChats = get_immediate_subdirectories(root + '/messages')
	dictionary = {}
	for i, chat in enumerate(allChats):
		person = {}
		person['name'] = findName(root,chat)
		dictionary[chat] = person
		print('[{:15s}] ({:3d}/{:3d}) {:s}'.format('Graphing Chat', i, len(allChats), chat), end='\r', flush=True)
		name = createWordFreqGraph(root, chat)
	print()
	return dictionary	
				
###############################################################################
# Get all subdirectories
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


