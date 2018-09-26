# SIEM
Automated agent for OSSEC and NAGIOS (currently working on OSSEC)

## Naming conventions:
**OSSEC server** The system where all the logs will get aggregated and monitored.  
**OSSEC client** The devices in network which are being monitored by OSSEC.  
**Client** The analogical organisation using this automated agent.

## System Goal/Objective:
To create an automated agent that will run on the `client`'s `OSSEC server`, providing a webUI wherein `client` enters the necessary credientials of all the `OSSEC client` devices that need to be monitored for threats in his/her network.
Once `install` is initiated via webUI, scripts from `Installation` repo must execute on the IP provided by `client`.

*More details on scripts in the Installation/README.md*
