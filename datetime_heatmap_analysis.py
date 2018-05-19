import os
import json
import string
import unicodedata
import sys
from pprint import pprint
import plotly.offline as offline
import plotly.graph_objs as go
import numpy as np

param_rootdir = ''


def generate_graph_data():
  if os.path.exists(param_rootdir):
    
    with open(param_rootdir, encoding='utf-8') as json_data:
      data = json.load(json_data)
      json_data.close()

    if 'messages' in data and 'title' in data:
      participants = {}
      date_list=[]
      for msg in data['messages']:
        if 'timestamp' in msg and 'sender_name' in msg:
          pass
          
    else:
      print("ERROR: Invalid Messages Data" + param_rootdir + "has no messages or title in the file!")
