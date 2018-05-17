import overall_message_stats as overall
import word_analysis as word_analysis
import generate_html as gen
import sys
import math 

###############################################################################
# python analyse.py /Users/harrytbp/Desktop/facebook-harrybp

def printProgress(percent):
	percent = int(math.ceil(percent / 10.0))
	for x in range(0, 10):
		if x <= percent:
			print('#', end="", flush=True)
		else:
			print('.', end="", flush=True)
	print(' %s percent' % (str(percent * 10)), end="\r")		

 
root = sys.argv[1]

#Create graphs
overall.graph(root, 'wgc', False)
overall.graph(root, 'ngc', True)

#Get message count and conversation count
people, messageCount, messageCountYou, messageCountOther = overall.getMessageCounts(root, False, 20)
convoCount, groupChatCount = overall.getConversationCounts(root)

chatMap = word_analysis.graphAllChats(root)	

#Write to html
gen.create_index_html(sum(messageCountYou), sum(messageCountOther), convoCount, groupChatCount, chatMap)





