#!/usr/bin/env python
from __future__ import print_function
import obd
from obd import OBDStatus
import time
import pyautogui

print ("""
       _  ______     _________     _______  ______
      | |/ __ \ \   / /  __ \ \   / /  __ \|  ____|
      | | |  | \ \_/ /| |__) \ \_/ /| |  | | |__
  _   | | |  | |\   / |  _  / \   / | |  | |  __|
 | |__| | |__| | | |  | | \ \  | |  | |__| | |____
  \____/ \____/  |_|  |_|  \_\ |_|  |_____/|______|
         ~~Accelerator to click the mouse~~

""")
print("!!!! Scanning for serial ports !!!!")
ODB_PORT = "/dev/pts/8" #SIMULATOR##

##DEBUG ACTIVATED##
# obd.logger.setLevel(obd.logging.DEBUG)

connection = None
print("####################### Starting... #######################")
try:
    connection = obd.OBD(ODB_PORT, None, None, False) # auto-connects to USB or RF port
    #connection = obd.OBD(ODB_PORT)
    # self.fail('message')
    print("Status: " + connection.status())
except Exception as e:
    print("Setting up inital connection... ")
    while connection == None or connection.status() != OBDStatus.CAR_CONNECTED:
        try:
            connection = obd.OBD(ODB_PORT, None, None, False)
            print("Status: " + connection.status())
        except Exception as e:
            print("Initial connection failed, trying to reconnect... ")

if connection.status() == OBDStatus.CAR_CONNECTED:
    print("####################### Successful link established #######################")

def queryCar( query ):
    try:
        cmd = obd.commands[query] # select an OBD command (sensor)
        response = connection.query(cmd) # send the command, and parse the response
        if 'None' in str(response.value):
            return False
            pass
        else:
            return response.value;
    except Exception as e:
        print('Error reading [' + query + ']')
        print(e)

### MOUSE CLICKING MODULE ###
count = 0
held = False
sensitivity = 50
print("Choose which PID use wish to use.")
queryPID = raw_input("Type PID:  ")
print( '\'' + queryPID + '\'')


def barShow(queryAnswer, sensitivity):
    maxPoint = sensitivity*2

    amount = queryAnswer / maxPoint

    amount = int(amount * 10)

    spaceHold = 10 - amount

    result = "["

    for value in range(0, amount):
        result = result + '='
        pass
    for value in range(0, spaceHold):
        result = result + ' '
        pass

    result = result + '] ' + queryPID + ": " + str(queryAnswer)
    print( result )
    pass

while count < 5000:
    count += 1

    # Send PID to the queryCar function
    queryAnswer = queryCar(queryPID)

    # Turn the response from a string to a numerical value
    queryAnswer = float(str(queryAnswer)[:str(queryAnswer).find('.')])

    # Check if the response is past sensitivity
    # and has not been held down since last check
    # if queryAnswer > sensitivity and held == False:
    barShow(queryAnswer, sensitivity)
    # held = True
    # elif queryAnswer <= sensitivity and held == True:
    #     barShow(queryAnswer, sensitivity)
    #     held = False


# # Emissions
# queryPrintCar('Emissions', ['O2_SENSORS','O2_SENSORS_ALT','AIR_STATUS','O2_S1_WR_VOLTAGE','O2_S2_WR_VOLTAGE','O2_S3_WR_VOLTAGE','O2_S4_WR_VOLTAGE','O2_S5_WR_VOLTAGE','O2_S6_WR_VOLTAGE','O2_S7_WR_VOLTAGE','O2_S8_WR_VOLTAGE','O2_S1_WR_CURRENT','O2_S2_WR_CURRENT','O2_S3_WR_CURRENT','O2_S4_WR_CURRENT','O2_S5_WR_CURRENT','O2_S6_WR_CURRENT','O2_S7_WR_CURRENT','O2_S8_WR_CURRENT'])
#
# # Pneumatics
# queryPrintCar('Pneumatics', ['AMBIANT_AIR_TEMP','MAX_MAF','COOLANT_TEMP','INTAKE_TEMP','INTAKE_PRESSURE','FUEL_PRESSURE','EVAP_VAPOR_PRESSURE','EVAP_VAPOR_PRESSURE_ABS','EVAP_VAPOR_PRESSURE_ALT','BAROMETRIC_PRESSURE','WARMUPS_SINCE_DTC_CLEAR','FUEL_RAIL_PRESSURE_VAC','FUEL_RAIL_PRESSURE_DIRECT'])



#print(response.value.to("f")) # user-friendly unit conversions
