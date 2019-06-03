import os, sys, logging
#from createAgentFolders import timeStamper

def retreive_key ( agent_ID, password ):

	try:
		fileOb = open ("key_input.in", "w")
		# press e for extracting a key
		fileOb.write ("e\n")
		# which is the key you want to extract?
		fileOb.write (agent_ID + "\n")
		# press ENTER to return to main menu
		fileOb.write ("\n")
		# press q to quit
		fileOb.write ("q\n")
		fileOb.close ()

	except Exception as e:
		print (e)

	try:
		comm = "echo %s | sudo -S /var/ossec/bin/manage_agents < key_input.in > key.out " % (password)
		os.system (comm)
		os.system ("sudo /var/ossec/bin/ossec-control restart")
#		log_time = timeStamper ()
#		logging.info ( log_time + "\tContents extracted to file 'key.out'." )
	except Exception as e:
		print (e)
#		log_time = timeStamper ()
#		logging.info ( log_time + "\tFailed to extract contents to file 'output.out'." )
	#os.system ( "echo %s | sudo /var/ossec/bin/list_agents -a" % ( server_password ) )

def store_key ():
	try:
		fileOb = open ( "key.out", "r" )
		lines = fileOb.readlines ()
		foundKey = False
		iter = 0

		while ( not foundKey ):
			currLine = lines [ iter ]

			iter += 1
			if "Agent key information for" in currLine:
				
				currLine = lines [ iter ]
				newFileOb = open ("final_key.out", "w")
				# on agent side: "press i for importing a key"
				newFileOb.write ("i\n")
				# enter the key 
				newFileOb.write ( currLine )
				# confirm adding it?
				newFileOb.write ( "y\n" )
				newFileOb.close ()
				foundKey = True

	except Exception as e:
		print ( e )

def keys ( agent_ID, password ):

	retreive_key ( agent_ID, password )
	store_key ()