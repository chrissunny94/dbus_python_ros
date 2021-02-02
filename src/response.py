#!/usr/bin/env python3
#!
from pydbus.generic import signal
from pydbus import SessionBus
from std_msgs.msg import UInt8
import json
import rospy
import yaml
from gi.repository import GLib
from hmi_rosbridge.msg import wrapper, message, message_array, VehicleMessage, response_message


loop = GLib.MainLoop()
dbus_ = "/org/bosch/AddaAgent/Message"
bus = SessionBus()
remote_object = bus.get(
    "org.bosch.AddaAgent",  # Bus name
    "/org/bosch/AddaAgent/Message"  # Object path
)


def response_recieved(object, msgDataType, seqNum, *response):
    response_recd = response[1][2]
    value_recd = json.loads(response_recd)
    print(json.dumps(value_recd, indent=4))
    s = value_recd['VehicleMessage']
    json_s = json.dumps(s, indent=4)
    f = json.loads(json_s)
    field = f['field']
    topicValue = (int)(f['value'])
    flag = 1

    ack = message()
    ack.field = "TripStarted"
    ack.datatype = "String"
    ack.value = "2"

    vehicle_message = VehicleMessage()
    vehicle_message.VehicleMessage.field = "VehicleInfoNotification"
    vehicle_message.VehicleMessage.datatype = "array"

    vehicle_message.VehicleMessage.value.append(ack)

    y = yaml.load(str(vehicle_message))
    startRes = json.dumps(y, indent=4)

    pubStart = rospy.Publisher('FromHMI_StartTrip', UInt8, queue_size=1)
    pubStartFalse = rospy.Publisher('FromHMI_StartTrip', UInt8, queue_size=1)
    pubResume = rospy.Publisher('FromHMI_ResumeAD', UInt8, queue_size=1)
    pubResumeFalse = rospy.Publisher('FromHMI_ResumeAD', UInt8, queue_size=1)
    rospy.init_node('response', anonymous=True)
    rate = rospy.Rate(3)
    beginTime = rospy.Time.now()
    Duration = rospy.Duration(4.0)
    endtime = beginTime+Duration

    while rospy.Time.now() < endtime:
        if(field == "TripStart"):
            pubStart.publish(topicValue)
            rate.sleep()
        else:
            pubResume.publish(topicValue)
            rate.sleep()

    pubStartFalse.publish(0)
    pubResumeFalse.publish(0)

if __name__ == "__main__":
    bus.subscribe(object=dbus_, signal_fired=response_recieved)
    loop.run()

class Client():
   def __init__(self):
      bus = dbus.SessionBus()
      service = bus.get_object('com.example.service', "/com/example/service")
      self._message = service.get_dbus_method('get_message', 'com.example.service.Message')
      self._quit = service.get_dbus_method('quit', 'com.example.service.Quit')

   def run(self):
      print "Mesage from service:", self._message()
      self._quit()

if __name__ == "__main__":
   Client().run()