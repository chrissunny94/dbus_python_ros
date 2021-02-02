#!/usr/bin/env python
import yaml
import json
import sys
from time import sleep
import os
import subprocess
from dbus.mainloop.glib import DBusGMainLoop
import dbus
import gobject

import rospy
from hmi_rosbridge.msg import wrapper, message, message_array, VehicleMessage

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

mainloop = gobject.MainLoop()

the_object = bus.get_object(
    "org.bosch.AddaAgent", "/org/bosch/AddaAgent/Message")
the_interface = dbus.Interface(the_object, "org.bosch.AddaAgent.Message")

seq =0

def msg2json(msg, seq):

   veh_speed = message()  # signals
   veh_bat_status = message()
   aux_bat_status = message()
   auto_mode = message()
   veh_drive_mode = message()
   latitude = message()
   longitude = message()
   brake_mode = message()
   park_brake_status = message()
   veh_failure = message()
   veh_standstill = message()
   diag_status = message()
   #junction_ahead = message()
   #junction_reached = message()
   #stop_ahead = message()
   #stop_reached = message()
   StartTrip = message()
   junction_status = message()  
   stop_status = message() 
   SafeToDrive = message()
   ResumeTrip = message()
   JunctionApproaching = message()

   veh_speed.field = "VehicleSpeed"
   veh_speed.datatype = "int"
   veh_speed.value = (int)(msg.VehicleSpeed)

   veh_bat_status.field = "VehBatteryStatus"
   veh_bat_status.datatype = "int"
   #veh_bat_status.value = (int)(msg.VehBatteryStatus)

   aux_bat_status.field = "AuxBatteryStatus"
   aux_bat_status.datatype = "int"
   #aux_bat_status.value = (int)(msg.AuxBatteryStatus)

   auto_mode.field = "AutoMode"
   auto_mode.datatype = "int"
   auto_mode.value = int(msg.AutoMode)

   veh_drive_mode.field = "VehDriveMode"
   veh_drive_mode.datatype = "int"
   veh_drive_mode.value = (int)(msg.VehDriveMode)

   latitude.field = "Latitude"
   latitude.datatype = "double"
   latitude.value = msg.Latitude

   longitude.field = "Longitude"
   longitude.datatype = "double"
   longitude.value = msg.Longitude

   brake_mode.field = "BrakeMode"
   brake_mode.datatype = "int"
   brake_mode.value = (int)(msg.BrakeMode)

   park_brake_status.field = "ParkBrakeStatus"
   park_brake_status.datatype = "int"
   #park_brake_status.value = (int)(msg.ParkBrakeStatus)

   veh_failure.field = "VehFailureStatus"
   veh_failure.datatype = "int"
   #veh_failure.value = (int)(msg.VehFailureStatus)

   veh_standstill.field = "VehStandstillReason"
   veh_standstill.datatype = "int"
   #veh_standstill.value = (int)(msg.VehStandstillReason)

   diag_status.field = "Diagnostic"
   diag_status.datatype = "int"
   diag_status.value = 1

   """ junction_ahead.field = "JuncAhead"
   junction_ahead.datatype = "string"
   junction_ahead.value = "JunctionNameA" """

   """ junction_reached.field = "JuncReached"
   junction_reached.datatype = "String"
   junction_reached.value = (msg.JuncReached) """

   """ stop_ahead.field = "StopAhead"
   stop_ahead.datatype = "string"
   stop_ahead.value = "StopNameA" """

   ''' stop_reached.field = "StopReached"
   stop_reached.datatype = "string"
   stop_reached.value = msg.StopReached '''

   StartTrip.field = "TripStatus"
   StartTrip.datatype = "int"
   StartTrip.value = (int)(msg.TripStatus)

   junction_status.field = "JuncStatus"
   junction_status.datatype = "int"
   junction_status.value = (int)(msg.JunctionStatus)

   stop_status.field = "StopStatus"
   stop_status.datatype = "int"
   stop_status.value = (int)(msg.StopStatus)  
 

   SafeToDrive.field = "SafeToDrive"
   SafeToDrive.datatype = "int"
   SafeToDrive.value = (int)(msg.SafeToDrive)

   ResumeTrip.field = "ResumeTrip"
   ResumeTrip.datatype = "int"
   ResumeTrip.value = (int)(msg.ResumeTrip)

   JunctionApproaching.field = "JunctionApproaching"
   JunctionApproaching.datatype = "int"
   JunctionApproaching.value = (int)(msg.JunctionApproaching)

   

   vehicle_message = VehicleMessage()  # complete_json_message

   vehicle_message.VehicleMessage.field = "VehicleInfoNotification"
   vehicle_message.VehicleMessage.datatype = "array"

   vehicle_message.VehicleMessage.value.append(veh_speed)
   #vehicle_message.VehicleMessage.value.append(veh_bat_status)
   #vehicle_message.VehicleMessage.value.append(aux_bat_status)
   vehicle_message.VehicleMessage.value.append(auto_mode)
   vehicle_message.VehicleMessage.value.append(veh_drive_mode)
   vehicle_message.VehicleMessage.value.append(latitude)
   vehicle_message.VehicleMessage.value.append(longitude)
   vehicle_message.VehicleMessage.value.append(brake_mode)
   #vehicle_message.VehicleMessage.value.append(park_brake_status)
   #vehicle_message.VehicleMessage.value.append(veh_failure)
   #vehicle_message.VehicleMessage.value.append(veh_standstill)
   vehicle_message.VehicleMessage.value.append(diag_status)
   #vehicle_message.VehicleMessage.value.append(junction_ahead)
   #vehicle_message.VehicleMessage.value.append(junction_reached)
   #vehicle_message.VehicleMessage.value.append(stop_ahead)
   #vehicle_message.VehicleMessage.value.append(stop_reached)
   vehicle_message.VehicleMessage.value.append(StartTrip)
   vehicle_message.VehicleMessage.value.append(junction_status)
   vehicle_message.VehicleMessage.value.append(stop_status)
   vehicle_message.VehicleMessage.value.append(SafeToDrive)
   vehicle_message.VehicleMessage.value.append(ResumeTrip)

   y = yaml.load(str(vehicle_message))
   json_value = json.dumps(y, indent=4)

   reply = the_interface.VehicleNotification(1, seq, json_value)
   print(reply)
   seq += 1

   return json_value


def callback(data):
    message = data
    print (msg2json(message, seq))


def listener():
    rospy.init_node('to_json', anonymous=True)
    rospy.Subscriber("/ros_signals", wrapper, callback, queue_size=1)
    rospy.spin()

if __name__ == '__main__':
    listener()
