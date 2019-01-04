## Objective
This is the first script that must be executed after `install` is initiated from WebUI for a particular `OSSEC client` device. 
The script must execute manage-agents on the `OSSEC server` and add agent information into it, extract the "client-key" so-generated.

### Scripts breakdown:
The task accomplished here is to install the OSSEC agent on the device.   
1. Create a folder with agent-specific credentials (like copying the client key into `/var/ossec/etc/`).
2. Add agent information into the `ossec server` by executing `/var/ossec/bin/manage-agents` using 	`<manage.py>`.
3. Copy the key that is generated from previous step and store it into the agent-specific folder generated in step 1.
4. Copy this folder onto the remote machine (to-be `ossec agent`) using scp. Acheived via the `fetchFileSCP()` method in `header.py`.
5. Connect to the remote machine via SSH using `pxssh` (pexpect) module provided by Python.
6. Unpack files, execute `install.sh` using agent-specific files created in the step 1 through 3. 
7. Restart `ossec server and client` to observe the newly added agent into the list of connected agents, can be checked from the WebUI via `list_agents.py` script.
