# Installing nrpe for system health check monitoring
# Parameters: CPU utilisation, disk usage
'''
CMD parameters required:
python install_nrpe.py [<remote system username> <remote system password>
						 <remote system IP> <server's IP> <server system's password> <agent_name> ]



$ sudo apt install libssl-dev


add server IP in /etc/nagios/nrpe.cfg

put this in /etc/hosts.allow
nrpe: 192.168.1.100   nagios.example.edu

$ sudo iptables -A INPUT -p tcp --dport 5666 -j ACCEPT
$ sudo iptables-save

---------
to check, in case of connection reset:
$ service nrpe status --> on remote machine
---------

'''

import os, sys, logging, header, ipaddress, add_basic_services
from pexpect import pxssh
from define_host import define_host

LOG_FILENAME = 'Nagios_install.log'
logging.basicConfig (filename=LOG_FILENAME, level = logging.INFO)

def check_arguments():
	if ( len ( sys.argv ) != 7 ):
		print ("Missing cmd parameters.")
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tMissing arguments, exiting.")
		exit ()
	else:
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tParameters OK." )

def installation ():

	username = sys.argv [ 1 ]
	agent_password = sys.argv [ 2 ]
	agent_IP = sys.argv [ 3 ]
	server_IP = sys.argv [ 4 ]
	server_password = sys.argv [ 5 ]
	agent_name = sys.argv [ 6 ]
	
	try :
		ipaddress.ip_address ( agent_IP )
	except ValueError:
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tThe IP \'" + agent_IP + "\' is not a valid IP address.")	
		exit ()
	try :
		ipaddress.ip_address ( server_IP )
	except ValueError:
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tThe IP \'" + server_IP + "\' is not a valid IP address.")	
		exit ()


	created_time = header.timeStamper ()
	logging.info ( created_time + "\tInitiating installation on " + username + " with IP " + agent_IP)

	# Copying installation files from server to the to-be-agent.
	print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	print (os.system(pwd))
	print ("Aaaaaaaaaaaaaaaaaaaaaaaa")
	stat = True
	stat = header.fetchFileSCP ( "/opt/lampp/htdocs/localSIEM_withtabs/Installation/nagios_agent_deploy/nagios_plugin_nrpe/nagios_binary.tar.gz", username, agent_IP, agent_password, None )
	if stat:
		print ("File Transferred successfully.")
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tFile nagios_binary.tar.gz copied." )
	else:
		print ("Failure while copying files securely.")
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tFile nagios_binary.tar.gz copying failed." )
		exit ()

	stat = True
	stat = header.fetchFileSCP ( "/opt/lampp/htdocs/localSIEM_withtabs/Installation/nagios_agent_deploy/nagios_plugin_nrpe/nrpe_binary.tar.gz", username, agent_IP, agent_password, None )
	if stat:
		print ("File Transferred successfully.")
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tFile nrpe_binary.tar.gz copied." )
	else:
		print ("Failure while copying files securely.")
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tFile nrpe_binary.tar.gz copying failed." )
		exit ()

	stat = True
	stat = header.fetchFileSCP ( "/opt/lampp/htdocs/localSIEM_withtabs/Installation/nagios_agent_deploy/nagios_plugin_nrpe/lib_package_input.in", username, agent_IP, agent_password, None )
	if stat:
		print ("File Transferred successfully.")
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tFile lib_package_input.in copied." )
	else:
		print ("Failure while copying files securely.")
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tFile lib_package_input.in copying failed." )
		exit ()


	'''
	Installing nagios on the remote system
	'''
	try:
		s = pxssh.pxssh ()
		s.login ( agent_IP, username, agent_password)
		s.sendline ('uptime')   # run a command
		s.prompt()             # match the prompt
		print ( s.before )          # print everything before the prompt.

		s.sendline ('sudo apt install libssl-dev < lib_package_input.in ')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )
		
		s.sendline ('tar xzf nagios_binary.tar.gz')
		s.prompt()
		print ( s.before )

		print ('231')
		
		s.sendline ('sudo chmod -R a+rwx nagios-plugins-2.2.1/')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt ()
		print ( s.before )
		
		print ('237')
		
		s.sendline ('cd nagios-plugins-2.2.1')
		s.prompt()	
		print ( s.before )

		'''
		# At this time, the remote machine expects a password, this condition is identified and taken care of using s.expect
		s.sendline ('sudo ./configure')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo make')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )
		'''

		s.sendline ('sudo make install')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo useradd nagios')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo groupadd nagios')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo usermod -a -G nagios nagios')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo chown nagios.nagios /usr/local/nagios')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo chown -R nagios.nagios /usr/local/nagios/libexec')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo apt install xinetd < lib_package_input.in')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )


		s.sendline ('cd ..')
		s.prompt ()
		print (s.before) 

		s.sendline ( 'tar xzf nrpe_binary.tar.gz')
		s.prompt ()
		print (s.before)

		s.sendline ('sudo chmod -R a+rwx nrpe-nrpe-3.2.1/')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt ()
		print ( s.before )
		
		s.sendline ('cd nrpe-nrpe-3.2.1')
		s.prompt()	
		print ( s.before )

		'''
		s.sendline ('sudo ./configure')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo make all')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )
		'''
		
		s.sendline ('sudo make install-groups-users')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo make install')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo make install-config')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo make install-init')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo service xinetd restart')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo systemctl reload xinetd')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo systemctl enable nrpe && sudo systemctl start nrpe')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo initctl reload-configuration')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo iptables -A INPUT -p tcp --dport 5666 -j ACCEPT')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo iptables -A INPUT -p tcp --dport ssh -j ACCEPT')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo iptables-save')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		comm = 'sudo sed -i "$ a nrpe: %s nagios.example.edu" /etc/hosts.allow' % ( server_IP )
		s.sendline ( comm )
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		comm = 'sudo sed -i s/allowed_hosts=127.0.0.1,/allowed_hosts=127.0.0.1,%s,/g /usr/local/nagios/etc/nrpe.cfg' % ( server_IP )
		s.sendline ( comm )
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo ufw allow 5666')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )


		s.sendline ('sudo /sbin/service nrpe start')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.sendline ('sudo systemctl restart nrpe')
		#s.expect ('(?i)password.*:')
		s.sendline(agent_password)
		s.prompt()
		print ( s.before )

		s.logout()
	
	except Exception as e:
		created_time = header.timeStamper ()
		logging.info ( created_time + "\tError while installing.\t" + "\n")
		print ("Check log for errors.\nExiting... Ossec not installed.")
		print (e)
		exit ()

	# Add details to localhost.cfg
	define_host ( server_password, agent_IP,  agent_name )
	
	serv = add_basic_services.Service ()
	serv.capture_parameters ( agent_name, username, server_password )
	serv.add_service_CPU_Load ()
	serv.add_service_current_users ()
	serv.add_service_total_processes ()
	serv.add_service_zombie_processes ()

	header.restart_nagios ( server_password )

if __name__ == '__main__':
	check_arguments()
	installation ()
	exit()
