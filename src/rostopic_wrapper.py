#!/usr/bin/env python
import rospy
from hmi_rosbridge.msg import wrapper
from ace_msgs.msg import VehicleInfo, VehiclePositionInfo
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import UInt8, Bool, String


pub = rospy.Publisher('ros_signals', wrapper, queue_size=1)

message = wrapper()

def callbackA(data):   
    message.VehicleSpeed = data.VehicleSpeed
    message.AutoMode = data.AutoSwitchStatus
    message.BrakeMode = data.BrakeStatus
    message.VehDriveMode = data.DriveMode
    pub.publish(message)

def callbackB(data):
    message.Latitude = data.latitude
    message.Longitude = data.longitude
    pub.publish(message)

def callbackC(data):
    message.TripStatus = (int)(data.data)
    pub.publish(message)

def callbackD(data):
    message.JunctionStatus = data.data
    pub.publish(message) 

def callbackE(data):
    message.SafeToDrive = data.data
    pub.publish(message)

def callbackF(data):
    message.ResumeTrip = data.data
    pub.publish(message)

def callbackG(data):
    message.StopStatus = (int)(data.data)
    pub.publish(message)


def callbackJunctionApproaching(data):
    message.JunctionApproaching = (int)(data.data)
    pub.publish(message)

def listener():
    rospy.init_node('rostopic_wrapper', anonymous=True)

    rospy.Subscriber("VehicleInfo",VehicleInfo, callbackA, queue_size=1) #VehicleSpeed, BrakeMode, AutoMode, VehDriveMode
    rospy.Subscriber("gnss",NavSatFix, callbackB, queue_size=1) #GNSSLatitude, GNSSLongitude
    rospy.Subscriber("ToHMIStartTripAck",Bool, callbackC, queue_size=1) #tripStarted:1 else 0
    rospy.Subscriber("ToHMIJunction",Bool, callbackD, queue_size=1) #junctionReached:1 else 0
    rospy.Subscriber("ToHMIResumeAD",Bool, callbackE, queue_size=1) #safe to drive --resumeAD:1 else 0
    rospy.Subscriber("ToHMIResumeADAck",Bool, callbackF, queue_size=1) #trip resumed ack:1 else 0
    rospy.Subscriber("ToHMISpecialZone",Bool, callbackG, queue_size=1) #StopReached:1, else 0 
    rospy.Subscriber("ToHMISpecialZone",Bool, callbackG, queue_size=1) #StopReached:1, else 0 
    rospy.Subscriber("ToHMISpecialZone",UInt8, callbackJunctionApproaching, queue_size=1) #StopReached:1, else 0 
    
    rospy.spin()

if __name__ == '__main__':
    listener()

