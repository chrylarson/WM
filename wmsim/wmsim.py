#!/usr/bin/env python
import Controls
import time
import thread
from ConfigParser import ConfigParser
import Tkinter
import tkMessageBox
import pythonprog
import wm_global


class CExit:
    exit = 0
    def __init__(self, val):
        self.exit  = val

#==============================================================================
#   ScreenManager(self):
#==============================================================================
def ScreenManager(exitSimulation):
    while exitSimulation.exit == 1:
        if tkMessageBox.askyesno("Terminate", "Do you want to quit?"):
            exitSimulation.exit = 0

#==============================================================================
#   readTag():
#==============================================================================
def readTag():

    ini = ConfigParser()
    ini.read('wmsim.ini')

    myTagDic = ini._sections['GENERAL']

    # Set the global configuration dictionary
    for key in myTagDic.iterkeys():
        wm_global.config[key] = myTagDic[key]

    # Set the global object for the OPC server
    wm_global.OpcServerName = wm_global.config['opc_server']
    wm_global.OpcGroupName = wm_global.config['opc_group']
    wm_global.OpcClientName = wm_global.config['opc_client']

    # Clear the OPCdict
    wm_global.OPCdict.clear()

    # Iteration in the wm_global.config file to generate tags dict
    for i in range(0, int(wm_global.config['qty_devices'])):
        myTagDic.clear()
        dev = "DEV_" + str(i+1)
        myTagDic = ini._sections[dev]

        # Skip the first 4 key because no tags
        skip = 4

        for key in myTagDic.iterkeys():
            if skip == 0:
                # Add the prefix to the tag
                myTagDic[key] = wm_global.config['tag_prefix'] + myTagDic[key]
                # Add the tag:0 to the OPCdict
                wm_global.OPCdict[myTagDic[key]] = 0
            else:
                skip -=1

        # Set the device according to the type
        if  int(myTagDic['type']) == 1:
            wm_global.devicesList.append(Controls.Device(myTagDic.copy()))
        elif int(myTagDic['type']) == 2:
            wm_global.devicesList.append(Controls.Pump(myTagDic.copy()))
        elif int(myTagDic['type']) == 3:
            wm_global.devicesList.append(Controls.Pump_3(myTagDic.copy()))
        else:
            print "Errore del cazzo"

#=== main ================================================================

# read ini file
# add parse for OPC module
readTag()

# Define Sim obj
sim = Controls.Simulation(wm_global.devicesList,1)

w = CExit(1)

# Start OPC mdule
thread.start_new_thread(pythonprog.readTag,(w,))

# start simulation
sim.start()

# start screen manager
thread.start_new_thread(ScreenManager,(w,))


while w.exit ==1 :
    time.sleep(1)

sim.keepRun = 0
sim.join()





