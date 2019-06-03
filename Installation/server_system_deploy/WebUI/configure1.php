<!DOCTYPE html>
<html>

   <head>
      <title>HTML Frames</title>
   </head>
   
   <style>
   	body, html {
  width: 100%;
  height: 100%;
  margin: 0;
}

.container {
  width: 100%;
  height: 100%;
}

.leftpane {
    width: 50%;
    height: 100%;
    float: left;
    text-align: left;
    background-color: white;
    border-collapse: collapse;
}

/*.middlepane {
    width: 50%;
    height: 100%;
    float: left;
    background-color: royalblue;
    border-collapse: collapse;
}*/

.rightpane {
  width: 50%;
  height: 100%;
  position: relative;
  float: right;
  text-align: right;
  background-color: white;
  border-collapse: collapse;
}

.toppane {
  width: 100%;
  height: 200px;
  border-collapse: collapse;
  background-color: white;
}

.select_ar {
	font-family: Ubuntu-Bold;
  color: #403866;
  line-height: 1.2;
  font-size: 18px;
  /*margin-left: 70px;*/
  display: block;
  width: 100%;
  background: transparent;
  height: 50px;
  padding: 0 20px 0 38px;
}

.wrap-input100_left {
  width: 80%;
  margin-left: -165px;
  position: relative;
  background-color: #e6e6e6;
  border: 1px solid transparent;
  border-radius: 3px;
}

.wrap-input100_right {
  width: 80%;
  margin-left: 250px;
  position: relative;
  background-color: #e6e6e6;
  border: 1px solid transparent;
  border-radius: 3px;
}
   </style>
   
   <body>
   
   	<div class="container">
  <!--<div class="toppane"></div>-->
  
  <div class="leftpane">
    <h1>OSSEC</h1>
    <br><br>
    <form method="post">
    
    <div class="wrap-input100_left" data-validate = "Agent name is required">
						<input class="select_ar" type="text" name="agentname" placeholder="Agent Name">
						
					</div>
    <br>
    <div class="wrap-input100_left">
    	<select class="select_ar">
    		<option>--Select--</option>
    		<option>Sample 1</option>
    		<option>Sample 2</option>
    		<option>Sample 3</option>
    		<option>Sample 4</option>
    		<option>Sample 5</option>
    		<option>Sample 6</option>
    		<option>Sample 7</option>
    		<option>Sample 8</option>
    		<option>Sample 9</option>
    		<option>Sample 10</option>
    	</select>
    </div>
    
    </form>
  </div>
  
<!--  <div class="middlepane"></div>-->
  <div class="rightpane">
    <h1>NAGIOS</h1>
    
    <br><br>
    <form method="post">
    
    <div class="wrap-input100_right" data-validate = "Agent name is required">
						<input class="select_ar" type="text" name="agentname" placeholder="Agent Name">
						
					</div>
    <br>
    <div class="wrap-input100_right">
    	<select class="select_ar">
    		<option>--Select the parameters--</option>
    		<option>CPU load</option>
    		<option>Disk Utilization</option>
    		<option>Total processes</option>
    		<option>Memory</option>
    		<!--<option>Sample 5</option>
    		<option>Sample 6</option>
    		<option>Sample 7</option>
    		<option>Sample 8</option>
    		<option>Sample 9</option>
    		<option>Sample 10</option>-->
    	</select>
    </div>
    
    </form>
    
    </div>
</div>
   </body>
   
</html>
