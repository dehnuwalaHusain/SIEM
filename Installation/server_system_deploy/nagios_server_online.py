'''
	Installation of Nagios Core and plug-ins required password of server
	and while configuring Apache password for server is required which is taken by command line argument
	By default password will be "nagiosadmin"

	Command Line argument:
	python3 ServerInstall.py [<System password> <Password for Apache server>]
'''

import os,logging,sys
def serverInstall():
	#Updating required dependancies
	'''	
		if sys.argc != 2:
		print ("No proper number of parameter found")
		exit()
	'''
	systemPassword = sys.argv[1]
	command = "echo %s| sudo apt-get update"
	os.system(command%(systemPassword))
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

	#Creating Nagios user account
	command = "sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin"
	os.system(command)

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

serverInstall()