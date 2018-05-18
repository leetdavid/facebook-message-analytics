import plotly.offline as offline
import plotly.graph_objs as go
import os 

###############################################################################
# Takes an ordered dictionary of words: frequency and creates a graph
def graph_word_frequency(word_frequency, file_name):
	words, freq = zip(*word_frequency.items())
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
	offline.plot(fig, filename='graphs/individual-word-freq/' + file_name + '.html',auto_open=False, config=config)

###############################################################################
# Creates a graph of message counts for all chats
def graph_overall_message_count(chat_data, filter_groupchats, file_name):
	you_count = []
	other_count = []
	total_count = []
	names = []
	for chat in chat_data:
		if not filter_groupchats or not chat['is_group_chat']:
			names.append(chat['name'][:13])
			you_count.append(chat['you_count'])
			other_count.append(chat['other_count'])
			total_count.append(chat['you_count'] + chat['other_count'])
	total_count, other_count, you_count, names = zip(*sorted(zip(total_count, other_count, you_count, names), reverse=True))
	trace1 = go.Bar(
		x=list(names), 
		y=list(you_count), 
		name='You',  
		hoverinfo='none'
    )
	trace2 = go.Bar(
		x=list(names), 
		y=list(other_count), 
		name='Other',
		hoverinfo='text',
    	text=[('Total: ' + "{:,}".format(x + y) + '<br>Other: ' + "{:,}".format(x) + '<br>You: ' + "{:,}".format(y) ) for x, y in zip(other_count, you_count)] 
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
	offline.plot(fig, filename='graphs/' +file_name + '.html', auto_open=False, config=config)
