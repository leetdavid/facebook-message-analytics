import os
import json
import datetime
import time
import calendar

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
# Converts one date format to another format according to 'format' value (default: datetime)
# e.g.
# converttime(1480610024) -> datetime.datetime(2016, 12, 2, 0, 33, 44)
# converttime(1480610024, 'iso8601') -> '2016-12-02 00:33:44'
def converttime(input, format = 'datetime'):
    dt = None

    # datetime
    if isinstance(input, datetime.date):
        dt = input

    #is timestamp (int or str)
    if isinstance(input, (int, str)):
        try: #UNIX Time
            dt = datetime.datetime.fromtimestamp(int(input))
        except ValueError:
            pass
        try: #ISO8601
            dt = datetime.datetime.strptime(input, '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            pass
        
        try: #Whatsapp Time
            dt = datetime.datetime.strptime(input, '%m/%d/%y, %I:%M %p')
        except (ValueError, TypeError):
            pass
        

        raise TypeError('input is not in proper format')

    if dt is None:
        raise TypeError('input must be a datetime.datetime, UNIX timestamp, or ISO8601, not a %s' % type(input))

    fc = format.lower().replace('-','') #Format Code

    if fc == 'datetime':
        return dt
    elif fc == 'timestamp' or fc == 'unix':
        return calendar.timegm(dt.timetuple())
    elif fc == 'string' or fc == 'iso8601':
        return dt.strftime('%Y-%m-%d %H:%M:%S')