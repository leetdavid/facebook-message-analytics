import sys
import json

import helper as helper


param_title = sys.argv[1].split('WhatsApp Chat with ')[1].replace('.txt','')

param_input_dir = sys.argv[1]

# Specify 'messages' folder
param_output_dir = sys.argv[2] + '/' + param_title.replace(' ','')[:-4] + '/message.json'

participants = []
messages = []
currentMsg = ''
acc = ''

def isTimestamped(str):
    return str.find('M - ') > 10

def isConveration(str):
    return isTimestamped(str) and str.find(': ') > 19

def convert(line):
    #Find Date
    dateStr = line[:line.find(' - ')]
    #Remove First Occurance of Colon , which is in the time
    line = line.replace(':','x', 1)
    nameStr = line[line.find(' - ')+3:line.find(':')]
    m = {}
    if nameStr not in participants:
        participants.append(nameStr)
    m['sender_name'] = nameStr
    m['timestamp'] = dateStr
    m['content'] = line[line.find(':')+2:len(line)].replace('\r','').replace('\n','')

    #Convert Whatsapp Timestamp to UNIX Time
    m['timestamp'] = helper.converttime(m['timestamp'],'timestamp')

    return m

def convertWhatsappChat():
    with open(param_input_dir, encoding='UTF-8', newline='\n') as f:

        for line in f:
            if line.find("<Media omitted>") != -1:
                continue
            if isTimestamped(line):
                messages.append(convert(line))
            else:
                messages[-1]['content'] += line

    helper.createDirectories(param_output_dir)

    with open(param_output_dir, 'w', encoding='utf-8') as fp:
        d = {}
        d['messages'] = messages
        d['title'] = param_title
        d['is_still_participant'] = True
        d['status'] = "Pending"
        d['thread_type'] = "Regular"
        d['participants'] = participants
        json.dump(d, fp, indent=4, ensure_ascii=False)#.encode('utf8')

convertWhatsappChat()