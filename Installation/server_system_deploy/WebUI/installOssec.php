<?php
	$agent_username = $_GET['un'];
	$agent_password = $_GET['ps'];
	$agent_id = $_GET['id'];
	$agent_name = $_GET['an'];
	$agent_IP = $_GET['ip'];
	$server_password = $_GET['sps'];
	$server_IP = $_GET['sip'];
	//echo $an1;
	//exec("echo root | sudo python3 createAgentFolders.py '$un1' '$ps1' '$id1' '$an1' '$ip1' '$sip1' '$sps1' > output1.out", $output);

	echo shell_exec("echo $server_password | sudo -S python3 ../../ossec_agent_deploy/scripts/createAgentFolders.py '$agent_username' '$agent_password' '$agent_id' '$agent_name' '$agent_IP' '$server_IP' '$server_password' 2>&1");
	//echo exec("python3 createAgentFolders.py '$un1' '$ps1' '003' '$an1' '$ip1' '10.65.6.49' '$sps1' 2>&1");
	/*for($i=0;$i<count($output);$i++) {
		print_r($output[$i]);
		echo "<br>";
	}*/
	
	/*$command = escapeshellcmd("test.py '$un1' '$ps1' '$id1' '$an1' '$ip1' '$sip1' '$sps1'");
	$output = shell_exec($command);*/
	
	/*$file = "output_agent.out";
	
	$file = escapeshellarg($file); // for the security concious (should be everyone!)
	$line = `tail -n 1 $file`;
	echo $line;*/
			
?>
