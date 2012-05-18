import OpenOPC
import time
import wm_global



def OPCconnect():
    opc = OpenOPC.client()
    #opc = OpenOPC.open_client('localhost')
    opc = OpenOPC.open_client(wm_global.OpcClientName)
    opc.servers()

    # opc.connect('KEPware.KEPServerEx.V4')

    opc.connect(wm_global.OpcServerName)
    return opc

def readOPC(tag):
    return wm_global.OPCdict[tag]

def writeOPC(tag, val):
    writeTag(tag, val)

def readTag(exitSimulation):
   # opc = OPCconnect()
   # TagArray = opc.read(wm_global.OPCdict.keys(), group="Group")
    while exitSimulation.exit == 1:
        #print 'Start OPC Read'
        opc = OPCconnect()
        TagArray = opc.read(wm_global.OPCdict.keys(), group=wm_global.OpcGroupName)

        #TagArray = opc.read(group="Group")
 #       print '@@@TagArray: ', TagArray
        #print 'Finished OPC Read'
        i = 0
        # Iteration tags dict
        for key in wm_global.OPCdict.iterkeys():
            if TagArray[i][1] == 1:
                wm_global.OPCdict[key] = 1
                #print key
            else:
                wm_global.OPCdict[key] = 0
            i += 1
        opc.close()
        time.sleep(2)

def writeTag(tag, val):
    tag = (tag, val)
    #print 'Start OPC Write'
    wopc = OPCconnect()
    wopc.write(tag)
    #print 'Finished OPC write'
    wopc.close()
