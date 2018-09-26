## Next Up
This is the first script that must be executed after `install` is initiated from WebUI for a particular `OSSEC client` device. 
The script must execute manage-agents on the `OSSEC server` and add agent information into it, extract the "client-key" so-generated.

## createAgentFolders.py
The main task here is to install the OSSEC agent on the device.  
This is a __ part process:  
1. Create a folder with agent-specific credentials (like copying the client key into `/var/ossec/etc/`).  
2. Create sudo priviliges users named `ossec`, `ossecm`, `ossecr` on the client device.  
  (OSSEC uses these users to gather logs and other important files from the system)
3. Copy the folder created in 1 into the `/var/ossec/` directory of client device.  
