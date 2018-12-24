import datetime, time

def timeStamper () :
	timestamp = time.time ()
	created_time = datetime.datetime.fromtimestamp (timestamp).strftime ('%Y-%m-%d_%H:%M:%S')
	return created_time