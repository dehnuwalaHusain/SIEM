<?php include('includes/connect.php');


//include('tabs.php');
?>

<!DOCTYPE html>
<html>
	<head>
		<title>Show agents</title>
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
	<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
<!--===============================================================================================-->

	<!--<script>
		function jsfunc(an, ip) {
			<?php $an1 = an; $ip1 = ip; ?>
			alert("<?php phpfunc('$an1', '$ip1'); ?>");
		}
	</script>
	
	<?php
		function phpfunc($an, $ip) {
			 
			exec("python3 test.py '$an' '$ip'", $output);
			for($i=0;$i<count($output);$i++) {
				print_r($output[$i]);
			}
		}
	?>-->


	</head>

	<body>
	<br>
	 <form action="add_agent_info.php" method="post">
	<div align="right" style="padding-right: 40px;">
		<button name="add" id="add" class="btn btn-primary btn-lg" style="background-color: #1abc9c;">
			Add agent
		</button>
	</div>
	</form>
	<span class="login100-form-title p-b-51">AGENT LIST</span>
	<div class="container" align="center">
		<div class="row">
			<div class="col-md-12 col-xs-12 col-sm-12 col-lg-12">
			
				<div class="card">
					<div class="card-text">
						<table class="table table-hover">
						  <thead>
							<tr class="table-success">
							  <th scope="col" class="centered">#</th>
							  <th scope="col" class="centered">Agent Name</th>
							  <th scope="col" class="centered">OS</th>
							  <th scope="col" class="centered">IP Address</th>
							  <th scope="col" class="centered">Action</th>
							</tr>
						  </thead>
						  
						  <tbody>
						  
								<?php
									$i = 1;
									$result_count = mysqli_query( $conn, "SELECT count(*) as total from agentinfo");
									$count = mysqli_fetch_assoc($result_count);
									while( $i <= $count['total'] ) {
									?>
										
										<tr>
											<td class="centered"><?php echo $i; ?></td>
											<td class="centered">
												<?php
													$result = mysqli_query( $conn, "SELECT * from agentinfo WHERE srno=$i");
													$data = mysqli_fetch_assoc($result);
													
													$result_server = mysqli_query( $conn, "SELECT * from serverinfo");
													$data_server = mysqli_fetch_assoc($result_server);
													
													echo $data['agentname'];
												?>
											</td>
											<td class="centered"><?php echo $data['OS_type']; ?></td>
											<td class="centered"><?php echo $data['IP']; ?></td>
											
											
									<td class="centered">
									<a href="installOssec.php?un=<?php echo $data['username']; ?>&ps=<?php echo $data['password']; ?>&id=<?php echo $data['srno']; ?>&an=<?php echo $data['agentname']; ?>&ip=<?php echo $data['IP']; ?>&sip=<?php echo $data_server['server_ip']; ?>&sps=<?php echo $data_server['server_password']; ?>" >
									<div class="btn btn-success" style="background-color: #1abc9c;">Install OSSEC</div>
									</a>
									<br><br>
									<a href="installNagios.php?un=<?php echo $data['username']; ?>&ps=<?php echo $data['password']; ?>&id=<?php echo $data['srno']; ?>&an=<?php echo $data['agentname']; ?>&ip=<?php echo $data['IP']; ?>&sip=<?php echo $data_server['server_ip']; ?>&sps=<?php echo $data_server['server_password']; ?>" >
									<div class="btn btn-success" style="background-color: #1abc9c;">Install Nagios</div>
									</a>
									</td>
										</tr>
									
								<?php
									$i++;
									}
								?>
						  
						  </tbody>
						</table>
					</div>
				</div>
			</div>
		</div> <!--row ends-->
	</div> <!-- container ends -->
	</body>
</html>
