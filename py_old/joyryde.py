#!/usr/bin/env python
from __future__ import print_function
import obd
from obd import OBDStatus
import time

print("!!!! Scanning for serial ports !!!!")
ports = obd.scan_serial()      # return list of valid USB or RF ports
print(ports)                   # ['/dev/ttyUSB0', '/dev/ttyUSB1']
# ODB_PORT = ports[0] # Enter COM port here, e.g /dev/rfcomm0
ODB_PORT = "/dev/pts/6" # Enter COM port here manually if needed, e.g /dev/rfcomm0

connection = None
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



def queryCar( title, queries ):
    print("####################### " + title + " #######################")
    for _query in queries:
        try:
            cmd = obd.commands[_query] # select an OBD command (sensor)
            response = connection.query(cmd) # send the command, and parse the response
            if 'None' in str(response.value):
                print(_query + ": Unsupported for this car")
                pass
            else:
                print(_query + ": ", end='') # returns unit-bearing values thanks to Pint
                print(response.value)
        except Exception as e:
            print('Error reading [' + _query + ']')
            print(e)

# Engine
queryCar('Engine', ['RPM','SPEED','FUEL_LEVEL'])

# # Accelerator
queryCar('Accelerator', ['THROTTLE_POS','RELATIVE_THROTTLE_POS','THROTTLE_POS_B','THROTTLE_POS_C','ACCELERATOR_POS_D','ACCELERATOR_POS_E','ACCELERATOR_POS_F','THROTTLE_ACTUATOR','RELATIVE_ACCEL_POS'])
#
# # Emissions
# queryCar('Emissions', ['O2_SENSORS','O2_SENSORS_ALT','AIR_STATUS','O2_S1_WR_VOLTAGE','O2_S2_WR_VOLTAGE','O2_S3_WR_VOLTAGE','O2_S4_WR_VOLTAGE','O2_S5_WR_VOLTAGE','O2_S6_WR_VOLTAGE','O2_S7_WR_VOLTAGE','O2_S8_WR_VOLTAGE','O2_S1_WR_CURRENT','O2_S2_WR_CURRENT','O2_S3_WR_CURRENT','O2_S4_WR_CURRENT','O2_S5_WR_CURRENT','O2_S6_WR_CURRENT','O2_S7_WR_CURRENT','O2_S8_WR_CURRENT'])
#
# # Pneumatics
# queryCar('Pneumatics', ['AMBIANT_AIR_TEMP','MAX_MAF','COOLANT_TEMP','INTAKE_TEMP','INTAKE_PRESSURE','FUEL_PRESSURE','EVAP_VAPOR_PRESSURE','EVAP_VAPOR_PRESSURE_ABS','EVAP_VAPOR_PRESSURE_ALT','BAROMETRIC_PRESSURE','WARMUPS_SINCE_DTC_CLEAR','FUEL_RAIL_PRESSURE_VAC','FUEL_RAIL_PRESSURE_DIRECT'])



#print(response.value.to("f")) # user-friendly unit conversions
