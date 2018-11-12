<?php

$conn = mysqli_connect('localhost:3307','root','');
	if( !$conn ) {
		
		echo "Connection Failed";
	}
    mysqli_select_db( $conn, "agentmaster");
?>