'''
[EDIT]
Alright, so logging will not work here for exceptions. And that's because Python does not have any problems executing those commands on the terminal. When an error occurs, it's from the terminal itself. Need to find a way to find those exeptions and add it to log.  
  

To print the current directory you're in ( debugging )
print (os.getcwd())

To save the last chdir you made through script:
os.system("/bin/bash")
'''

import os, datetime, time, logging

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
	# Username from webUI
	username = "tempUsername"

	# Password from webUI
	password = "root@12"

	# Agent name from webUI
	agent_name = "tempAgentName"

	# Agent ID from webUI
	agentID = "001"

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
	Move files into this directory
	'''
	# folder from path, (this path will be the server's path to ossec bin files)
	folder_from_path = "/home/husain/Workspace/SIEM/ossec-hids-2.9.4"
	# folder to path, (this path will be the client's path to /var/ossec)
	folder_to_path = folder_name + "/"
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
	Converting to a zip file
	'''
	try:
		os.system ("ls")
		command = folder_name
		os.chdir ( command )
		print ( os.getcwd() )
		command = 'tar -cvf ' + agent_name + '.tar ../../ossec-hids-2.9.4' + '/'
		
		os.system ( command )	
		# Log
		created_time = timeStamper ()
		logging.info ( created_time + "\tAgent folder zipped.\n")
	except:
		created_time = timeStamper ()
		logging.info ( created_time + "\tFailed to create .tar file for agent folder.\t")
		print ( "Check log for errors.\nExiting... .tar for agent folder not created." )
		exit ()

if __name__ == '__main__':
	main ()
	exit ()
