'''
This script makes changes in /usr/local/nagios/etc/objects/localhost.cfg to add a new host.

Inputs from command line: sudo python3 define_hosts.py <server's password> <agent IP> <agent name>
'''

import os, sys, ipaddress, header
from subprocess import Popen, PIPE

def define_host ( server_password, agent_IP, agent_name ):

	try:
		ipaddress.ip_address ( agent_IP )
	except ValueError:
		print ( "\n\nInvalid IP, AGENT INSTALLATION FAILED." )
		exit ()

	header.backup_localhost_cfg ( server_password )

	file = open ( "/usr/local/nagios/etc/objects/localhost.cfg", "a" )
	script = "\n# Adding HOST " + agent_name + " at IP " + agent_IP + "#\n\n"
	file.write ( script )

	script = "define host {\n\tuse\t\tlinux-box\n\thost_name\t" + agent_name + "\n\talias\t\t" + agent_name + "\n\taddress\t\t" + agent_IP + "\n}\n\n"
	file.write ( script )
	file.close ()

	script = "sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg"
	header.check_errors ( script, "Define host", server_password )
