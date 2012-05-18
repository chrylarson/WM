import threading
import time
import datetime
import pythonprog
import wm_global

#=== CLASS DEVICE Valve Device Type 1 ==========================================
class Device(object):
    # to avoid sharing between objects
    #step = 0
    #initDone = 0
    def __init__(self, deviceTags):
        self.deviceTags = deviceTags
        self.deviceDelay = int(deviceTags['timeout'])
        self.initDone = 0
        self.step =0
    # the working method
    def run(self):

        # Set intial device condition
        if self.initDone == 0 :
            self.devInit()
            self.initDone = 1

        # Get actual time
        self.now1 = self.now()

        if self.step == 0:
            # Set initial condition for
            if ( self.read(self.deviceTags['c_open']) == 1 ): # wait for cmd to open
                self.write(self.deviceTags['s_closed'], 0)
                self.timeOut =  self.now()
                self.step  +=1

        elif self.step  == 1:
            if ( (self.now1 - self.timeOut) > self.deviceDelay ): # wait simlating transaction
                self.write(self.deviceTags['s_opend'], 1)
                self.step  +=1

        elif self.step  == 2:
            if ( self.read(self.deviceTags['c_close']) == 1): # wait for cmd to go back
                self.write(self.deviceTags['s_opend'], 0)
                self.timeOut =  self.now()
                self.step  += 1

        elif self.step  == 3:
            if ( (self.now1 - self.timeOut) > self.deviceDelay  ): # wait simlating transaction
                self.write(self.deviceTags['s_closed'], 1)
                self.step  = 0

        if int( wm_global.config['verbose'])== 1:
            self.info()

    # Stub method for reading from PLC
    def read(self, tag = 'CL7.S13.VAL-1603-HSAR'):
        localval = pythonprog.readOPC(tag)
        if wm_global.config['verbose']== 1:
            print "reading val [%d] for tag [%s] from OPC module" % (localval, tag)
        return localval

    # Stub method to write to PLC
    def write(self, tag, val):
        pythonprog.writeOPC(tag,val)
        if int( wm_global.config['verbose'])== 1:
            print "Write Tag[%s] =  %i" % (tag, val)

    def devInit(self):
        # initial condition for the valve
        # remote, closed and not open
        self.write(self.deviceTags['s_remote'], 1)
        self.write(self.deviceTags['s_closed'], 1)
        self.write(self.deviceTags['s_opend'], 0)
        print "Device %s initialized" %( self.deviceTags['name'])

    def now(self):
        tmp = datetime.datetime.now()
        return ( (tmp.day * 24 * 60 * 60 + tmp.second) * 1000 + tmp.microsecond / 1000.0)

    def info(self):
        print "Device %s step ->%i" %( self.deviceTags['name'],self.step)
        return int(self.step)

#=== Pump Device Type 2 ========================================================
class Pump_2(Device):
    def __init__(self, deviceTags):
        # Calling the super init
        super(Pump_2, self).__init__(deviceTags)

    # the working method
    def run(self):
        # Set intial device condition
        if self.initDone == 0 :
            self.devInit()
            self.initDone = 1
        # Get actual time
        self.now1 = self.now()

        if self.step == 0:
            # Set initial condition for
            if ( self.read(self.deviceTags['c_run']) == 1 ): # wait for cmd to run
                self.timeOut =  self.now()
                self.step  +=1

        elif self.step  == 1:
            if ( (self.now1 - self.timeOut) > self.deviceDelay ): # wait simlating transaction
                self.write(self.deviceTags['s_on'], 1)
                self.step  +=1

        elif self.step  == 2:
            if ( self.read(self.deviceTags['c_run']) == 0): # wait for cmd to stop
                self.write(self.deviceTags['s_on'], 0)
                self.timeOut =  self.now()
                self.step  =0

        if int( wm_global.config['verbose'])== 1:
            self.info()

    def devInit(self):
        # initial condition for the pump
        # auto, not fault, not running and not ohigh temp
        self.write(self.deviceTags['s_auto'], 1)
        self.write(self.deviceTags['s_fault'], 0)
        self.write(self.deviceTags['s_on'], 0)
        self.write(self.deviceTags['s_tsh'], 0)
        print "Device %s initialized" %( self.deviceTags['name'])


#=== PUMP Device Type 3 ========================================================
class Pump_3(Pump_2):
    def __init__(self, deviceTags):
        # Calling the super init
        super(Pump_2, self).__init__(deviceTags)

    def devInit(self):
        # initial condition for the pump
        # auto, not fault, not running and not ohigh temp
        self.write(self.deviceTags['s_msh'],0)
        super(Pump_3, self).devInit()

#=== Valve_4 Device Type 4 ========================================================
class Valve_4(Device):
    def __init__(self, deviceTags):
        # Calling the super init
        super(Valve_4, self).__init__(deviceTags)

    # the working method
    def run(self):
        # Set intial device condition
        if self.initDone == 0 :
            self.devInit()
            self.initDone = 1
        # Get actual time
        self.now1 = self.now()

        # discrete cmd to close overide analog out
        time.sleep(1)

        if int( wm_global.config['verbose'])== 1:
            self.info()

    def devInit(self):
        # initial condition for the valve
        # remote, closed and not open
        self.write(self.deviceTags['s_remote'], 1)
        self.write(self.deviceTags['s_closed'], 0)
        self.write(self.deviceTags['s_opend'], 1)
        self.write(self.deviceTags['s_pos_fbk'], 0)
        print "Device %s initialized" %( self.deviceTags['name'])


#=== SIMULATION ================================================================

class Simulation(threading.Thread):
    # to change in a private property
    keepRun = 1

    def __init__(self, deviceList, seconds):
        threading.Thread.__init__(self)
        self.deviceList = deviceList
        self.seconds = seconds

    # the working method
    def run(self):
        print "Start simulation"

        while self.keepRun:
            for device in self.deviceList:
                device.run()
            time.sleep(self.seconds)

        print "Stop simulation"

#=== MAIN =====================================================================

if __name__ == '__main__':
    pass
