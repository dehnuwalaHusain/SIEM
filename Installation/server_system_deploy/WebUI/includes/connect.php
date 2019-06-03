<?php

$conn = mysqli_connect('localhost:3306','Neha','root');
	if( !$conn ) {
		
		echo "Connection Failed";
	}
    mysqli_select_db( $conn, "agentmaster");
?>	
