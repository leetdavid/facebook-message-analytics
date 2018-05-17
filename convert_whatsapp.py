import sys
import helper as helper

messages = []

currentMsg = ''

def isConvoLine(str):
    arr = str.split("M - ")
    if len(arr) == 1:
        return False
    
def convert(line):
    dateStr = line.split(' - ')[0]
    nameStr = line.split(' - ')[1].split(':')[0]
    m = {}
    m['sender_name'] = nameStr
    m['timestamp'] = dateStr
    

if helper.hasParam(sys.argv):
    with open(sys.argv[1], encoding='UTF-8', newline='\n') as f:
        for line in f:
            if isConvoLine(line):
                messages.append(convert(currentMsg))
                currentMsg = ''
            else:
                currentMsg = currentMsg + '\n' + line

        print(messages)