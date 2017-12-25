#!/usr/bin/env python
from __future__ import print_function
import obd
from obd import OBDStatus
import time

ODB_PORT = "/dev/pts/6" # Enter COM port here manually if needed, e.g /dev/rfcomm0
# ODB_PORT = obd.scan_serial()[0] # Enter COM port here, e.g /dev/rfcomm0
connection = None

# print("!!!! Scanning for serial ports, but will connect to " + ODB_PORT + " only. !!!!")
# ports = obd.scan_serial()      # return list of valid USB or RF ports
# print(ports)                   # ['/dev/ttyUSB0', '/dev/ttyUSB1']

print("####################### Starting... #######################")
try:
    connection = obd.OBD(ODB_PORT, None, None, True) # auto-connects to USB or RF port
    #connection = obd.OBD(ODB_PORT)
    # self.fail('message')
    print("Status: " + connection.status())
except Exception as e:
    print("Setting up inital connection... ")
    while connection == None or connection.status() != OBDStatus.CAR_CONNECTED:
        time.sleep(1)
        try:
            connection = obd.OBD(ODB_PORT, None, None, True)
            print("Status: " + connection.status())
        except Exception as e:
            print("Initial connection failed, trying to reconnect... ")

if connection.status() == OBDStatus.CAR_CONNECTED:
    print("####################### Successful link established #######################")

def queryCar(_query):
    connection = obd.OBD(ODB_PORT, None, None, True)
    cmd = obd.commands[_query]
    response = connection.query(cmd)
    return float(str(response)[:str(response).find('.')])

cmd = obd.commands['THROTTLE_POS']

# connection = obd.OBD(ODB_PORT, None, None, True)
# response = connection.query(cmd)
# print("1(" + str(response) + ")," + str(cmd) + ", CONNECTION: " + connection.status())
#
# response = connection.query(cmd)
# print("2(" + str(response) + ")," + str(cmd) + ", CONNECTION: " + connection.status())

throttlePOS = queryCar('THROTTLE_POS')
while throttlePOS >= 0: # While the throttle is alive
    if throttlePOS >= 25:
        print("(" + str(throttlePOS) + ") Click!")
    else:
        print("(" + str(throttlePOS) + ") Throttle not halfway, no click.")
    throttlePOS = queryCar('THROTTLE_POS')
    pass
