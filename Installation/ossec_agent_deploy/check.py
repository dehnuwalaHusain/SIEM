import subprocess, os

sudoPassword = 'root@12'
folder_from_path = "/home/husain/Workspace/SIEM/ossec-hids-2.9.4"
folder_to_path = "/home/husain/Workspace/SIEM/src/"
command = 'echo %s | sudo -S cp -r -p %s %s' % (sudoPassword, folder_from_path, folder_to_path)
os.system ( command )
