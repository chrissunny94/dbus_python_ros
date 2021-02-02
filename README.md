# HMI rosbridge 



#### Install dependencies

    sudo apt install libgirepository1.0-dev

#### Build instructions

	catkin_make
	
	
#### Run instructions


1) rostopic_wrapper.py

   Subscribes to various rostopics and publishes the required signals into single rostopic "ros_signals"
   
	rosrun hmi_rosbridge rostopic_wrapper.py
   
2) to_json.py

  Subscribes to the rostopic "ros_signals" and converts them into json format, and sents it to the DBUS server
  		
 	rosrun hmi_rosbridge to_json.py
 	
 3)response.py
 
   Subscribes to the dbus signal; Sends the responses(start trip, resume trip) received from HMI to the vehicle.
   
   	rosrun hmi_rosbridge response.py
 	
 
 ==***Published CAN message**s*==

|Topic name| Message type  |Who uses this ?|
|---------------|--------------------|-------------------- |
|/VehicleInfo| [ace_msgs/VehicleInfo](https://sourcecode.socialcoding.bosch.com/projects/LSAD/repos/dbc_rosbridge/browse/ace_msgs/msg/VehicleInfo.msg?at=refs%2Fheads%2Fdevelopment) | This puts out the vehicleInfo such as **Vehicle Speed** and** Autonomous Switch status **|
|/WheelInfo| [ace_msgs/WheelInfo](https://sourcecode.socialcoding.bosch.com/projects/LSAD/repos/dbc_rosbridge/browse/ace_msgs/msg/WheelInfo.msg?at=refs%2Fheads%2Fdevelopment) | This puts out wheel speed FL ,FR ,RL, RR|
|/VehicleDynamicsInfo| [ace_msgs/WheelInfo](https://sourcecode.socialcoding.bosch.com/projects/LSAD/repos/dbc_rosbridge/browse/ace_msgs/msg/VehicleDynamicsInfo.msg?at=refs%2Fheads%2Fdevelopment) | yaw rate , Longitudinal Acceleration , Lateral acceleration|
|/VehiclePositionInfo| [sensor_msgs/NavSatFix](http://docs.ros.org/melodic/api/sensor_msgs/html/msg/NavSatFix.html) | GPS Latitude , Longitude , Altitude|
|/SteeringInfo| [ace_msg/SteeringInfo](https://sourcecode.socialcoding.bosch.com/projects/LSAD/repos/dbc_rosbridge/browse/ace_msgs/msg/SteeringInfo.msg?at=refs%2Fheads%2Fdevelopment) | SteeringAngleFb|
|/RadarInfo| [ace_msg/RadarInfo](https://sourcecode.socialcoding.bosch.com/projects/LSAD/repos/dbc_rosbridge/browse/ace_msgs/msg/RadarInfo.msg?at=refs%2Fheads%2Fdevelopment) | PObj0_Longitudinal PObj0_Lateral Radar_AccelerationRequest|
|/USS_Object_Array| [ace_msg/USS_object_array](https://sourcecode.socialcoding.bosch.com/projects/LSAD/repos/dbc_rosbridge/browse/ace_msgs/msg/USS_object_array.msg?at=development) | [ace_msgs/USS_object](https://sourcecode.socialcoding.bosch.com/projects/LSAD/repos/dbc_rosbridge/browse/ace_msgs/msg/USS_object.msg?at=development)|



==***Subscribed ROS topics***==

|Topic name| Message type  |Who gives this input  |
|---------------|--------------------|----------------------------|
|/can_rx| [can_msgs/Frame.msg](http://docs.ros.org/melodic/api/sensor_msgs/html/msg/Image.html) |Socketcan node |



