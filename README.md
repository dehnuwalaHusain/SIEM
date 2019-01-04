# SIEM
Automated agent for OSSEC and NAGIOS (currently working on OSSEC)

## Naming conventions:
**OSSEC server** The system where all the logs will get aggregated and monitored.  
**OSSEC client** The devices in network which are being monitored by OSSEC.
**NAGIOS server** The system where all the system parameters returned from NSCA plugin _or_ requested from NRPE plugin will be accumulated.
**NAGIOS client** The devices in network which are being monitored by NAGIOS.
**Client** The analogical organisation using this automated agent.

## System Goal/Objective:
To create an automated agent that will run on the `client`'s `OSSEC / NAGIOS server`, providing a webUI wherein `client` enters the necessary credientials of all the `OSSEC / NAGIOS client` devices that need to be monitored for threats in his/her network.
Once `install` is initiated via webUI, scripts from `Installation` must execute on the IP provided by `client`.

[More details on scripts](Installation/ossec_agent_deploy/scripts/README.md)
