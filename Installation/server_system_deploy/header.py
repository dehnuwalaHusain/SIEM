from subprocess import Popen, PIPE
import datetime, time, os, logging
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

# ===========================================================================================
# ---------------------------------------------------
# /usr/local/nagios/etc/objects/localhost.cfg backup operations
# ---------------------------------------------------

# Take back up of configuration file before making changes to it.
def backup_cfg ( server_password, file_name ):
	comm = "echo %s | sudo -S mkdir /usr/local/nagios/etc/objects/temp" % ( server_password )
	os.system ( comm )

	comm = "echo %s | sudo -S cp /usr/local/nagios/etc/objects/%s /usr/local/nagios/etc/objects/temp/" % ( server_password, file_name )
	os.system ( comm )

# Restore the back up in case "Total Error and Total Warnings" are not 0.
def restore_cfg ( server_password, file_name ):
	comm = "echo %s | sudo -S cp /usr/local/nagios/etc/objects/temp/%s /usr/local/nagios/etc/objects/" % ( server_password, file_name )
	os.system ( comm )

# Delete the temp directory created for back up.
def delete_backup ( server_password ):
	comm = "echo %s | sudo rm -rf /usr/local/nagios/etc/objects/temp" % ( server_password )
	os.system ( comm )
# ===========================================================================================


# ===========================================================================================
# ---------------------------------------------------
# Nagios operations
# ---------------------------------------------------

# Check if the changes are safe to save, by compiling the cfg file and checking errors.
def check_errors ( script, service, server_password, file_name ):

	comm = script.split ()

	process = Popen ( comm, stdout = PIPE, stderr = PIPE )
	stdout, stderr = process.communicate ()

	if "Total Warnings: 0" and "Total Errors:   0" in str ( stdout ):
		print ("ok.")
	
		delete_backup ( server_password )

		created_time = timeStamper ()
		logging.info ( created_time + "\tService " + service + " added." )
		print ("success.")
		print ( str (stdout))
	else:
		restore_cfg ( server_password, file_name )
		delete_backup ( server_password )
		print ( "An error occured, service not added." )
		created_time = timeStamper ()
		logging.info ( created_time + "\tError occured. Restoring back ups, service " + service + " not added." )
		print ( str ( stdout ))
		print ( str ( stderr ))
		exit ()

# Restart nagios after changes to cfg files.
def restart_nagios ( server_password ):
	comm = "echo %s | sudo -S service nagios restart" % ( server_password )
	os.system ( comm )

	comm = "echo %s | sudo -S systemctl restart nagios" % ( server_password )
	os.system ( comm )


# ===========================================================================================

# ===========================================================================================
# ---------------------------------------------------
# SCP
# ---------------------------------------------------
def fetchFileSCP ( file_path, username, IPadd, agent_password, child=None ):
	print ( "Received Args:",child, file_path, username, IPadd, agent_password )
	try:
		if not child:
			comm = username + "@" + IPadd + ":/home/" + username
			child = pexpect.spawn ( 'scp -r -p %s %s' % ( file_path, comm ))
		res = child.expect ( expectations )
		print ( "Child Exit Status :", child.exitstatus )
		print ( res,"::", child.before, " :After:", child.after )
		if res == 0:
			child.sendline ( agent_password )
			return fetchFileSCP ( file_path, username, IPadd, agent_password, child )
		if res == 1:
			child.sendline ( 'yes' )
			return fetchFileSCP ( file_path, username, IPadd, agent_password, child )
		if res == 2:
			line = child.before
			print ( "Line:", line )
			print ( "Now check the result and return status." )
		if res == 3:
			print ( "TIMEOUT Occurred." )
			child.kill ( 0 )
			return False
		if res >= 4:
			child.kill ( 0 )
			print ( "ERROR:", expectations [ res ])
			return False
		return True
	except Exception as e:
		import traceback; traceback.print_exc ()
		print ( "Did file finish?", child.exitstatus )