'''
Created on 21 Jul 2012

@author: shearer
'''

import re
import os
import sys
#from optparse import OptionParser

from xml.dom.minidom import parseString
from xml.etree import ElementTree

from functools import partial

import numpy as np
from datetime import timedelta
#from pandas import *
        
from kivy.support import install_twisted_reactor
#from pandas.tools.merge import concat
from pydoc import deque
install_twisted_reactor() 

try:
    from twisted.internet import reactor
    from twisted.internet.protocol import ReconnectingClientFactory
    from twisted.protocols.basic import LineReceiver
except:
    print '''Missing dependencies:
    from http://www.lfd.uci.edu/~gohlke/pythonlibs/ download twisted and install 

    run "python ez_setup.py", then add the script location to your path
    easy_install zope.interface'''
    sys.exit(1)

from kivy.logger import Logger
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from stringUtils import stringToBestType, stringReplace, insertLineBreaks
from mindCupolaPythonUtils import whoAmI, lineno
from kivyUtils import LabeledSlider, LabeledCheckBox, LabeledLabel, LabeledSwitch,\
    BoxLayoutOrientationRelativeToParent
#from deprecated import deprecated
 
class EyeTrackerProtocol(LineReceiver):
    
    attribToParamDict = {
                                'ENABLE_SEND_DATA': 'sendDataFlag',
                                
                                'ENABLE_SEND_PUPIL_LEFT': 'pupilLeftSendDataFlag',
                                'LPCX': 'pupilLeftX',
                                'LPCY': 'pupilLeftY',
                                'LPD': 'pupilLeftDiameter',
                                'LPS': 'pupilLeftDistance',
                                'LPV': 'pupilLeftValid',
                                
                                'ENABLE_SEND_PUPIL_RIGHT': 'pupilRightSendDataFlag',
                                'RPCX': 'pupilRightX',
                                'RPCY': 'pupilRightY',
                                'RPD': 'pupilRightDiameter',
                                'RPS': 'pupilRightDistance',
                                'RPV': 'pupilRightValid',
                                
                                
                                'ENABLE_SEND_POG_LEFT': 'pointOfGazeLeftSendDataFlag',
                                'LPOGX': 'pointOfGazeLeftX',
                                'LPOGY': 'pointOfGazeLeftY',
                                'LPOGV': 'pointOfGazeLeftValid',
                                
                                'ENABLE_SEND_POG_RIGHT': 'pointOfGazeRightSendDataFlag',
                                'RPOGX': 'pointOfGazeRightX',
                                'RPOGY': 'pointOfGazeRightY',
                                'RPOGV': 'pointOfGazeRightValid',
                                
                                'ENABLE_SEND_POG_FIX': 'fixationSendDataFlag',
                                'FPOGX': 'fixationX',
                                'FPOGY': 'fixationY',
                                'FPOGID': 'fixationID',
                                'FPOGS': 'fixationTimeStart',
                                'FPOGD': 'fixationTimeDuration',        
                                'FPOGV': 'fixationValid',   
                                
                                'CALIBRATE_START': 'calibrationActiveFlag',
                                'CALIBRATE_SHOW': 'calibrationShowFlag',
                                
#                                'CALX': 'calibrationPointX',
#                                'CALY': 'calibrationPointY',
#                                'CALIB_START_PT': 'calibrationPointStarted',
#                                'CALIB_RESULT_PT': 'calibrationPointCompleted',
#                                
                                }
    
    tmpDFList = []
    tmpDFListLimit = 25
    lookBackRatio = 50
    
    
    def __init__(self, factory):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        assert isinstance(factory, EyeTrackerFactory)
        self.factory = factory # protocol's factory, so can access persistent data (in the factory)
        #self.factory.protocol = self
        #set up call backs for externally changed
        #note that the eyeTracker is an object within factory that has data we're interested in,
        #but there could also be other attributes in factory that we use to store stuff
        assert isinstance(self.factory.eyeTracker, EyeTracker)
        self.eyeTracker = self.factory.eyeTracker
        
        ## bind local callbacks to eyeTracker parameters that can be changed by the protocol
        self.eyeTracker.bind(    host                            =   self.on_host,
                                 port                            =   self.on_port,
                                 sendDataFlag                    =   self.on_sendDataFlag,
                                 pupilLeftSendDataFlag           =   self.on_pupilLeftSendDataFlag,
                                 pupilRightSendDataFlag          =   self.on_pupilRightSendDataFlag,
                                 pointOfGazeLeftSendDataFlag     =   self.on_pointOfGazeLeftSendDataFlag,
                                 pointOfGazeRightSendDataFlag    =   self.on_pointOfGazeRightSendDataFlag,
                                 fixationSendDataFlag            =   self.on_fixationSendDataFlag,
                                 packetCounterSendDataFlag       =   self.on_packetCounterSendDataFlag,
                                 timeTimeSendDataFlag            =   self.on_timeTimeSendDataFlag,
                                 timeTickSendDataFlag            =   self.on_timeTickSendDataFlag,
                                 calibrationActiveFlag           =   self.on_calibrationActiveFlag,
                                 calibrationShowFlag             =   self.on_calibrationShowFlag,
                            )
        
        #TODOLATE there are a few other externally changable things that we should watch for
        
    def connectionMade(self):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        Logger.info(self.__class__.__name__ + ': Connection made')
        self.eyeTracker.connectedFlag = True
        self.eyeTracker.factory = self.factory
        self.loadConfiguration()
        
    def loadConfiguration(self):
        
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        defaultList = [
                       'pupilLeftSendDataFlag',
                       'pupilRightSendDataFlag',
                       'pointOfGazeLeftSendDataFlag',
                       'pointOfGazeRightSendDataFlag', 
                       'fixationSendDataFlag',
                       'sendDataFlag',
                       ]
        
        #flip to force sending of defaults
        for item in defaultList:
            setattr(self.eyeTracker, item, False)
        for item in defaultList:
            setattr(self.eyeTracker, item, True)
          
    def lineReceived(self, line):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        tree = ElementTree.fromstring(line)
        
        #spin attribs to the best guessed type
        for a in tree.attrib:
            value = tree.attrib[a]
            tree.attrib[a] = stringToBestType(value)
        
        if tree.tag == 'ACK':
            self.eyeTrackerAck(attribDict = tree.attrib)
        elif tree.tag == 'REC':
            self.eyeTrackerReceivedData(attribDict = tree.attrib)
        elif tree.tag == 'CAL':
            self.eyeTrackerReceivedCalibration(attribDict = tree.attrib)
        else:
            Logger.exception(self.__class__.__name__ + ': tag not implemented yet!! Tag is: ' + str(tree.tag))
            
    def _setState(self, stateDict):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        #assert type(stateDict) is ObservableDict
        for key, value in stateDict.items():
            s = '<SET ID="{}" STATE="{}" />'.format(key, str(value))
            Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] sending string to EyeTracker: ' + str(s))
            self.transport.write(s + '\r\n') #the eyetracker requires a newline to terminate
    
    def disconnect(self):
        self.eyeTracker.connectedFlag = False
        if hasattr(self, 'transport'):
            self.transport.loseConnection()
            
    def connect(self):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        if hasattr(self, 'transport'): #have transport:
            if self.eyeTracker.wantToBeConnectedFlag:
                #check right connection, and if wrong  disconnect and reconnect
                if self.transport.addr[0] is not self.eyeTracker.host and self.tranport.addr[1] is not self.eyeTracker.port: 
                    global reactor #HxxxACK keeps eclipse happy
                    self.disconnect()
                    print 'breaking connection'
                    reactor.connectTCP(self.factory.eyeTracker.host, self.factory.eyeTracker.port, self.factory, timeout=5)
                    print 'reconnecting'
                else:
                    pass #ok
            else: #don't want to be connected
                self.disconnect()
                print "connected, but don't want to be - breaking connection."
        else: #no transport
            if self.eyeTracker.wantToBeConnectedFlag:
                print 'no connection, so connecting'
                reactor.connectTCP(self.factory.eyeTracker.host, self.factory.eyeTracker.port, self.factory, timeout=5)
            else:
                pass
        
    def eyeTrackerReceivedData(self, attribDict):    
#        Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        et = self.factory.eyeTracker
        
        for key, value in attribDict.items():
            if self.attribToParamDict.has_key(key):#                
                if type(value) is bool: value=int(value)
                #if key in ['LPV']: print 'LPV ' + str(value)
                
                #TODO 7 make dispatch work without this HACK
                if key in ['LPV', 'RPV']:
#                    Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] got eyetracker data for key: ' + key + ' value is: ' + str(value))
                    setattr(et, self.attribToParamDict[key], -1) #force a change to fire the event handler
                    
                setattr(et, self.attribToParamDict[key], value)
                
                assert getattr(et, self.attribToParamDict[key]) == value #read back to confirm
            else:
                Logger.exception(self.__class__.__name__ + ': in [' + whoAmI() + '] got eyetracker data for unknown key: ' + key)
        
        d = {}
        for key, value in attribDict.items():
            d[key] = [value]
#        now = Timestamp('now')
#
#        df = DataFrame(d, index=[now])
#        self.tmpDFList.append(df)
#        if len(self.tmpDFList) >= self.tmpDFListLimit:
#            tmpDF = {}
#            et.eyeDataFrame = concat([et.eyeDataFrame, concat(self.tmpDFList)])
#            self.tmpDFList = []
#            
#            short = et.eyeDataFrame.ix[-1 * self.tmpDFListLimit:]
#            long  = et.eyeDataFrame.ix[-self.lookBackRatio * self.tmpDFListLimit:]
#            s = short.mean()
#            l = long.mean()
#            et.pupilDiameterMeanRelative = float(s['LPD'] - l['LPD'])
#            #print et.pupilDiameterMeanRelative
#            
#            
#            #compute stats
#            #et.eyeDataFrame.

    def eyeTrackerReceivedCalibration(self, attribDict):
#        Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        et = self.factory.eyeTracker
        
        #if PT =true then this point is about to be calibrated
        if attribDict.has_key('ID'):
#            Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] ID=' + attribDict['ID'])
            if attribDict['ID'] == 'CALIB_START_PT':
                assert attribDict.has_key('CALX')
                assert attribDict.has_key('CALY')
                assert attribDict.has_key('PT')
                x = attribDict['CALX']
                y = attribDict['CALY']
                
                low = 0.1
                mid = 0.5
                high = 0.9
                tolerance = 0.05
#                print x, y
                if (low - tolerance) <= x and x<=(low + tolerance)   and   (low - tolerance) <= y and y <= (low + tolerance):
                    et.calibrationActivePoint = 0
                if (mid - tolerance) <= x and x<=(mid + tolerance)   and   (low - tolerance) <= y and y <= (low + tolerance):
                    et.calibrationActivePoint = 1
                if (high - tolerance) <= x and x<=(high + tolerance)   and   (low - tolerance) <= y and y <= (low + tolerance):
                    et.calibrationActivePoint = 2
                if (low - tolerance) <= x and x<=(low + tolerance)   and   (mid - tolerance) <= y and y <= (mid + tolerance):
                    et.calibrationActivePoint = 3
                if (mid - tolerance) <= x and x<=(mid + tolerance)   and   (mid - tolerance) <= y and y <= (mid + tolerance):
                    et.calibrationActivePoint = 4
                if (high - tolerance) <= x and x<=(high + tolerance)   and   (mid - tolerance) <= y and y <= (mid + tolerance):
                    et.calibrationActivePoint = 5
                if (low - tolerance) <= x and x<=(low + tolerance)   and   (high - tolerance) <= y and y <= (high + tolerance):
                    et.calibrationActivePoint = 6
                if (mid - tolerance) <= x and x<=(mid + tolerance)   and   (high - tolerance) <= y and y <= (high + tolerance):
                    et.calibrationActivePoint = 7
                if (high - tolerance) <= x and x<=(high + tolerance)   and   (high - tolerance) <= y and y <= (high + tolerance):
                    et.calibrationActivePoint = 8
#                print et.calibrationActivePoint
            elif attribDict['ID'] == 'CALIB_RESULT_PT':
                pass #ignore, nothing intesting in 'CALIB_RESULT_PT'
            elif attribDict['ID'] == 'CALIB_RESULT':
                et.calibrationActivePoint = -1
                et.calibrationActiveFlag = False
                
                runningTotal = 0
                for key, value in attribDict.items():
                    if key.startswith('LV') or key.startswith('RV'):
                        if value: runningTotal += 1
                
                #running Total will be in range [0,18] (left eye, right eye, for 9 calibration points
                Logger.debug(self.__class__.__name__ + ': in [' + whoAmI() + '] Calibration Complete. Calibration score = ' + str(runningTotal) + ' out of 18')
                if runningTotal > et.goodCalibrationThreshold: #good calibration threshold
                    et.goodCalibration = True
                else:
                    print 'got calibration result (BAD)'
                    et.badCalibration = True
            else:
                Logger.exception(self.__class__.__name__ + ': in [' + whoAmI() + '] got eyetracker calibration for unknown ID: ' + attribDict['ID'])
            
    def eyeTrackerAck(self, attribDict):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        #extract ID
        assert type(attribDict) is dict
        assert 'ID' in attribDict
        assert 'STATE' in attribDict
        key = attribDict['ID']
        value = stringToBestType(attribDict['STATE'])
        
        if key in self.attribToParamDict:
            Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] Got implemented key: ' + key)
            #setattr(self.factory.eyeTracker, self.attribToParamDict[key], value)
        else:
            Logger.exception(self.__class__.__name__ + ': in [' + whoAmI() + '] Key not implemented yet: ' + key)
        
    def on_host(self, obj, value): #host changed, reconnect
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self.connect()
    
    def on_port(self, obj, value): #port changed, reconnect
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self.connect()
        
    def on_sendDataFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'ENABLE_SEND_DATA': int(value)})
        
    def on_pupilLeftSendDataFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'ENABLE_SEND_PUPIL_LEFT': int(value)})
#                                 
    def on_pupilRightSendDataFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'ENABLE_SEND_PUPIL_RIGHT': int(value)})
            
    def on_pointOfGazeLeftSendDataFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'ENABLE_SEND_POG_LEFT': int(value)})
        
    def on_pointOfGazeRightSendDataFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'ENABLE_SEND_POG_RIGHT': int(value)})
       
    def on_fixationSendDataFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'ENABLE_SEND_POG_FIX': int(value)})
        
    def on_packetCounterSendDataFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'ENABLE_SEND_COUNTER': int(value)})  
    
    def on_timeTimeSendDataFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'ENABLE_SEND_TIME': int(value)})  
    
    def on_timeTickSendDataFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'ENABLE_SEND_TIME_TICK': int(value)})  
    
    def on_calibrationActiveFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'CALIBRATE_START': int(value)})
        
    def on_calibrationShowFlag(self, obj, value):
        #Logger.trace(self.__class__.__name__ + ': in [' + whoAmI() + '] ')
        self._setState({'CALIBRATE_SHOW': int(value)})
    
            
class EyeTracker(EventDispatcher):

    host            = StringProperty('localhost')
    port            = NumericProperty(4242)
    factory         = None
    
    wantToBeConnectedFlag = BooleanProperty(False)
    def on_wantToBeConnectedFlag(self, obj, value):
        if self.wantToBeConnectedFlag:
            if not self.connectedFlag:
                self.factory = EyeTrackerFactory(eyeTracker=self)
        else:
            if self.connectedFlag:
                assert isinstance(self.factory, EyeTrackerFactory)
                if self.factory is not None:
                    self.factory.protocol.disconnect()
#                if self.factory.
                        
    connectedFlag   = BooleanProperty(False)
    
    sendDataFlag    = BooleanProperty(False)
    
    cameraSizeX     = NumericProperty(0)
    cameraSizeY     = NumericProperty(0)
    cameraSize      = ReferenceListProperty(cameraSizeX, cameraSizeY)
    
    trackRectX      = NumericProperty(0)
    trackRectY      = NumericProperty(0)
    trackRect       = ReferenceListProperty(trackRectX, trackRectY)
    
    productID       = StringProperty('')
    serialID        = NumericProperty(0) 
    companyID       = StringProperty('')
    
    manufacturerID  = StringProperty('')
    apiVersion      = NumericProperty(0)
    apiID           = ReferenceListProperty(manufacturerID, apiVersion)
    
    pupilLeftX      = NumericProperty(0)
    pupilLeftY      = NumericProperty(0)
    pupilLeftDiameter = NumericProperty(0)
    pupilLeftDistance = NumericProperty(0)
    pupilLeftValid  = NumericProperty(-1)
    pupilLeftSendDataFlag = BooleanProperty(False)
    pupilLeft       = ReferenceListProperty(pupilLeftX, pupilLeftY, pupilLeftDiameter, pupilLeftDistance, pupilLeftValid, pupilLeftSendDataFlag)
    
    pupilRightX      = NumericProperty(0)
    pupilRightY      = NumericProperty(0)
    pupilRightDiameter = NumericProperty(0)
    pupilRightDistance = NumericProperty(0)
    pupilRightValid  = NumericProperty(-1)
    pupilRightSendDataFlag = BooleanProperty(False)
    pupilRight       = ReferenceListProperty(pupilRightX, pupilRightY, pupilRightDiameter, pupilRightDistance, pupilRightValid, pupilRightSendDataFlag)

    pupils          = ReferenceListProperty(pupilLeft, pupilRight)
    
    pointOfGazeLeftX  = NumericProperty(0)
    
    pointOfGazeLeftY  = NumericProperty(0)
    pointOfGazeLeftValid = BooleanProperty(False)
    pointOfGazeLeftSendDataFlag = BooleanProperty(False)
    pointOfGazeLeft   = ReferenceListProperty(pointOfGazeLeftX, pointOfGazeLeftY, pointOfGazeLeftValid, pointOfGazeLeftSendDataFlag)
    
    pointOfGazeRightX  = NumericProperty(0)
    pointOfGazeRightY  = NumericProperty(0)
    pointOfGazeRightValid = BooleanProperty(False)
    pointOfGazeRightSendDataFlag = BooleanProperty(False)
    pointOfGazeRight   = ReferenceListProperty(pointOfGazeRightX, pointOfGazeRightY, pointOfGazeRightValid, pointOfGazeRightSendDataFlag)
    
    pointOfGaze    = ReferenceListProperty(pointOfGazeLeft, pointOfGazeRight)
    
    fixationX       = NumericProperty(0)
    fixationY       = NumericProperty(0)
    fixationID      = NumericProperty(0)
    fixationTimeStart = NumericProperty(0)
    fixationTimeDuration = NumericProperty(0)
    fixationValid = BooleanProperty(False)
    fixationSendDataFlag = BooleanProperty(False)
    fixation        = ReferenceListProperty(fixationX, fixationY, fixationID, fixationTimeStart, fixationTimeDuration, fixationValid, fixationSendDataFlag)
    
    packetCounterCounter = NumericProperty(0)
    packetCounterSendDataFlag = BooleanProperty(False)
    packetCounter = ReferenceListProperty(packetCounterCounter, packetCounterSendDataFlag)
    
    timeTime = NumericProperty(0)
    timeTimeSendDataFlag = BooleanProperty(False)
    timeTick = NumericProperty(0)
    timeTickSendDataFlag = BooleanProperty(False)
    time = ReferenceListProperty(timeTime, timeTimeSendDataFlag, timeTick, timeTickSendDataFlag)
    
    calibrationCountdownTime = NumericProperty(5.0);
    #todo calibration countdown timer
    
    calibrationActiveFlag = BooleanProperty(False)
    def on_calibrationActiveFlag(self, instance, value):
        print 'on_calibrationActiveFlag, value is: ', value
        
    calibrationShowFlag =  BooleanProperty(False)
    
    calibrationActivePoint = NumericProperty(-1)
#    def on_calibrationActivePoint(self, instance, value):
#        print 'on_calibrationActivePoint:', type(instance), value
    
    calibrationPointCompleted = NumericProperty(0)
    calibration = ReferenceListProperty(calibrationActiveFlag, calibrationShowFlag, calibrationPointCompleted)
        
    goodEyesBuildUpValueThresholdUpwards = 6.5 #8.5 works, push higher to wait longer before start
    goodEyesBuildUpValueThresholdDownwards = 4.0
    goodEyesBuildUpValue = NumericProperty(0.0)
    def on_goodEyesBuildUpValue(self, instance, value):
#        Logger.trace(self.__class__.__name__ + 'Line: ' + str(lineno()) + ': goodEyesBuildUpValue=' + str(self.goodEyesBuildUpValue))
        
        if self.goodEyesBuildUpValue > self.goodEyesBuildUpValueThresholdUpwards:
            self.goodEyeTimerTrigger = Clock.create_trigger(self.goodEyeTimerDone, self.goodEyeTimerLength) #Start timer
            self.goodEyeTimerTrigger()
#            Logger.trace(self.__class__.__name__ + ': goodEyeTimerDone scheduled')
            #TODO DONE 1.1 make eye colour correct?
        elif self.goodEyesBuildUpValue < self.goodEyesBuildUpValueThresholdDownwards:
            Clock.unschedule(self.goodEyeTimerDone) #clear timer
#            Logger.trace(self.__class__.__name__ + ': goodEyeTimerDone UNscheduled')

            #TODO DONE 1.1 make eye colour correct?
            self.goodEyes = False #has side-effect of unscheduling self.goodEyeTimerdone
        
    goodEyeTimerLength = NumericProperty(2.5)
    
    goodEyes = BooleanProperty(False)
    def on_goodEyes(self, instance, value):
        Logger.debug(self.__class__.__name__ + 'Line: ' + str(lineno())  + ': on_goodEyes:  value is: ' + str(value))
        if value:
            Clock.unschedule(self.goodEyeTimerDone) #make sure goodEyeTimerDone will no longer fire
        else:
            self.calibrationActiveFlag = False
         
    def goodEyeCheck(self, instance=None, value=None):
#        Logger.trace(self.__class__.__name__ + 'Line: ' + str(lineno())  + ': goodEyeCheck')
        
        newValue = self.goodEyesBuildUpValue
        if self.pupilLeftValid == 1:
            newValue += 1
        if self.pupilRightValid ==1:
            newValue += 1
        if newValue > 0.1:
            newValue *= 0.99 #push towards 0
        self.goodEyesBuildUpValue = newValue
            
    def goodEyeTimerDone(self, dt=None):
        self.goodEyes = True
        #TODO DONE 1.2 on timer run out make goodEyes = true
        
    goodCalibration = BooleanProperty(False)
    goodCalibrationThreshold = 11
    def on_goodCalibration(self, instance, value):
        print 'on_goodCalibration, value is: ', value
        
    badCalibration = BooleanProperty(False)
    def on_badCalibration(self, instance, value):
        print 'on_badCalibration, value is: ', value
        
    def __init__(self, host = 'localhost', port = 4242, goodCalibrationThreshold=11):
        super(EyeTracker, self).__init__()
        assert type(host) is str
        assert type(port) is int
        self.host = host
        self.port = port
        self.wantToBeConnectedFlag = False
        self.goodCalibrationThreshold = goodCalibrationThreshold
        
        #self.bind(connectedFlag=self.on_connectedFlag)
        self.bind(pupilLeftValid=self.goodEyeCheck)
        self.bind(pupilRightValid=self.goodEyeCheck)
        #Clock.schedule_interval(self.goodEyeCheck, 0.25) #repeatable check, so it will decrease even if disconnected or unchanged
        
            
class EyeTrackerFactory(ReconnectingClientFactory):

    global reactor #HxxxACK keeps eclipse happy
    
    def __init__(self, eyeTracker = None, **kwargs):
        #super(EyeTrackerFactory, self).__init__(**kwargs)
        
        
        self.eyeTracker = EyeTracker() if eyeTracker is None else eyeTracker
        assert isinstance(self.eyeTracker, EyeTracker)
         
        #set self to be the registered factory for the eyeTracker
        self.eyeTracker.factory = self
        
        assert hasattr(self.eyeTracker, 'host')
        assert hasattr(self.eyeTracker, 'port')
        self.connect()
        
    def connect(self):
        reactor.connectTCP(self.eyeTracker.host, self.eyeTracker.port, self, timeout=5)
    
    #===================
    # reactor callbacks
    #===================
    
    def startedConnecting(self, connector): 
        Logger.info(self.__class__.__name__ + ': Started to connect to EyeTracker at ' + str(self.eyeTracker.host) + ':' + str(self.eyeTracker.port))
    
    def buildProtocol(self, addr): 
        Logger.info(self.__class__.__name__ + ': Connected')
        
        #Logger.trace(self.__class__.__name__ + ':     resetting reconnection delay')
        self.resetDelay()
        #Logger.trace(self.__class__.__name__ + ':     building protocol')
        self.protocol = EyeTrackerProtocol(factory=self)
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        Logger.info(self.__class__.__name__ + ': Lost connection. ' + str(reason.value))
        if 'Connection was closed cleanly' in str(reason.value):
            Logger.debug(self.__class__.__name__ + ': Clean disconnect.')
            self.stopTrying()
        else:
            Logger.info(self.__class__.__name__ + ': Tracker not connected?')
             
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        self.eyeTracker.connectedFlag = False

    def clientConnectionFailed(self, connector, reason):
        Logger.info(self.__class__.__name__ + ': Connection failed. Reason:' + str(reason))
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)
        self.eyeTracker.connectedFlag = False

class EyeTrackerWidget(BoxLayout):
    
    def __init__(self, eyeTracker=None, **kwargs):
        super(EyeTrackerWidget, self).__init__(**kwargs)
        
        self.orientation = 'vertical'
        
        self.eyeTracker = EyeTracker() if eyeTracker is None else eyeTracker
        assert isinstance(self.eyeTracker, EyeTracker)
        
        self.connectedFlag_widget = LabeledSwitch(labelingString='connectedFlag', active = self.eyeTracker.connectedFlag)
        self.connectedFlag_widget.bind(active=self.eyeTracker.setter('connectedFlag'))
        self.eyeTracker.bind(connectedFlag=self.connectedFlag_widget.setter('active'))
        self.add_widget(self.connectedFlag_widget)
        
        self.wantToBeConnectedFlag_widget = LabeledSwitch(labelingString='wantToBeConnectedFlag', active = self.eyeTracker.wantToBeConnectedFlag)
        self.wantToBeConnectedFlag_widget.bind(active=self.eyeTracker.setter('wantToBeConnectedFlag'))
        self.eyeTracker.bind(wantToBeConnectedFlag=self.wantToBeConnectedFlag_widget.setter('active'))
        self.add_widget(self.wantToBeConnectedFlag_widget)
        
        self.calibrationShowFlag_widget = LabeledSwitch(labelingString='calibrationShowFlag', active = self.eyeTracker.calibrationShowFlag)
        self.calibrationShowFlag_widget.bind(active=self.eyeTracker.setter('calibrationShowFlag'))
        self.eyeTracker.bind(calibrationShowFlag=self.calibrationShowFlag_widget.setter('active'))
        self.add_widget(self.calibrationShowFlag_widget)
        
        self.pupilsValidBox = BoxLayoutOrientationRelativeToParent()
        self.add_widget(self.pupilsValidBox)
        
        self.pupilLeftValid_widget = LabeledSlider(labelingString='pupilLeftValid', value = self.eyeTracker.pupilLeftValid, min=-1, max=1)
        self.pupilLeftValid_widget.bind(value=self.eyeTracker.setter('pupilLeftValid'))
        self.eyeTracker.bind(pupilLeftValid=self.pupilLeftValid_widget.setter('value'))
        self.pupilsValidBox.add_widget(self.pupilLeftValid_widget)
        
        self.pupilRightValid_widget = LabeledSlider(labelingString='pupilRightValid', value = self.eyeTracker.pupilRightValid, min=-1, max=1)
        self.pupilRightValid_widget.bind(value=self.eyeTracker.setter('pupilRightValid'))
        self.eyeTracker.bind(pupilRightValid=self.pupilRightValid_widget.setter('value'))
        self.pupilsValidBox.add_widget(self.pupilRightValid_widget)
        
        self.goodEyesBuildUpValue_widget = LabeledSlider(labelingString='goodEyesBuildUpValue', value = self.eyeTracker.goodEyesBuildUpValue, min=-1, max=10)
        self.goodEyesBuildUpValue_widget.bind(value=self.eyeTracker.setter('goodEyesBuildUpValue'))
        self.eyeTracker.bind(goodEyesBuildUpValue=self.goodEyesBuildUpValue_widget.setter('value'))
        self.add_widget(self.goodEyesBuildUpValue_widget)
        
        self.goodEyes_widget = LabeledSwitch(labelingString='goodEyes', active = self.eyeTracker.goodEyes)
        self.goodEyes_widget.bind(active=self.eyeTracker.setter('goodEyes'))
        self.eyeTracker.bind(goodEyes=self.goodEyes_widget.setter('active'))
        self.add_widget(self.goodEyes_widget)
        
        self.goodCalibration_widget = LabeledSwitch(labelingString='goodCalibration', active = self.eyeTracker.goodCalibration)
        self.goodCalibration_widget.bind(active=self.eyeTracker.setter('goodCalibration'))
        self.eyeTracker.bind(goodCalibration=self.goodCalibration_widget.setter('active'))
        self.add_widget(self.goodCalibration_widget)
        
        self.badCalibration_widget = LabeledSwitch(labelingString='badCalibration', active = self.eyeTracker.badCalibration)
        self.badCalibration_widget.bind(active=self.eyeTracker.setter('badCalibration'))
        self.eyeTracker.bind(badCalibration=self.badCalibration_widget.setter('active'))
        self.add_widget(self.badCalibration_widget)
        
        self.calibrationActiveFlag_widget = LabeledSwitch(labelingString='calibrationActiveFlag', active = self.eyeTracker.calibrationActiveFlag)
        self.calibrationActiveFlag_widget.bind(active=self.eyeTracker.setter('calibrationActiveFlag'))
        self.eyeTracker.bind(calibrationActiveFlag=self.calibrationActiveFlag_widget.setter('active'))
        self.add_widget(self.calibrationActiveFlag_widget)
        
        self.calibrationActivePoint_widget = LabeledSlider(labelingString='calibrationActivePoint', value = self.eyeTracker.calibrationActivePoint, min=-1, max=8)
        self.calibrationActivePoint_widget.bind(value=self.eyeTracker.setter('calibrationActivePoint'))
        self.eyeTracker.bind(calibrationActivePoint=self.calibrationActivePoint_widget.setter('value'))
        self.add_widget(self.calibrationActivePoint_widget)
        
        
from kivy.app import App
class EyeTrackerWidgetTestApp(App):
    
    def __init__(self, eyeTracker=None):
        super(EyeTrackerWidgetTestApp, self).__init__()
        
        self.eyeTracker = EyeTracker() if eyeTracker is None else eyeTracker
        assert isinstance(self.eyeTracker, EyeTracker)
        
    def build(self):
        self.eyeTrackerWidget = EyeTrackerWidget(eyeTracker=self.eyeTracker, sizehint=(1,1))
        self.eyeTracker.wantToBeConnectedFlag = True
        return self.eyeTrackerWidget

# self run, self test     
if __name__ == "__main__":
    host = 'localhost'
    host = '192.168.1.118'
    eyeTracker = EyeTracker(host=host, goodCalibrationThreshold=8)
    eyeTrackerWidgetTestApp = EyeTrackerWidgetTestApp(eyeTracker=eyeTracker)
    eyeTrackerWidgetTestApp.run()
    
    
    
    
