'''
########################################################################################
This script adds the configuration for checking remotehost's basic services into the...
..."/usr/local/nagios/etc/objects/localhost.cfg" file

--------------
Before we do anything here, it is important to understand that information about a user is
added in localhost.cfg -> HOST DEFINITION. We automate this in define_host.py file.
When we define the host, we give it a unique name, (thinking, we'll use the agent name we
use for OSSEC)

We presume this has already been done, and hence this script takes as cmd-line-arguments
the unique name.
--------------

--------------
COMPILE
sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg
--------------
=========================================================================
# script to be added into the localhost.cfg for check_load

define service	{
	use					generic-service		
	host_name			remotehost		;our remote host
	service_description	CPU Load		; name of service
	check_command		check_nrpe!check_load	; command
}
=========================================================================


sudo python3 add_basic_services.py <agent_name> <server's username> <server's password>


########################################################################################
'''

import os, sys, header, logging
from subprocess import Popen, PIPE

class Service:
	def capture_parameters ( self, agent_name, username, server_password ):
		self.agent_name = agent_name
		self.username = username
		self.server_password = server_password
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tCaptured parameters. Initiating services set up for " + self.agent_name )

	def add_service_CPU_Load ( self ):
		
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tAdding service CPU Load for " + self.agent_name )

		# Back-up existing cfg file before making any changes
		header.backup_localhost_cfg ( self.server_password )

		f = open ("/usr/local/nagios/etc/objects/localhost.cfg", "a")
		script = "\n# Adding service CPU Load for " + self.agent_name
		f.write ( script )

		script = "\ndefine service {\n\tuse\t\tgeneric-service\n\thost_name\t\t" + self.agent_name + "\n\tservice_description\tCPU Load\n\tcheck_command\t\tcheck_nrpe!check_load\n}\n\n"
		f.write ( script )
		f.close ()

		# Compile/check for errors with the changes
		script = "sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg"
		header.check_errors ( script, "CPU_load", self.server_password )

	def add_service_current_users ( self ):

		created_time = header.timeStamper ()
		logging.info ( created_time + "\tAdding service Current Users for " + self.agent_name )

		# Back-up existing cfg file before making any changes
		header.backup_localhost_cfg ( self.server_password )

		f = open ( "/usr/local/nagios/etc/objects/localhost.cfg", "a" )
		script = "\n# Adding service Current Users for " + self.agent_name
		f.write ( script )

		script = "\n\tdefine service {\n\tuse\t\tgeneric-service\n\thost_name\t\t" + self.agent_name + "\n\tservice_description\tCurrent Users\n\tcheck_command\tcheck_nrpe!check_users\n}\n\n"
		f.write (script)
		f.close ()

		# Compile/check for errors with the changes
		script = "sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg"
		header.check_errors ( script, "Current Users", self.server_password )

	def add_service_total_processes ( self ):
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tAdding service Total Processes for " + self.agent_name )

		# Back-up existing cfg file before making any changes
		header.backup_localhost_cfg ( self.server_password )

		f = open ( "/usr/local/nagios/etc/objects/localhost.cfg", "a" )
		script = "\n# Adding service Total Processes for " + self.agent_name
		f.write ( script )

		script = "\n\tdefine service {\n\tuse\t\tgeneric-service\n\thost_name\t\t" + self.agent_name + "\n\tservice_description\tTotal Processes\n\tcheck_command\tcheck_nrpe!check_total_procs\n}\n\n"
		f.write (script)
		f.close ()

		# Compile/check for errors with the changesAn error
		script = "sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg"
		header.check_errors ( script, "Total Processes", self.server_password )

	def add_service_zombie_processes ( self ):
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tAdding service Zombie Processes for " + self.agent_name )

		# Back-up existing cfg file before making any changes
		header.backup_localhost_cfg ( self.server_password )

		f = open ( "/usr/local/nagios/etc/objects/localhost.cfg", "a" )
		script = "\n# Adding service Zombie Processes for " + self.agent_name
		f.write ( script )

		script = "\n\tdefine service {\n\tuse\t\tgeneric-service\n\thost_name\t\t" + self.agent_name + "\n\tservice_description\tZombie Processes\n\tcheck_command\tcheck_nrpe!check_zombie_procs\n}\n\n"
		f.write (script)
		f.close ()

		# Compile/check for errors with the changes
		script = "sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg"
		header.check_errors ( script, "Zombie Processes", self.server_password )

'''
serv = Service ()
serv.capture_parameters ()
serv.add_service_CPU_Load ()
serv.add_service_current_users ()
serv.add_service_total_processes ()
serv.add_service_zombie_processes ()
'''