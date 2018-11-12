<?php include('includes/connect.php'); ?>

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
	</head>

	<body>
	<br>
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
													echo $data['agentname'];
												?>
											</td>
											<td class="centered"><?php echo $data['ostype']; ?></td>
											<td class="centered"><?php echo $data['ip']; ?></td>
											<td class="centered"><button type="button" style="background-color: #1abc9c;" class="btn btn-success">Install</button></td>
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