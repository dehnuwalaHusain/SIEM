'''

TO UNINSTALL OSSEC:
sudo rm -f /etc/init.d/ossec /etc/rc0.d/K20ossec /etc/rc1.d/K20ossec /etc/rc2.d/S20ossec /etc/rc3.d/S20ossec /etc/rc4.d/S20ossec /etc/rc5.d/S20ossec /etc/rc6.d/K20ossec; sudo rm -rf /var/ossec; sudo /usr/sbin/deluser ossec; sudo /usr/sbin/deluser ossecm; sudo /usr/sbin/deluser ossecr; sudo /usr/sbin/deluser ossecd; sudo /usr/sbin/delgroup ossec; sudo /usr/sbin/delgroup ossecd


[EDIT]
Alright, so logging will not work here for exceptions. And that's because Python does not have any problems executing those commands on the terminal. When an error occurs, it's from the terminal itself. Need to find a way to find those exeptions and add it to log.  
  

To print the current directory you're in ( debugging )
print (os.getcwd())

To save the last chdir you made through script:
os.system("/bin/bash")

COMMAND LINE ARGUMENTS FOR THIS SCRIPT:
python createAgentFolders.py [<username> <agent_password> <agent_name> <client/agent IP address> <serverIP> <server_password>.....]


'''

import os, datetime, time, logging, sys, ipaddress
from pexpect import pxssh
from manage import manageAgents

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
	server_password = "root@12"

	# Agent name from webUI via cmd arguments
	agent_name = "tempAgentName"

	# Agent ID from webUI via cmd arguments
	agentID = "001"
	
	# IP from webUI via cmd arguments
	IPadd = "10.65.6.10"

	# server IP address
	serverIP = "10.65.6.78"


	if ( len ( sys.argv ) != 7 ):
		created_time = timeStamper ()
		logging.info ( created_time + "\tDid not receive the pre-required information from UI for installation." )
		print ("Check log file for errors.")
		exit ()
	else: 
		username = sys.argv [ 1 ]
		agent_password = sys.argv [ 2 ]
		agent_name = sys.argv [ 3 ] 
		IPadd = sys.argv [ 4 ]
		serverIP = sys.argv [ 5 ]
		server_password = sys.argv [ 6 ]
		try :
			ipaddress.ip_address ( IPadd )
		except ValueError:
			created_time = timeStamper ()
			logging.info ( created_time + "\tThe IP \'" + IPadd + "\' is not a valid IP address.")	
			exit ()
		try :
			ipaddress.ip_address ( serverIP )
		except ValueError:
			created_time = timeStamper ()
			logging.info ( created_time + "\tThe IP \'" + serverIP + "\' is not a valid IP address.")	
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
	dir2 = "../Linux/ossec-hids-2.8.1"
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
	folder_to_path = "../scripts/" + folder_name + "/"
	# command would be scp instead of cp, to copy files over network
	# cp "-r" for copying folders
	# cp "-p" for preserving permissions
	try:
		command = 'echo %s | sudo -S cp -r -p %s %s' % (server_password, folder_from_path, folder_to_path)
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
	Add information of agent to be added in the server ( manage_agents )
	'''
	try:
		manageAgents ( agent_name, IPadd, server_password )
		created_time = timeStamper ()
		logging.info ( created_time + "\nAgent info added to server\n")
	except:
		created_time = timeStamper ()
		logging.info ( created_time + "\tFailed to add agent info to server.\t" + "\n")
		print ("Check log for errors.\nExiting...")
		exit ()

	'''
	Copying the files over to the remote network
	'''
	try:
		command = 'echo %s | sudo scp -r -p ossec-binary.tar %s' % (server_password, (username + "@" + IPadd + ":/home/" + username))
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
		print ("Check215")
		s.login (IPadd, username, agent_password)
		print ("Check217")
		s.sendline ('uptime')   # run a command
		print ("check219")
		s.prompt()             # match the prompt
		print ( s.before )          # print everything before the prompt.
		
		s.sendline ('tar xfv ossec-binary.tar')
		s.prompt()
		print ( s.before )

		s.sendline ('cd ossec-hids-*')
		s.prompt()
		print ( s.before )
		
		# At this time, the remote machine expects a password, this condition is identified and taken care of using s.expect
		s.sendline ('sudo ./install.sh < input.in')
		s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before ) 
		
		s.logout()
	except Exception as e:
		created_time = timeStamper ()
		logging.info ( created_time + "\tError while installing.\t" + "\n")
		print ("Check log for errors.\nExiting... Ossec not installed.")
		print (e)
		exit ()
	
if __name__ == '__main__':
	main ()
	exit ()
