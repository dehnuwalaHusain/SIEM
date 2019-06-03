'''
	Installation of Nagios Core and plug-ins required password of server
	and while configuring Apache password for server is required which is taken by command line argument
	By default password will be "nagiosadmin"

	Command Line argument:
	python3 ServerInstall.py [<server's password> <to-be Password for Nagios server> <server's IP> <server's username>]
	
	To uninstall:
	> rm -rf /usr/local/nagios
	> sudo userdel nagios
	> sudo groupdel nagios

	# 
'''

import os, logging, sys
from pexpect import pxssh
sys.path.append ('../nagios_plugin_nrpe/')
import header

def serverInstall():
	#Updating required dependancies
	'''	
		if sys.argc != 2:
		print ("No proper number of parameter found")
		exit()
	'''
	server_password = sys.argv[1]
	nag_new_password = sys.argv[2]
	server_IP = sys.argv[3]
	server_username = sys.argv[4]
	command = "echo %s | sudo -S apt-get update" %(server_password)
	os.system(command)
	#installing required softwares for nagios core installation
	command = "sudo apt-get install -y autoconf gcc libc6 make wget unzip apache2 php libapache2-mod-php7.2 libgd-dev"
	os.system(command)

	#Downloading files from source
	os.chdir("/tmp")
	command = "wget -O nagioscore.tar.gz https://github.com/NagiosEnterprises/nagioscore/archive/nagios-4.4.1.tar.gz"
	os.system(command)
	command = "tar xzf nagioscore.tar.gz"
	os.system(command)

	#Compilation of files
	dir = "/tmp/nagioscore-nagios-4.4.1/"
	os.chdir(dir)
	command = "sudo ./configure --with-httpd-conf=/etc/apache2/sites-enabled"
	os.system(command)
	command = "sudo make all"
	os.system(command)

	#This creates the nagios user and group. The www-data user is also added to the nagios group.
	command = "sudo make install-groups-users"
	os.system(command)
	command = "sudo usermod -a -G nagios www-data"
	os.system(command)

	#This step installs the binary files, CGIs, and HTML files.
	command = "sudo make install"
	os.system(command)

	#This installs the service or daemon files and also configures them to start on boot.
	command = "sudo make install-daemoninit"
	os.system(command)

	#This installs and configures the external command file.
	command = "sudo make install-commandmode"
	os.system(command)

	#This installs the *SAMPLE* configuration files. These are required as Nagios needs some configuration files to allow it to start.
	command = "sudo make install-config"
	os.system(command)

	#Install apache configuration files
	command = "sudo make install-webconf"
	os.system(command)
	command = "sudo a2enmod rewrite"
	os.system(command)
	command = "sudo a2enmod cgi"
	os.system(command)

	#Configuring firewall
	command = "sudo ufw allow Apache"
	os.system(command)
	command = "sudo ufw reload"
	os.system(command)


	##########################################
	try:
		s = pxssh.pxssh(timeout=1000)
		s.login (server_IP, server_username, server_password)
		s.sendline ('uptime')   # run a command
		s.prompt()             # match the prompt
		print ( s.before )          # print everything before the prompt.

		comm = "sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin"
		s.sendline (comm)
		#s.expect ('(?i)password.*:')
		s.sendline(server_password)
		s.sendline(nag_new_password)
		s.sendline(nag_new_password)
		s.prompt()
		print ( s.before )

		s.logout ()

	except Exception as e:
		print (e)
	##########################################

	'''
	#Creating Nagios user account
	command = "sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin root"
	os.system(command)
	'''

	#Reastarting web server
	command = "sudo systemctl restart apache2.service"
	os.system(command)

	#Starting Daemon
	command = "sudo systemctl start nagios.service"
	os.system(command)

	#Installing plug-ins for Nagios Core
	command = "sudo apt-get install -y autoconf gcc libc6 libmcrypt-dev make libssl-dev wget bc gawk dc build-essential snmp libnet-snmp-perl gettext"
	os.system(command)
	os.chdir("/tmp")
	command = "wget --no-check-certificate -O nagios-plugins.tar.gz https://github.com/nagios-plugins/nagios-plugins/archive/release-2.2.1.tar.gz"
	os.system(command)
	command = "tar zxf nagios-plugins.tar.gz"
	os.system(command)

	os.chdir("/tmp/nagios-plugins-release-2.2.1/")
	command = "sudo ./tools/setup"
	os.system(command)
	command = "sudo ./configure"
	os.system(command)
	command = "sudo make"
	os.system(command)
	command = "sudo make install"
	os.system(command)

	os.chdir ("/opt/lampp/htdocs/localSIEM_withtabs/Installation/server_system_deploy")
	# Installing NRPE plugin
	command = "sudo cp ../nagios_agent_deploy/nagios_plugin_nrpe/nrpe-nrpe-3.2.1.tar.gz ."
	os.system (command)
	command = "sudo tar zxf nrpe-nrpe-3.2.1.tar.gz"
	os.system (command)
	os.chdir ("nrpe-nrpe-3.2.1/")

	command = "sudo ./configure"
	os.system (command)

	command = "sudo make check_nrpe"
	os.system (command)

	command = "sudo make install-plugin"
	os.system (command)

	# Changing configuration file for including NRPE command definition
	header.backup_cfg ( server_password, "commands.cfg" )

	f = open ("/usr/local/nagios/etc/objects/commands.cfg", "a")
	script = "\n# Adding host command definition for nrpe"
	f.write (script)

	script = "\ndefine command {\n\tcommand_name\tcheck_nrpe\n\tcommand_line\t$USER1$/check_nrpe -H $HOSTADDRESS$ -c $ARG1$\n\t}\n"
	f.write (script)
	f.close ()

	# Compile and check for errors:
	script = "sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg"
	header.check_errors ( script, "Command definition", server_password, "commands.cfg")


	# Changing configuration file for including host-box definition

	header.backup_cfg ( server_password, "localhost.cfg")

	f = open ("/usr/local/nagios/etc/objects/localhost.cfg", "a")
	script = "\n# Adding host-box definition, NAME: linux-box\n"
	f.write (script)

	# ---------------------------------------------------
	# IMPORTANT - this line defines the behavior of a host group. How often the checks must be made etc. Any user specific configuration must 
	# be programmed to take place here.
	# ---------------------------------------------------
	script = "\ndefine host {\n\tname\tlinux-box\n\tuse\tgeneric-host\n\tcheck_period\t24x7\n\tcheck_interval\t5\n\tretry_interval\t1\n\tmax_check_attempts\t10\n\tcheck_command\tcheck-host-alive\n\tnotification_period\t24x7\n\tnotification_interval\t30\n\tnotification_options\td,r\n\tcontact_groups\tadmins\n\tregister\t0\n\t}\n"
	f.write (script)
	f.close ()

	# Compile and check for errors
	script = "sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg"
	header.check_errors ( script, "Host definition", server_password, "localhost.cfg")
serverInstall()
