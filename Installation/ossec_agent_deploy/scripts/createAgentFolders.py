'''

TO UNINSTALL OSSEC:
sudo rm -f /etc/init.d/ossec /etc/rc0.d/K20ossec /etc/rc1.d/K20ossec /etc/rc2.d/S20ossec /etc/rc3.d/S20ossec /etc/rc4.d/S20ossec /etc/rc5.d/S20ossec /etc/rc6.d/K20ossec; sudo rm -rf /var/ossec; sudo /usr/sbin/deluser ossec; sudo /usr/sbin/deluser ossecm; sudo /usr/sbin/deluser ossecr; sudo /usr/sbin/deluser ossecd; sudo /usr/sbin/delgroup ossec; sudo /usr/sbin/delgroup ossecd

Alright, so logging will not work here for exceptions. And that's because Python does not have any problems executing those commands on the terminal. When an error occurs, it's from the terminal itself. Need to find a way to find those exeptions and add it to log.  
  

To print the current directory you're in ( debugging )
print (os.getcwd())

To save the last chdir you made through script:
os.system("/bin/bash")

COMMAND LINE ARGUMENTS FOR THIS SCRIPT:
python createAgentFolders.py [<username> <agent_password> <agent_ID> <agent_name> <client/agent IP address>
									 <serverIP> <server_password>]


'''

import os, logging, sys, ipaddress, header, time
from pexpect import pxssh
from manage import manageAgents
from copy_keys import keys

LOG_FILENAME = 'installation.log'
logging.basicConfig (filename = LOG_FILENAME, level = logging.INFO)

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


	'''
	Name of the ossec folder in ../Installation/ossec_agent_deploy/Linux/"
	'''
	ossec_folder = "ossec-hids-3.1.0"


	if ( len ( sys.argv ) != 8 ):
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tDid not receive the pre-required information from UI for installation." )
		print ("Check log file for errors.")
		exit ()
	else: 
		username = sys.argv [ 1 ]
		agent_password = sys.argv [ 2 ]
		agent_ID = sys.argv [ 3 ]
		agent_name = sys.argv [ 4 ] 
		IPadd = sys.argv [ 5 ]
		serverIP = sys.argv [ 6 ]
		server_password = sys.argv [ 7 ]
		try :
			ipaddress.ip_address ( IPadd )
		except ValueError:
			created_time = header.timeStamper ()
			logging.info ( created_time + "\tThe IP \'" + IPadd + "\' is not a valid IP address.")	
			exit ()
		try :
			ipaddress.ip_address ( serverIP )
		except ValueError:
			created_time = header.timeStamper ()
			logging.info ( created_time + "\tThe IP \'" + serverIP + "\' is not a valid IP address.")	
			exit ()

	created_time = header.timeStamper ()
	logging.info ( created_time + "\tInitiating installation for machine with username \'" + username + "\' and IP \'" + IPadd +
									"\' and assigning it (agent) the name \'" + agent_name + "\'")  



	'''
	Making folder in the directory
	Current directory: ../Installation/ossec_agent_deploy/scripts
	'''
	# foldername = agentName_timestamp
	try:
		created_time = header.timeStamper()
		folder_name = agent_name + '_' + created_time
		os.chdir("../../ossec_agent_deploy/scripts/")
		os.mkdir ( folder_name )
		# Log
		created_time = header.timeStamper()
		logging.info ( created_time + "\tFolder \" "+ folder_name + "\" created\n")
	except Exception as e:
		created_time = header.timeStamper()
		logging.info ( created_time + "\tFailed to create folder.\t" + e + "\n")
		print ("Check log for errors.\nExiting... Agent folder not created.")
		exit ()
		

	'''
	Move ossec file into this directory and unpack
	'''
	
	dir2 =folder_name
	os.chdir (dir2)
	'''
	Current Directory: ../Installation/ossec_agent_deploy/scripts/<<folder_name>>
	'''
	
	# folder from path, (this path is where ossec binary files are stored)
	folder_from_path = "../../Linux/" + ossec_folder + ".tar.gz"
	# folder to path, (this path is where client's copy is to be stored)
	folder_to_path = "."
	# command would be scp instead of cp, to copy files over network
	# cp "-r" for copying folders
	# cp "-p" for preserving permissions
	try:
		command = 'echo %s | sudo -S cp -r -p %s %s' % (server_password, folder_from_path, folder_to_path)
		os.system ( command )
		command = 'tar xf ' + ossec_folder + '.tar.gz'
		os.system ( command )
		# Log
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tFile copied\n")
		
		time.sleep (2)
	except Exception as e:
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tFailed to copy contents to folder.\t" + e + "\n")
		print ("Check log for errors.\nExiting... Files un-copied to agent folder.")
		exit ()


	'''
	Storing the required installation parameters into a file
	'''
	dir2 = ossec_folder
	os.chdir (dir2)
	'''
	Current Directory: ../Installation/ossec_agent_deploy/scripts/<<folder_name>>/<<ossec_folder>>
	'''
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

	'''
	Add information of agent to be added in the server ( manage_agents )
	'''
	try:
		dir2 = "../"
		os.chdir (dir2)
		'''
		Current Directory: ../Installation/ossec_agent_deploy/scripts/<<folder_name>>
		'''
		manageAgents ( agent_name, IPadd, server_password )
		print (os.getcwd())
		created_time = header.timeStamper ()
		logging.info ( created_time + "\nAgent info added to server\n")
	except Exception as e:
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tFailed to add agent info to server.\t" + str(e) + "\n")
		print ("Check log for errors.\nExiting...")
		exit ()

	'''
	Copy keys
	'''
	try:
		dir2 = ossec_folder
		os.chdir ( dir2 )
		'''
		Current Directory: ../Installation/ossec_agent_deploy/scripts/<<folder_name>>/<<ossec_folder>>
		'''
		keys ( agent_ID, server_password )
		dir2 = "../"
		os.chdir ( dir2 )
		'''
		Current Directory: ../Installation/ossec_agent_deploy/scripts/<<folder_name>>
		'''
	except Exception as e:
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tError while copying client key.\t" + "\n")
		print ("Check log for errors.\nExiting... Ossec not installed.")
		print (e)
		exit ()

	'''
	Converting to a zip file
	'''
	try:
		print ( os.getcwd() )
		# remove 'v' -cf
		command = 'tar -cf ossec-binary.tar ' + ossec_folder + '/'
		
		os.system ( command )	
		# Log
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tAgent folder zipped.\n")
	except Exception as e:
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tFailed to create .tar file for agent folder.\t")
		print ( "Check log for errors.\nExiting... .tar for agent folder not created." )
		exit ()


	'''
	Copying the files over to the remote network
	'''	
	stat = True
	stat = header.fetchFileSCP("ossec-binary.tar",username, IPadd, agent_password, None)
	if stat:
		print ("File Transferred successfully.")
	else:
		print ("Failure while copying files securely.")

	'''
	Installing ossec on the remote system
	'''
	try:
		s = pxssh.pxssh(timeout=1000)
		s.login (IPadd, username, agent_password)
		s.sendline ('uptime')   # run a command
		s.prompt()             # match the prompt
		print ( s.before )          # print everything before the prompt.
		
		s.sendline ('tar xf ossec-binary.tar')
		s.prompt()
		print ( s.before )

		s.sendline ( 'pwd' )
		s.prompt ()
		print ( s.before )

		print ('231')
		comm = "sudo chmod -R a+rwx " + ossec_folder + "/"
		s.sendline (comm)
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )
		print ('237')
		comm = "cd " + ossec_folder
		s.sendline (comm)
		s.prompt()	
		print ( s.before )

		# At this time, the remote machine expects a password, this condition is identified and taken care of using s.expect
		s.sendline ('sudo sh ./install.sh < input.in')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ( 'pwd' )
		s.prompt ()
		print ( s.before )

		s.sendline ( 'ls' )
		s.prompt ()
		print ( s.before )


		s.sendline ('sudo /var/ossec/bin/manage_agents < final_key.out')
		s.prompt ()
		print (s.before) 
		
		#comm = "sudo chown -R " + username + " /var/ossec/"
		#s.sendline (comm)
		#s.prompt()
		#print (s.before)

		s.sendline ( 'sudo /var/ossec/bin/ossec-control restart')
		s.prompt ()
		print (s.before)
		
		s.logout()
	except Exception as e:
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tError while installing.\t" + "\n")
		print ("Check log for errors.\nExiting... Ossec not installed.")
		print (e)
		exit ()

	print("OSSEC Agent installed.")
	'''
	Delete the created folder
	
	dir2 = "scripts/"
	os.chdir ( dir2 )
	os.rmdir ( folder_name )
	'''
	
if __name__ == '__main__':
	main ()
	exit ()
