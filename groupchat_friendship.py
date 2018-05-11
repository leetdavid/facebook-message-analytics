import os
import sys
import json
import string
import unicodedata

from pprint import pprint

message_dir = 'C:\\Users\\David\\Developer\\facebook-message-analytics\\messages\\WeNasty_9f21cce0d4\\message.json'

interactions = {}
interaction_wait_threshold = 30*60 # 30 minutes = 30*60

prevmsg = None

class Interaction:
    def __init__(self, p1, p2):
        self.person1 = p1
        self.person2 = p2
        self.count = 0

    def increment(self):
        self.count += 1

    def isInteractedPerson(self, name):
        return name == self.person1 or name == self.person2

    def __str__(self):
        return self.person1 + ' -> ' + self.person2 + ': ' + str(self.count)

# Checks if msg2 happens within msg1+interaction_wait_threshold
def isWithinInteraction(msg1, msg2):
    return msg2['timestamp'] - msg1['timestamp'] <= interaction_wait_threshold

# Read the file
with open(message_dir) as json_data:
    data = json.load(json_data)
    json_data.close()

    if 'messages' in data:
        prevmsg = data['messages'][0]
        for msg in data['messages'][1:]:
            if isWithinInteraction(prevmsg, msg):
                # Create Interaction
                interaction_name = msg['sender_name'] + prevmsg['sender_name']
                if interaction_name in interactions:
                    interactions[interaction_name].increment()
                else:
                    interactions[interaction_name] = Interaction(msg['sender_name'], prevmsg['sender_name'])
            prevmsg = msg

for interaction in  interactions:
    print(interactions[interaction])