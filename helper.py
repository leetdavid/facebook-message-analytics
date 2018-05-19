import os
import json
import datetime
import time

def hasParam(argv, howToUse = None):
    if len(argv) > 1:
        return len(argv)
    else:
        if howToUse:
            print(howToUse)
        return False

def createDirectories(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: #Guard Against Race Condition
            if exc.errno != errno.EEXIST:
                raise

###############################################################################
#Returns the name of the person the data belongs to
def findName(rootdir):
	with open(rootdir + '/profile_information/profile_information.json', encoding='utf-8') as json_data:
		data = json.load(json_data)
		json_data.close()
		return data['profile']['name']

def whatsapp_to_timestamp(wtaptime):
    return int(time.mktime(datetime.datetime.strptime(wtaptime, "%m/%d/%y, %I:%M %p").timetuple()))

###############################################################################
# Converts timestamp to date format according to 'format' value
# e.g.
# timestamp_to(1480610024, 'datetime') -> datetime.datetime(2016, 12, 2, 0, 33, 44)
# timestamp_to(1480610024, 'iso8601') -> '2016-12-02 00:33:44'
# timestamp_to(1480610024, 'datetime') -> 
def timestamp_to(timestamp, format):
    return {
        'datetime': datetime.datetime.fromtimestamp(int(timestamp)),
        'string':  datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
        'iso8601':  datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
        'ISO8601':  datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    }[format]()

def time_convert(input, inputformat, outputformat):
    pass