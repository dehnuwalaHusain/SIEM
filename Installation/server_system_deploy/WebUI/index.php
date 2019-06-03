<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>SIEM - OSSEC and NAGIOS</title>
		<link rel="stylesheet" type="text/css" href="tabs_css.css">
	</head>
	
	<body style="padding: 20px;">
		<!--<h1 class="title">Tabs</h1>-->
		<div class="tabContainer">
			<div class="buttonContainer">
				<button style="font-size: 19px; text-align: center;" onclick="showPanel(0,'white')">INSTALL</button>
				<button style="font-size: 19px; text-align: center;" onclick="showPanel(1,'white')">CONFIGURE</button>
				<!--<button onclick="showPanel(2,'white')">Tab 3</button>
				<button onclick="showPanel(3,'white')">Tab 4</button>-->
			</div>
			<div class="tabPanel"><?php include('show_agents.php');  ?></div>
			<div class="tabPanel"><?php include('configure1.php');  ?></div>
			<!--<div class="tabPanel">Tab 3:Content</div>
			<div class="tabPanel">Tab 4:Content</div>-->
		</div>
		
		<script src="tabs_script.js"></script>
	</body>
</html>
