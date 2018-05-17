import os
import json
import string
import unicodedata
import sys

from pprint import pprint

import plotly.offline as offline
import plotly.graph_objs as go

if len(sys.argv) > 1:
    fdir = sys.argv[1]
    if fdir.endswith('message.json'):
        message_dir = fdir
    elif fdir.endswith('/') or fdir.endswith('\\'):
        message_dir = fdir + 'message.json'
    else: message_dir = fdir + '\\message.json'
else:
    message_dir = 'C:\\Users\\David\\Developer\\facebook-message-analytics\\facebook-leetdavid\\messages\\PeytonZhang_b19cce929a\\message.json'

#Punctuation Remover
tbl = dict.fromkeys(i for i in range(sys.maxunicode)
    if unicodedata.category(chr(i)).startswith('P'))
def remove_punctuation(text):
    return text.translate(tbl)

dictionary = {}

#Read the file
with open(message_dir) as json_data:
    data = json.load(json_data)
    json_data.close()

    if 'messages' in data:
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

#Remove Common Words
temp = dict(dictionary)
common_words = ['lol','as','i','u','ur','im','you','the','and','to','a','is','but','for','of','was','do','not','are','or','be','it','so','its','that','on','have','with','dont','if','this','got','thats','then','we','right','did','like','in','me','at']
for word in dictionary:
    if word in common_words:
        del temp[word]
dictionary = temp
del temp

#Sort
freq, words = zip(*sorted(zip(list(dictionary.values()),list(dictionary.keys())), reverse=True))

#Trim
trim_amount = 50 #show top 50 words
freq = freq[:trim_amount]
words = words[:trim_amount]

plotdata = [go.Bar(x=words, y=freq)]
offline.plot(plotdata, filename='word_frequency-bar.html')