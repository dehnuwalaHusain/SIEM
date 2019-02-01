from subprocess import Popen, PIPE
comm = "sudo /var/ossec/bin/manage_agents"
cm = comm.split()
print (cm)
process = Popen(cm, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
if "command not found" in str(stdout):
	print ("check") 
else:
	print (stdout)
	print (stderr)