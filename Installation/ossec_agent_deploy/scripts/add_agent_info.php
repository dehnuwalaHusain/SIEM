<?php

//echo "CHECK";

include('includes/connect.php');
include('tabs.php');

if (!empty($_POST)) {

	if(isset( $_POST['sub'] )) {
		$username = $_POST['username'];
		$password = $_POST['password'];
		//$agentname = $_POST['agentname'];
		$IP = $_POST['ip'];
		$OS_type = $_POST['select_os'];

		echo $username."<br>".$password."<br>".$IP."<br>".$OS_type;
			
		$result = mysqli_query( $conn, "SELECT count(*) as total from agentinfo");
		$data = mysqli_fetch_assoc( $result );
			
		$count = $data['total'] + 1;
		
		if($count<10)
			$count="00".(string)$count;

		else if($count<100)
			$count="0".(string)$count;
		
		echo "<br>".$count;

		//$output = passthru('python3 pyt.py');
		//echo $output;
		//(username, password, agentname, IP, OSType, AgentId)
		$res = mysqli_query( $conn, "INSERT INTO agentinfo VALUES('$username','$password','$count','$IP','$OS_type','$count')");
		
		if( !$res ) {
			
			echo "<script>alert('Could not add agent!');</script>";
		}
	}
}
?>


<!DOCTYPE html>
<html lang="en">
<head>
	<title>Add agent</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->	
	<link rel="icon" type="image/png" href="images/icons/favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="fonts/Linearicons-Free-v1.0.0/icon-font.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="vendor/css-hamburgers/hamburgers.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/animsition/css/animsition.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
<!--===============================================================================================-->	
	<link rel="stylesheet" type="text/css" href="vendor/daterangepicker/daterangepicker.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="css/util.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">
<!--===============================================================================================-->
</head>
<body>
	
	<div class="limiter">
		<div class="container-login100">
			<div class="wrap-login100 p-t-50 p-b-90">
				<form method=post class="login100-form validate-form flex-sb flex-w">
					<span class="login100-form-title p-b-51">
						AGENT INFORMATION
					</span>

					<div class="wrap-input100 validate-input m-b-16" data-validate = "User name is required">
						<input class="input100" type="text" name="username" placeholder="User Name">
						<span class="focus-input100"></span>
					</div>
					
					<div class="wrap-input100 validate-input m-b-16" data-validate = "Password is required">
						<input class="input100" type="password" name="password" placeholder="Password">
						<span class="focus-input100"></span>
					</div>
					
					<!--div class="wrap-input100 validate-input m-b-16" data-validate = "Agent name is required">
						<input class="input100" type="text" name="agentname" placeholder="Agent Name">
						<span class="focus-input100"></span>
					</div-->
					
					<div class="wrap-input100 validate-input m-b-16" data-validate = "IP is required" required>
						<input class="input100" type="text" name="ip" placeholder="IP" pattern="(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" oninvalid="setCustomValidity('Please enter valid IP Address')" onchange="try{setCustomValidity('')}catch(e){}" >
						<span class="focus-input100"></span>
					</div>
					
					<div class="wrap-input100 validate-input m-b-16">
						<select name="select_os" class="input100" required oninvalid="setCustomValidity('Please select an Operating System')" onchange="try{setCustomValidity('')}catch(e){}" >
							<option value="" style="color:red;" >Select OS</option>
							<option>Windows</option>
							<option>Ubuntu</option>
						</select>
					</div>

					<div class="container-login100-form-btn m-t-17">
						<button name="sub" id="sub" class="login100-form-btn">
							Add agent
						</button>
					</div>
				</form>
				<form action="index2.php" method="post">
					<div class="container-login100-form-btn m-t-17">
						<button class="login100-form-btn">
							Show Agent List
						</button>
					</div>

				</form>
			</div>
		</div>
	</div>
	

	<div id="dropDownSelect1"></div>
	
<!--===============================================================================================-->
	<script src="vendor/jquery/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/animsition/js/animsition.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/bootstrap/js/popper.js"></script>
	<script src="vendor/bootstrap/js/bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/select2/select2.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/daterangepicker/moment.min.js"></script>
	<script src="vendor/daterangepicker/daterangepicker.js"></script>
<!--===============================================================================================-->
	<script src="vendor/countdowntime/countdowntime.js"></script>
<!--===============================================================================================-->
	<script src="js/main.js"></script>

</body>
</html>
