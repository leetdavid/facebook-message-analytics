import sys
import operator
import os
import json
import unicodedata


###############################################################################
# Returns the string it was passed with punctuation removed
tbl = dict.fromkeys(i for i in range(sys.maxunicode)
    if unicodedata.category(chr(i)).startswith('P'))
def remove_punctuation(text):
    return text.translate(tbl)

###############################################################################
# Get all subdirectories
def get_immediate_subdirectories(a_dir):
	return [name for name in os.listdir(a_dir)
			if os.path.isdir(os.path.join(a_dir, name))]

###############################################################################
# Returns number of messages sent by you, and number of messages sent to you
def get_message_counts(data, data_owner):
	if 'messages' in data and 'title' in data and 'participants' in data:
		you_count = other_count = 0

		for message in data['messages']:
			if 'sender_name' in message and message['sender_name'] == data_owner:
				you_count+=1
			else:
				other_count+=1
		return you_count, other_count		

###############################################################################
# Returns the name of the facebook user running the program
def get_data_owner(root):
	with open(root + '/profile_information/profile_information.json', encoding='utf-8') as json_data:
		data = json.load(json_data)
		json_data.close()
	return data['profile']['name']				

###############################################################################
# Reads chat from file into json
def read_chat(root, chat):
	message_dir = root + '/messages/' + chat + '/message.json'
	if os.path.exists(message_dir):
		with open(message_dir, encoding='utf-8') as json_data:
			data = json.load(json_data)
			json_data.close()
		return data	
	else: 
		return False		

###############################################################################
# Returns title of the chat
def get_chat_title(data):
	if 'title' in data:
		return data['title']	

###############################################################################
# Returns true if the chat is a group chat
def get_is_group_chat(data):
	return len(data['participants']) > 1	

###############################################################################
# Returns an ordered array of tuples of the most frequent words & their frequency
def get_most_frequent_words(data):
	if 'messages' in data and 'title' in data:
		dictionary = {}
		for i, msg in enumerate(data['messages']):
			if 'content' in msg:
				content = msg['content']
				strip_punct = remove_punctuation(content)
				for word in strip_punct.split():
					if word.isalnum():
						word = word.lower()
						dictionary[word] = dictionary[word] + 1 if word in dictionary else 1
		dictionary = filter_common_words(dictionary)				
		sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
		trimmed_dictionary = dict(sorted_dictionary[:50])
		return trimmed_dictionary
				

###############################################################################
# Filters a dictionary against a list of common words
def filter_common_words(dictionary):
	temp = dict(dictionary)
	common_words = ['lol','as','i','u','ur','im','you','the','and','to','a','is','but','for','of','was','do','not','are','or','be','it','so','its','that','on','have','with','dont','if','this','got','thats','then','we','right','did','like','in','me','at']
	for word in dictionary:
		if word in common_words:
			del temp[word]
	return temp

###############################################################################
# Build datastructure for all chats
def analyse(root):
	all_chat_data = []
	data_owner = get_data_owner(root)
	all_chats = get_immediate_subdirectories(root + '/messages')
	for i, chat in enumerate(all_chats):
		chat_data = {}
		data = read_chat(root, chat)
		if data and 'messages' in data and 'title' in data and 'participants' in data:
			you_count, other_count = get_message_counts(data, data_owner)
			chat_data['you_count'] = you_count
			chat_data['other_count'] = other_count
			chat_data['name'] = get_chat_title(data)
			chat_data['is_group_chat'] = get_is_group_chat(data)
			chat_data['most_frequent_words'] = get_most_frequent_words(data)
			chat_data['folder_name'] = chat
			if len(chat_data['most_frequent_words']) > 0:
				all_chat_data.append(chat_data)
			print('[{:15s}] ({:3d}/{:3d}) {:s}'.format('Analysing Chat', i, len(all_chats), chat_data['name'].ljust(40)), end='\r', flush=True)
	
		#if i > 20:
		#	break	
	metadata = {}		
	metadata['group_chat_count'] = sum(1 for chat in all_chat_data if chat['is_group_chat'])
	metadata['individual_chat_count'] = sum(1 for chat in all_chat_data if not chat['is_group_chat'])
	metadata['message_total_you'] = sum(item['you_count'] for item in all_chat_data)	
	metadata['message_total_other'] = sum(item['other_count'] for item in all_chat_data)	
	return all_chat_data, metadata	






