import json
import yaml
import rospy
from hmi_rosbridge.msg import wrapper2, message, message_array, VehicleMessage
from gi.repository import GLib
from pydbus import SessionBus


# Create and run main loop
loop = GLib.MainLoop()


bus = SessionBus()

# Create an object that will proxy for a particular remote object.
remote_object = bus.get(
    "org.bosch.AddaAgent", # Bus name
    "/org/bosch/AddaAgent/Message" # Object path
)

def response_(*args):
    print("done")

def msg2json(msg):
    
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

   #array_signal = message_array() #array_of_signals

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

   y = yaml.load(str(vehicle_message))
   json_value = json.dumps(y, indent=4)

   reply = remote_object.VehicleRequest(1, 4, json_value)
   print(reply) 

   #remote_object.VehicleResponse.connect()
   
   """ bus.subscribe(object = "/org/bosch/AddaAgent/Message", signal_fired = response_) """
   #bus.subscribe(iface=None, signal = "VehicleResponse", object = "/org/bosch/AddaAgent/Message", signal_fired = response_)
   """ session_bus.subscribe(iface='my.iface',
                      signal='my_signal_name',
                      object='/my/object',
                      signal_fired=my_callback) """


   #loop.run()

   return json_value



def callback(data):
    message = data
    print (msg2json(message))

def listener():
    rospy.init_node('to_json', anonymous=True)
    rospy.Subscriber("/ros_signals", wrapper2, callback, queue_size=1)
    rospy.spin()


if __name__ == '__main__':
    listener()