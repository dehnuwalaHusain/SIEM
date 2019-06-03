<?php
	$un1 = $_GET['un'];
	$ps1 = $_GET['ps'];
	$id1 = $_GET['id'];
	$an1 = $_GET['an'];
	$ip1 = $_GET['ip'];
	$sps1 = $_GET['sps'];
	$sip1 = $_GET['sip'];
	//echo $an1;
	//exec("echo root | sudo python3 ../createAgentFolders.py '$un1' '$ps1' '$id1' '$an1' '$ip1' '$sip1' '$sps1' > output1.out", $output);
	echo shell_exec("echo root | sudo -S python3 ../../nagios_agent_deploy/install_nrpe.py '$un1' '$ps1' '$ip1' '$sip1' '$sps1' '$an1' 2>&1");
	//echo exec("python3 ../../nagios_agent_deploy/install_nrpe.py '$un1' '$ps1' '003' '$an1' '$ip1' '10.65.6.49' '$sps1' 2>&1");
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
