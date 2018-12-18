import os

def manageAgents ( agent_name, IPadd, password ):

	print ("here")
	#command = 'sudo su'
	#os.system ( command )
	#dir2 = "/var/ossec/bin"
	#os.chdir (dir2)
	#dir2 = "sudo su cd /var/ossec/bin"
	#os.system (dir2)
	#print (os.getcwd())

	fileOb = open ("input.in", "w")
	fileOb.write ("a\n")
	fileOb.write (agent_name + "\n")
	fileOb.write (IPadd + "\n")
	fileOb.write ("\n")
	fileOb.write ("y\n")
	fileOb.close()

	command = 'sudo /var/ossec/bin/manage_agents < input.in'
	#command = "./manage_ag	ents"
	os.system ( command )

	os.system ("exit")
	print ("done")

#manageAgents("check", "10.65.6.7", "root@12")
