import os, header

def manageAgents ( agent_name, IPadd, password ):

	print ("here")
	#command = 'sudo su'
	#os.system ( command )
	#dir2 = "/var/ossec/bin"
	#os.chdir (dir2)
	#dir2 = "sudo su cd /var/ossec/bin"
	#os.system (dir2)
	#print (os.getcwd())

	fileOb = open ("manage_input.in", "w")
	fileOb.write ("a\n")
	fileOb.write (agent_name + "\n")
	fileOb.write (IPadd + "\n")
	fileOb.write (agent_name + "\n") #Agent ID same as Agent Name
	fileOb.write ("y\n")
	fileOb.close()

	command = 'echo %s | sudo -S /var/ossec/bin/manage_agents < manage_input.in' % (password)
	#command = "./manage_agents"
	if "command not find" in os.system ( command ):
		exit()
	else:
		os.system ("exit")
	print ("done")

#manageAgents("check", "10.65.6.7", "root@12")
