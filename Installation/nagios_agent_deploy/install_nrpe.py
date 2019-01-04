# Installing nrpe for system health check monitoring
# Parameters: CPU utilisation, disk usage
'''
CMD parameters required:
python install_nrpe.py [<remote system username> <remote system password>
						 <remote system IP> <server's IP> <server system's password>]

'''

import os, sys, logging, header, ipaddress
from pexpect import pxssh

LOG_FILENAME = 'Nagios_install.log'
logging.basicConfig (filename=LOG_FILENAME, level = logging.INFO)

def check_arguments():
	if ( len ( sys.argv ) != 6 ):
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

	'''
	Making a connection:
	'''
	try:
		s = pxssh.pxssh ()
		s.login ( agent_IP, username, agent_password )
		s.sendline ('uptime')
		s.prompt ()
		print ( s.before )

		s.sendline ( 'cd /tmp' )
		s.prompt ()
		print ( s.before )

		s.sendline ( 'wget http://nagios-plugins.org/download/nagios-plugins-2.2.1.tar.gz' )
		s.prompt ()
		print ( s.before )

		s.sendline ( 'tar xzf linux-nrpe-agent.tar.gz' )
		s.prompt ()
		print ( s.before )

		s.sendline ( 'cd linux-nrpe-agent' )
		s.prompt ()
		print ( s.before )

		s.sendline ( 'sudo ./fullinstall')
		s.sendline ( agent_password )
		s.prompt ()
		print ( s.before )

	except Exception as e:
		print (e)
		created_time = header.timeStamper ()
		logging.info ("Error while installing, I don't know where hehehehe")


if __name__ == '__main__':
	check_arguments()
	installation ()
	exit()