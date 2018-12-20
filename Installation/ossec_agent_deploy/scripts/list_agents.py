'''
	NEEDS server_password as cmd line argument

	Recommended for the UI to run script from the directory itself for continued logging support.
'''

import os, sys, logging
from createAgentFolders import timeStamper

def list_agents ( server_password ):
	os.system ( "echo %s | sudo /var/ossec/bin/list_agents -a" % ( server_password ))


if __name__ == '__main__':

	if ( len ( sys.argv ) != 2 ):
		print ( "Did not receive server's password as arguments." )
		log_time = timeStamper ()
		logging.info ( log_time + "\tDid not receive proper arguments (server's password) for listing agents." )
		exit ()
	else:	
		server_password = sys.argv [ 1 ]
		list_agents ( server_password )
		log_time = timeStamper ()
		logging.info ( log_time + "\tServer initiated list_agents, succeeded." )