import overall_message_stats as overall
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
printProgress(0)
overall.graph(root, 'wgc', False)
printProgress(25)
overall.graph(root, 'ngc', True)
printProgress(50)

#Get message count and conversation count
people, messageCount, messageCountYou, messageCountOther = overall.getMessageCounts(root, False, 20)
printProgress(75)
convoCount, groupChatCount = overall.getConversationCounts(root)

#Write to html
gen.create_index_html(sum(messageCountYou), sum(messageCountOther), convoCount, groupChatCount)
printProgress(100)



