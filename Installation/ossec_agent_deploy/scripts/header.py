import datetime, time
import pexpect

expectations = ['[Pp]assword',
	'continue (yes/no)?',
	pexpect.EOF,
	pexpect.TIMEOUT,
	'Name or service not known',
	'Permission denied',
	'No such file or directory',
	'No route to host',
	'Network is unreachable',
	'failure in name resolution',
	'No space left on device'
	]

def timeStamper () :
	timestamp = time.time ()
	created_time = datetime.datetime.fromtimestamp (timestamp).strftime ('%Y-%m-%d_%H:%M:%S')
	return created_time

def fetchFileSCP(file_path, username, IPadd, agent_password, child=None):
	print ("Received Args:",child, file_path, username, IPadd, agent_password)
	try:
		if not child:
			comm = username + "@" + IPadd + ":/home/" + username
			child = pexpect.spawn( 'scp -r -p %s %s'%(file_path, comm))
		res = child.expect( expectations )
		print ("Child Exit Status :",child.exitstatus)
		print  (res,"::",child.before," :After:",child.after)
		if res == 0:
			child.sendline(agent_password)
			return fetchFileSCP(file_path, username, IPadd, agent_password, child)
		if res == 1:
			child.sendline('yes')
			return fetchFileSCP(file_path, username, IPadd, agent_password, child)
		if res == 2:
			line = child.before
			print ("Line:",line)
			print ("Now check the result and return status.")
		if res == 3:
			print ("TIMEOUT Occurred.")
			child.kill(0)
			return False
		if res >= 4:
			child.kill(0)
			print ("ERROR:",expectations[res])
			return False
		return True
	except Exception as e:
		import traceback; traceback.print_exc()
		print ("Did file finish?",child.exitstatus)
