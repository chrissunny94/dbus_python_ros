


#### Install dependencies

    sudo apt install libgirepository1.0-dev

#### Build instructions

	catkin_make
	
	
#### Run instructions


1) rostopic_wrapper.py

   Subscribes to various rostopics and publishes the required signals into single rostopic "ros_signals"
   
	rosrun rostopic_wrapper.py
   
2) to_json.py

  Subscribes to the rostopic "ros_signals" and converts them into json format, and sents it to the DBUS server
  		
 	rosrun to_json.py
 	
 3)response.py
 
   Subscribes to the dbus signal; Sends the responses
   
   	rosrun  response.py
 	
 


