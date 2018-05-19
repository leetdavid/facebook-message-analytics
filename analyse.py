import message_analysis
import graphing
import generate_html
import sys
import math 
import os

###############################################################################
# python analyse.py /Users/harrytbp/Desktop/facebook-harrybp
root = sys.argv[1]
if not os.path.exists('graphs/'):
	os.makedirs('graphs/')
if not os.path.exists('graphs/individual-word-freq'):
	os.makedirs('graphs/individual-word-freq')
chat_data, metadata = message_analysis.analyse(root)
graphing.graph_overall_message_count(chat_data, False, 'with_group_chats')
graphing.graph_overall_message_count(chat_data, True, 'without_group_chats')
for i, chat in enumerate(chat_data):
	graphing.graph_word_frequency(chat['most_frequent_words'], chat['folder_name'])
	print('[{:15s}] ({:3d}/{:3d}) {:s}'.format('Graphing Chat', i, len(chat_data), chat['name'].ljust(80)), end='\r', flush=True)
generate_html.create_index_html(chat_data, metadata)




