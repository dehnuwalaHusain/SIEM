'''
[EDIT]
Alright, so logging will not work here for exceptions. And that's because Python does not have any problems executing those commands on the terminal. When an error occurs, it's from the terminal itself. Need to find a way to find those exeptions and add it to log.  
  

To print the current directory you're in ( debugging )
print (os.getcwd())

To save the last chdir you made through script:
os.system("/bin/bash")

COMMAND LINE ARGUMENTS FOR THIS SCRIPT:
python createAgentFolders.py [<username> <password> <agent_name> <agent_ID> <client/agent IP address> .....]

		... <server IP address>


'''

import os, datetime, time, logging, sys, ipaddress
from pexpect import pxssh

LOG_FILENAME = 'installation.log'
logging.basicConfig (filename = LOG_FILENAME, level = logging.INFO)

def timeStamper () :
	timestamp = time.time ()
	created_time = datetime.datetime.fromtimestamp (timestamp).strftime ('%Y-%m-%d_%H:%M:%S')
	return created_time

def main() :
	'''
	INITIALIZATIONS
	'''
	# Username from webUI via cmd arguments
	username = "tempUsername"

	# Password from webUI via cmd arguments
	password = "root@12"

	# Agent name from webUI via cmd arguments
	agent_name = "tempAgentName"

	# Agent ID from webUI via cmd arguments
	agentID = "001"
	
	# IP from webUI via cmd arguments
	IPadd = "10.65.6.10"

	# server IP address
	serverIP = "10.65.6.78"


	if ( len ( sys.argv ) != 5 ):
		created_time = timeStamper ()
		logging.info ( created_time + "\tDid not receive the pre-required information from UI for installation." )
		print ("Check log file for errors.")
		exit ()
	else: 
		username = sys.argv [ 1 ]
		password = sys.argv [ 2 ]
		agent_name = sys.argv [ 3 ] 
		IPadd = sys.argv [ 4 ]
		try :
			ipaddress.ip_address ( IPadd )
		except ValueError:
			created_time = timeStamper ()
			logging.info ( created_time + "\tThe IP \'" + IPadd + "\' is not a valid IP address.")	
			exit ()
		
	created_time = timeStamper ()
	logging.info ( created_time + "\tInitiating installation for machine with username \'" + username + "\' and IP \'" + IPadd +
									"\' and assigning it (agent) the name \'" + agent_name + "\'")  



	'''
	Making folder in the directory
	'''
	# foldername = agentName_timestamp
	try:
		created_time = timeStamper()
		folder_name = agent_name + '_' + created_time
		os.mkdir ( folder_name )
		# Log
		created_time = timeStamper()
		logging.info ( created_time + "\tFolder \" "+ folder_name + "\" created\n")
	except errorOcc:
		created_time = timeStamper()
		logging.info ( created_time + "\tFailed to create folder.\t" + errorOcc + "\n")
		print ("Check log for errors.\nExiting... Agent folder not created.")
		exit ()
		

	'''
	Storing the required installation parameters into a file
	'''
	dir2 = "../../ossec-hids-2.8.1"
	os.chdir (dir2)
	fileOb = open ( "input.in", "w" )
	# OSSEC language
	fileOb.write ("en\n")
	# Press ENTER to continue
	fileOb.write ("\n")
	# Which type of installation do you want?
	fileOb.write ("agent\n")
	# Where to install ossec (default is set)
	fileOb.write ("\n")
	# IP address of the server
	fileOb.write (serverIP + "\n")
	# Do you want to run the integrity check daemon? (y/n) [y]:
	fileOb.write ("\n")
	# Do you want to run the rootkit detection engine? (y/n) [y]
	fileOb.write ("\n")
	# Do you want to enable active response? (y/n) [y]
	fileOb.write ("\n")
	# Press ENTER to continue
	fileOb.write ("\n")
	fileOb.close()

	dir2 = "../"
	os.chdir (dir2)

	'''
	Converting to a zip file
	'''
	try:
		print ( os.getcwd() )
		command = 'tar -cvf ossec-binary.tar ossec-hids-2.8.1/'
		
		os.system ( command )	
		# Log
		created_time = timeStamper ()
		logging.info ( created_time + "\tAgent folder zipped.\n")
	except:
		created_time = timeStamper ()
		logging.info ( created_time + "\tFailed to create .tar file for agent folder.\t")
		print ( "Check log for errors.\nExiting... .tar for agent folder not created." )
		exit ()



	'''
	Move files into this directory
	'''
	
	# folder from path, (this path will be the server's path to ossec bin files)
	folder_from_path = "ossec-binary.tar"
	# folder to path, (this path will be the client's path to /var/ossec)
	folder_to_path = "ossec_agent_deploy/scripts/" + folder_name + "/"
	# command would be scp instead of cp, to copy files over network
	# cp "-r" for copying folders
	# cp "-p" for preserving permissions
	try:
		command = 'echo %s | sudo -S cp -r -p %s %s' % (password, folder_from_path, folder_to_path)
		os.system ( command )
		# Log
		created_time = timeStamper ()
		logging.info ( created_time + "\tFile copied\n")
		
		time.sleep (2)
	except errorOcc:
		created_time = timeStamper ()
		logging.info ( created_time + "\tFailed to copy contents to folder.\t" + errorOcc + "\n")
		print ("Check log for errors.\nExiting... Files un-copied to agent folder.")
		exit ()
	
	'''
	Copying the files over to the remote networl
	'''
	try:
		command = 'echo %s | sudo scp -r -p ossec-binary.tar %s' % (password, (username + "@" + IPadd + ":/home/" + username))
		os.system ( command )
		
		# Log
		created_time = timeStamper ()
		logging.info ( created_time + "\tFile copied to remote server.\n")

	except ValueError:
		created_time = timeStamper ()
		logging.info ( created_time + "\tFailed to copy contents to remote system.\t" + errorOcc + "\n")
		print ("Check log for errors.\nExiting... Files un-copied to remote machine.")
		exit ()
	
	'''
	Installing ossec on the remote system
	'''
	try:
		s = pxssh.pxssh()
		s.login (IPadd, username, "root")
		s.sendline ('uptime')   # run a command
		s.prompt()             # match the prompt
		print ( s.before )          # print everything before the prompt.
		
		s.sendline ('tar xfv ossec-binary.tar')
		s.prompt()
		print ( s.before )
		
		s.sendline ('cd ossec-hids-*')
		s.prompt()
		print ( s.before )
		
		s.sendline ('echo %s | echo %s | sudo -S ./install.sh < input.in' % ("agent", "root"))
		s.prompt()
		print ( s.before )
		
		s.logout()
	except:
		created_time = timeStamper ()
		logging.info ( created_time + "\tError while installing.\t" + "\n")
		print ("Check log for errors.\nExiting... Ossec not installed.")
		exit ()
	
if __name__ == '__main__':
	main ()
	exit ()